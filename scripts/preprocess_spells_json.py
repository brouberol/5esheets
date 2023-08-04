import glob
import json
from pathlib import Path

from bs4 import BeautifulSoup

data_dir = Path(__file__).parent.parent / "dnd5esheets" / "data"
spells_filepath = data_dir / "spells-*.json"
spells_translations_filepath = data_dir / "translations-spells-*.json"
output_filepath = data_dir / "spells.json"

ignore_fields = ["basicRules", "hasFluffImages", "otherSources"]
source_fields = ["book", "page"]

field_name_translations = {
    "source": "book",
    "components": "casting",
}
casting_translations = {"v": "verbal", "s": "somatic", "m": "material"}
school_translations = {
    "A": "abjuration",
    "C": "conjuration",
    "V": "evocation",
    "D": "divination",
    "T": "transmutation",
    "E": "enchantment",
    "I": "illusion",
    "N": "necromancy",
}

translations = {}
for translations_filepath in glob.glob(str(spells_translations_filepath)):
    language = Path(translations_filepath).stem.split("-")[-1]
    translated_data = json.load(open(translations_filepath))
    translated_data = {entry["id"]: entry for entry in translated_data["entries"]}
    translations[language] = translated_data


def is_camel_case(s: str) -> bool:
    return s != s.lower() and s != s.upper() and "_" not in s


def camel_to_snake(s: str) -> str:
    return "".join(["_" + c.lower() if c.isupper() else c for c in s]).lstrip("_")


def aggregate_entry(value: str | dict | list) -> str:
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
    return "\n\n".join(description_parts)


def reformat_spell(spell: dict) -> dict | None:
    reformatted_spell = {"meta": {"translations": {}}, "source": {}, "casting": {}}

    for field, value in spell.items():
        field = field_name_translations.get(field) or field
        if field in ignore_fields:
            continue
        if is_camel_case(field):
            field = camel_to_snake(field)

        if field in source_fields:
            reformatted_spell["source"][field] = value
        elif field == "entries":
            reformatted_spell["meta"]["description"] = aggregate_entry(value)
        elif field == "entries_higher_level":
            reformatted_spell["meta"]["description_higher_level"] = aggregate_entry(
                value
            )
        elif field == "meta":
            for k, v in spell["meta"].items():
                if k == "ritual":
                    reformatted_spell["casting"]["ritual"] = v
                else:
                    reformatted_spell["meta"][k] = v
        elif field == "casting":
            for k, v in value.items():
                translated_k = casting_translations[k]
                if translated_k == "material" and isinstance(v, str):
                    reformatted_spell["casting"][translated_k] = {"text": v}
                else:
                    reformatted_spell["casting"][translated_k] = v
        elif field == "duration":
            durations = []
            for duration_item in value:
                if "concentration" in duration_item:
                    reformatted_spell["casting"]["concentration"] = duration_item.pop(
                        "concentration"
                    )
                if "duration" in duration_item:
                    for subfield, subvalue in duration_item.pop("duration").items():
                        if subfield == "type":
                            duration_item["unit"] = subvalue
                        else:
                            duration_item[subfield] = subvalue
                durations.append(duration_item)
            reformatted_spell["duration"] = durations
        elif field == "school":
            reformatted_spell["school"] = school_translations[value]
        elif field == "scaling_level_dice":
            if isinstance(value, dict):
                value = [value]
            reformatted_spell[field] = value
        else:
            reformatted_spell[field] = value

    if "description_higher_level" in reformatted_spell["meta"]:
        reformatted_spell["meta"][
            "description"
        ] += f"\n\n{reformatted_spell['meta'].pop('description_higher_level')}"

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
