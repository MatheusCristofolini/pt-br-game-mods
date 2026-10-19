import sys
import json
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('workspace/extracted/localization/subtitles_en.json', 'r', encoding='utf-8') as f: en = json.load(f)
with open('workspace/extracted/localization/subtitles_es.json', 'r', encoding='utf-8') as f: es = json.load(f)
with open('workspace/extracted/localization/subtitles_nl.json', 'r', encoding='utf-8') as f: nl = json.load(f)

print("=== Chaves $m_l... ===")
for k, v in en.items():
    if k.startswith('$m_l') or k.startswith('$chapter'):
        print(f"{k:25} | EN: {v:25} | NL: {nl.get(k, ''):25} | ES: {es.get(k, ''):25}")
