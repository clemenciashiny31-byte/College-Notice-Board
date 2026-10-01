from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.secret_key = "college-notice-board-secret-key"
DATABASE = "notice_board.db"

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS notices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            category TEXT NOT NULL,
            posted_by TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()

    count = conn.execute("SELECT COUNT(*) FROM notices").fetchone()[0]
    if count == 0:
        sample_notices = [
            ("Internal Assessment - I", "The first internal assessment examination schedule will be displayed shortly. Students are requested to check the notice board regularly.", "Exam", "Administrator"),
            ("Placement Training", "Placement training sessions for final-year students will begin from Monday. Attendance is mandatory.", "Placement", "Administrator"),
            ("College Cultural Fest", "Students interested in participating in the annual cultural fest can register through their department coordinator.", "Event", "Administrator")
        ]
        for title, content, category, posted_by in sample_notices:
            conn.execute(
                "INSERT INTO notices (title, content, category, posted_by, created_at) VALUES (?, ?, ?, ?, ?)",
                (title, content, category, posted_by, datetime.now().strftime("%d-%m-%Y %I:%M %p"))
            )
        conn.commit()
    conn.close()

def admin_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin_login"))
        return view(*args, **kwargs)
    return wrapped_view

@app.route("/")
def index():
    conn = get_db()
    notices = conn.execute("SELECT * FROM notices ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("index.html", notices=notices)

@app.route("/notice/<int:notice_id>")
def notice_detail(notice_id):
    conn = get_db()
    notice = conn.execute("SELECT * FROM notices WHERE id = ?", (notice_id,)).fetchone()
    conn.close()
    if notice is None:
        flash("Notice not found.", "error")
        return redirect(url_for("index"))
    return render_template("notice_detail.html", notice=notice)

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        # Demo credentials
        if username == "admin" and password == "admin123":
            session["admin_logged_in"] = True
            session["admin_username"] = username
            return redirect(url_for("admin_dashboard"))

        flash("Invalid username or password.", "error")

    return render_template("admin_login.html")

@app.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/admin")
@admin_required
def admin_dashboard():
    conn = get_db()
    notices = conn.execute("SELECT * FROM notices ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("admin_dashboard.html", notices=notices)

@app.route("/admin/add", methods=["GET", "POST"])
@admin_required
def add_notice():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        category = request.form.get("category", "").strip()
        posted_by = session.get("admin_username", "Administrator")

        if not title or not content or not category:
            flash("Please fill in all fields.", "error")
            return render_template("add_notice.html")

        conn = get_db()
        conn.execute(
            "INSERT INTO notices (title, content, category, posted_by, created_at) VALUES (?, ?, ?, ?, ?)",
            (title, content, category, posted_by, datetime.now().strftime("%d-%m-%Y %I:%M %p"))
        )
        conn.commit()
        conn.close()
        flash("Announcement published successfully.", "success")
        return redirect(url_for("admin_dashboard"))

    return render_template("add_notice.html")

@app.route("/admin/delete/<int:notice_id>", methods=["POST"])
@admin_required
def delete_notice(notice_id):
    conn = get_db()
    conn.execute("DELETE FROM notices WHERE id = ?", (notice_id,))
    conn.commit()
    conn.close()
    flash("Announcement deleted.", "success")
    return redirect(url_for("admin_dashboard"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
