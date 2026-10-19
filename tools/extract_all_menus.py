import sys
import json
import re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

with open('workspace/extracted/localization/subtitles_en.json', 'r', encoding='utf-8') as f:
    en = json.load(f)
with open('workspace/extracted/localization/subtitles_es.json', 'r', encoding='utf-8') as f:
    es = json.load(f)

# Procurar chaves que NÃO são áudios de personagens
# Áudios de diálogo no Metro contêm barras: voices\... ou 2033\voices\...
ui_entries = {}
dialogue_entries = {}

for k, v in en.items():
    if '\\' in k or '/' in k:
        dialogue_entries[k] = v
    else:
        ui_entries[k] = v

print(f"Total de chaves no arquivo: {len(en)}")
print(f"Chaves de diálogos com arquivos de áudio: {len(dialogue_entries)}")
print(f"Chaves de UI / Menus / Legendas / HUD: {len(ui_entries)}")

# Classificar chaves de UI
menus = {}
credits = {}
chapters = {}
hints = {}

for k, v in ui_entries.items():
    if 'credit' in k.lower():
        credits[k] = v
    elif re.match(r'^\$(m_)?l\d+', k):
        chapters[k] = v
    elif 'hint' in k.lower() or 'tip' in k.lower():
        hints[k] = v
    else:
        menus[k] = v

print(f"Créditos: {len(credits)}")
print(f"Falas/Textos de Níveis e Capítulos ($l01...): {len(chapters)}")
print(f"Dicas / Hints / Tutoriais: {len(hints)}")
print(f"Menus / Opções / HUD / Botões: {len(menus)}")

print("\n--- Amostra de 50 chaves de Menus/Opções/Botões ---")
sample_keys = list(menus.keys())[:50]
for k in sample_keys:
    en_text = menus[k]
    es_text = es.get(k, '')
    print(f"{k} | EN: {repr(en_text)} | ES: {repr(es_text)}")

# Salvar dicionário completo de menus em JSON
with open('workspace/menu_and_ui_raw.json', 'w', encoding='utf-8') as f:
    json.dump({k: {'en': menus[k], 'es': es.get(k, '')} for k in menus}, f, ensure_ascii=False, indent=2)

print("\nArquivo workspace/menu_and_ui_raw.json gerado!")
