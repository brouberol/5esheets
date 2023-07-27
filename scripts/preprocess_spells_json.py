import glob
import json
import sys
from pathlib import Path

from bs4 import BeautifulSoup

data_dir = Path(__file__).parent.parent / "dnd5esheets" / "data"
spells_filepath = data_dir / "spells-*.json"
spells_translations_filepath = data_dir / "translations-spells-*.json"
output_filepath = data_dir / "spells.json"

ignore_fields = ["basicRules", "packContents"]
source_fields = ["book", "page"]

field_name_translations = {
    "source": "book",
}

translations = {}
for translations_filepath in glob.glob(str(spells_translations_filepath)):
    language = Path(translations_filepath).stem.split("-")[-1]
    translated_data = json.load(open(translations_filepath))
    translated_data = {entry["id"]: entry for entry in translated_data["entries"]}
    translations[language] = translated_data


def reformat_spell(spell: dict) -> dict | None:
    if not spell.get("srd"):
        return

    reformatted_spell = {
        "meta": {"translations": {}},
        "source": {},
    }

    for field, value in spell.items():
        field = field_name_translations.get(field) or field
        if field in ignore_fields:
            continue
        if field in source_fields:
            reformatted_spell["source"][field] = value
        elif field == "entries":
            description_parts = []
            for entry in value:
                if isinstance(entry, str):
                    description_parts.append(entry)
                elif isinstance(entry, dict):
                    if "entries" not in entry:
                        continue
                    for sub_entry in entry["entries"]:
                        if isinstance(sub_entry, str):
                            description_parts.append(sub_entry)
                elif isinstance(entry, list):
                    for sub_entry in entry:
                        if isinstance(sub_entry, str):
                            description_parts.append(sub_entry)
            reformatted_spell["meta"]["description"] = "\n\n".join(description_parts)
        elif field == "meta":
            for k, v in spell["meta"].items():
                reformatted_spell["meta"][k] = v
        else:
            reformatted_spell[field] = value

    for language, lang_translations in translations.items():
        if translated_spell := lang_translations.get(spell["name"]):
            reformatted_spell["meta"]["translations"][language] = {
                "name": translated_spell["name"],
                "description": BeautifulSoup(
                    translated_spell["description"], features="html.parser"
                ).text,
            }
        else:
            print(f"No translation found for {spell['name']}")

    reformatted_spell = {k: v for k, v in reformatted_spell.items() if v != {}}
    return reformatted_spell


def main():
    generated_spells = []
    for filepath in glob.glob(str(spells_filepath)):
        spells_data = json.load(open(filepath))

        for spell in spells_data["spell"]:
            reformatted_spell = reformat_spell(spell)
            if not reformatted_spell:
                continue
            generated_spells.append(reformatted_spell)

    with open(output_filepath, "w") as out:
        json.dump(generated_spells, out, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
