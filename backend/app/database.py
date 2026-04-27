from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from threading import Lock
from typing import Any, Dict, List, Optional

DB_PATH = Path(__file__).resolve().parent / "smartnews.db"
_lock = Lock()


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with _lock:
        conn = _connect()
        try:
            cur = conn.cursor()
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS user_preferences (
                    user_id TEXT PRIMARY KEY,
                    payload TEXT NOT NULL
                )
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS topic_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    topic TEXT NOT NULL,
                    timeframe TEXT NOT NULL,
                    region TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.commit()
        finally:
            conn.close()


def get_preferences(user_id: str) -> Dict[str, Any]:
    with _lock:
        conn = _connect()
        try:
            row = conn.execute(
                "SELECT payload FROM user_preferences WHERE user_id = ?",
                (user_id,),
            ).fetchone()
            return json.loads(row["payload"]) if row else {}
        finally:
            conn.close()


def save_preferences(user_id: str, payload: Dict[str, Any]) -> None:
    with _lock:
        conn = _connect()
        try:
            conn.execute(
                """
                INSERT INTO user_preferences (user_id, payload)
                VALUES (?, ?)
                ON CONFLICT(user_id) DO UPDATE SET payload = excluded.payload
                """,
                (user_id, json.dumps(payload)),
            )
            conn.commit()
        finally:
            conn.close()


def record_topic_usage(user_id: str, topic: str, timeframe: str, region: str) -> None:
    with _lock:
        conn = _connect()
        try:
            conn.execute(
                "INSERT INTO topic_events (user_id, topic, timeframe, region) VALUES (?, ?, ?, ?)",
                (user_id, topic, timeframe, region),
            )
            conn.commit()
        finally:
            conn.close()


def get_usage_counts(user_id: str) -> Dict[str, int]:
    with _lock:
        conn = _connect()
        try:
            rows = conn.execute(
                """
                SELECT topic, COUNT(*) as count
                FROM topic_events
                WHERE user_id = ?
                GROUP BY topic
                ORDER BY count DESC
                """,
                (user_id,),
            ).fetchall()
            return {row["topic"]: row["count"] for row in rows}
        finally:
            conn.close()
