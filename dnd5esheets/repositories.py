"""
Repositories are the layer through which we communicate with the database.

Any database access outside of repositories (eg: in the app routes) is strongly
discouraged.

"""

from sqlalchemy.orm import Session, defer, joinedload
from .models import Character
from .schemas import UpdateCharacterSchema


class CharacterRepository:
    @staticmethod
    def list_all(session: Session) -> list[Character]:
        """List all existing characters, with their associated related data"""
        return (
            session.query(Character)
            # efficiently join the player and party tables
            .options(joinedload(Character.player), joinedload(Character.party))
            # exclude the large json patyload
            .options(defer(Character.data)).all()
        )

    @staticmethod
    def get_by_slug(session: Session, slug: str) -> Character | None:
        """Return a Character given an argument slug"""
        return (
            session.query(Character)
            .options(joinedload(Character.player), joinedload(Character.party))
            .filter(Character.slug == slug)
            .one_or_none()
        )

    @staticmethod
    def update_character(
        session: Session, slug: str, body: UpdateCharacterSchema
    ) -> Character | None:
        character = CharacterRepository.get_by_slug(session, slug)
        if not character:
            return None

        # Any non-nil field should be taken as the new value
        fields_to_update = {
            field: val for field, val in body.dict().items() if val is not None
        }

        # if body has a `data` attribute, we peform updates of the associated nested fields
        # in the character.json_data json object
        if "data" in fields_to_update:
            data = character.data.copy()
            for key, value in fields_to_update["data"].items():
                data[key] = value
            character.json_data = json.dumps(data)
            fields_to_update.pop("data")

        # Update the character other fields
        for field, value in fields_to_update.items():
            setattr(character, field, value)

        # Persist the changes
        session.add(character)
        session.commit()
