import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

with open('workspace/extracted/localization/subtitles_en.json', 'r', encoding='utf-8') as f: en = json.load(f)
with open('workspace/extracted/localization/subtitles_es.json', 'r', encoding='utf-8') as f: es = json.load(f)

for k, v in en.items():
    if any(w in k.lower() for w in ['toggle', 'fullscreen', 'windowed', 'crouch_mode', 'aim_mode']):
        print(f"{k:25} | EN: {repr(v):18} | ES: {repr(es.get(k, '')):18}")
