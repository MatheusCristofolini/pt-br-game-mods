"""
Script para gerar o teste do menu e seletor de idioma PT-BR no Metro 2033 Redux.
"""

import json
import shutil
from pathlib import Path
from games.metro_2033_redux.lng_tool import LNGTool

def main():
    print("=" * 60)
    print(" GERANDO MOD DE TESTE: IDIOMA E MENU EM PORTUGUÊS (BR)")
    print("=" * 60)

    json_path = Path("workspace/extracted/localization/subtitles_en.json")
    if not json_path.exists():
        print("Erro: subtitles_en.json não encontrado.")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        base_subs = json.load(f)

    # 1. Modificar stable_us.lng (Inglês) para que no menu exiba "PORTUGUÊS (BR)" no slot do Dutch
    us_subs = dict(base_subs)
    us_subs["$nl"] = "PORTUGUÊS (BR)"

    # 2. Criar stable_nl.lng (Português BR completo para o Menu)
    nl_json_path = Path("workspace/extracted/localization/subtitles_nl.json")
    if nl_json_path.exists():
        with open(nl_json_path, "r", encoding="utf-8") as f:
            pt_subs = json.load(f)
    else:
        pt_subs = dict(base_subs)

    # Rótulos dos idiomas na lista
    pt_subs["$nl"] = "PORTUGUÊS (BR)"
    pt_subs["$us"] = "INGLÊS"
    pt_subs["$ru"] = "RUSSO"
    pt_subs["$de"] = "ALEMÃO"
    pt_subs["$es"] = "ESPANHOL"
    pt_subs["$fr"] = "FRANCÊS"
    pt_subs["$it"] = "ITALIANO"
    pt_subs["$pl"] = "POLONÊS"
    pt_subs["$cz"] = "TCHECO"
    pt_subs["$uk"] = "UCRANIANO"

    # Tradução do Menu Principal
    menu_translations = {
        "$continue_game": "CONTINUAR",
        "$continue_menu": "CONTINUAR",
        "$continue": "Pressione <use> para continuar",
        "$press_any_key_to_continue": "Pressione qualquer tecla para continuar",
        "$new_game": "NOVO JOGO",
        "$load_game": "CARREGAR JOGO",
        "$load_game_short": "CAPÍTULOS",
        "$options": "OPÇÕES",
        "$credits": "CRÉDITOS",
        "$quit_game": "SAIR DO JOGO",
        "$quit_game_3d": "<menu_back> SAIR DO JOGO",

        # Menus de Opções
        "$lang_text": "IDIOMA DO TEXTO",
        "$lang_sound": "IDIOMA DA VOZ",
        "$game_options": "JOGO",
        "$video": "VÍDEO",
        "$audio_options": "ÁUDIO",
        "$controls": "CONTROLES",
        "$back": "VOLTAR",
        "$apply_settings": "APLICAR",
        "$use_defaults": "PADRÕES",
        "$game_subtitles": "LEGENDAS",
        "$gamma": "GAMA",
        "$yes": "Sim",
        "$no": "Não",
        "$cancel": "CANCELAR"
    }

    for k, v in menu_translations.items():
        pt_subs[k] = v

    # Diretório do mod local
    out_dir = Path("workspace/mod_output/localization")
    out_dir.mkdir(parents=True, exist_ok=True)

    us_out_lng = out_dir / "stable_us.lng"
    nl_out_lng = out_dir / "stable_nl.lng"

    # Referências das tabelas oficiais da 4A Engine
    data_dir = Path("games/metro_2033_redux/data")
    ref_us = data_dir / "table_us.json"
    ref_nl = data_dir / "table_nl.json"

    with open(ref_us, "r", encoding="utf-8") as f: tbl_us = json.load(f)
    with open(ref_nl, "r", encoding="utf-8") as f: tbl_nl = json.load(f)

    print("Compilando stable_us.lng (Inglês com opção Português BR)...")
    LNGTool.pack(us_subs, us_out_lng, base_table=tbl_us)

    print("Compilando stable_nl.lng (Português BR - Menu Principal)...")
    LNGTool.pack(pt_subs, nl_out_lng, base_table=tbl_nl)

    # Injetar diretamente no Virtual File System (VFX/VFS) do jogo
    game_install = Path(r"C:\Program Files (x86)\Steam\steamapps\common\Metro 2033 Redux")
    orig_vfx = game_install / "content.vfx.backup_original"
    if not orig_vfx.exists() and (game_install / "content.vfx").exists():
        shutil.copy2(game_install / "content.vfx", orig_vfx)

    if orig_vfx.exists():
        from games.metro_2033_redux.vfx_injector import VFXInjector
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

        shutil.copy2(staging_dir / "content99.vfs0", game_install / "content99.vfs0")
        shutil.copy2(staging_vfx, game_install / "content.vfx")
        print("\n[OK] Pacote de mod e content.vfx atualizados na pasta do jogo!")

    print("\n" + "=" * 60)
    print(" MOD DE TESTE INSTALADO COM SUCESSO!")
    print("=" * 60)
    print("Como testar no jogo:")
    print("1. Abra o Metro 2033 Redux pela Steam.")
    print("2. Vá em: OPTIONS (OPÇÕES) -> GAME (JOGO).")
    print("3. Em TEXT LANGUAGE (IDIOMA DO TEXTO), alterne até: PORTUGUÊS (BR).")
    print("4. O menu principal e os botões passarão para Português!")
    print("5. Todos os outros idiomas continuam 100% disponíveis.")
    print("=" * 60)

if __name__ == "__main__":
    main()
