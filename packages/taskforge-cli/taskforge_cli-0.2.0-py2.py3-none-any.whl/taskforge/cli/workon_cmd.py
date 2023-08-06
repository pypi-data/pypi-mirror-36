"""usage: task workon <ID>

Find task with ID and make it so the priority of the task is 0.1 higher than
that of the current highest priority task. Effectively making it the "current"
task in Taskforge terms.
"""

import sys

from taskforge.cli.utils import inject_list
from taskforge.lists import NotFoundError


@inject_list
def run(args, task_list=None):
    """Print the current task in task_list."""
    try:
        new_current = task_list.find_by_id(args['<ID>'])
    except NotFoundError:
        print('no task with that id exists')
        sys.exit(1)

    try:
        task = task_list.current()
        current_priority = task.priority
    except NotFoundError:
        current_priority = 1.0

    new_current.priority = current_priority + 0.1
    try:
        task_list.update(new_current)
    except NotFoundError:
        print('something unexpected went wrong, unable to update task')
        sys.exit(1)
