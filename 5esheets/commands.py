import json

import click
from flask.cli import AppGroup

from .db import db, db_dir
from .models import Character

db_commands = AppGroup("db")


@db_commands.command("populate")
def populate_db():
    with open(db_dir / "fixtures" / "dev.json") as dev_fixtures_fd:
        dev_fixtures = json.load(dev_fixtures_fd)
    with db.atomic():
        for character_attrs in dev_fixtures["characters"]:
            json_data = json.dumps(character_attrs.pop("json_data"))
            character = Character.create(json_data=json_data, **character_attrs)
            click.echo(f"Character {character} saved")
