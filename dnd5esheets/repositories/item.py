from dnd5esheets.models import Item
from dnd5esheets.repositories import BaseRepository


class ItemRepository(BaseRepository):
    model = Item
