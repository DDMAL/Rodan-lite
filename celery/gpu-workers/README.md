# GPU Celery
> As of May 2025.

The GPU-celery container has the following jobs:
- Text Alignment
- Background Removal
- SAE_binarization
- Paco classifier

We plan for July-August 2025 to be able to split all 4 of these jobs into its own container, since they use different versions of Tensorflow and other libraries. An old issue was cross-dependencies between jobs crashing each others.

To be expected changes: New containers will be added to Rodan-lite
- [ ] `celery-gpu-text-alignment`
- [ ] `celery-gpu-background-removal`
- [ ] `celery-gpu-sae-binarization`
- [ ] `celery-gpu-paco-classifier`