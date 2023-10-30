import sys
from collections import Counter

import orjson as json

fields = Counter()
data = json.load(open(sys.argv[1]))

if len(sys.argv) == 3:
    iterator = data[sys.argv[2]]
else:
    iterator = data
for i, item in enumerate(data, 1):
    for key in item:
        fields[key] += 1
else:
    num_items = i

ubiquitous_items = {field for field, seen_times in fields.items() if seen_times == num_items}
non_ubiquitous_items = {
    field: seen_times for field, seen_times in fields.items() if field not in ubiquitous_items
}

print("Ubiquitous:")
for field in ubiquitous_items:
    print(f"* {field}")

print("\nNon ubiquitous:")
for field, seen_times in non_ubiquitous_items.items():
    print(f"* {field}: {seen_times}/{num_items}")
