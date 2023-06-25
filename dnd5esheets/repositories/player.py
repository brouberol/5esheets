from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dnd5esheets.models import Player
from dnd5esheets.repositories import BaseRepository
from dnd5esheets.schemas import UpdatePlayerSchema


class PlayerRepository(BaseRepository):
    model = Player

    @classmethod
    async def get_by_id(cls, session: AsyncSession, id: int) -> Player:
        """Return a Player given an argument id"""
        result = await session.execute(select(Player).filter(Player.id == id))
        return cls.one_or_raise_model_not_found(result)  # type: ignore

    @classmethod
    async def get_by_email(cls, session: AsyncSession, email: str) -> Player:
        """Return a Player given an argument email"""
        result = await session.execute(select(Player).filter(Player.email == email))
        return cls.one_or_raise_model_not_found(result)  # type: ignore

    @classmethod
    async def update(
        cls, session: AsyncSession, id: int, body: UpdatePlayerSchema
    ) -> Player:
        player = await cls.get_by_id(session, id)

        # Any non-nil field should be taken as the new value
        fields_to_update = {
            field: val for field, val in body.dict().items() if val is not None
        }

        player.update_from_dict(fields_to_update)

        # Persist the changes
        session.add(player)
        await session.commit()

        return player
