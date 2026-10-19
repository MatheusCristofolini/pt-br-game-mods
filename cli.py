"""
Interface CLI do Framework de Tradução e Dublagem PT-BR (narracao-pt-br).
"""

import argparse
import json
import sys
from pathlib import Path
import yaml

from games.metro_2033_redux.vfx_unpacker import VFXReader
from games.metro_2033_redux.lng_tool import LNGTool
from core.translation.glossary import Glossary
from core.translation.translator import GameTranslator
from core.dubbing.tts_engine import TTSEngine
from core.dubbing.voice_caster import VoiceCaster
from core.dubbing.audio_dsp import get_audio_duration
from core.packager.mod_packager import ModPackager

def load_metro_configs():
    with open("games/metro_2033_redux/config.yaml", "r", encoding="utf-8") as f:
        game_cfg = yaml.safe_load(f)
    with open("games/metro_2033_redux/characters.yaml", "r", encoding="utf-8") as f:
        char_cfg = yaml.safe_load(f)
    glossary = Glossary(Path("games/metro_2033_redux/glossary_ptbr.json"))
    return game_cfg, char_cfg, glossary

def cmd_status(args):
    print("=" * 60)
    print(" STATUS DO PROJETO - MOD DUBLAGEM & TRADUÇÃO PT-BR")
    print("=" * 60)
    game_cfg, char_cfg, glossary = load_metro_configs()
    game_path = Path(game_cfg["default_install_path"])
    vfx_file = game_path / game_cfg["archive"]["index_file"]

    print(f"Jogo: {game_cfg['game_name']} ({game_cfg['engine']})")
    print(f"Diretório do jogo: {game_path} [{'OK' if game_path.exists() else 'NÃO ENCONTRADO'}]")
    print(f"Arquivo VFX: {vfx_file.name} [{'OK' if vfx_file.exists() else 'NÃO ENCONTRADO'}]")
    print(f"Termos no glossário de Metro: {len(glossary.terms)}")

    sub_en = Path("workspace/extracted/localization/subtitles_en.json")
    if sub_en.exists():
        with open(sub_en, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"Legendas extraídas: {len(data)} falas/textos disponíveis")
    else:
        print("Legendas extraídas: Ainda não extraídas (execute 'python cli.py extract-subtitles')")

    dubbed_files = list(Path("workspace/dubbed_audio").glob("*.vba"))
    print(f"Áudios dublados gerados: {len(dubbed_files)} arquivos .vba")

    mod_content = game_path / "content"
    loose_lng = mod_content / "localization" / "stable_us.lng"
    print(f"Mod ativo no jogo: {'SIM (loose files detectados)' if loose_lng.exists() else 'NÃO'}")
    print("=" * 60)

def cmd_extract_subtitles(args):
    game_cfg, _, _ = load_metro_configs()
    vfx_path = Path(game_cfg["default_install_path"]) / game_cfg["archive"]["index_file"]
    print(f"Carregando {vfx_path}...")
    reader = VFXReader(vfx_path)
    reader.load()

    lng_entry = reader.find_files("stable_us.lng")[0]
    raw_lng_path = Path("workspace/extracted/localization/stable_us.lng")
    print(f"Extraindo {lng_entry.full_path}...")
    reader.extract_file(lng_entry, raw_lng_path)

    json_path = Path("workspace/extracted/localization/subtitles_en.json")
    print("Exportando textos para JSON...")
    entries = LNGTool.export_json(raw_lng_path, json_path)
    print(f"Sucesso! {len(entries)} textos exportados para {json_path}")

def cmd_list_narratives(args):
    json_path = Path("workspace/extracted/localization/subtitles_en.json")
    if not json_path.exists():
        print("Arquivo subtitles_en.json não encontrado. Execute primeiro: python cli.py extract-subtitles")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        subs = json.load(f)

    narratives = {k: v for k, v in subs.items() if "narrative" in k.lower() or k == "2033\\intro"}
    print(f"\nTotal de narrações de capítulos do Artyom encontradas: {len(narratives)}\n")
    for idx, (k, v) in enumerate(narratives.items(), 1):
        print(f"{idx:02d}. [{k}]")
        print(f"    Texto: {v[:100]}...\n")

