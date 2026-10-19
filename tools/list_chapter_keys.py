import sys
import json
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('workspace/extracted/localization/subtitles_en.json', 'r', encoding='utf-8') as f: en = json.load(f)
with open('workspace/extracted/localization/subtitles_es.json', 'r', encoding='utf-8') as f: es = json.load(f)
with open('workspace/extracted/localization/subtitles_nl.json', 'r', encoding='utf-8') as f: nl = json.load(f)

print("=== Nomes dos Capítulos e Níveis ($lXX_...) ===")
chapter_level_keys = {}
for k, v in en.items():
    if '\\' in k or '/' in k: continue
    # Todas as chaves $l... com menos de 30 caracteres
    if re.match(r'^\$l\d{1,2}(_[a-zA-Z0-9]+)?$', k):
        if len(v) < 50:
            chapter_level_keys[k] = (v, es.get(k, ''), nl.get(k, ''))

for k, (v_en, v_es, v_nl) in chapter_level_keys.items():
    print(f"{k:20} | EN: {v_en:25} | NL: {v_nl:25} | ES: {v_es:25}")
