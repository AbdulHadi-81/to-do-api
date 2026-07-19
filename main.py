"""
Routes layer — handles HTTP only: reading requests, calling the service,
and returning the right status codes. No business logic and no data
storage details live here.
"""

from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from typing import Optional

import service

app = FastAPI()


class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None


@app.get("/")
def root():
    """Returns basic info about this API."""
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health")
def health():
    """Health check — confirms the server is running."""
    return {"status": "ok"}


@app.get("/tasks")
def get_tasks():
    """Returns the full list of tasks."""
    return service.list_tasks()


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    """Returns a single task by id, or 404 if it doesn't exist."""
    try:
        return service.get_task(task_id)
    except service.NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    """Creates a new task. Title is required and cannot be empty."""
    try:
        return service.create_task(task.title)
    except service.ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/tasks/{task_id}")
def update_task(task_id: int, update: TaskUpdate):
    """Updates a task's title and/or done status. Returns 404 if not found."""
    try:
        return service.update_task(task_id, update.title, update.done)
    except service.ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except service.NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    """Deletes a task by id. Returns 404 if not found."""
    try:
        service.delete_task(task_id)
        return Response(status_code=204)
    except service.NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))