import json

import click
from flask.cli import AppGroup

from .db import db, db_dir
from .models import Character, Party, Player

db_commands = AppGroup("db")


@db_commands.command("populate")
def populate_db():
    with open(db_dir / "fixtures" / "dev.json") as dev_fixtures_fd:
        dev_fixtures = json.load(dev_fixtures_fd)

    for player_attrs in dev_fixtures["players"]:
        Player.replace(**player_attrs).execute()
        player = Player.get_by_id(player_attrs["id"])
        click.echo(f"Player {player} saved")

    for party_attrs in dev_fixtures["parties"]:
        Party.replace(**party_attrs).execute()
        party = Party.get_by_id(party_attrs["id"])
        click.echo(f"Party {party} saved")

    for character_attrs in dev_fixtures["characters"]:
        json_data = json.dumps(character_attrs.pop("json_data"))
        Character.replace(json_data=json_data, **character_attrs).execute()
        character = Character.get_by_id(character_attrs["id"])
        click.echo(f"Character {character} saved")
