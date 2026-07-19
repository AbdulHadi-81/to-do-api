"""
Repository layer — the ONLY place that knows how tasks are stored.
Right now: a plain Python list (in memory).
Later (Week 3): this file gets replaced with a Postgres version —
nothing in service.py or main.py will need to change.
"""

# Our "database" — just a list living in memory
_tasks = [
    {"id": 1, "title": "Buy milk", "done": False},
    {"id": 2, "title": "Walk the dog", "done": False},
    {"id": 3, "title": "Finish assignment", "done": True},
]


def get_all():
    """Return every task."""
    return _tasks


def get_by_id(task_id: int):
    """Return one task by id, or None if it doesn't exist."""
    for task in _tasks:
        if task["id"] == task_id:
            return task
    return None


def create(title: str):
    """Create a new task with the next available id."""
    next_id = max((t["id"] for t in _tasks), default=0) + 1
    new_task = {"id": next_id, "title": title, "done": False}
    _tasks.append(new_task)
    return new_task


def update(task_id: int, title: str | None, done: bool | None):
    """Update an existing task's title and/or done status. Returns None if not found."""
    task = get_by_id(task_id)
    if task is None:
        return None
    if title is not None:
        task["title"] = title
    if done is not None:
        task["done"] = done
    return task


def delete(task_id: int) -> bool:
    """Delete a task by id. Returns True if deleted, False if not found."""
    task = get_by_id(task_id)
    if task is None:
        return False
    _tasks.remove(task)
    return True
