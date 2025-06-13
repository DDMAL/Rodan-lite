# Rodan Client Requirements

Each 'pane' has its own individual, rough reqs doc. Items in **bold** refer to the associated ERD object. Note that this is here only to facilitate development.

- [[Rodan Client Requirements - Status]]
- Pages (done)
- Jobs (done)
- Users (TBD)
- [[Rodan Client Requirements - Results]]
- Workflow Designer

Other functionality:

- Poller (TBD)

---

# Pages

### Populated by:

- **Page.name**
- current **Job.name** associated with **Page**
- current **RunJob.status** associated with **Page**

### Events:

##### Row selection

- populates 'Results' view with associated **RunJob** **Result**
- populates 'Action' view with associated actions

### Default:

- none selected

# Actions

Context-sensitive area that displays buttons (or "actions") based on (1) which of 'Workflows', 'Runs', or 'Pages' is selected and (2) which element in the respective view is selected.

### Workflows

| Type   |     Name      |                                              Action/Data |      Availability |
| ------ | :-----------: | -------------------------------------------------------: | ----------------: |
| Button | Run Workflow  | Creates new **WorkflowRun** for associated **Workflow**. | Always available. |
| Info   |    Status     |                                   **WorkflowRun.status** |                NA |
| Info   | Creation date |                                     **Workflow.created** |                NA |
| Info   |  Description  |                                 **Workflow.description** |                NA |

### Runs

| Type   |     Name      |                    Action/Data |                                                             Availability |
| ------ | :-----------: | -----------------------------: | -----------------------------------------------------------------------: |
| Button |     Stop      |     Stops the **WorkflowRun**. |   Available only if associated **WorkflowRun.status** is running/active. |
| Button |     Stop      | Continues the **WorkflowRun**. | Available only if associated **WorkflowRun.status** is stopped/inactive. |
| Info   |    Status     |         **WorkflowRun.status** |                                                                       NA |
| Info   | Creation date |        **WorkflowRun.created** |                                                                       NA |

### Pages

| Type   | Name |                   Action/Data |                                                 Availability |
| ------ | :--: | ----------------------------: | -----------------------------------------------------------: |
| Button | Work | Launches interactive session. | Available only if associated **RunJob.needs_input** is TRUE. |

### Default:

- nothing

---

# Result

The Pages pane acts as a view to the project's image repository. Uploading and deletion of images is accomplished here.

![pages](http://i.imgur.com/5f9WDIc.png)

Functionality is complete here.

![Rodan Client - Result pane](http://i.imgur.com/JiGbt9U.png)

# Workflows

### Populated by:

- **Workflow.name**
- number of associated **WokflowRun** (maybe)

### Events:

##### Row selection:

- populates 'Runs' view with associated **WorkflowRun**s for the **Workflow**
- populates 'Action' view with associated actions for the **Workflow**

### Default:

- none selected

# Runs

### Populated by:

- **WorkflowRun.name**
- **WorkflowRun.status** (not yet in ERD)

### Events:

##### Row selection:

- populates the 'Pages' view with associated **Page**s
- populates the 'Action' view with associated actions for the **WorkflowRun**

### Default:

- none selected

---

# Status

The Status pane provides information regarding known running workflows (i.e. those that have been started and have not been finished or terminated in some way), and the status of job servers.

![status](http://i.imgur.com/ALX3Hbu.png)

# Workflow Status

Each row represents a **WorkflowRun**

### Populated by:

- associated **Workflow.name**
- **WorkflowRun.status**

### Events:

- none

### Default:

- none selected

# Server Status

Each row represents a Celery queue.

### Populated by:

- Queue name (name of queue...duh)
- Machine IP (server IP)
- Capacity (queue capacity)

---
