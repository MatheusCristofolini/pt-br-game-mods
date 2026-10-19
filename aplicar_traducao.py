"""
Aplica a tradução manual editada pelo usuário diretamente no Metro 2033 Redux.
Suporta tanto JSON quanto CSV.
"""

import csv
import json
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

from games.metro_2033_redux.lng_tool import LNGTool
from games.metro_2033_redux.vfx_injector import VFXInjector
from games.metro_2033_redux.vfx_unpacker import VFXReader

def load_user_translations(input_file: Path) -> dict:
    """Lê o arquivo traduzido pelo usuário em formato JSON ou CSV."""
    translations = {}
    
    if input_file.suffix.lower() == ".json":
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        for k, item in data.items():
            if isinstance(item, dict):
                pt = item.get("traducao_ptbr", "").strip()
                if pt:
                    translations[k] = pt
            elif isinstance(item, str) and item.strip():
                translations[k] = item.strip()

    elif input_file.suffix.lower() == ".csv":
        with open(input_file, "r", encoding="utf-8-sig") as f:
            reader = csv.reader(f, delimiter=";")
            header = next(reader, None)
            for row in reader:
                if len(row) >= 4:
                    k = row[0].strip()
                    pt = row[3].strip()
                    if pt:
                        translations[k] = pt

    return translations

def apply_translation(custom_file: Path = Path("workspace/traducao/textos_completos_jogo.json")):
    print("=" * 65)
    print(" APLICANDO TRADUÇÃO MANUAL NO METRO 2033 REDUX")
    print("=" * 65)

    if not custom_file.exists():
        print(f"Erro: Arquivo '{custom_file}' não encontrado.")
        return

    translations = load_user_translations(custom_file)
    print(f"Carregadas {len(translations)} traduções manuais do arquivo.")

    if not translations:
        print("Aviso: Nenhuma tradução preenchida na coluna 'traducao_ptbr'. Preencha o arquivo antes de aplicar.")
        return

    data_dir = Path("games/metro_2033_redux/data")
    with open(data_dir / "table_us.json", "r", encoding="utf-8") as f: tbl_us = json.load(f)
    with open(data_dir / "table_nl.json", "r", encoding="utf-8") as f: tbl_nl = json.load(f)

    # 1. Carregar base de legendas
    with open("workspace/extracted/localization/subtitles_en.json", "r", encoding="utf-8") as f:
        us_subs = json.load(f)
    with open("workspace/extracted/localization/subtitles_nl.json", "r", encoding="utf-8") as f:
        pt_subs = json.load(f)

    # Configurar slot do Português no menu do Inglês
    us_subs["$nl"] = "PORTUGUÊS (BR)"

    # Aplicar as traduções do usuário
    for k, v in translations.items():
        pt_subs[k] = v
    pt_subs["$nl"] = "PORTUGUÊS (BR)"

    out_dir = Path("workspace/mod_output/localization")
    out_dir.mkdir(parents=True, exist_ok=True)
    us_out_lng = out_dir / "stable_us.lng"
    nl_out_lng = out_dir / "stable_nl.lng"

    # 2. Compilar arquivos .lng
    print("Compilando arquivos .lng com a tabela oficial da engine...")
    LNGTool.pack(us_subs, us_out_lng, base_table=tbl_us)
    LNGTool.pack(pt_subs, nl_out_lng, base_table=tbl_nl)

    # 3. Injetar no Virtual File System (VFX/VFS)
    game_install = Path(r"C:\Program Files (x86)\Steam\steamapps\common\Metro 2033 Redux")
    orig_vfx = game_install / "content.vfx.backup_original"
    if not orig_vfx.exists():
        orig_vfx = game_install / "content.vfx"

    staging_dir = Path("workspace/test_vfx_mod")
    staging_dir.mkdir(parents=True, exist_ok=True)
    staging_vfx = staging_dir / "content.vfx"
    shutil.copy2(orig_vfx, staging_vfx)

    with open(us_out_lng, "rb") as f: data_us = f.read()
    with open(nl_out_lng, "rb") as f: data_nl = f.read()

    injector = VFXInjector(staging_vfx)
    injector.inject_mod_package({
        "stable_us.lng": data_us,
        "stable_nl.lng": data_nl
    }, mod_pak_name="content99.vfs0")

    # Copiar para a pasta do jogo
    shutil.copy2(staging_dir / "content99.vfs0", game_install / "content99.vfs0")
    shutil.copy2(staging_vfx, game_install / "content.vfx")

    print("\n[SUCESSO] Sua tradução foi compilada e injetada no jogo!")
    print("Pode iniciar o Metro 2033 Redux pela Steam e conferir o resultado.")

if __name__ == "__main__":
    apply_translation()
