from dnd5esheets.models import Spell
from dnd5esheets.repositories import BaseRepository


class SpellRepository(BaseRepository):
    model = Spell