def cmd_dub_prologue(args):
    """Gera a dublagem de demonstração do prólogo e das primeiras narrações de Artyom em PT-BR."""
    game_cfg, char_cfg, glossary = load_metro_configs()
    tts = TTSEngine(char_cfg["voices"])
    vfx_path = Path(game_cfg["default_install_path"]) / game_cfg["archive"]["index_file"]

    reader = VFXReader(vfx_path)
    reader.load()

    # Narrações icônicas de abertura do Metro 2033
    prologue_lines = [
        {
            "id": "2033/voices/l01_hunter/narrative",
            "en": "Life was never easy in the tunnels, but it was our home. There was comfort in its routines, in its familiar faces, and there was safety in its isolation. All that changed the day Hunter arrived.",
            "pt": "A vida nunca foi fácil nos túneis, mas aquele era o nosso lar. Havia conforto na sua rotina, em seus rostos conhecidos, e havia segurança no seu isolamento. Tudo isso mudou no dia em que Hunter chegou.",
            "char": "artyom"
        },
        {
            "id": "2033/voices/l02_exhibition/narrative",
            "en": "Hunter did not return. It wouldn't be easy to find an excuse to leave the station and travel to Polis, but I had given my word.",
            "pt": "Hunter não retornou. Não seria fácil encontrar uma desculpa para deixar a estação e viajar até Pólis, mas eu havia dado a minha palavra.",
            "char": "artyom"
        },
        {
            "id": "2033/voices/l02_exhibition/npc_exh_2",
            "en": "Thanks, Artyom! I knew I could count on you.",
            "pt": "Obrigado, Artyom! Sabia que podia contar com você.",
            "char": "default_male"
        }
    ]

    print("\n--- INICIANDO DUBLAGEM PT-BR DE DEMONSTRAÇÃO ---")
    for item in prologue_lines:
        vba_rel_path = f"{item['id']}.vba"
        orig_match = reader.find_files(f"content/sounds.us/{vba_rel_path}")
        
        orig_dur = None
        if orig_match:
            # Extrair original para medir duração exata
            temp_orig = Path(f"workspace/extracted/audio/{vba_rel_path}")
            reader.extract_file(orig_match[0], temp_orig)
            orig_dur = get_audio_duration(temp_orig)

        out_vba = Path(f"workspace/dubbed_audio/{vba_rel_path}")
        print(f"\nDublando: {item['id']}")
        print(f" Personagem: {item['char']} ({char_cfg['voices'][item['char']]['voice']})")
        print(f" Fala PT-BR: \"{item['pt']}\"")
        if orig_dur:
            print(f" Duração original: {orig_dur:.2f}s")

        tts.synthesize_sync(
            text=item["pt"],
            character_key=item["char"],
            output_vba_path=out_vba,
            target_max_duration=orig_dur
        )

        new_dur = get_audio_duration(out_vba)
        print(f" Gerado com sucesso: {out_vba} (duração: {new_dur:.2f}s, tamanho: {out_vba.stat().st_size} bytes)")

def cmd_build_mod(args):
    """Compila as legendas PT-BR e prepara o diretório do mod em workspace/mod_output/."""
    print("\nCompilando Mod PT-BR...")
    game_cfg, char_cfg, glossary = load_metro_configs()
    json_path = Path("workspace/extracted/localization/subtitles_en.json")
    if not json_path.exists():
        print("Extraia primeiro as legendas com 'python cli.py extract-subtitles'")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        subs = json.load(f)

    # Aplicar traduções e glossário
    translator = GameTranslator(glossary)
    
    # Injetar traduções de falas prioritárias de demonstração
    subs["2033\\voices\\l01_hunter\\narrative"] = "A vida nunca foi fácil nos túneis, mas aquele era o nosso lar. Havia conforto na sua rotina, em seus rostos conhecidos, e havia segurança no seu isolamento. Tudo isso mudou no dia em que Hunter chegou."
    subs["2033\\voices\\l02_exhibition\\narrative"] = "Hunter não retornou. Não seria fácil encontrar uma desculpa para deixar a estação e viajar até Pólis, mas eu havia dado a minha palavra."
    subs["2033\\voices\\l02_exhibition\\npc_exh_2"] = "Obrigado, Artyom! Sabia que podia contar com você."
    subs["2033_intro_notags"] = "Eu nasci em Moscou, mas não me lembro de nada daquela época. Eu era apenas um bebê quando o velho mundo foi consumido pelo fogo do apocalipse nuclear. Quarenta mil pessoas conseguiram salvar suas vidas fugindo para o Metrô, o maior abrigo antinuclear já construído..."

    mod_dir = Path("workspace/mod_output")
    target_lng = mod_dir / "localization" / "stable_us.lng"
    print(f"Recompilando {target_lng}...")
    LNGTool.pack(subs, target_lng)
    print(f"Legendas compiladas ({target_lng.stat().st_size} bytes)!")

    # Copiar áudios dublados gerados para mod_dir
    dubbed_dir = Path("workspace/dubbed_audio")
    for vba_file in dubbed_dir.rglob("*.vba"):
        rel = vba_file.relative_to(dubbed_dir)
        dest = mod_dir / "sounds.us" / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        import shutil
        shutil.copy2(vba_file, dest)
        print(f"Áudio incluído no mod: sounds.us/{rel}")

    print(f"\nMod estruturado com sucesso em: {mod_dir}")

