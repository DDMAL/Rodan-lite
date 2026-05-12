# Rodan-lite Repository Overview

## What This Is

Rodan-lite is a containerized music document analysis platform. It provides a workflow engine where users chain together image-processing "jobs" (segmentation, classification, OCR, etc.) to analyze historical music manuscripts. The interactive glyph classifier is the most complex job — it lets users manually correct and train a kNN classifier on segmented musical symbols (glyphs).

---

## Directory Structure

```
Rodan-lite/
├── backend/
│   ├── django/code/            # Django REST API + all job implementations
│   │   ├── jobs/               # Individual job packages
│   │   │   └── interactive_classifier/   # THE main focus (see below)
│   │   ├── models/             # Django ORM: Workflow, RunJob, Resource, etc.
│   │   ├── views/              # DRF views (REST + interactive endpoints)
│   │   └── settings.py
│   └── iipsrv/                 # IIPServer for large image tile serving (Diva.js)
├── frontend/
│   ├── client/                 # Vue/Backbone SPA
│   └── nginx/                  # Reverse proxy
├── celery/
│   ├── python-workers/         # General Python job workers
│   └── gpu-workers/            # GPU-accelerated workers
├── database/
│   ├── postgres/               # PostgreSQL with PL-Python extension
│   └── redis/                  # Redis (WebSocket pub/sub + caching)
├── taskqueue/                  # RabbitMQ message broker
├── scripts/                    # local.env, cron configs
├── docs/                       # Architecture docs, API reference
└── docker-compose.yml
```

---

## Architecture

```
Browser
  └─> nginx (80/443)
        ├─> frontend-client (Vue SPA)
        └─> backend-django (DRF REST API, port 8000)
                ├─> PostgreSQL (data persistence)
                ├─> Redis (WebSocket, sessions)
                ├─> RabbitMQ (task queue)
                │     └─> Celery workers (python + GPU)
                └─> IIPServer (image tiles for Diva.js viewer)
```

- **Workflow engine**: Users build DAG workflows from jobs. Each job instance is a `RunJob` row in the DB.
- **Interactive jobs**: Special jobs that pause and expose an HTTP interface for the user to interact with before continuing.
- **Standard jobs**: Run headlessly on Celery workers.

---

## Interactive Classifier for Glyphs

### Location

```
backend/django/code/jobs/interactive_classifier/
├── wrapper.py                  # RodanTask subclass; state machine driver
├── interactive_classifier.py   # Core logic: kNN, grouping, serialization
├── gamera_xml_distributor.py   # XML distribution helper
├── intermediary/
│   ├── gamera_glyph.py         # Glyph wrapper (RLE ↔ PIL ↔ Gamera image)
│   ├── gamera_xml.py           # XML parser → list of GameraGlyph objects
│   └── run_length_image.py     # RLE codec (decode RLE → pixel → PIL/Gamera)
└── ic_frontend/public/js/app/
    ├── App.js                  # Marionette application root
    ├── models/Glyph.js         # Backbone model for a single glyph
    ├── collections/            # Backbone collections (glyph sets)
    ├── views/                  # Rendering (grid, table, detail panel)
    └── events/                 # Radio channel event handlers
```

### Glyph Data Shape

Each glyph is a dict (stored as JSON in `RunJob.job_settings`):

```python
{
    "id":              "uuid-hex",
    "class_name":      "neume.punctum",
    "image":           "rle-encoded-binary",   # compact storage
    "image_b64":       "base64-png",           # for UI rendering
    "ncols":           int,
    "nrows":           int,
    "ulx":             int,                    # position in source image
    "uly":             int,
    "id_state_manual": bool,                   # True = human-labelled
    "confidence":      float,                  # kNN confidence [0-1]
    "is_training":     bool
}
```

### State Machine (`ClassifierStateEnum` in `wrapper.py`)

