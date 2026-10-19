import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

with open('workspace/extracted/localization/subtitles_en.json', 'r', encoding='utf-8') as f: en = json.load(f)
with open('workspace/extracted/localization/subtitles_es.json', 'r', encoding='utf-8') as f: es = json.load(f)

for k, v in en.items():
    if '\\' in k or '/' in k: continue
    v_l = v.lower()
    if 'spartan' in v_l or 'survival' in v_l or 'ranger' in v_l:
        print(f"{k} | EN: {repr(v)} | ES: {repr(es.get(k, ''))}")
