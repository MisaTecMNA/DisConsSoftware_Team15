# ws_crud_work.py
import sqlite3
from pathlib import Path
from typing import Optional, List, Dict, Any

DB_FILE = "crud_dr.db"

# ---------- Utils de conexión ----------
def get_conn():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

# ---------- Esquema ----------
def init_db():
    with get_conn() as c:
        # crea tabla work
        c.execute("""
        CREATE TABLE IF NOT EXISTS work (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            theme TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        """)

# ---------- CRUD ----------
def create_work(title: str, theme: Optional[str]) -> Dict[str, Any]:
    init_db()
    with get_conn() as c:
        c.execute("""
            INSERT INTO work(title, theme, created_at, updated_at)
            VALUES (?, ?, datetime('now'), datetime('now'))
        """, (title, theme))
        new_id = c.execute("SELECT last_insert_rowid()").fetchone()[0]
        row = c.execute("SELECT * FROM work WHERE id = ?", (new_id,)).fetchone()
        return dict(row)

def get_work(work_id: int) -> Optional[Dict[str, Any]]:
    init_db()
    with get_conn() as c:
        row = c.execute("SELECT * FROM work WHERE id = ?", (work_id,)).fetchone()
        return dict(row) if row else None

def list_works(
    q: Optional[str] = None,
    theme: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    order: str = "desc"
) -> Dict[str, Any]:
    init_db()
    where, params = [], []
    if q:
        where.append("title LIKE ?")
        params.append(f"%{q}%")
    if theme:
        where.append("theme = ?")
        params.append(theme)

    where_sql = f"WHERE {' AND '.join(where)}" if where else ""
    order_sql = "ASC" if order.lower() == "asc" else "DESC"

    with get_conn() as c:
        total = c.execute(f"SELECT COUNT(*) FROM work {where_sql}", params).fetchone()[0]
        rows = c.execute(
            f"SELECT * FROM work {where_sql} ORDER BY created_at {order_sql} LIMIT ? OFFSET ?",
            (*params, limit, offset)
        ).fetchall()
        return {
            "items": [dict(r) for r in rows],
            "total": total,
            "limit": limit,
            "offset": offset
        }

def update_work(work_id: int, title: str, theme: Optional[str]) -> Optional[Dict[str, Any]]:
    init_db()
    with get_conn() as c:
        cur = c.execute("""
            UPDATE work
               SET title = ?, theme = ?, updated_at = datetime('now')
             WHERE id = ?
        """, (title, theme, work_id))
        if cur.rowcount == 0:
            return None
        row = c.execute("SELECT * FROM work WHERE id = ?", (work_id,)).fetchone()
        return dict(row)

def patch_work(work_id: int, fields: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    init_db()
    allowed = {"title", "theme"}
    updates = {k: v for k, v in fields.items() if k in allowed}
    if not updates:
        raise ValueError("No valid fields. Use any of: title, theme")

    sets = []
    values = []
    for k, v in updates.items():
        sets.append(f"{k} = ?")
        values.append(v)
    sets.append("updated_at = datetime('now')")
    values.append(work_id)

    sql = "UPDATE work SET " + ", ".join(sets) + " WHERE id = ?"

    with get_conn() as c:
        cur = c.execute(sql, tuple(values))
        if cur.rowcount == 0:
            return None
        row = c.execute("SELECT * FROM work WHERE id = ?", (work_id,)).fetchone()
        return dict(row)

def delete_work(work_id: int) -> bool:
    init_db()
    with get_conn() as c:
        cur = c.execute("DELETE FROM work WHERE id = ?", (work_id,))
        return cur.rowcount > 0
