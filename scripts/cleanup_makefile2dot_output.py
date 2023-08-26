#!/usr/bin/env python3

"""
Collapse large collection of files in a file glob pattern
to simplify the output of makefile2dot.
"""

import re
import sys

patterns_to_collapse = {
    'dnd5esheets/front/src/.*\.[jt]s[^"]*': "dnd5esheets/front/src/*.[jt]*",
    "dnd5esheets/api/.*\.py": "dnd5esheets/api/*.py",
    'lib/libsqlite3\.[^"]+': "lib/libsqlite3.*",
}
output = []
for line in sys.stdin:
    line = line.strip()
    parts = line.split(" -> ")
    cleaned_parts = []
    for part in parts:
        for pattern, repl_str in patterns_to_collapse.items():
            part = re.sub(pattern, repl_str, part)
        cleaned_parts.append(part)
    line = " -> ".join(cleaned_parts)
    if line not in output:
        output.append(line)

for line in output:
    print(line)
