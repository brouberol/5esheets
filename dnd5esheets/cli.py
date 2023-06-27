import json
from pathlib import Path

import click
from sqlalchemy import select

from dnd5esheets.db import create_session, db_dir
from dnd5esheets.models import Character, Equipment, EquippedItem, Item, Party, Player
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


@populate.command("base-items")
def populate_base_items():
    with open(data_dir / "items-base.json") as base_items_fd:
        base_items = json.load(base_items_fd)

    with create_session(commit_at_end=True) as session:
        for i, base_item in enumerate(base_items, 1):
            item_name = base_item.pop("name")
            item = Item(id=i, name=item_name, data=base_item)
            session.merge(item)
            click.echo(f"Item {item} created")


@populate.command("fixtures")
def populate_db():
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
            click.echo(f"Player {player} saved")

        for party_attrs in dev_fixtures["parties"]:
            party = Party(**party_attrs)
            session.merge(party)
            click.echo(f"Party {party} saved")

        for character_attrs in dev_fixtures["characters"]:
            character = Character(
                **character_attrs,
                equipment=Equipment(
                    id=character_attrs["id"],
                    items=[
                        EquippedItem(item_id=longsword.id, id=character_attrs["id"])
                    ],
                ),
            )
            session.merge(character)
            click.echo(f"Character {character} saved")


if __name__ == "__main__":
    cli()
