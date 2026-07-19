"""
Service layer — business logic and validation.
Talks to the repository for data, but knows nothing about HTTP,
status codes, or how requests/responses work. That's main.py's job.
"""

import repository


class NotFoundError(Exception):
    """Raised when a task doesn't exist."""
    pass


class ValidationError(Exception):
    """Raised when input data is invalid."""
    pass


def list_tasks():
    return repository.get_all()


def get_task(task_id: int):
    task = repository.get_by_id(task_id)
    if task is None:
        raise NotFoundError(f"Task {task_id} not found")
    return task


def create_task(title: str):
    if not title or not title.strip():
        raise ValidationError("Title is required and cannot be empty")
    return repository.create(title)


def update_task(task_id: int, title: str | None, done: bool | None):
    if title is not None and not title.strip():
        raise ValidationError("Title cannot be empty")
    task = repository.update(task_id, title, done)
    if task is None:
        raise NotFoundError(f"Task {task_id} not found")
    return task


def delete_task(task_id: int):
    deleted = repository.delete(task_id)
    if not deleted:
        raise NotFoundError(f"Task {task_id} not found")
