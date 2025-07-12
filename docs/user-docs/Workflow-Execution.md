The execution of a workflow is implemented by creating and executing a `WorkflowRun` instance in order to conform to RESTful API.

# WorkflowRun Creation

The creation of a `WorkflowRun` is implemented by following subroutines.

### Validate Resource Assignments

The `WorkflowRun` must be created with a resource assignment dictionary, mapping an `InputPort` URL to a list of `Resource` URLs. Following conditions should be satisfied:
 * all unsatisfied `InputPort`s must be provided with `Resource`s.
 * there must be one "multiple resource collection".
 * the resource must be ready (`has compat_resource_file`)
 * the resource type of related `InputPort` should agree with assigned `Resource`s.


### Get "Singleton" `RunJob`s
A "singleton" in this context is a `WorkflowJob` that will have exactly one `RunJob` associated with it in a `WorkflowRun`.  That is, it does not exist in an execution path that is involved with a `resource_collection` that has multiple `Resource`s. The `output` of this singleton will be used as many times as required for the `WorkflowRun`.
* **singleton_workflowjobs** <-- all `WorkflowJob`s
* if there exists a `resource_collection` in `Workflow.resource_collections[]` where the size of `resources[]` > 1
 * traverse down graph (i.e. from `input_port` to `output_port`); for each node (i.e. `WorkflowJob`) visited, remove it from **singleton_workflowjobs**
* return **singleton_workflowjobs**

### Get "end-point" `WorkflowJob`s
An "end-point" is simply a stopping point in the execution path.  End-points are used as the starting place for building `RunJob`s.
* **endpoint_workflowjobs** <-- []
* for each `WorkflowJob`
 * if an `output_port` is not referenced in `Connections`
   * add `WorkflowJob` to **endpoint_workflowjobs**
* return **endpoint_workflowjobs**

### Create `RunJob`
This recursively creates `RunJob`s.  Assume the input `WorkflowJob` is A.
* if `WorkflowJob` A has no associated `RunJob` in **workflowjob_runjob_map**
 * create `RunJob` A
 * create `Resource` entries (setting `origin` and `resource_type` accordingly) for `RunJob` A's `outputs[]` and add to `RunJob.outputs[]`
 * for each `input_port` with associated `Connection` that points to a `WorkflowJob`'s (call it B) `output_port`
    * if `WorkflowJob` B has no associated `RunJob` in **workflowjob_runjob_map**
        * run Create `RunJob` on `Workflow` B
    * get `RunJob` for `WorkflowJob` B (call it `RunJob` B)
    * add `input` for this `input_port`, using the information from the appropriate `output` of `RunJob` B
 * for each `input_port` with associated `resource_assignment`
   * add `input` for this `input_port`, using the information from the appropriate `resource_assignment`
 * add `WorkflowJob` A <-> `RunJob` A to **workflowjob_runjob_map**

### Create `WorkflowRun`
This goes through the end-points and builds `RunJob`s upwards. Those `WorkflowJob`s that are "singletons" have references kept for them so they are not recreated.

The outer loop iterates over a `resource_assignment` that has multiple `Resource`s.
* **endpoint_workflowjobs** <-- Get "End-point" `WorkflowJob`s
* **singleton_workflowjobs** <-- Get "Singleton" `WorkflowJob`s
* **workflowjob_runjob_map** <-- []
* if there exists a `resource_collection` in `Workflow.resource_collections[]` where the size of `resources[]` > 1, execute the following loop using a unique `Resource` from the `resources` at each iteration; else, execute the loop as is
  * for each **endpoint_workflowjobs**
     * run Create `RunJob` on `WorkflowJob`
  * clear **workflowjob_runjob_map** of those entries associated with `WorkflowJob`s that do not exist in **singleton_workflowjobs**

# WorkflowRun Execution

After creating a `WorkflowRun` with `RunJob`s, `Input`s, `Output`s and `Resource`s, its execution immediately starts.

### Behind the Scene

Rodan jobs are not running in Django thread. Instead, Django thread sends message to Celery thread, so task running does not block Django processing HTTP requests. (In fact, there may be multiple Celery worker threads. Here I simplify the concept with "Celery thread".)

The message sending is based on a message queue (in our case RabbitMQ). Both Django and Celery thread can put messages into the queue, but only can Celery thread take out messages.

[[images/workflow_execution__message_queue.png]]


### Master Task

Master task is the only entrance to execute Rodan jobs. It runs purely in Celery thread.

Master task takes a single parameter `workflow_run_id`. It first checks database to find `RunJob`s that are ready to run, i.e., the resources of `Input`s are all produced by previous `RunJob`s in the `WorkflowRun`, AND have received user's input (for interactive jobs, see below). Then it calls all runnable `RunJob`s and chains another Master task. At the end of execution, Master task cannot find any more runnable `RunJob`, and will return without calling any jobs.

A simple example:

[[images/workflow_execution__simple_example.png]]

### Interactive Jobs

An interactive job in the manual phase has its status `WAITING_FOR_INPUT`. Master task will not execute it. After the user has finished the manual phase, its status is set to `SCHEDULED` and master task is called to execute the remaining automatic phases.

[[images/workflow_execution__simple_interactive.png]]


### RunJob status

A RunJob could have one of the following statuses:

[[images/workflow_execution__runjob_status.png]]

Its celery task ID is only assigned after putting into the Celery queue. The statuses are defined in [`constants.py`](https://github.com/DDMAL/Rodan/blob/develop/rodan/constants.py)

### WorkflowRun status

A RunJob could have one of the following statuses:

[[images/workflowrun_statuses.png]]

The three `REQUEST_*` statuses are inserted because WorkflowRun creation, cancellation, and redo are executed in Celery thread asynchronously.

##### Cancellation

Cancelling an execution is by PATCHing `{cancelled: True}`. Django thread will set WorkflowRun to `REQUEST_CANCELLING`. Then the Celery thread terminates all running `RunJob`s, set all unfinished `RunJob`s to `CANCELLED`, and finally set the WorkflowRun as `CANCELLED`.

##### Redo

Redoing an execution can happen when a RunJob is failed (thus the WorkflowRun is failed) or the user would like to redo an interactive RunJob. It is necessary to provide a RunJob as the root of the RunJob tree to be redone.

As cancellation, Django thread will set WorkflowRun to `REQUEST_RETRYING`. Then the Celery thread terminates all running `RunJob`s, deletes the execution records of the RunJob tree, restarts them, and finally set the WorkflowRun as `RETRYING`.

### Test dummy workflow

Test is based on dummy jobs -- one automatic and one interactive. They basically copy one of the input to all outputs. If a string "fail" is in the input, the job will fail by raising an exception.

[[images/workflow_execution__complex.png]]

[draw.io XML source file of this image](images/workflow_execution__complex.drawio.xml)