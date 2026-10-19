import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

with open('workspace/extracted/localization/subtitles_en.json', 'r', encoding='utf-8') as f: en = json.load(f)
with open('workspace/extracted/localization/subtitles_es.json', 'r', encoding='utf-8') as f: es = json.load(f)

for k, v in en.items():
    if '\\' in k or '/' in k: continue
    if 'credit' in k.lower(): continue
    if 'sens' in k.lower() or 'sens' in v.lower():
        print(f"{k:30} | EN: {repr(v):25} | ES: {repr(es.get(k, '')):25}")
