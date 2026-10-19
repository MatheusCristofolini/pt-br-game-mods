import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

with open('workspace/menu_target_strings.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("\n=== CONTROLES ===")
controls = {k: v for k, v in data.items() if any(w in k.lower() for w in ['ctrl', 'key', 'btn', 'bind', 'mouse', 'gamepad', 'stick', 'joy', 'invert', 'sensit', 'vibrat'])}
for k, v in list(controls.items())[:40]:
    print(f"{k} | EN: {repr(v['en'])} | ES: {repr(v['es'])}")

print("\n=== DIFICULDADE E MODOS ===")
diff = {k: v for k, v in data.items() if any(w in k.lower() for w in ['diff', 'ranger', 'spartan', 'survival', 'crosshair', 'subtit'])}
for k, v in list(diff.items())[:40]:
    print(f"{k} | EN: {repr(v['en'])} | ES: {repr(v['es'])}")
