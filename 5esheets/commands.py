import json
from contextlib import closing

import click
from flask.cli import AppGroup

from .db import create_session, db_dir
from .models import Character, Party, Player

db_commands = AppGroup("db")


@db_commands.command("populate")
def populate_db():
    with open(db_dir / "fixtures" / "dev.json") as dev_fixtures_fd:
        dev_fixtures = json.load(dev_fixtures_fd)

    session = create_session()
    with closing(session):
        for player_attrs in dev_fixtures["players"]:
            player = Player(**player_attrs)
            session.merge(player)
            click.echo(f"Player {player} saved")

        for party_attrs in dev_fixtures["parties"]:
            party = Party(**party_attrs)
            session.merge(party)
            click.echo(f"Party {party} saved")

        for character_attrs in dev_fixtures["characters"]:
            json_data = json.dumps(character_attrs.pop("json_data"))
            character = Character(json_data=json_data, **character_attrs)
            session.merge(character)
            click.echo(f"Character {character} saved")
        session.commit()
