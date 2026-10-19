"""
Ferramenta para extrair todos os textos do jogo Metro 2033 Redux para tradução manual.
Gera arquivos em formato JSON e CSV organizados para fácil edição.
"""

import csv
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

from games.metro_2033_redux.lng_tool import LNGTool
from games.metro_2033_redux.vfx_unpacker import VFXReader

def export_all():
    print("=" * 65)
    print(" EXTRAINDO TODOS OS TEXTOS DO METRO 2033 REDUX")
    print("=" * 65)

    game_dir = Path(r"C:\Program Files (x86)\Steam\steamapps\common\Metro 2033 Redux")
    vfx_file = game_dir / "content.vfx.backup_original"
    if not vfx_file.exists():
        vfx_file = game_dir / "content.vfx"

    # 1. Extrair os arquivos originais em inglês e espanhol (referência)
    reader = VFXReader(vfx_file)
    reader.load()

    raw_us = reader.extract_file(reader.entries[30])
    raw_es = reader.extract_file(reader.entries[33])

    out_dir = Path("workspace/traducao")
    out_dir.mkdir(parents=True, exist_ok=True)

    temp_us = out_dir / "temp_us.lng"
    temp_es = out_dir / "temp_es.lng"
    with open(temp_us, "wb") as f: f.write(raw_us)
    with open(temp_es, "wb") as f: f.write(raw_es)

    subs_en = LNGTool.unpack(temp_us)
    subs_es = LNGTool.unpack(temp_es)

    temp_us.unlink(missing_ok=True)
    temp_es.unlink(missing_ok=True)

    print(f"Total de textos extraídos: {len(subs_en)} strings.")

    # 2. Separar em categorias para facilitar a sua edição:
    # A) Apenas Menus, Opções, Interface, HUD e Capítulos (essencial para menus)
    # B) Textos Completos do Jogo (todas as 27.035 falas e legendas)

    menu_dict = {}
    full_dict = {}

    from games.metro_2033_redux.menu_translations_ptbr import MENU_TRANSLATIONS_PTBR

    for key, text_en in subs_en.items():
        if not text_en.strip():
            continue
        text_es = subs_es.get(key, "")
        existing_pt = MENU_TRANSLATIONS_PTBR.get(key, "")

        item = {
            "chave": key,
            "original_en": text_en,
            "referencia_es": text_es,
            "traducao_ptbr": existing_pt
        }
        full_dict[key] = item

        # Critério de Menus e Interface: não é áudio de fase longo nem créditos de desenvolvedores
        if "\\" not in key and "/" not in key and "credit" not in key.lower():
            menu_dict[key] = item

    # 3. Salvar os arquivos em JSON (fácil de editar em qualquer editor de código)
    path_menu_json = out_dir / "textos_menus_opcoes.json"
    with open(path_menu_json, "w", encoding="utf-8") as f:
        json.dump(menu_dict, f, ensure_ascii=False, indent=2)

    path_full_json = out_dir / "textos_completos_jogo.json"
    with open(path_full_json, "w", encoding="utf-8") as f:
        json.dump(full_dict, f, ensure_ascii=False, indent=2)

    # 4. Salvar também em CSV (para poder abrir e editar no Excel se preferir)
    path_menu_csv = out_dir / "textos_menus_opcoes.csv"
    with open(path_menu_csv, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["chave", "original_en", "referencia_es", "traducao_ptbr"])
        for item in menu_dict.values():
            writer.writerow([item["chave"], item["original_en"], item["referencia_es"], item["traducao_ptbr"]])

    print("\n[OK] Arquivos gerados com sucesso na pasta 'workspace/traducao/':")
    print(f"  1. {path_menu_json} ({len(menu_dict)} textos de menus, opções e interface)")
    print(f"  2. {path_menu_csv} (Mesmo arquivo de menus, abrível no Excel)")
    print(f"  3. {path_full_json} ({len(full_dict)} textos de todo o jogo)")

if __name__ == "__main__":
    export_all()
