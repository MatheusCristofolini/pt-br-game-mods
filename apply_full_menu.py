"""
Aplica a tradução completa de todos os menus, opções, controles e interface em PT-BR no Metro 2033 Redux.
"""

import json
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

from games.metro_2033_redux.lng_tool import LNGTool
from games.metro_2033_redux.vfx_injector import VFXInjector
from games.metro_2033_redux.vfx_unpacker import VFXReader
from games.metro_2033_redux.menu_translations_ptbr import MENU_TRANSLATIONS_PTBR

def apply_full_menu():
    print("=" * 65)
    print(" IMPLANTANDO TRADUÇÃO COMPLETA DOS MENUS E OPÇÕES PT-BR")
    print("=" * 65)

    data_dir = Path("games/metro_2033_redux/data")
    with open(data_dir / "table_us.json", "r", encoding="utf-8") as f:
        tbl_us = json.load(f)
    with open(data_dir / "table_nl.json", "r", encoding="utf-8") as f:
        tbl_nl = json.load(f)

    # 1. Carregar legendas originais
    with open("workspace/extracted/localization/subtitles_en.json", "r", encoding="utf-8") as f:
        us_subs = json.load(f)
    with open("workspace/extracted/localization/subtitles_nl.json", "r", encoding="utf-8") as f:
        pt_subs = json.load(f)

    # Configurar slot do Português no menu inglês
    us_subs["$nl"] = "PORTUGUÊS (BR)"

    # Aplicar todas as traduções completas de menu no slot Português
    print(f"Aplicando {len(MENU_TRANSLATIONS_PTBR)} strings traduzidas...")
    for k, text in MENU_TRANSLATIONS_PTBR.items():
        pt_subs[k] = text

    out_dir = Path("workspace/mod_output/localization")
    out_dir.mkdir(parents=True, exist_ok=True)
    us_out_lng = out_dir / "stable_us.lng"
    nl_out_lng = out_dir / "stable_nl.lng"

    # 2. Compilar com as tabelas oficiais da engine
    print("Compilando stable_us.lng...")
    LNGTool.pack(us_subs, us_out_lng, base_table=tbl_us)

    print("Compilando stable_nl.lng...")
    LNGTool.pack(pt_subs, nl_out_lng, base_table=tbl_nl)

    # 3. Injetar no jogo
    game_install = Path(r"C:\Program Files (x86)\Steam\steamapps\common\Metro 2033 Redux")
    orig_vfx = game_install / "content.vfx.backup_original"
    assert orig_vfx.exists(), "content.vfx.backup_original não encontrado!"

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

    staging_vfs = staging_dir / "content99.vfs0"

    # Copiar para o diretório da Steam
    shutil.copy2(staging_vfs, game_install / "content99.vfs0")
    shutil.copy2(staging_vfx, game_install / "content.vfx")

    # 4. Validar integridade
    reader = VFXReader(game_install / "content.vfx")
    reader.load()
    extracted_nl = reader.extract_file(reader.entries[36])
    assert extracted_nl == data_nl, "Erro de integridade na extração do mod injetado!"

    print("\n[SUCESSO] Mod de tradução completa dos menus instalado com êxito!")
    print(f"Total de strings no idioma PT-BR: {len(pt_subs)}")
    print("Telas traduzidas:")
    print("  ✓ Menu Principal (Continuar, Novo Jogo, Capítulos, Opções, Sair)")
    print("  ✓ Modos de Jogo e Dificuldades (Fácil, Normal, Difícil, Ranger, Ranger Difícil)")
    print("  ✓ Menu de Vídeo e Gráficos (Qualidade, Resolução, Gama, SSAA, VSync, etc.)")
    print("  ✓ Menu de Áudio (Volume Geral, Música, Vozes, Idiomas)")
    print("  ✓ Menu de Controles (Esquema de Teclas, Sensibilidade, Inversão de Eixos)")
    print("  ✓ Capítulos da História (Capítulos 1 a 7)")
    print("  ✓ Telas de Confirmação, Avisos de Salvamento e Diálogos do Sistema")
    print("  ✓ Kiosks de Trocas e Customização de Armas")

if __name__ == "__main__":
    apply_full_menu()
