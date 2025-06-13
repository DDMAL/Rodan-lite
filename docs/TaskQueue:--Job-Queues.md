# Rodan Job Queues

Rodan assigns jobs to different queues in Celery depending on the kind of job it is.
At the time of writing the queues are:

* None or celery: this is **only** for core jobs and runs on the celery container;
* Python3: this is for all Python3 jobs and runs on the py3-celery container; and
* GPU: this is for all Python3 jobs that need a GPU and runs on the gpu-celery container.

# Specifying a Queue for a Job

There are two places a job queue must be specified for a job: in Rodan's `settings.py` and the `settings` parameter of the job itself.

## Updating `settings.py`

In the file `/rodan/code/rodan/settings.py` there are three arrays representing queues for rodan jobs.
These are `RODAN_PYTHON3_JOBS`, and `RODAN_GPU_JOBS` for the Python3, and GPU queues respectively.
These contain the location of the module for your job. So if your job `some-job` is in the `jobs` folder, it would be represented as `rodan.jobs.some-job`.

Each job is commented out in `settings.py` by default. It should be prefixed with the appropriate comment for that queue. The prefixes for the Python3 and GPU queues are, respectively, `#py3 ` and `#gpu `. Note that each contains a space at the end.
This would make the full line for your job if it was in the Python3 queue `#py3 "rodan.jobs.some-job",`.

## Specifying Queue in the Job

Each Rodan job can have a settings attribute among the others as specified [on the Rodan wiki](https://github.com/DDMAL/Rodan/wiki/Write-a-Rodan-job-package#1-describe-a-rodan-job).
This settings attribute should be a dictionary containing a key `job_queue` whose value is the desired queue.

**A queue should be specified**

The settings dictionary should look something like this:
```python
settings = {
    ...
    "job_queue": "Python3",
    ...
}
```

