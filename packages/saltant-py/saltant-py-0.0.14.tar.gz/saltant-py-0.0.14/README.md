[![Build Status](https://travis-ci.com/mwiens91/saltant-py.svg?branch=master)](https://travis-ci.com/mwiens91/saltant-py)
[![Documentation Status](https://readthedocs.org/projects/saltant-py/badge/?version=latest)](https://saltant-py.readthedocs.io/en/latest/?badge=latest)
[![PyPI](https://img.shields.io/pypi/v/saltant-py.svg)](https://pypi.org/project/saltant-py/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/saltant-py.svg)](https://pypi.org/project/saltant-py/)

# saltant SDK for Python

### NOTE: this project is an active work in progress

This attempts to follow the coding paradigms of
[docker-py](https://github.com/docker/docker-py) fairly closely.

## Example

```python
from __future__ import print_function
import time
from saltant.client import Client
from saltant.constants import (
    SUCCESSFUL,
    FAILED,
)

API_TOKEN = 'p0gch4mp101fy451do9uod1s1x9i4a'
API_BASE_URL = 'https://shahlabjobs.ca/api/'
TASK_INSTANCE_UUID_TO_GET = '4ce0f9f1-9ae3-4baf-8838-76a19758fb29'


# Instantiate a Client object
client = Client(base_api_url=API_BASE_URL, auth_token=API_TOKEN)

# GET a task instance we know the UUID of. This will return an instance
# of the ExecutableTaskInstance model.
my_task_instance = client.executable_task_instances.get(
    uuid=TASK_INSTANCE_UUID_TO_GET)

# List attributes and methods of the task instance we just got.
print(dir(my_task_instance))

# Launch an instance of executable task type 1 :D
new_task_instance = client.executable_task_instances.create(
    name="saltant-py test",
    arguments={
        "tag_name": None,
        "output_dir": "/shahlab/archive/single_cell_indexing/NextSeq/fastq/160705_NS500668_0105_AHGTTWBGXY",
        "flowcell_id": "AHGTTWBGXY",
        "storage_name": "shahlab",
        "storage_directory": "/shahlab/archive"
    },
    task_queue_id=1,
    task_type_id=1,
)

# Wait until task instance completes
while True:
    # Wait a bit
    time.sleep(3)

    # Get job's status
    status = client.executable_task_instances.get(
        uuid=new_task_instance.uuid).state

    if status == SUCCESSFUL:
        print("yay!")
        break
    elif status == FAILED:
        print("noo!")
        break
```

## Installation

Using pip,

```
pip install saltant-py
```
