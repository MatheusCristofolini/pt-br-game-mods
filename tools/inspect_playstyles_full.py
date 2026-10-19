import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

with open('workspace/extracted/localization/subtitles_en.json', 'r', encoding='utf-8') as f: en = json.load(f)
with open('workspace/extracted/localization/subtitles_es.json', 'r', encoding='utf-8') as f: es = json.load(f)

for k, v in en.items():
    if '\\' in k or '/' in k: continue
    v_l = v.lower()
    if 'scarce' in v_l or 'survival' in v_l or 'spartan' in v_l or 'play style' in v_l:
        print(f"KEY: {k}")
        print(f"  EN: {v}")
        print(f"  ES: {es.get(k, '')}")
