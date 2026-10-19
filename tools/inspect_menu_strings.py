import sys
import json
import re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

with open('workspace/extracted/localization/subtitles_en.json', 'r', encoding='utf-8') as f:
    subs = json.load(f)

# Padrões que não são menu
level_dialogue = re.compile(r'^\$(m_)?l\d+')
credits_pattern = re.compile(r'^\$credits')

menu_keys = {}
diary_keys = {}
other_ui = {}

for k, v in subs.items():
    if not v.strip():
        continue
    # Falas com caminho de pasta (áudios)
    if '\\' in k or '/' in k:
        continue
    if credits_pattern.match(k):
        continue
    if level_dialogue.match(k):
        continue
    if k.startswith('$art_note') or k.startswith('$diary'):
        diary_keys[k] = v
    elif k.startswith('$'):
        menu_keys[k] = v
    else:
        other_ui[k] = v

print(f"Total de textos no jogo: {len(subs)}")
print(f"Textos de Menus, Opções, HUD e Tutoriais: {len(menu_keys)}")
print(f"Textos de Diário e Notas do Artyom: {len(diary_keys)}")
print(f"Outras tags de UI/Controles: {len(other_ui)}")

print("\n--- Amostra de Menus e Opções ---")
for k in list(menu_keys.keys())[:25]:
    print(f"{k} = {repr(menu_keys[k])}")

# Salvar arquivo JSON específico com todos os textos de menu para tradução
output_path = Path("workspace/menu_strings_en.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(menu_keys, f, ensure_ascii=False, indent=2)

print(f"\nArquivo gerado para tradução: {output_path} ({len(menu_keys)} strings)")
