#!/usr/bin/env python3

import re
import sys
from pathlib import Path

TEXT_WITHIN_TAG = re.compile(r">\s*([^\{>]+)\s*<")

parent_dir = Path(__file__).parent.parent
templates_dir = parent_dir / "dnd5esheets" / "templates"
filename = sys.argv[1]


def snake_case(match):
    if match.group(1).strip():
        if all([c.isalpha() or c.isspace() for c in match.group(1).strip()]):
            return '>{{ _("' + match.group(1).lower().replace(" ", "_") + '") }}<'
    return match.group(0)


with open(templates_dir / filename) as htmlf:
    html = htmlf.read()
    html = re.sub(TEXT_WITHIN_TAG, snake_case, html)

with open(templates_dir / Path(str(filename) + ".new"), "w") as out:
    out.write(html)
