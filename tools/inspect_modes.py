import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

with open('workspace/extracted/localization/subtitles_en.json', 'r', encoding='utf-8') as f: en = json.load(f)
with open('workspace/extracted/localization/subtitles_es.json', 'r', encoding='utf-8') as f: es = json.load(f)

for k, v in en.items():
    k_l = k.lower()
    if any(w in k_l for w in ['survival', 'spartan', 'playstyle', 'difficulty', 'play_style', 'game_mode']):
        print(f"{k} | EN: {repr(v)} | ES: {repr(es.get(k, ''))}")
