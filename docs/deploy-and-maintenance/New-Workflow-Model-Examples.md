Jump to:

- [`Job` Example](https://github.com/DDMAL/Rodan/wiki/New-Workflow-Model-Examples#job-example)
- [`Workflow` Example](https://github.com/DDMAL/Rodan/wiki/New-Workflow-Model-Examples#workflow-example)
- [`WorkflowJob` Example](https://github.com/DDMAL/Rodan/wiki/New-Workflow-Model-Examples#workflowjob-example)

# `Job` Example

Suppose we have two images from a [table-book](http://en.wikipedia.org/wiki/Table-book) we would like to process. For our example, this will include:

1. binarization
1. border cropping (interactive)
1. segmentation (interactive)
1. classification for lute tablature
1. classification for voice

Let's assume that these tasks can be taken care of by five different jobs.

## Binarization

- name: binarization
- description: Given a colour PNG, returns a onebit PNG.
- interactive: false
- settings:

| key       | range                |
| --------- | -------------------- |
| threshold | non-negative integer |

- input_port_types:

| name  | resource_type | minimum | maximum |
| ----- | ------------- | ------- | ------- |
| image | image/rgb+png | 1       | 1       |

- output_port_types:

| name  | resource_type    |
| ----- | ---------------- |
| image | image/onebit+png |

## Border Cropping

- name: border_cropping
- description: Given a onebit PNG, an interactive job is launched that allows to mask a square of the given image, leaving the remaining border white.
- interactive: true
- settings: none
- input_port_types:

| name  | resource_type    | minimum | maximum |
| ----- | ---------------- | ------- | ------- |
| image | image/onebit+png | 1       | 1       |

- output_port_types:

| name  | resource_type    |
| ----- | ---------------- |
| image | image/onebit+png |

## Segmentation

- name: segmentation
- description: Given a onebit PNG, an interactive job is launched that allows the user to denote areas of the image with one of three labels. The possible labels are "lute", "voice", and "perc".
- interactive: true
- settings: none
- input_port_types:

| name  | resource_type    | minimum | maximum |
| ----- | ---------------- | ------- | ------- |
| image | image/onebit+png | 1       | 1       |

- output_port_types:

| name  | resource_type    |
| ----- | ---------------- |
| lute  | image/onebit+png |
| voice | image/onebit+png |
| perc  | image/onebit+png |

## Lute Tab Classification

- name: classification_lute_tab
- description: Given a onebit PNG and XML classifier file for lute tab, returns an XML classifier result file.
- interactive: false
- settings: none
- input_port_types:

| name       | resource_type    | minimum | maximum |
| ---------- | ---------------- | ------- | ------- |
| image      | image/onebit+png | 1       | 1       |
| classifier | application/xml  | 1       | 1       |

- output_port_types:

| name              | resource_type |
| ----------------- | ------------- |
| classifier_result | xml           |

## Voice Classification

- name: classification_voice
- description: Given a onebit PNG and XML classifier file for voice, returns an XML classifier result file.
- interactive: false
- settings: none
- input_port_types:

| name       | resource_type    | minimum | maximum |
| ---------- | ---------------- | ------- | ------- |
| image      | image/onebit+png | 1       | 1       |
| classifier | application/xml  | 1       | 1       |

- output_port_types:

| name              | resource_type   |
| ----------------- | --------------- |
| classifier_result | application/xml |

# `Workflow` Example

Given the above jobs, we can construct the appropriate `WorkflowJobs` which will then form a complete `Workflow`.

![Workflow Example](images/workflow_jobs.jpg)

# `WorkflowJob` Example

## WorkflowJob 1

![WorkflowJob 1](images/WorkflowJob1.jpg)

- job: binarization
- settings: none
- input_ports:

| label    | input_port_type |
| -------- | --------------- |
| input1-1 | image           |

- output_ports:

| label     | output_port_type |
| --------- | ---------------- |
| output1-1 | image            |

## WorkflowJob 2

![WorkflowJob 2](images/WorkflowJob2.jpg)

- job: border_cropping
- settings: none
- input_ports:

| label    | input_port_type |
| -------- | --------------- |
| input2-1 | image           |

- output_ports:

| label     | output_port_type |
| --------- | ---------------- |
| output2-1 | image            |

## WorkflowJob 3

Notice how this `WorkflowJob` has only two `output_port`s despite the associated `Job` (segmentation) having three `output_port_type`s. The segmentation `Job` is able to provide "lute", "voice", and "perc" outputs, but WorkflowJob 3 will deliver only the "lute" and "voice" parts.

![WorkflowJob 3](images/WorkflowJob3.jpg)

- job: segmentation
- settings: none
- input_ports:

| label    | input_port_type |
| -------- | --------------- |
| input3-1 | image           |

- output_ports:

| label     | output_port_type |
| --------- | ---------------- |
| output3-1 | lute             |
| output3-2 | voice            |

## WorkflowJob 4

![WorkflowJob 4](images/WorkflowJob4.jpg)

- job: classification_lute_tab
- settings: none
- input_ports:

| label    | input_port_type |
| -------- | --------------- |
| input4-1 | lute            |
| input4-2 | classifier      |

- output_ports:

| label     | output_port_type  |
| --------- | ----------------- |
| output4-1 | classifier_result |

## WorkflowJob 5

![WorkflowJob 5](images/WorkflowJob5.jpg)

- job: classification_voice
- settings: none
- input_ports:

| label    | input_port_type |
| -------- | --------------- |
| input5-1 | voice           |
| input5-2 | classifier      |

- output_ports:

| label     | output_port_type  |
| --------- | ----------------- |
| output5-1 | classifier_result |
