import sys
import json
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('workspace/extracted/localization/subtitles_en.json', 'r', encoding='utf-8') as f: en = json.load(f)
with open('workspace/extracted/localization/subtitles_es.json', 'r', encoding='utf-8') as f: es = json.load(f)
with open('workspace/extracted/localization/subtitles_nl.json', 'r', encoding='utf-8') as f: nl = json.load(f)

print("=== Chaves de Opções no Jogo ===")
keywords = ['fullscreen', 'window', 'aspect', 'physx', 'vsync', 'subtit', 'crosshair', 'hitmark', 'hint', 'aim', 'crouch', 'invert', 'vibrat', 'preset', 'sensit', 'volume', 'audio', 'video', 'quality', 'tessel', 'blur', 'gamma', 'bright', 'contrast', 'texture', 'filter', 'resolution', 'language']

options_keys = {}
for k, v in en.items():
    if '\\' in k or '/' in k: continue
    if 'credit' in k.lower(): continue
    k_l = k.lower()
    v_l = v.lower()
    if any(w in k_l for w in keywords) or any(w in v_l for w in keywords):
        if len(v) < 60:
            options_keys[k] = (v, es.get(k, ''), nl.get(k, ''))

for k, (v_en, v_es, v_nl) in options_keys.items():
    if v_es and v_es != v_en:
        print(f"{k:30} | EN: {v_en:22} | NL: {v_nl:22} | ES: {v_es:22}")
