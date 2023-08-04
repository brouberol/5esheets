import hashlib
from itertools import chain
from typing import Sequence, cast

from slugify import slugify
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import defer

from dnd5esheets.models import Character, EquippedItem, KnownSpell, Party, Player
from dnd5esheets.repositories import BaseRepository, DuplicateModel, ModelNotFound
from dnd5esheets.repositories.equipped_item import EquippedItemRepository
from dnd5esheets.repositories.item import ItemRepository
from dnd5esheets.repositories.known_spell import KnownSpellRepository
from dnd5esheets.repositories.player import PlayerRepository
from dnd5esheets.repositories.spell import SpellRepository
from dnd5esheets.schemas import CreateCharacterSchema, UpdateCharacterSchema


class CharacterRepository(BaseRepository):
    model = Character

    @classmethod
    async def list_all(
        cls, session: AsyncSession, owner_id: int | None = None
    ) -> Sequence[Character]:
        """List all existing characters, with their associated related data"""
        query = select(Character).options(
            defer(Character.data)
        )  # exclude the large json payload
        if owner_id is not None:
            query = query.filter(Character.player_id == owner_id)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def get_by_slug(
        cls, session: AsyncSession, slug: str, owner_id: int | None = None
    ) -> Character:
        """Return a Character given an argument slug"""
        query = select(Character).filter(Character.slug == slug)
        if owner_id is not None:
            query = query.filter(Character.player_id == owner_id)
        result = await session.execute(query)
        return cast(Character, cls.one_or_raise_model_not_found(result))

    @classmethod
    async def get_by_slug_if_owned(
        cls, session: AsyncSession, slug: str, owner_id: int | None
    ) -> Character:
        """Return a Character given an argument slug"""
        character = await cls.get_by_slug(session, slug)
        if owner_id is not None and character.player_id != owner_id:
            cls.raise_model_not_found()
        return character

    @classmethod
    async def update(
        cls,
        session: AsyncSession,
        slug: str,
        body: UpdateCharacterSchema,
    ) -> Character:
        """Update fields of the Character identified by the argument slug"""
        character = await cls.get_by_slug(session, slug)

        # Any non-nil field should be taken as the new value
        fields_to_update = {
            field: val for field, val in body.model_dump().items() if val is not None
        }
        character.update_from_dict(fields_to_update)

        # Persist the changes
        session.add(character)
        await session.commit()
        await session.refresh(character)

        return character

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        character_data: CreateCharacterSchema,
        owner_id: int | None,
    ) -> Character:
        """Create a new character described by the argument character data"""
        slug = slugify(character_data.name)

        if owner_id is not None:
            if not await PlayerRepository.player_has_character_in_party(
                session, player_id=owner_id, party_id=character_data.party_id
            ):
                raise ModelNotFound.from_model_name("Party")

            try:
                await cls.get_by_slug(session, slug=slug, owner_id=owner_id)
            except ModelNotFound:
                # If the model isn't found, we can proceed with the insertion
                pass
            else:
                # We have found an already existing Character in DB, belonging to the
                # current player, with the same slug
                raise DuplicateModel(
                    f"A character named {character_data.name} already exists"
                )

        character = Character(
            name=character_data.name,
            party_id=character_data.party_id,
            slug=slug,
            player_id=owner_id,
            level=None,
            class_=None,
            data=None,
        )
        session.add(character)
        await session.commit()
        await session.refresh(character)
        return character

    @classmethod
    async def etag(
        cls, session: AsyncSession, slug: str, owner_id: int | None
    ) -> str | None:
        """Compute a stable hash for a given Character that will be used as its ETag.

        For this, we rely on the hash of all updated_at timestamps for the Character itself,
        as well as each related entity:
        - Player
        - Party
        - EquippedItems

        """
        query = (
            select(
                Character.id,
                Character.updated_at,
                Party.updated_at,
                Player.updated_at,
            )
            .join(Party)
            .join(Player)
            .filter(Character.slug == slug)
        )
        if owner_id is not None:
            query = query.filter(Player.id == owner_id)
        result = (await session.execute(query)).first()
        if not result:
            return None

        character_id, *update_timestamps = result

        equipped_items_results = await session.execute(
            select(EquippedItem.updated_at)
            .filter(EquippedItem.character_id == character_id)
            .order_by(EquippedItem.item_id)
        )
        equipped_items_update_timestamps = equipped_items_results.scalars().all()

        # hash all updated_at timestamps
        digest = hashlib.sha1()
        for update_dt in chain(update_timestamps, equipped_items_update_timestamps):
            digest.update(update_dt.isoformat().encode("utf-8"))

        return digest.hexdigest()

    @classmethod
    async def delete(cls, session: AsyncSession, slug: str, owner_id: int | None):
        """Delete the character identified by the argument slug"""
        character = await cls.get_by_slug(session, slug=slug, owner_id=owner_id)
        await session.delete(character)
        await session.commit()

    @classmethod
    async def change_equipment_item_equipped_status(
        cls,
        session: AsyncSession,
        slug: str,
        owner_id: int | None,
        equipped_item_id: int,
        equipped: bool,
    ):
        """Change the equipped status of the argument equipped item in the character's equipment"""
        character = await cls.get_by_slug_if_owned(
            session, slug=slug, owner_id=owner_id
        )
        await EquippedItemRepository.change_equipped_status(
            session, id=equipped_item_id, owner_id=character.id, equipped=equipped
        )
        await session.refresh(character)
        return character

    @classmethod
    async def change_known_spell_prepared_status(
        cls,
        session: AsyncSession,
        slug: str,
        owner_id: int | None,
        known_spell_id: int,
        prepared: bool,
    ):
        """Change the prepared status of the argument known spell in the character's spellbook"""
        character = await cls.get_by_slug_if_owned(
            session, slug=slug, owner_id=owner_id
        )
        await KnownSpellRepository.change_prepared_status(
            session, id=known_spell_id, owner_id=character.id, prepared=prepared
        )
        await session.refresh(character)
        return character

    @classmethod
    async def learn_spell(
        cls,
        session: AsyncSession,
        slug: str,
        owner_id: int | None,
        spell_id: int,
        prepared: bool = False,
    ):
        """Ensure a given spell is present in the character's spellbook"""
        character = await cls.get_by_slug_if_owned(
            session, slug=slug, owner_id=owner_id
        )
        for known_spell in character.spellbook:
            if known_spell.spell_id == spell_id:
                return character

        # will raise if spell_id is not found
        await SpellRepository.get_by_id(session, id=spell_id)
        known_spell = KnownSpell(
            character_id=character.id, spell_id=spell_id, prepared=prepared
        )
        character.spellbook.append(known_spell)
        session.add(character)
        await session.commit()
        await session.refresh(character)
        return character

    @classmethod
    async def forget_spell(
        cls,
        session: AsyncSession,
        slug: str,
        owner_id: int | None,
        known_spell_id: int,
    ):
        """Ensure a given spell is absent from the character's spellbook"""
        character = await cls.get_by_slug_if_owned(
            session, slug=slug, owner_id=owner_id
        )
        await KnownSpellRepository.delete_by_id(session, id=known_spell_id)
        await session.refresh(character)
        return character

    @classmethod
    async def add_item_to_equipment(
        cls,
        session: AsyncSession,
        slug: str,
        owner_id: int | None,
        item_id: int,
        amount: int = 1,
    ):
        """Ensure a given item is present in the character's equipment"""
        character = await cls.get_by_slug_if_owned(
            session, slug=slug, owner_id=owner_id
        )
        for equipped_item in character.equipment:
            if equipped_item.item_id == item_id:
                return character

        # will raise if spell_id is not found
        await ItemRepository.get_by_id(session, id=item_id)
        equipped_item = EquippedItem(
            character_id=character.id, item_id=item_id, amount=amount
        )
        character.equipment.append(equipped_item)
        session.add(character)
        await session.commit()
        await session.refresh(character)
        return character

    @classmethod
    async def remove_item_from_equipment(
        cls,
        session: AsyncSession,
        slug: str,
        owner_id: int | None,
        equipped_item_id: int,
    ):
        """Ensure a given item is absent from the character's equipment"""
        character = await cls.get_by_slug_if_owned(
            session, slug=slug, owner_id=owner_id
        )
        await EquippedItemRepository.delete_by_id(session, id=equipped_item_id)
        await session.refresh(character)
        return character
