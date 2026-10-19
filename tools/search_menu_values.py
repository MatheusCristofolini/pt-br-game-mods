import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

with open('workspace/extracted/localization/subtitles_en.json', 'r', encoding='utf-8') as f: en = json.load(f)
with open('workspace/extracted/localization/subtitles_es.json', 'r', encoding='utf-8') as f: es = json.load(f)

keywords = ['physx', 'crosshair', 'hitmark', 'hit mark', 'laser', 'vsync', 'v-sync', 'fullscreen', 'full screen', 'window', 'aspect', 'resolution', 'subtitles', 'fast hints', 'quick hints', 'hints', 'invert', 'aim assist', 'auto aim']

for k, v in en.items():
    if '\\' in k or '/' in k: continue
    if 'credit' in k.lower(): continue
    v_l = v.lower()
    if any(w in v_l for w in keywords):
        print(f"{k:25} | EN: {repr(v):25} | ES: {repr(es.get(k, '')):25}")
