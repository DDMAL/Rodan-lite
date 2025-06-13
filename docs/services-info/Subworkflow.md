Rodan supports the concept of "subworkflow" in the sense of importing a `Workflow` to current `Workflow` and exporting a part of the current `Workflow`. It is represented and implemented by "WorkflowJobGroup" instances.

### Importing a Workflow

Rodan copies all `WorkflowJob`s, `InputPort`s, `OutputPort`s, and `Connection`s of an imported `Workflow` to the target `Workflow`. The imported `Workflow` should be validated, and the user can check the `InputPort`s and `OutputPort`s with `extern=True` to know which ports are at the top level of the `Workflow`.

The importation requires a POST request to `/workflowjobgroups/` providing `workflow` as the target `Workflow`, and `origin` as the imported `Workflow`. Then all `WorkflowJob`s, `InputPort`s, `OutputPort`s, and `Connection`s are copied to the new `Workflow` and all `WorkflowJob`s are automatically assigned as a new `WorkflowJobGroup`.

### Exporting a Workflow

Rodan allows regrouping of `WorkflowJob`s in a `Workflow`. Within a `WorkflowJobGroup`, the update and deletion of its `WorkflowJob`s, `InputPort`s, `OutputPort`s, and `Connection`s are restricted, but the user can choose to ungroup at any time.

To export a `Workflow`, Rodan requires a POST request to `/workflows/` providing `workflow_job_group` and `project`. It will copy all `WorkflowJob`s, `InputPort`s, `OutputPort`s, and `Connection`s of the given group to a new `Workflow`.