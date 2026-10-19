
from flask import Flask, render_template, request, redirect, url_for, abort
import sqlite3
import secrets
import time
from pathlib import Path

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "notedrop.db"


def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

from datetime import datetime

@app.template_filter("datetimeformat")
def datetimeformat(timestamp):
    return datetime.fromtimestamp(timestamp).strftime("%d %b %Y, %I:%M %p")
def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                created_at INTEGER NOT NULL,
                expires_at INTEGER NOT NULL,
                max_views INTEGER NOT NULL,
                views INTEGER NOT NULL DEFAULT 0
            )
        """)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/create", methods=["POST"])
def create_note():
    content = request.form.get("content", "").strip()

    try:
        ttl = int(request.form.get("ttl", "60"))
        max_views = int(request.form.get("max_views", "5"))
    except ValueError:
        abort(400, description="Expiry and view limit must be numbers.")

    if not content or len(content) > 10000:
        abort(400, description="Content must be between 1 and 10,000 characters.")

    if ttl not in (5, 60, 1440, 10080):
        abort(400, description="Invalid expiry duration.")

    if not 1 <= max_views <= 100:
        abort(400, description="View limit must be between 1 and 100.")

    now = int(time.time())
    note_id = secrets.token_urlsafe(9)

    with get_db() as conn:
        conn.execute(
            """INSERT INTO notes
               (id, content, created_at, expires_at, max_views)
               VALUES (?, ?, ?, ?, ?)""",
            (note_id, content, now, now + ttl * 60, max_views)
        )

    return redirect(url_for("view_note", note_id=note_id))


@app.route("/note/<note_id>")
def view_note(note_id):
    now = int(time.time())

    with get_db() as conn:
        conn.execute("BEGIN IMMEDIATE")
        note = conn.execute(
            "SELECT * FROM notes WHERE id = ?", (note_id,)
        ).fetchone()

        if note is None:
            abort(404, description="This note does not exist.")

        if now >= note["expires_at"] or note["views"] >= note["max_views"]:
            conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
            abort(404, description="This note has expired or reached its view limit.")

        conn.execute(
            "UPDATE notes SET views = views + 1 WHERE id = ?", (note_id,)
        )

        views_used = note["views"] + 1
        views_left = note["max_views"] - views_used

    return render_template(
        "view.html",
        content=note["content"],
        expires_at=note["expires_at"],
        views_left=views_left
    )


@app.route("/health")
def health():
    try:
        with get_db() as conn:
            conn.execute("SELECT 1")
        return {"status": "healthy"}, 200
    except sqlite3.Error:
        return {"status": "unhealthy"}, 503


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
