import os
from contextlib import contextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:dev@localhost:5432/tasks"
)

app = FastAPI(title="Task API")


class TaskIn(BaseModel):
    title: str
    done: bool = False


def get_connection():
    return psycopg.connect(DATABASE_URL)


def init_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    done BOOLEAN NOT NULL DEFAULT FALSE
                )
            """)
            cur.execute("SELECT COUNT(*) FROM tasks")
            count = cur.fetchone()[0]

            if count == 0:
                cur.executemany(
                    "INSERT INTO tasks (title, done) VALUES (%s, %s)",
                    [
                        ("Learn PostgreSQL", False),
                        ("Build Task API", False),
                        ("Test CRUD endpoints", False),
                    ],
                )
        conn.commit()


@app.on_event("startup")
def startup():
    init_db()


@app.get("/health")
def health():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                cur.fetchone()
        return {"status": "ok", "db": "ok"}
    except Exception:
        return {"status": "error", "db": "error"}


@app.get("/tasks")
def get_tasks():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, title, done FROM tasks ORDER BY id")
            rows = cur.fetchall()

    return [{"id": r[0], "title": r[1], "done": r[2]} for r in rows]


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, title, done FROM tasks WHERE id = %s",
                (task_id,),
            )
            row = cur.fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"id": row[0], "title": row[1], "done": row[2]}


@app.post("/tasks", status_code=201)
def create_task(task: TaskIn):
    if not task.title.strip():
        raise HTTPException(status_code=400, detail="Title is required")

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO tasks (title, done)
                VALUES (%s, %s)
                RETURNING id, title, done
                """,
                (task.title.strip(), task.done),
            )
            row = cur.fetchone()
        conn.commit()

    return {"id": row[0], "title": row[1], "done": row[2]}


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskIn):
    if not task.title.strip():
        raise HTTPException(status_code=400, detail="Title is required")

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE tasks
                SET title = %s, done = %s
                WHERE id = %s
                RETURNING id, title, done
                """,
                (task.title.strip(), task.done, task_id),
            )
            row = cur.fetchone()
        conn.commit()

    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"id": row[0], "title": row[1], "done": row[2]}


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM tasks WHERE id = %s RETURNING id",
                (task_id,),
            )
            row = cur.fetchone()
        conn.commit()

    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return None
