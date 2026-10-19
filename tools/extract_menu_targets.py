import sys
import json
import re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

with open('workspace/extracted/localization/subtitles_en.json', 'r', encoding='utf-8') as f:
    en = json.load(f)
with open('workspace/extracted/localization/subtitles_es.json', 'r', encoding='utf-8') as f:
    es = json.load(f)

# Filtrar chaves relevantes para o menu e interface
menu_dict = {}

for k, v in en.items():
    if not v.strip():
        continue
    # Pula áudios de diálogo
    if '\\' in k or '/' in k:
        continue
    # Pula créditos
    if 'credit' in k.lower():
        continue
    # Pula diálogos in-game longos de fases ($l01_..., etc.)
    if re.match(r'^\$(m_)?l\d{2,}_[a-zA-Z0-9]+', k):
        continue
    # Mantém nomes de capítulos, menus, opções, botões, dicas, hud, etc.
    menu_dict[k] = {
        'en': v,
        'es': es.get(k, '')
    }

print(f"Total de strings selecionadas para o Menu e UI: {len(menu_dict)}")

# Salvar JSON estruturado
with open('workspace/menu_target_strings.json', 'w', encoding='utf-8') as f:
    json.dump(menu_dict, f, ensure_ascii=False, indent=2)

print("Salvo em workspace/menu_target_strings.json")
