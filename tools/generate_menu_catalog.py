import sys
import json
import re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

with open('workspace/extracted/localization/subtitles_en.json', 'r', encoding='utf-8') as f:
    en = json.load(f)
with open('workspace/extracted/localization/subtitles_es.json', 'r', encoding='utf-8') as f:
    es = json.load(f)

# Selecionar todas as strings de Menu, Opções e Interface
menu_items = {}

# Padrões de chaves de menu
menu_prefixes = [
    '$continue', '$new_game', '$load_game', '$options', '$quit', '$credits',
    '$game_', '$video', '$audio', '$controls', '$ctrl_', '$mouse', '$key', '$btn',
    '$difficulty', '$diff', '$survival', '$spartan', '$ranger',
    '$gamma', '$quality', '$resolution', '$vsync', '$motion_blur', '$tessellation', '$ssaa',
    '$volume', '$lang_', '$subtitles', '$crosshair', '$hitmarks',
    '$back', '$apply', '$cancel', '$yes', '$no', '$default', '$reset',
    '$press_', '$use', '$chapter', '$level', '$menu_', '$confirm', '$warning', '$error',
    '$corrupted', '$storage', '$profile', '$signed_in', '$signed_out',
    'menu_', 'opt_', 'video_', 'audio_', 'ctrl_'
]

# Chaves exatas de idiomas
lang_keys = ['$us', '$ru', '$de', '$es', '$fr', '$it', '$nl', '$pl', '$cz', '$uk']

for k, v in en.items():
    if not v.strip():
        continue
    k_low = k.lower()
    # Pula áudios de diálogo e créditos longos
    if '\\' in k or '/' in k or 'credits_us.' in k_low or 'credits.' in k_low:
        continue
    if re.match(r'^\$(m_)?l\d{2,}_[a-zA-Z0-9]+', k):
        continue

    # Verifica se bate com os prefixos de menu
    matched = False
    if k in lang_keys:
        matched = True
    elif any(k_low.startswith(p) for p in menu_prefixes):
        matched = True
    elif any(p in k_low for p in ['option', 'difficulty', 'resolution', 'quality', 'gamma', 'vsync', 'volume', 'subtitles', 'controls']):
        matched = True

    if matched:
        menu_items[k] = {
            'en': v,
            'es': es.get(k, '')
        }

print(f"Total de itens de menu identificados: {len(menu_items)}")

# Salvar catálogo
out_file = Path('workspace/menu_catalog.json')
with open(out_file, 'w', encoding='utf-8') as f:
    json.dump(menu_items, f, ensure_ascii=False, indent=2)

print(f"Catálogo salvo em {out_file}")
