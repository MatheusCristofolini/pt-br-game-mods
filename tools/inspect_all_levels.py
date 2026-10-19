import sys
import json
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('workspace/extracted/localization/subtitles_en.json', 'r', encoding='utf-8') as f: en = json.load(f)
with open('workspace/extracted/localization/subtitles_es.json', 'r', encoding='utf-8') as f: es = json.load(f)
with open('workspace/extracted/localization/subtitles_nl.json', 'r', encoding='utf-8') as f: nl = json.load(f)

# Procurar todas as chaves associadas a nomes de fases no Metro 2033
# Níveis do Metro 2033:
# Intro / Tower, Hunter, Exhibition, Chase, Riga, Lost Tunnel, Market, Dead City,
# Dry, Ghosts, Cursed, Armory, Frontline, Trolley Combat, Depot, Defense, Outpost,
# Black Station, Polis, Alley, Library, Depository, Archives, Driving to Sparta, Sparta,
# Dark Star, D6, Caves, Biomass, Separation, Tower, Top.

level_names = [
    'hunter', 'exhibition', 'chase', 'riga', 'lost tunnel', 'market', 'dead city',
    'dry', 'ghosts', 'cursed', 'armory', 'frontline', 'trolley', 'depot', 'defense',
    'outpost', 'black station', 'polis', 'alley', 'library', 'depository', 'archives',
    'sparta', 'dark star', 'd6', 'caves', 'biomass', 'separation', 'tower', 'top',
    'prologue', 'chapter'
]

print("=== Nomes de Níveis e Capítulos no en ===")
found_levels = {}
for k, v in en.items():
    if '\\' in k or '/' in k: continue
    if 'credit' in k.lower(): continue
    v_l = v.strip().lower()
    k_l = k.lower()
    if any(name in v_l for name in level_names) or any(name in k_l for name in level_names):
        # se for texto relativamente curto (título de capítulo, fase, objetivo ou rich presence)
        if len(v) < 60:
            found_levels[k] = (v, es.get(k, ''), nl.get(k, ''))

for k, (v_en, v_es, v_nl) in found_levels.items():
    print(f"{k:30} | EN: {v_en:25} | NL: {v_nl:25} | ES: {v_es:25}")
