import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path

import caribou
from flask import Flask, redirect, render_template, request, url_for
from flask_babel import Babel

from .models import Character, CharacterSheet

SUPPORTED_TRANSLATION_LANGUAGES = ["fr", "en"]


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


@contextmanager
def get_db_connection():
    conn = sqlite3.connect(db_file)
    conn.row_factory = dict_factory
    yield conn
    conn.commit()
    conn.close()


def get_locale():
    # From https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xiv-i18n-and-l10n-legacy
    return request.accept_languages.best_match(
        SUPPORTED_TRANSLATION_LANGUAGES, default="en"
    )


def is_field_from_checkbox(field_name):
    return (
        field_name.endswith(("-prof", "-prepped"))
        or field_name in ("inspiration", "darkvision")
        or field_name.startswith(("deathfail", "deathsuccess"))
    )


db_file = Path(__file__).parent / "db" / "5esheets.db"
migrations_dir = Path(__file__).parent / "migrations"
app = Flask("5esheets", template_folder=Path(__file__).parent / "templates")
babel = Babel(app, locale_selector=get_locale)

with app.app_context():
    caribou.upgrade(db_url=db_file, migration_dir=migrations_dir)


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
            sheets.append(CharacterSheet.from_dict(row))

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
        character = Character.from_dict(row)

        return render_template("sheet.html", character=character)


@app.route("/<slug>", methods=["POST"])
def update_sheet(slug: str):
    with get_db_connection() as db:
        character_data = request.form.to_dict()
        character_name = character_data.pop("charname")
        classlevel_tokens = character_data.pop("classlevel").split()
        character_class = " ".join(classlevel_tokens[:-1])
        character_level = classlevel_tokens[-1]
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
            WHERE character_slug=:slug
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
