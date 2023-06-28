import json
import sys
import glob

from bs4 import BeautifulSoup
from pathlib import Path

data_dir = Path(__file__).parent.parent / "dnd5esheets" / "data"
base_items_filepath = data_dir / "items-base.json"
items_translations_filepath = data_dir / "translations-items-*.json"

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

translations = {}
for translations_filepath in glob.glob(str(items_translations_filepath)):
    language = Path(translations_filepath).stem.split("-")[-1]
    translated_data = json.load(open(translations_filepath))
    translated_data = {entry["id"]: entry for entry in translated_data["entries"]}
    translations[language] = translated_data


def generate_effect(item: dict) -> str | None:
    if item.get("armor"):
        if item["type"] == "LA":
            return f'$ac := {item["ac"]} + $dex'
        elif item["type"] == "MA":
            return f'$ac := {item["ac"]} + min($dex, 2)'
        else:
            return f'$ac := {item["ac"]}'


def reformat_item(item: dict) -> dict | None:
    if not item.get("srd"):
        return

    reformatted_item = {
        "meta": {"translations": {}},
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

    for language, lang_translations in translations.items():
        if translated_item := lang_translations.get(item["name"]):
            reformatted_item["meta"]["translations"][language] = {
                "name": translated_item["name"],
                "description": BeautifulSoup(
                    translated_item["description"], features="html.parser"
                ).text,
            }
        else:
            print(f"No translation found for {item['name']}")

    reformatted_item = {k: v for k, v in reformatted_item.items() if v != {}}
    return reformatted_item


def main():
    base_items_data = json.load(sys.stdin)

    generated_items = []
    for item in base_items_data["baseitem"]:
        reformatted_item = reformat_item(item)
        generated_items.append(reformatted_item)

    with open(base_items_filepath, "w") as out:
        json.dump(generated_items, out, indent=2)


if __name__ == "__main__":
    main()
