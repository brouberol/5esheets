import json
import sqlite3
from collections import defaultdict
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for
from slugify import slugify

app = Flask("5esheets", template_folder=Path(__file__).parent / "templates")


@contextmanager
def get_db_connection():
    conn = sqlite3.connect("sheets.db")
    conn.row_factory = sqlite3.Row
    yield conn
    conn.commit()
    conn.close()


def create_table():
    with get_db_connection() as db:
        db.execute(
            """CREATE TABLE sheets(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                character_name VARCHAR(255),
                character_slug VARCHAR(255),
                character_class VARCHAR(50),
                character_level INTEGER,
                character_json_data TEXT NOT NULL
            );
            CREATE INDEX sheets_character_slug ON sheets(character_slug);
            """
        )


def is_field_from_checkbox(field_name):
    return (
        field_name.endswith(("-prof", "-prepped"))
        or field_name in ("inspiration", "darkvision")
        or field_name.startswith(("deathfail", "deathsuccess"))
    )


@dataclass
class Character:
    name: str
    level: int
    _class: int
    slug: str
    data: dict = field(default_factory=lambda: defaultdict(str))


@dataclass
class CharacterSheet:
    id: int
    character: Character


@app.route("/", methods=["GET"])
def list_sheets():
    sheets = []
    with get_db_connection() as db:
        res = db.execute(
            """
            SELECT id, character_name, character_class, character_level, character_slug
            FROM sheets
            ORDER BY character_name;
            """
        )
        for row in res.fetchall():
            sheets.append(
                CharacterSheet(
                    id=row["id"],
                    character=Character(
                        name=row["character_name"],
                        level=row["character_level"],
                        _class=row["character_class"],
                        slug=row["character_slug"],
                    ),
                )
            )

        return render_template("sheets.html", sheets=sheets)


@app.route("/<slug>", methods=["GET"])
def display_sheet(slug: str):
    with get_db_connection() as db:
        row = db.execute(
            """
            SELECT character_name, character_class, character_level, character_slug, character_json_data
            FROM sheets
            WHERE character_slug=:slug;
            """,
            {"slug": slug},
        ).fetchone()
        character = Character(
            name=row["character_name"],
            level=row["character_level"],
            _class=row["character_class"],
            data=json.loads(row["character_json_data"]),
            slug=row["character_slug"],
        )

        return render_template("sheet.html", character=character)


@app.route("/<slug>", methods=["POST"])
def update_sheet(slug: str):
    with get_db_connection() as db:
        character_data = request.form.to_dict()
        character_name = character_data.pop("charname")
        character_class, character_level = character_data.pop("classlevel").split()
        for k in character_data:
            if is_field_from_checkbox(k):
                character_data[k] = True
        db.execute(
            """
            UPDATE sheets
            SET
                character_name=:name,
                character_class=:class,
                character_level=:level,
                character_json_data=:data
            WHERE slug=:slug
        """,
            {
                "slug": slug,
                "name": character_name,
                "level": int(character_level),
                "class": character_class,
                "data": json.dumps(character_data),
            },
        )
        return redirect(url_for("display_sheet", slug=slug))


if __name__ == "__main__":
    if not Path("sheets.db").exists():
        create_table()
    app.run()
