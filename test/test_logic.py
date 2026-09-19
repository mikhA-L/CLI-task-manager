import json
import pytest  
from tmain.taskmanager import (
    add_task,
    save_tasks,
    load_tasks,
    mark_complete,
    del_tasks
)

def test_add_task_success():
    #test adding a valid task to an empty list
    tasks = []
    add_task(tasks, "Study Python", "High")

    assert len(tasks) == 1
    assert tasks[0]["id"] == 1
    assert tasks[0]["title"] == "Study Python"
    assert tasks[0]["priority"] == "High"
    assert tasks[0]["completed"] is False

def test_add_task_default_priority():
    #test if adding a task with no name raise value error
    tasks = []
    with pytest.raises(ValueError):
        add_task(tasks, "   ")

def test_mark_complete_success():
    #marking an already existing task
    tasks = [{"id":1, "title":"Buy grocery", "completed":False}]

    result = mark_complete(tasks, tasks_id=1)

    assert result is True
    assert tasks[0]["completed"] is True

def test_mark_complete_invalid_id():
    #test marking an id that doesnt exist
    tasks = [{"id":1, "title":"Buy grocery", "completed":False}]

    result = mark_complete(tasks, tasks_id=99)

    assert result is False
    assert tasks[0]["completed"] is False

def delete_task_and_reindex():
    #testing deleting a task and ensure reindex id
    tasks = [
        {"id": 1, "title": "Task 1", "completed": False},
        {"id": 2, "title": "Task 2", "completed": False},
        {"id": 3, "title": "Task 3", "completed": False},
    ]

    deleted_item = del_tasks(tasks, task_id=2)

    assert deleted_item["title"] == "Task 2"
    assert len(tasks) == 2
    # Ensure IDs were re-indexed from 1 to 2
    assert tasks[0]["id"] == 1
    assert tasks[1]["id"] == 2
    assert tasks[1]["title"] == "Task 3"

def test_save_and_load_task(tmp_path):
    #test saving task to JSON and loading back using temporary directories
    temp_file = tmp_path/"test_task.json"

    original_tasks = [{"id": 1, "title": "Temp Task", "completed": False}]

    save_tasks(original_tasks, filepath=str(temp_file))

    loaded_tasks = load_tasks(filepath=str(temp_file))

    assert loaded_tasks == original_tasks

def test_load_tasks_missing_file(tmp_path):
    #testing for a file that doesnt exist
    non_existent_file = tmp_path / "does_not_exist.json"

    tasks = load_tasks(filepath=str(non_existent_file))

    assert tasks == []