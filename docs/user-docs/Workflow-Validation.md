Only _valid_ `Workflow`s can be used to create `WorkflowRun`s. In order to be valid, a `Workflow` must have all its elements (`WorkflowJob`, `InputPort`, `OutputPort`, `Connection`) valid, and its _workflow graph_ valid.

1. For any `WorkflowJob` in the `Workflow`:

- it has at least one `OutputPort`
- the number of its `InputPort` and `OutputPort` should satisfy the requirements of `InputPortType` and `OutputPortType` of corresponding `Job`
- each field in its `setting` should satisfy the requirements of the corresponding `Job`

2. For any `InputPort` in the `Workflow`:

- its `InputPortType` must belong to the underlying `Job`
- it should have zero or one `Connection`

3. For any `OutputPort` in the `Workflow`:

- its `OutputPortType` must belong to the underlying `Job`
- there must exist a common `ResourceType` between this `OutputPort` and its connected `InputPort`s.

4. Finally, the _workflow graph_ should:

- be nonempty (have at least one `WorkflowJob`)
- be connected, i.e., from any `WorkflowJob` it is possible to reach every other `WorkflowJob` in the `Workflow` (treating the `Workflow`'s connections as undirected)
- have no cycles.

#### Validation Error Table

| Error Code                   | Description                                                                                                               | Arguments                                                   |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| `WFJ_NO_OP`                  | The WorkflowJob has no OutputPort.                                                                                        | `WorkflowJob`                                               |
| `WFJ_TOO_FEW_IP`             | The WorkflowJob has too few InputPorts.                                                                                   | `WorkflowJob`, `InputPortType`                              |
| `WFJ_TOO_MANY_IP`            | The WorkflowJob has too many InputPorts.                                                                                  | `WorkflowJob`, `InputPortType`                              |
| `WFJ_TOO_FEW_OP`             | The WorkflowJob has too few OutputPorts.                                                                                  | `WorkflowJob`, `OutputPortType`                             |
| `WFJ_TOO_MANY_OP`            | The WorkflowJob has too many OutputPorts.                                                                                 | `WorkflowJob`, `OutputPortType`                             |
| `WFJ_INVALID_SETTINGS`       | The WorkflowJob has invalid settings.                                                                                     | `WorkflowJob`                                               |
| `IP_TYPE_MISMATCH`           | The InputPortType of InputPort does not belong to the underlying Job of WorkflowJob.                                      | `InputPort`                                                 |
| `IP_TOO_MANY_CONNECTIONS`    | The InputPort has more than one connections.                                                                              | `InputPort`                                                 |
| `OP_TYPE_MISMATCH`           | The OutputPortType of OutputPort does not belong to the underlying Job of WorkflowJob.                                    | `OutputPort`                                                |
| `RESOURCETYPE_LIST_CONFLICT` | InputPort accepts a list of resources but OutputPort is not list-typed. OR OutputPort is list-typed but InputPort is not. | `OutputPort`, `InputPort`                                   |
| `NO_COMMON_RESOURCETYPE`     | There is no common ResourceType between an OutputPort and connected InputPorts.                                           | `OutputPort`, `InputPort1`, `InputPort2`, ..., `InputPortN` |
| `WF_EMPTY`                   | Workflow is empty.                                                                                                        | None                                                        |
| `WF_NOT_CONNECTED`           | The Workflow is not connected.                                                                                            | None                                                        |
| `WF_HAS_CYCLES`              | The Workflow has cycles.                                                                                                  | `Connection` (that causes the problem)                      |

Example: the server may return -

```
HTTP 409 CONFLICT
{
    'associated_objects': {
        'workflowjobs': ['http://testserver/workflowjob/06b056b9282f445591c6f564e09bdae2/']
    },
    'details': ['The WorkflowJob gamera.rotate has invalid settings.'],
    'error_code': 'WFJ_INVALID_SETTINGS'
}
```

## Workflow Graph Validity Check Algorithm

**Step 0** If there are no `WorkflowJob`s, the graph is empty. Terminate the algorithm.

**Step 1** Initialize variable `permanent_marks_global <- ∅` and `temporary_marks_global <- ∅`. Let `U` denotes to the universal set containing all `WorkflowJob`s.

**Step 2** Initialize [disjoint-set data structure](http://en.wikipedia.org/wiki/Disjoint-set_data_structure): for every `WorkflowJob` as `v`, perform `MakeSet(v)`.

**Step 3** Perform following "integrated depth-first-search" subroutine on an arbitrary `WorkflowJob` in `U\permanent_marks_global` as `w`: (algorithm enhanced from [cycle detection algorithm](http://en.wikipedia.org/wiki/Topological_sorting#Algorithms) to perform connectivity check in one DFS)

- If `w ∈ temporary_marks_global`, the graph HAS a cycle. Raise an exception.
- If `w ∉ permanent_marks_global`:
  - `temporary_marks_global <- temporary_marks_global ∪ {w}`
  - Find all distinct `WorkflowJob`s whose `input_port`s are connected to `output_port`s of `w`, for every of them as `v`:
    - perform "integrated depth-first-search" subroutine on `v`.
    - perform `Union(w, v)`
  - `permanent_marks_global <- permanent_marks_global ∪ {w}`
  - `temporary_marks_global <- temporary_marks_global - {w}`

**Step 4** If `U\permanent_marks_global ≠ ∅`, jump to **Step 2**

**Step 5** If `∃w, v   s.t., Find(w) ≠ Find(v)`, the graph is NOT connected. Terminate the algorithm.

**Step 6** Declare that the graph is connected and has no cycles.

## Examples of Workflow Validity

| Example                                            | Validity                            |
| -------------------------------------------------- | ----------------------------------- |
| ![loop test](images/test_loop.jpg)                 | Not valid. The Workflow has cycles. |
| ![merge test](images/test_merging_workflow.jpg)    | Valid.                              |
| ![branch test](images/test_branching_workflow.jpg) | Valid.                              |
