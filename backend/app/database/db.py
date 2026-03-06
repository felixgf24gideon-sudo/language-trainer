import sqlite3
import os
from pathlib import Path

def get_db_path() -> str:
    return os.getenv("DATABASE_PATH", "./language_trainer.db")

def get_connection() -> sqlite3.Connection:
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    schema_path = Path(__file__).parent / "schema.sql"
    conn = get_connection()
    try:
        with open(schema_path, "r") as f:
            schema_sql = f.read()
        conn.executescript(schema_sql)
        conn.commit()
    finally:
        conn.close()

def create_user(username: str) -> int:
    conn = get_connection()
    try:
        cursor = conn.execute(
            "INSERT OR IGNORE INTO users (username) VALUES (?)", (username,)
        )
        conn.commit()
        if cursor.lastrowid:
            return cursor.lastrowid
        row = conn.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
        return row["id"]
    finally:
        conn.close()

def get_user(username: str) -> dict:
    conn = get_connection()
    try:
        row = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if row:
            return dict(row)
        return None
    finally:
        conn.close()

def update_user_stats(user_id: int, level: int, total_tasks: int, correct_tasks: int):
    conn = get_connection()
    try:
        conn.execute(
            """UPDATE users SET level = ?, total_tasks = ?, correct_tasks = ?,
               updated_at = CURRENT_TIMESTAMP WHERE id = ?""",
            (level, total_tasks, correct_tasks, user_id)
        )
        conn.commit()
    finally:
        conn.close()

def save_task(user_id: int, task_type: str, instruction: str, expected_answer: str, user_answer: str) -> int:
    conn = get_connection()
    try:
        cursor = conn.execute(
            """INSERT INTO tasks (user_id, task_type, instruction, expected_answer, user_answer)
               VALUES (?, ?, ?, ?, ?)""",
            (user_id, task_type, instruction, expected_answer, user_answer)
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()

def save_evaluation(task_id: int, grammar: int, vocabulary: int, naturalness: int,
                    task_completion: int, is_correct: bool, errors: str, error_types: str):
    conn = get_connection()
    try:
        conn.execute(
            """INSERT INTO evaluations (task_id, grammar_score, vocabulary_score, naturalness_score,
               task_completion_score, is_correct, errors, error_types)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (task_id, grammar, vocabulary, naturalness, task_completion, is_correct, errors, error_types)
        )
        conn.commit()
    finally:
        conn.close()

def update_user_error(user_id: int, error_type: str):
    conn = get_connection()
    try:
        existing = conn.execute(
            "SELECT id FROM user_errors WHERE user_id = ? AND error_type = ?",
            (user_id, error_type)
        ).fetchone()
        if existing:
            conn.execute(
                """UPDATE user_errors SET count = count + 1, last_occurrence = CURRENT_TIMESTAMP
                   WHERE user_id = ? AND error_type = ?""",
                (user_id, error_type)
            )
        else:
            conn.execute(
                "INSERT INTO user_errors (user_id, error_type) VALUES (?, ?)",
                (user_id, error_type)
            )
        conn.commit()
    finally:
        conn.close()

def get_user_error_profile(user_id: int) -> dict:
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT error_type, count FROM user_errors WHERE user_id = ? ORDER BY count DESC",
            (user_id,)
        ).fetchall()
        if not rows:
            return {}
        total = sum(row["count"] for row in rows)
        return {row["error_type"]: row["count"] / total for row in rows}
    finally:
        conn.close()
