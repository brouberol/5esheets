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
        sheet = CharacterSheet.from_form(request.form.to_dict())
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
                "name": sheet.character.name,
                "level": sheet.character.level,
                "class": sheet.character._class,
                "data": json.dumps(sheet.character.data),
            },
        )
        return redirect(url_for("display_sheet", slug=slug))
