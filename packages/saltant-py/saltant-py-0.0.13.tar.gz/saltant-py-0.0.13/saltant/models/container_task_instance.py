"""Container task instance model and manager."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from .base_task_instance import (
    BaseTaskInstance,
    BaseTaskInstanceManager,
)


class ContainerTaskInstance(BaseTaskInstance):
    """Model for container task instances.

    Attributes:
        name (str): The name of the task instance.
        uuid (str): The UUID of the task instance.
        state (str): The state of the task instance.
        user (str): The username of the user who started the task.
        task_queue (int): The ID of the task queue the instance is
            running on.
        task_type (int): The ID of the task type for the instance.
        datetime_created (:class:`datetime.datetime`): The datetime when
            the task instance was created.
        datetime_finished (:class:`datetime.datetime`): The datetime
            when the task instance finished.
        arguments (dict): The arguments the task instance was run with.
    """
    pass


class ContainerTaskInstanceManager(BaseTaskInstanceManager):
    """Manager for container task instances.

    Attributes:
        _client (:py:class:`saltant.client.Client`): An authenticated
            saltant client.
        list_url (str): The URL to list task instances.
        detail_url (str): The URL format to get specific task instances.
        model (:py:class:`saltant.models.resource.Model`): The model of
            the task instance being used.
    """
    list_url = 'containertaskinstances/'
    detail_url = 'containertaskinstances/{id}/'
    model = ContainerTaskInstance
