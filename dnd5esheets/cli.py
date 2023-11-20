from pathlib import Path

import click
import orjson
from sqlalchemy import select

from dnd5esheets.config.base import db_dir
from dnd5esheets.db import create_session
from dnd5esheets.models import (
    Character,
    EquippedItem,
    Item,
    KnownSpell,
    Party,
    Player,
    PlayerRole,
    Spell,
)

data_dir = Path(__file__).parent / "data"


@click.group()
def cli():
    ...


@cli.group()  # type: ignore
def db():
    ...


@db.group()
def populate():
    ...


def _populate_base_items(silent: bool = False):
    with open(data_dir / "items-base.json") as base_items_fd:
        base_items_str = base_items_fd.read()
        base_items = orjson.loads(base_items_str)

    with create_session(commit_at_end=True) as session:
        for i, base_item in enumerate(base_items, 1):
            item_name = base_item.pop("name")
            item = Item(id=i, name=item_name, data=base_item)
            session.merge(item)
            if not silent:
                click.echo(f"Item {item} created")


def _populate_spells(silent: bool = False):
    with open(data_dir / "spells.json") as spells_fd:
        spells_str = spells_fd.read()
        spells = orjson.loads(spells_str)

    with create_session(commit_at_end=True) as session:
        for i, spell in enumerate(spells, 1):
            spell_name = spell.pop("name")
            spell_school = spell.pop("school")
            spell_level = spell.pop("level")
            spell = Spell(
                id=i,
                name=spell_name,
                level=spell_level,
                school=spell_school,
                data=spell,
            )
            session.merge(spell)
            if not silent:
                click.echo(f"Spell {spell} created")


def _populate_db_with_dev_data(silent: bool = False):
    with open(db_dir / "fixtures" / "dev.json") as dev_fixtures_fd:
        dev_fixtures_str = dev_fixtures_fd.read()
        dev_fixtures = orjson.loads(dev_fixtures_str)

    with create_session(commit_at_end=True) as session:
        longsword = session.execute(select(Item).filter(Item.name == "Longsword")).scalar()
        spells = (
            session.execute(
                select(Spell).filter(
                    Spell.name.in_(
                        (
                            "Mending",
                            "Fire Bolt",
                            "Thunderwave",
                            "Shield",
                            "Detect Magic",
                            "Catapult",
                            "Absorb Elements",
                        )
                    )
                )
            )
            .scalars()
            .all()
        )

        for player_attrs in dev_fixtures["players"]:
            player = Player(**player_attrs)
            session.merge(player)
            if not silent:
                click.echo(f"Player {player} saved")

        for party_attrs in dev_fixtures["parties"]:
            party = Party(**party_attrs)
            session.merge(party)
            if not silent:
                click.echo(f"Party {party} saved")

        for player_role_attrs in dev_fixtures["player_roles"]:
            player_role = PlayerRole(**player_role_attrs)
            session.merge(player_role)
            if not silent:
                click.echo(f"PlayerRole {player_role} saved")

        for character_attrs in dev_fixtures["characters"]:
            character = Character(
                **character_attrs,
                equipment=[EquippedItem(item_id=longsword.id, id=character_attrs["id"])],
                spellbook=[
                    KnownSpell(
                        id=i + len(spells) * character_attrs["id"],
                        spell_id=spell.id,
                        character_id=character_attrs["id"],
                        prepared=True,
                    )
                    for i, spell in enumerate(spells, 1)
                ],
            )
            session.merge(character)
            if not silent:
                click.echo(f"Character {character} saved")


@populate.command("base-items")
@click.option("--silent", type=bool, default=False)
def populate_base_items(silent: bool = False):
    """Populate the database the base items data, with their translations"""
    _populate_base_items(silent=silent)


@populate.command("spells")
@click.option("--silent", type=bool, default=False)
def populate_spells(silent: bool = False):
    """Populate the database the spells data, with their translations"""
    _populate_spells(silent=silent)


@populate.command("fixtures")
@click.option("--silent", type=bool, default=False)
def populate_db_with_dev_data(silent: bool = False):
    """Populate the database with development fixtures"""
    _populate_db_with_dev_data(silent=silent)


@populate.command("all")
@click.option("--silent", type=bool, default=False)
def populate_db(silent: bool = False):
    """Populate the database with base data and dev fixtures"""
    _populate_base_items(silent=silent)
    _populate_spells(silent=silent)
    _populate_db_with_dev_data(silent=silent)


if __name__ == "__main__":
    cli()  # type: ignore