```
IMPORT_XML (0)
  → parse Gamera XML input
  → build glyph dicts, serialize to JSON
  → WAITING_FOR_INPUT

CLASSIFYING (1)           ←─────────────────┐
  ← user submits corrections                 │
  → run kNN on unclassified glyphs           │
  → serialize updated state                  │
  → WAITING_FOR_INPUT ───────────────────────┘

GROUP_AND_CLASSIFY (3)
  ← user requests auto-group
  → apply Gamera grouping (BoundingBox or Shaped)
  → retrain + reclassify
  → WAITING_FOR_INPUT

SAVE (5)
  ← user saves intermediate state
  → persist job_settings
  → WAITING_FOR_INPUT

EXPORT_XML (2)
  ← user finalizes
  → feature extraction on all glyphs
  → write output Gamera XML (with features)
  → write class names text file
  → mark RunJob SCHEDULED → continue workflow
```

### End-to-End Request Flow

**Session start (GET)**
1. User navigates to job URL.
2. Frontend POSTs to `/api/interactive/{run_job_uuid}/acquire/` → backend issues `working_user_token` + expiry.
3. Frontend GETs `/api/interactive/{run_job_uuid}/{token}/`.
4. `InteractiveWorkingView.get()` calls `job.get_interface()` → renders `interactive_classifier.html` with inline JSON:
   - `glyphs`, `training_glyphs`, `class_names`, `image_path`
5. Marionette app boots, parses JSON from `<div data-glyphs='...'>`, creates Backbone Glyph models, renders grid/table views.

**User classifies glyphs (POST)**
1. User drags/clicks to reassign `class_name` → Glyph model sets `id_state_manual=true`, `confidence=1.0`.
2. "Classify" button → App.js collects `changedGlyphs`, `deletedGlyphs`, etc.
3. POST payload:
   ```json
   {
     "@changed_glyphs":          [...],
     "@grouped_glyphs":          [...],
     "@deleted_glyphs":          [...],
     "@changed_training_glyphs": [...],
     "@deleted_classes":         [...],
     "@renamed_classes":         [...]
   }
   ```
4. `InteractiveWorkingView.post()` → `validate_my_user_input()` → state transition.
5. Backend runs kNN (`gamera.knn.kNNInteractive`, k=1) on auto glyphs using manual ones as training set.
6. Serializes updated glyphs back to JSON, saves in `RunJob.job_settings`.
7. Returns updated glyph JSON to frontend; Backbone models refresh DOM.

**Finalize (EXPORT_XML)**
1. User clicks "Finalize".
2. Backend calls `run_output_stage()`:
   - Converts glyph dicts → Gamera Image objects.
   - Runs `cknn.generate_features_on_glyphs()`.
   - `WriteXMLFile(features=True)` → output Gamera XML.
   - Writes class names to `.txt` output resource.
3. `RunJob.status` → SCHEDULED → master Celery task resumes workflow.

### Image Encoding Pipeline

```
Gamera XML (RLE strings)
  ──[RunLengthImage.decode()]──> pixel matrix
  ──[PIL.Image]──────────────> base64 PNG     (sent to browser)
  ──[Gamera ONEBIT image]────> kNN features   (classification)
  ──[RLE re-encode]──────────> output XML     (export)
```

### Key Classes

| Class | File | Role |
|---|---|---|
| `InteractiveClassifier` | `interactive_classifier.py` | kNN training, grouping, serialization |
| `GameraGlyph` | `intermediary/gamera_glyph.py` | Single glyph wrapper + image conversion |
| `GameraXML` | `intermediary/gamera_xml.py` | XML parser → list of GameraGlyph |
| `RunLengthImage` | `intermediary/run_length_image.py` | RLE ↔ PIL ↔ Gamera codec |
| `InteractiveWorkingView` | `views/` | DRF view handling GET/POST for interactive session |
| `Glyph` (JS) | `ic_frontend/.../models/Glyph.js` | Backbone model, tracks classification changes |
| `App` (JS) | `ic_frontend/.../App.js` | Marionette root; manages collections, submits POST |

---

## Open Questions / Areas to Investigate

- How is the Gamera library installed in the worker containers? (Python 2 vs 3 compatibility)
- Does the GPU worker add anything to classification, or is it only used by other jobs?
- `gamera_xml_distributor.py` — when is XML distribution used vs direct single-file processing?
- The frontend is Backbone/Marionette (legacy); any plans to migrate to Vue like the main client?
