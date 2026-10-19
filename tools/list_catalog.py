import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

with open('workspace/menu_catalog.json', 'r', encoding='utf-8') as f:
    cat = json.load(f)

for i, (k, item) in enumerate(cat.items(), 1):
    print(f"{i:03d}. {k}: {repr(item['en'])}")
