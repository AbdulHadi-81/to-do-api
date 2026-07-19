import os
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def _get_connection():
    """Open a fresh connection to Postgres."""
    return psycopg2.connect(DATABASE_URL)


def get_all():
    """Return every task."""
    conn = _get_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT id, title, done FROM tasks ORDER BY id;")
            return cur.fetchall()
    finally:
        conn.close()


def get_by_id(task_id: int):
    """Return one task by id, or None if it doesn't exist."""
    conn = _get_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT id, title, done FROM tasks WHERE id = %s;", (task_id,))
            return cur.fetchone()
    finally:
        conn.close()


def create(title: str):
    """Create a new task. Postgres assigns the id automatically (SERIAL)."""
    conn = _get_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                "INSERT INTO tasks (title, done) VALUES (%s, FALSE) RETURNING id, title, done;",
                (title,)
            )
            new_task = cur.fetchone()
            conn.commit()
            return new_task
    finally:
        conn.close()


def update(task_id: int, title: str | None, done: bool | None):
    """Update an existing task's title and/or done status. Returns None if not found."""
    conn = _get_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            if title is not None:
                cur.execute(
                    "UPDATE tasks SET title = %s WHERE id = %s;",
                    (title, task_id)
                )
            if done is not None:
                cur.execute(
                    "UPDATE tasks SET done = %s WHERE id = %s;",
                    (done, task_id)
                )
            conn.commit()

            cur.execute("SELECT id, title, done FROM tasks WHERE id = %s;", (task_id,))
            return cur.fetchone()
    finally:
        conn.close()


def delete(task_id: int) -> bool:
    """Delete a task by id. Returns True if deleted, False if not found."""
    conn = _get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM tasks WHERE id = %s;", (task_id,))
            deleted = cur.rowcount > 0
            conn.commit()
            return deleted
    finally:
        conn.close()