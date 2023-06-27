import json
from pathlib import Path

import click
from sqlalchemy import select

from dnd5esheets.config.base import db_dir
from dnd5esheets.db import create_session
from dnd5esheets.models import Character, EquippedItem, Item, Party, Player
from dnd5esheets.security.hashing import get_password_hash

data_dir = Path(__file__).parent / "data"


@click.group()
def cli():
    ...


@cli.group()
def db():
    ...


@db.group()
def populate():
    ...


def _populate_base_items(silent: bool = False):
    with open(data_dir / "items-base.json") as base_items_fd:
        base_items = json.load(base_items_fd)

    with create_session(commit_at_end=True) as session:
        for i, base_item in enumerate(base_items, 1):
            item_name = base_item.pop("name")
            item = Item(id=i, name=item_name, data=base_item)
            session.merge(item)
            if not silent:
                click.echo(f"Item {item} created")


def _populate_db_with_dev_data(silent: bool = False):
    with open(db_dir / "fixtures" / "dev.json") as dev_fixtures_fd:
        dev_fixtures = json.load(dev_fixtures_fd)

    with create_session(commit_at_end=True) as session:
        longsword = session.execute(
            select(Item).filter(Item.name == "Longsword")
        ).scalar()

        for player_attrs in dev_fixtures["players"]:
            plaintext_password = player_attrs.pop("plaintext_password")
            player_attrs["hashed_password"] = get_password_hash(plaintext_password)
            player = Player(**player_attrs)
            session.merge(player)
            if not silent:
                click.echo(f"Player {player} saved")

        for party_attrs in dev_fixtures["parties"]:
            party = Party(**party_attrs)
            session.merge(party)
            if not silent:
                click.echo(f"Party {party} saved")

        for character_attrs in dev_fixtures["characters"]:
            character = Character(
                **character_attrs,
                equipment=[
                    EquippedItem(item_id=longsword.id, id=character_attrs["id"])
                ],
            )
            session.merge(character)
            if not silent:
                click.echo(f"Character {character} saved")


@populate.command("base-items")
@click.option("--silent", type=bool, default=False)
def populate_base_items(silent: bool = False):
    _populate_base_items(silent=silent)


@populate.command("fixtures")
@click.option("--silent", type=bool, default=False)
def populate_db_with_dev_data(silent: bool = False):
    _populate_db_with_dev_data(silent=silent)


if __name__ == "__main__":
    cli()
