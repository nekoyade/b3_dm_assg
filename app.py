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
    group_list = cur.execute("SELECT id, name FROM groups").fetchall()
    return render_template("/groups/groups.html", groups=group_list)


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


if __name__ == "__main__":
    app.run()
