import json
import sys
from pathlib import Path

base_items_filepath = (
    Path(__file__).parent.parent / "dnd5esheets" / "data" / "items-base.json"
)

item_type_fields = ["weapon", "armor", "munition"]

weapon_type_fields = [
    "bow",
    "crossbow",
    "club",
    "hammer",
    "mace",
    "sword",
    "spear",
    "net",
    "firearm",
    "axe",
    "dagger",
    "staff",
]
attributes_fields = [
    "range",
    "weapon_type",
    "weapon_category",
    "spellcasting_focus_type",
    "ammo_type",
]
requirement_fields = ["strength"]
damage_fields = ["damage_1", "damage_type", "damage_2"]
meta_fields = ["age", "rarity", "value", "weight", "entries"]
effects_fields = ["ac"]
property_fields = ["property"]
ignore_fields = ["basicRules", "packContents"]
source_fields = ["book", "page"]

field_name_translations = {
    "scfType": "spellcasting_focus_type",
    "dmgType": "damage_type",
    "source": "book",
    "weaponCategory": "weapon_category",
    "dmg1": "damage_1",
    "dmg2": "damage_2",
    "ammoType": "ammo_type",
    "type": "subtype",
}


def generate_effect(item):
    if item.get("armor"):
        if item["type"] == "LA":
            return f'$ac := {item["ac"]} + $dex'
        elif item["type"] == "MA":
            return f'$ac := {item["ac"]} + min($dex, 2)'
        else:
            return f'$ac := {item["ac"]}'


base_items_data = json.load(sys.stdin)

generated_items = []
for item in base_items_data["baseitem"]:
    if not item.get("srd"):
        continue
    reformatted_item = {
        "meta": {},
        "attributes": {},
        "requirements": {},
        "damage": {},
        "source": {},
    }

    if "weaponCategory" in item and "weapon" not in item:
        item["weapon"] = True
    if "ammoType" in item and "|" in item["ammoType"]:
        item["ammoType"] = item["ammoType"].split("|")[0]
    if item["type"] == "A":
        item["munition"] = True

    for field, value in item.items():
        field = field_name_translations.get(field) or field
        if field in ignore_fields:
            continue
        elif field in item_type_fields:
            reformatted_item["type"] = field
        elif field in weapon_type_fields:
            reformatted_item["attributes"]["weapon_type"] = field
        elif field in attributes_fields:
            reformatted_item["attributes"][field] = value
        elif field in requirement_fields:
            reformatted_item["requirements"][field] = value
        elif field in damage_fields:
            reformatted_item["damage"][field] = value
        elif field in meta_fields:
            if field == "entries":
                description_parts = []
                for entry in value:
                    if isinstance(entry, str):
                        description_parts.append(entry)
                    elif isinstance(entry, dict):
                        for sub_entry in entry["entries"]:
                            description_parts.append(sub_entry)
                    elif isinstance(entry, list):
                        for sub_entry in entry:
                            description_parts.append(sub_entry)
                reformatted_item["meta"]["description"] = "\n\n".join(description_parts)
            else:
                reformatted_item["meta"][field] = value
        elif field in effects_fields:
            reformatted_item["effect"] = generate_effect(item)
        elif field in source_fields:
            reformatted_item["source"][field] = value
        else:
            reformatted_item[field] = value

    reformatted_item = {k: v for k, v in reformatted_item.items() if v != {}}
    generated_items.append(reformatted_item)

with open(base_items_filepath, "w") as out:
    json.dump(generated_items, out, indent=2)