def cmd_install(args):
    """Instala o mod diretamente na pasta de instalação do Metro 2033 Redux."""
    game_cfg, _, _ = load_metro_configs()
    packager = ModPackager(Path(game_cfg["default_install_path"]))
    mod_dir = Path("workspace/mod_output")

    if not mod_dir.exists():
        print("Execute primeiro: python cli.py build-mod")
        return

    print(f"Instalando mod em {packager.content_dir}...")
    installed = packager.install_loose_files(mod_dir)
    print(f"\nInstalados {len(installed)} arquivos com sucesso:")
    for f in installed:
        print(f" - {f}")
    print("\nMod pronto! Você pode abrir o jogo pela Steam para testar a tradução e narração!")

def cmd_uninstall(args):
    """Remove o mod da pasta do jogo."""
    game_cfg, _, _ = load_metro_configs()
    packager = ModPackager(Path(game_cfg["default_install_path"]))
    mod_dir = Path("workspace/mod_output")
    removed = packager.uninstall_loose_files(mod_dir)
    print(f"Removidos {len(removed)} arquivos do mod.")

def cmd_package(args):
    """Cria um pacote .ZIP com instalador para distribuição pública."""
    game_cfg, _, _ = load_metro_configs()
    packager = ModPackager(Path(game_cfg["default_install_path"]))
    mod_dir = Path("workspace/mod_output")
    out_zip = Path("workspace/Metro_2033_Redux_PTBR_Mod.zip")

    if not mod_dir.exists():
        print("Execute primeiro: python cli.py build-mod")
        return

    print(f"Empacotando mod em {out_zip}...")
    packager.create_distribution_zip(mod_dir, out_zip)
    print(f"Pacote de distribuição gerado com sucesso: {out_zip} ({out_zip.stat().st_size} bytes)!")

def main():
    parser = argparse.ArgumentParser(description="CLI de Tradução e Dublagem PT-BR para Jogos")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("status", help="Exibe o status do ambiente e dos arquivos")
    subparsers.add_parser("extract-subtitles", help="Extrai e exporta legendas de stable_us.lng para JSON")
    subparsers.add_parser("list-narratives", help="Lista as narrações de capítulos de Artyom")
    subparsers.add_parser("dub-prologue", help="Gera dublagem PT-BR do prólogo e primeiras narrações")
    subparsers.add_parser("build-mod", help="Compila as legendas e prepara os arquivos do mod")
    subparsers.add_parser("install", help="Instala o mod na pasta do jogo")
    subparsers.add_parser("uninstall", help="Remove o mod da pasta do jogo")
    subparsers.add_parser("package", help="Gera arquivo ZIP do mod para distribuição")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    commands = {
        "status": cmd_status,
        "extract-subtitles": cmd_extract_subtitles,
        "list-narratives": cmd_list_narratives,
        "dub-prologue": cmd_dub_prologue,
        "build-mod": cmd_build_mod,
        "install": cmd_install,
        "uninstall": cmd_uninstall,
        "package": cmd_package
    }

    commands[args.command](args)

if __name__ == "__main__":
    main()
