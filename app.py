import sqlite3
from typing import Final, Optional

from flask import Flask, g, render_template


DATABASE: Final[str] = "database/awaodori.db"


app = Flask(__name__)


def get_db() -> sqlite3.Connection:
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception: Optional[BaseException]) -> None:
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


@app.route("/")
def index() -> str:
    return render_template("/index.html")


@app.route("/groups/groups")
def groups_groups() -> str:
    cur = get_db().cursor()
    groups = cur.execute("SELECT id, name FROM groups").fetchall()
    return render_template("/groups/groups.html", groups=groups)


@app.route("/groups/group/<id>")
def groups_group(id: str) -> str:
    cur = get_db().cursor()
    group = cur.execute("SELECT * FROM groups WHERE id = ?", (id,)).fetchone()
    if group is None:
        return render_template("/groups/group-not-found.html")
    representer = cur.execute(
        "SELECT * FROM persons p"
        "    JOIN groups g ON p.id = g.represented_by"
        "    WHERE g.id = ?", (id,)).fetchone()
    persons = cur.execute(
        "SELECT * FROM persons p"
        "    JOIN persons_groups j ON p.id = j.person_id"
        "    JOIN groups g ON j.group_id = g.id"
        "    WHERE g.id = ?", (id,)).fetchall()
    return render_template(
        "/groups/group.html", group=group, representer=representer,
        persons=persons)


@app.route("/performers/performers")
def performers_performers() -> str:
    cur = get_db().cursor()
    performers = cur.execute("SELECT * FROM performers").fetchall()
    return render_template(
        "/performers/performers.html", performers=performers)


@app.route("/performers/performer/<id>")
def performers_performer(id: str) -> str:
    cur = get_db().cursor()
    performer = cur.execute(
        "SELECT * FROM performers WHERE id = ?", (id,)).fetchone()
    if performer is None:
        return render_template("/performers/performer-not-found.html")
    roles = cur.execute(
        "SELECT * FROM roles r"
        "    JOIN persons p ON r.person_id = p.id"
        "    WHERE p.id = ?", (id,)).fetchall()
    instruments = cur.execute(
        "SELECT * FROM instruments i"
        "    JOIN persons p ON i.person_id = p.id"
        "    WHERE p.id = ?", (id,)).fetchall()
    groups = cur.execute(
        "SELECT * FROM groups g"
        "    JOIN persons_groups j ON g.id = j.group_id"
        "    JOIN persons p ON j.person_id = p.id"
        "    WHERE p.id = ?", (id,)).fetchall()
    return render_template(
        "/performers/performer.html", performer=performer, roles=roles,
        instruments=instruments, groups=groups)


if __name__ == "__main__":
    app.run()
