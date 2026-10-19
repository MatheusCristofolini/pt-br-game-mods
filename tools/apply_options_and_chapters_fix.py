import sys
import json
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

from games.metro_2033_redux.menu_translations_ptbr import MENU_TRANSLATIONS_PTBR

updated = dict(MENU_TRANSLATIONS_PTBR)

full_corrections = {
    # =========================================================================
    # VALORES DE OPÇÕES (ON / OFF / TOGGLES / NÍVEIS DE QUALIDADE)
    # =========================================================================
    "$on": "LIGADO",
    "$off": "DESLIGADO",
    "on": "ligado",
    "off": "desligado",
    "$low": "BAIXA",
    "$medium": "MÉDIA",
    "$fairly_strong": "MÉDIA",
    "$high": "ALTA",
    "$very_high": "MUITO ALTA",
    "$auto": "AUTOMÁTICO",
    "$blur_off": "DESLIGADO",
    "$blur_normal": "NORMAL",
    "blur_low": "BAIXO",
    "blur_normal": "NORMAL",
    "toggle_aim_mode": "MODO DE MIRA",
    "toggle_aim_off": "SEGURAR",
    "toggle_aim_on": "ALTERNAR",
    "toggle_crouch_off": "SEGURAR",
    "toggle_crouch_on": "ALTERNAR",
    "ssaa_off": "DESLIGADO",
    "ssaa_4x": "4X",
    "ssaa_2x": "2X",
    "ssaa_0_5x": "0.5X",
    "Copy of $yes": "Sim",
    "Copy of $no": "Não",

    # =========================================================================
    # OPÇÕES DE JOGO (GAME OPTIONS)
    # =========================================================================
    "$game_options": "JOGO",
    "$game_difficulty": "DIFICULDADE",
    "$game_difficulty_easy": "FÁCIL",
    "$game_difficulty_medium": "NORMAL",
    "$game_difficulty_hard": "DIFÍCIL",
    "$game_difficulty_ranger": "RANGER",
    "$game_difficulty_ranger_hard": "RANGER DIFÍCIL",
    "$game_difficulty_survival": "RANGER FÁCIL",
    "$game_difficulty_survival_hard": "RANGER DIFÍCIL",
    "$game_subtitles": "LEGENDAS",
    "$crosshair": "MIRA NA TELA",
    "$laser_crosshair": "MIRA LASER",
    "hitmarks_mode": "INDICADORES DE ACERTO",
    "$quick_hints": "DICAS RÁPIDAS",
    "$hints": "DICAS",
    "$aim_assist": "ASSISTÊNCIA DE MIRA",
    "auto_aim_border": "LIMITE DA MIRA AUTOMÁTICA",
    "$aim_sensitivity": "SENSIBILIDADE DE MIRA",
    "$lang_text": "IDIOMA DO TEXTO",
    "$lang_sound": "IDIOMA DA VOZ",

    # =========================================================================
    # OPÇÕES DE VÍDEO (VIDEO OPTIONS)
    # =========================================================================
    "$video": "VÍDEO",
    "$video_quality": "QUALIDADE",
    "$video_quality_low": "- BAIXA",
    "$video_quality_medium": "- MÉDIA",
    "$video_quality_high": "- ALTA",
    "$video_quality_ultra_high": "- MUITO ALTA",
    "$adv_phisics": "PHYSX AVANÇADO",
    "$tesselation": "TESSELAÇÃO",
    "$texture_filtering": "FILTRAGEM DE TEXTURAS",
    "$shadow_resolution": "RESOLUÇÃO DE SOMBRAS",
    "$motion_blur": "DESFOQUE DE MOVIMENTO",
    "$ssaa": "SSAA",
    "$gamma": "GAMA",
    "gamma_option": "CORREÇÃO DE GAMA",
    "menu_gamma_0": "QUASE INVISÍVEL",
    "$video_brightness": "BRILHO",
    "$video_contrast": "CONTRASTE",
    "$dx_11_options": "OPÇÕES DIRECTX 11",
    "$volumetric_rendering": "TEXTURIZAÇÃO VOLUMÉTRICA",

    # =========================================================================
    # OPÇÕES DE ÁUDIO (AUDIO OPTIONS)
    # =========================================================================
    "$audio_options": "ÁUDIO",
    "$sound": "SOM",
    "$sound_effect_volume": "VOLUME GERAL",
    "$sound_music_volume": "VOLUME DA MÚSICA",
    "ps4_speaker_volume": "CONTROLE DE VOLUME (ALTO-FALANTE DO CONTROLE)",

    # =========================================================================
    # OPÇÕES DE CONTROLES (CONTROLS OPTIONS)
    # =========================================================================
    "$controls_options": "CONTROLES",
    "$controls": "CONTROLES",
    "$controls_preset": "ESQUEMA DE CONTROLE",
    "$controls_sensevity": "SENSIBILIDADE",
    "$controls_invert_y": "INVERTER EIXO Y",
    "$invert_y_axis": "INVERTER EIXO Y",
    "$controls_vibration": "VIBRAÇÃO",
    "$vibration_off": "DESLIGADO",
    "$controls_keyboard": "TECLADO",
    "$controls_mouse": "MOUSE",
    "$controls_gamepad": "CONTROLE",
    "$controls_gamepad_ps3": "CONTROLE SEM FIO",
    "joy_sens_y_scale": "ESCALA SENSIB. EIXO Y",

    # =========================================================================
    # MENU DE CAPÍTULOS E NÍVEIS
    # =========================================================================
    "$chapter_1": "CAPÍTULO 1 \"QUE COMECE A JORNADA\"",
    "$chapter_2": "CAPÍTULO 2 \"BOURBON\"",
    "$chapter_3": "CAPÍTULO 3 \"KHAN\"",
    "$chapter_4": "CAPÍTULO 4 \"GUERRA\"",
    "$chapter_5": "CAPÍTULO 5 \"ESPERANÇA\"",
    "$chapter_6": "CAPÍTULO 6 \"D6\"",
    "$chapter_7": "CAPÍTULO 7 \"TORRE\"",

    # Níveis individuais do menu de seleção de fases
    "$l00_1": "Prólogo",
    "$l00_intro": "TORRE",
    "$l01_1": "8 dias antes",
    "$l01_hunter": "HUNTER",
    "$l02_1": "Capítulo 1: Que comece a jornada",
    "$l02_exhibition": "EXPOSIÇÃO",
    "$l03_1": "Perseguição",
    "$l03_chase": "PERSEGUIÇÃO",
    "$l04_1": "Capítulo 2: Bourbon",
    "$l04_riga": "RIGA",
    "$l05_1": "Túneis perdidos",
    "$l06_1": "A ponte",
    "$l07_1": "Catacumbas perdidas",
    "$l08_1": "Mercado",
    "$l08_market": "MERCADO",
    "$l09_1": "Cidade Morta",
    "$l11_1": "Capítulo 3: Khan",
    "$l11_dry": "SECA",
    "$l12_1": "Fantasmas",
    "$l12_ghosts": "FANTASMAS",
    "$l13_1": "Anomalia",
    "$l14_1": "Amaldiçoada",
    "$l14_cursed": "AMALDIÇOADA",
    "$l15_1": "Armaria",
    "$l15_armory": "ARMARIA",
    "$l16_1": "Capítulo 4: Guerra",
    "$l16_frontline": "LINHA DE FRENTE",
    "$l17_1": "Combate no Vagão",
    "$l18_1": "Depósito",
    "$l18_depot": "DEPÓSITO",
    "$l19_1": "Defesa",
    "$l19_defence": "DEFESA",
    "$l20_1": "Criança",
    "$l21_1": "Posto Avançado",
    "$l22_1": "Estação Negra",
    "$l22_black": "ESTAÇÃO NEGRA",
    "$l23_1": "Capítulo 5: Esperança",
    "$l23_polis": "POLIS",
    "$l24_1": "Beco",
    "$l24_alley": "BECO",
    "$l25_1": "Biblioteca",
    "$l26_1": "Depósito de Livros",
    "$l26_depository": "DEPÓSITO DE LIVROS",
    "$l27_1": "Arquivos",
    "$l27_archives": "ARQUIVOS",
    "$l28_1": "A Caminho de Esparta",
    "$l29_church": "IGREJA",
    "$l30_1": "Capítulo 6: D6",
    "$l30_darkstar": "ESTRELA ESCURA",
    "$l31_1": "Catacumbas",
    "$l32_1": "Caverna",
    "$l32_cave": "CAVERNA",
    "$l33_1": "D6",
    "$l33_d6": "D6",
    "$l34_1": "Biomassa",
    "$l35_1": "Separação",
    "$l36_1": "Capítulo 7: Torre",
    "$l36_ostankino": "TORRE",
    "$l38_1": "Topo da Torre",
}

for k, v in full_corrections.items():
    updated[k] = v

print(f"Total de traduções atualizadas: {len(updated)}")

# Validar com a tabela table_nl.json
with open('games/metro_2033_redux/data/table_nl.json', 'r', encoding='utf-8') as f:
    tbl_nl = json.load(f)

all_chars = set(''.join(updated.values()))
missing = [c for c in all_chars if c not in tbl_nl]
print(f"Caracteres incompatíveis com a fonte da engine: {missing}")
assert len(missing) == 0, f"Caracteres incompatíveis encontrados: {missing}"

# Salvar dicionário expandido
with open('games/metro_2033_redux/menu_translations_ptbr.py', 'w', encoding='utf-8') as f:
    f.write('"""\nDicionário consolidado de traduções PT-BR para Menus, Opções, Modos e Interface do Metro 2033 Redux.\n"""\n\nMENU_TRANSLATIONS_PTBR = ')
    f.write(json.dumps(updated, ensure_ascii=False, indent=4))
    f.write('\n')

print("games/metro_2033_redux/menu_translations_ptbr.py atualizado com sucesso!")
