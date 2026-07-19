# Task API

A small CRUD (Create, Read, Update, Delete) API for managing a to-do list, built with **FastAPI** and Python.
Data is stored **in memory** it resets whenever the server restarts (no database yet, that's coming in Week 3).

Built as part of the FlyRank Internship — Backend Track, Week 2, Assignment A1.

---

## How to install & run

**Requirements:** Python 3.10+

```bash
# 1. Clone this repo
git clone https://github.com/AbdulHadi-81/to-do-api.git
cd to-do-api

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\Activate.ps1      # Windows PowerShell
# source venv/bin/activate     # Mac/Linux

# 3. Install dependencies
pip install fastapi uvicorn

# 4. Run the server
uvicorn main:app --reload
```

The server runs at: `http://localhost:8000`

Interactive Swagger docs: `http://localhost:8000/docs`

---

## Endpoints

| Method | Path            | Description                          | Success | Errors        |
|--------|-----------------|---------------------------------------|---------|---------------|
| GET    | `/`             | API info                             | 200     | —             |
| GET    | `/health`       | Health check                         | 200     | —             |
| GET    | `/tasks`        | List all tasks                       | 200     | —             |
| GET    | `/tasks/{id}`   | Get a single task                    | 200     | 404           |
| POST   | `/tasks`        | Create a new task                    | 201     | 400           |
| PUT    | `/tasks/{id}`   | Update a task's title and/or done    | 200     | 400, 404      |
| DELETE | `/tasks/{id}`   | Delete a task                        | 204     | 404           |

---

## Example request

```bash
curl -i -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d '{"title":"Buy milk"}'
```

**Example response:**
```
HTTP/1.1 201 Created
date: Sat, 18 Jul 2026 19:30:19 GMT
server: uvicorn
content-length: 40
content-type: application/json

{"id":5,"title":"Buy milk","done":false}
```

---

## Swagger UI


![Swagger UI screenshot](Swagger_1.jpeg)



![Swagger UI screenshot](Swagger_2.jpeg)


## Notes on in-memory storage

Because tasks are stored in a Python list (not a database), all data is lost whenever the server restarts.
This is intentional for this stage it's the reason Week 3 introduces a real database.


---

## Week 3 — Real Persistence with Postgres

### What changed
The API now uses a real **Postgres** database instead of an in-memory Python list.
Tasks now survive server restarts.

To make this possible, the project was first restructured into layers:
- **`main.py`** — routes only (HTTP handling, status codes)
- **`service.py`** — business logic and validation
- **`repository.py`** — the only file that knows how data is stored

When switching from in-memory storage to Postgres, **only `repository.py` changed.**
`service.py` and `main.py` were not touched proving the layered architecture works
as intended.

### A note on Docker
This assignment asks for Postgres to run inside Docker. I attempted this, but my
machine's BIOS has hardware virtualization disabled, and the BIOS itself is
password-protected by a previous owner/admin account I don't have access to
so Docker Desktop cannot run containers on this machine (`docker run` fails with
"virtualization support not detected", confirmed via `systeminfo`).

As an honest substitute, I installed **Postgres natively on Windows** instead.
This still satisfies the actual goal of the assignment — a real, persistent
database, connected via a `.env`-configured connection string, with the same
repository-swap architecture proof. The only difference is *how* Postgres is
running (native service vs. container), not *what* it demonstrates.

### How to install & run (Week 3 version)

**Requirements:** Python 3.10+, PostgreSQL 16+ installed locally

```bash
# 1. Clone this repo
git clone https://github.com/AbdulHadi-81/to-do-api.git
cd to-do-api

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\Activate.ps1      # Windows PowerShell

# 3. Install dependencies
pip install fastapi uvicorn psycopg2-binary python-dotenv

# 4. Create your .env file (copy .env.example and fill in your real password)
copy .env.example .env

# 5. Create the database and table
psql -U postgres -c "CREATE DATABASE todo_db;"
psql -U postgres -d todo_db -f init.sql

# 6. Run the server
uvicorn main:app --reload
```

### Proving persistence

1. Created a task via `POST /tasks`
2. Restarted the Postgres Windows service (Services → postgresql-x64-18 → Restart)
3. Restarted the FastAPI server (`Ctrl+C`, then `uvicorn main:app --reload` again)
4. Ran `GET /tasks` — the created task was still present

This confirms data is persisted by Postgres itself, not held in application memory.