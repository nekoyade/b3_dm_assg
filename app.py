import sqlite3
from typing import Final, Optional
import unicodedata

from flask import Flask, g, redirect, render_template, request, url_for


DATABASE: Final[str] = "database/awaodori.db"


app = Flask(__name__)


RESULT_MESSAGES: Final[dict[str, str]] = {
    "performer-id-does-not-exist":
        "指定された ID の参加者が存在しません．",
    "name-has-control-characters":
        "指定された氏名が制御文字を含んでいるため，"
        "除外してください．",
    "address-has-control-characters":
        "指定された住所が制御文字を含んでいるため，"
        "除外してください．",
    "database-error":
        "データベース上でエラーが発生しました．",
    "updated":
        "更新が完了しました．",
}


def has_control_characters(s: str) -> bool:
    return any(map(lambda c: unicodedata.category(c) == "Cc", s))


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
    groups = cur.execute("SELECT * FROM groups").fetchall()
    return render_template(
        "/groups/groups.html", groups=groups)


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


@app.route("/performers/performers", methods=["POST"])
def performers_performers_filtered() -> str:
    cur = get_db().cursor()
    performers = cur.execute(
        "SELECT * FROM performers p"
        "    WHERE p.name LIKE ?", (request.form["name_filter"],)).fetchall()
    return render_template(
        "/performers/performers.html", performers=performers)


@app.route("/performers/performer/<id>")
def performers_performer(id: str) -> str:
    cur = get_db().cursor()
    performer = cur.execute(
        "SELECT * FROM performers WHERE id = ?", (id,)).fetchone()
    if performer is None:
        return render_template("/performers/performer-not-found.html")
    phones = cur.execute(
        "SELECT * FROM phones h"
        "    JOIN persons p ON h.person_id = p.id"
        "    WHERE p.id = ?", (id,)).fetchall()
    emails = cur.execute(
        "SELECT * FROM emails e"
        "    JOIN persons p ON e.person_id = p.id"
        "    WHERE p.id = ?", (id,)).fetchall()
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
        "/performers/performer.html",
        performer=performer,
        phones=phones,
        emails=emails,
        roles=roles,
        instruments=instruments,
        groups=groups)


@app.route("/performers/performer-edit/<id>")
def performers_performer_edit(id: str) -> str:
    cur = get_db().cursor()
    performer = cur.execute(
        "SELECT * FROM performers p"
        "    WHERE p.id = ?", (id,)).fetchone()
    if performer is None:
        return render_template(
            "/performers/performer-edit-results.html",
            performer=None,
            results=RESULT_MESSAGES["performer-id-does-not-exist"])
    return render_template(
        "/performers/performer-edit.html", performer=performer)


@app.route("/performers/performer-edit/<id>", methods=["POST"])
def performers_performer_edit_update(id: str) -> str:
    con = get_db()
    cur = con.cursor()
    performer = cur.execute(
        "SELECT * FROM performers p"
        "    WHERE p.id = ?", (id,)).fetchone()
    if performer is None:
        return render_template(
            "/performers/performer-edit-results.html",
            performer=None,
            results=RESULT_MESSAGES["performer-id-does-not-exist"])
    name = request.form["name"]
    birth_date = request.form["birth_date"]
    address = request.form["address"]
    if has_control_characters(name):
        return redirect(url_for("performers_performer_edit_results",
                        code="name-has-control-characters"))
    if has_control_characters(address):
        return redirect(url_for("performers_performer_edit_results",
                        code="address-has-control-characters"))
    try:
        cur.execute(
            "UPDATE persons"
            "    SET name = ?, birth_date = ?, address = ?"
            "    WHERE id = ?",
            (name, birth_date, address, id,))
    except sqlite3.Error:
        return redirect(url_for("performers_performer_edit_results",
                        code="database-error"))
    con.commit()
    return redirect(
        url_for("performers_performer_edit_results", code="updated"))


@app.route("/performers/performer-edit-results/<code>")
def performers_performer_edit_results(code: str) -> str:
    return render_template(
        "/performers/performer-edit-results.html",
        results=RESULT_MESSAGES.get(code, "意図しないコードを受け取りました．"))


if __name__ == "__main__":
    app.run()
