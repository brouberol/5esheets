#!/usr/bin/env python3

import sys

for line in sys.stdin:
    line = line.strip()
    tokens = line.split(":")
    command = tokens[1]
    explanation = tokens[2].split("## ")[-1]
    print(f"make {command:<26} {explanation}")
