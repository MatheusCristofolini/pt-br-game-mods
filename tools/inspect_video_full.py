import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

with open('workspace/extracted/localization/subtitles_en.json', 'r', encoding='utf-8') as f: en = json.load(f)
with open('workspace/extracted/localization/subtitles_es.json', 'r', encoding='utf-8') as f: es = json.load(f)

for k, v in en.items():
    if '\\' in k or '/' in k: continue
    k_l = k.lower()
    v_l = v.lower()
    if any(w in k_l or w in v_l for w in ['fullscreen', 'window', 'aspect', 'vsync', 'blur', 'tessel', 'ssaa', 'physx', 'filter', 'gamma', 'contrast', 'bright']):
        print(f"{k} | EN: {repr(v)} | ES: {repr(es.get(k, ''))}")
