import json
from pathlib import Path

import caribou
from flask import Flask, redirect, render_template, request, url_for
from flask_babel import Babel
from sqlalchemy.orm import scoped_session

from .commands import db_commands
from .db import db_file, session_factory
from .models import Character
from .utils import is_field_from_checkbox, strip_empties_from_dict

SUPPORTED_TRANSLATION_LANGUAGES = ["fr", "en"]


def get_locale():
    # From https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xiv-i18n-and-l10n-legacy
    return request.accept_languages.best_match(
        SUPPORTED_TRANSLATION_LANGUAGES, default="en"
    )


migrations_dir = Path(__file__).parent / "migrations"
app = Flask("5esheets", template_folder=Path(__file__).parent / "templates")
babel = Babel(app, locale_selector=get_locale)
app.cli.add_command(db_commands)

session = scoped_session(session_factory)

with app.app_context():
    caribou.upgrade(db_url=db_file, migration_dir=migrations_dir)


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


@app.route("/", methods=["GET"])
def list_characters():
    characters = session.query(Character).all()
    return render_template("characters.html", characters=characters)


@app.route("/<slug>", methods=["GET"])
def display_sheet(slug: str):
    character = session.query(Character).filter_by(slug=slug).first()
    return render_template("sheet.html", character=character)


@app.route("/<slug>", methods=["POST"])
def update_sheet(slug: str):
    form = request.form.to_dict()

    character_name = form.pop("charname")
    classlevel_tokens = form.pop("classlevel").split()
    character_class = " ".join(classlevel_tokens[:-1])
    character_level = int(classlevel_tokens[-1])

    character_data = form.copy()
    for k in form:
        if is_field_from_checkbox(k):
            character_data[k] = True

    # Remove empty fields to keep the JSON payload as small as possible
    character_data = strip_empties_from_dict(character_data)
    session.query(Character).filter_by(slug=slug).update(
        {
            Character.name: character_name,
            Character._class: character_class,
            Character.level: character_level,
            Character.json_data: json.dumps(character_data),
        },
        synchronize_session=False,
    )
    session.commit()
    return redirect(url_for("display_sheet", slug=slug))
