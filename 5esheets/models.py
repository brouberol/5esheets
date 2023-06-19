import json
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Self

from .utils import is_field_from_checkbox


@dataclass
class Character:
    name: str
    level: int
    _class: int
    slug: str

    # Using a defaultdict allows us to perform a data.get(key) in the templates
    # and get '' instead of None, while staying concise
    data: dict = field(default_factory=lambda: defaultdict(str))

    @classmethod
    def from_dict(cls, d: dict) -> Self:
        return Character(
            name=d["character_name"],
            level=d["character_level"],
            _class=d["character_class"],
            slug=d["character_slug"],
            data=json.loads(d.get("character_json_data", "{}")),
        )


@dataclass
class CharacterSheet:
    id: int
    character: Character

    @classmethod
    def from_dict(cls, d: dict) -> Self:
        return CharacterSheet(id=d["id"], character=Character.from_dict(d))

    @classmethod
    def from_form(cls, form: dict) -> Self:
        character_name = form.pop("charname")
        classlevel_tokens = form.pop("classlevel").split()
        character_class = " ".join(classlevel_tokens[:-1])
        character_level = int(classlevel_tokens[-1])

        character_data = form.copy()
        for k in form:
            if is_field_from_checkbox(k):
                character_data[k] = True

        return CharacterSheet(
            id=-1,
            character=Character(
                name=character_name,
                level=character_level,
                _class=character_class,
                slug="",
                data=character_data,
            ),
        )
