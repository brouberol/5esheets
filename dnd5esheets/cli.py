import json

import click

from dnd5esheets.db import create_session, db_dir
from dnd5esheets.models import Character, Party, Player
from dnd5esheets.security.hashing import get_password_hash


@click.group()
def cli():
    ...


@cli.group()
def db():
    ...


@db.command("populate")
def populate_db():
    with open(db_dir / "fixtures" / "dev.json") as dev_fixtures_fd:
        dev_fixtures = json.load(dev_fixtures_fd)

    with create_session(commit_at_end=True) as session:
        for player_attrs in dev_fixtures["players"]:
            plaintext_password = player_attrs.pop("plaintext_password")
            player_attrs["hashed_password"] = get_password_hash(plaintext_password)
            player = Player(**player_attrs)
            session.merge(player)
            click.echo(f"Player {player} saved")

        for party_attrs in dev_fixtures["parties"]:
            party = Party(**party_attrs)
            session.merge(party)
            click.echo(f"Party {party} saved")

        for character_attrs in dev_fixtures["characters"]:
            character = Character(**character_attrs)
            session.merge(character)
            click.echo(f"Character {character} saved")


if __name__ == "__main__":
    cli()
