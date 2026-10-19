import sys
import json
import re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

with open('workspace/extracted/localization/subtitles_en.json', 'r', encoding='utf-8') as f: en = json.load(f)
with open('workspace/extracted/localization/subtitles_es.json', 'r', encoding='utf-8') as f: es = json.load(f)

from games.metro_2033_redux.menu_translations_ptbr import MENU_TRANSLATIONS_PTBR

expanded = dict(MENU_TRANSLATIONS_PTBR)

# Novas traduções essenciais identificadas
additions = {
    # Modos e Estilos de Jogo (Tela de NOVO JOGO)
    "choose_playstyle": "“Escolha seu estilo de jogo:”",
    "sur_mode_name": "Sobrevivência",
    "sur_mode_dsc": "Com munição e filtros escassos, combate mais letal e furtividade muito mais desafiadora, o estilo 'Sobrevivência' oferece aos jogadores a experiência original de survival horror do Metro 2033, com foco na gestão cuidadosa de recursos e confrontos tensos.",
    "acton_mode_name": "Espartano",
    "acton_mode_dsc": "Aproveite a experiência de combate e furtividade mais dinâmica de Metro: Last Light ao selecionar o estilo 'Espartano' – perfeito para jogadores que preferem um ritmo mais rápido e focado em ação. Munição, filtros e outros recursos são mais abundantes.",
    "standard_mode_dsc": "Recomendado para novos jogadores de Metro.<br><br>Se esta é sua primeira vez jogando, recomendamos selecionar o Modo Padrão.<br><br>Interface (HUD) e dicas no jogo estão ativadas, e a munição é abundante o suficiente para usar táticas de confronto direto.",
    "standard_mode_dsc_easy": "Recomendado para iniciantes em jogos de tiro.<br><br>O combate não será excessivamente desafiador, e munições e recursos são abundantes.",
    "standard_mode_dsc_normal": "Recomendado para jogadores regulares de jogos de tiro.<br><br>Você precisará gerenciar com cuidado seus suprimentos de munição e filtros, enfrentando cada situação de combate com cautela.",
    "standard_mode_dsc_hardcore": "Recomendado para jogadores experientes de jogos de tiro.<br><br>Cada confronto apresenta um teste sério às suas habilidades e táticas.<br><br>Munições e recursos devem ser rigorosamente preservados. O sucesso nunca é garantido…",
    "ranger_mode_dsc": "Um desafio único para veteranos do Metro.<br><br>Para os verdadeiros profissionais, o Modo Ranger força você a jogar sem interface (HUD) e sem dicas na tela.<br><br>O combate é implacável e os recursos são escassos.<br><br>Abordagem furtiva é altamente recomendada.",
    "ranger_mode_dsc_normal": "No Ranger Normal, a interface (HUD) é limitada e as dicas na tela são desativadas para imersão total.<br><br>Seus inimigos causam muito mais dano – mas você também! O combate é tenso, tático e brutal.<br><br>Recursos são ainda mais escassos – cada bala conta.",
    "ranger_mode_dsc_hardcore": "No Ranger Difícil, a interface (HUD), mira e dicas são completamente desativadas para a experiência mais imersiva de Metro, e a dificuldade é extrema em todos os aspectos.<br><br>Este é o desafio definitivo do Metro!",
    "ranger_mode_warning": "Neste modo, a interface (HUD), dicas e mira na tela são desativadas. A capacidade de munição é menor e os filtros duram menos tempo. Apenas duas armas principais podem ser carregadas simultaneamente, mas o jogador pode carregar até 10 facas de arremesso. Você começa com mais munição de padrão militar e ganha acesso a conquistas exclusivas deste modo. É possível escolher qualquer nível de dificuldade.",
    "ranger_mode_warning_ps3": "Neste modo, a interface (HUD), dicas e mira na tela são desativadas. A capacidade de munição é menor e os filtros duram menos tempo. Apenas duas armas principais podem ser carregadas simultaneamente, mas o jogador pode carregar até 10 facas de arremesso. Você começa com mais munição de padrão militar e ganha acesso a conquistas exclusivas deste modo. É possível escolher qualquer nível de dificuldade.",
    "ranger_mode_unavailable_dsc": "Você não possui o Modo Ranger instalado.<br><br>Acesse a loja Steam para baixar o conteúdo adicional do Modo Ranger.",

    # Vídeo e Gráficos complementares
    "$tesselation": "TESSELAÇÃO",
    "$video_contrast": "CONTRASTE",
    "$video_brightness": "BRILHO",
    "$texture_filtering": "FILTRAGEM DE TEXTURAS",
    "ssaa_off": "DESLIGADO",
    "ssaa_4x": "4X",
    "blur_normal": "NORMAL",

    # Áudio e Interface Geral
    "$sound": "SOM",
    "$extras": "EXTRAS",
    "$equipped": "EQUIPADO",
    "$stop": "PARAR",
    "$end": "FIM",
    "$delete": "EXCLUIR",
    "$add": "ADICIONAR",
    "$up": "CIMA",
    "$period": "PONTO",
    "$equals": "IGUAL",
    "$tab": "TAB",
    "$look": "Use o mouse para olhar ao redor.",
    "Copy of $look": "Use o mouse para olhar ao redor.",

    # Teclas Numéricas
    "$numpad0": "TECLADO NÚM. 0",
    "$numpad1": "TECLADO NÚM. 1",
    "$numpad2": "TECLADO NÚM. 2",
    "$numpad3": "TECLADO NÚM. 3",
    "$numpad4": "TECLADO NÚM. 4",
    "$numpad5": "TECLADO NÚM. 5",
    "$numpad6": "TECLADO NÚM. 6",
    "$numpad7": "TECLADO NÚM. 7",
    "$numpad8": "TECLADO NÚM. 8",
    "$numpad9": "TECLADO NÚM. 9",

    # Botões do controle Xbox / Gamepad
    "$x_start": "CONTROLE (START)",
    "$x_b": "CONTROLE (BOTÃO B)",
    "$x_a": "CONTROLE (BOTÃO A)",
    "$x_x": "CONTROLE (BOTÃO X)",
    "$x_y": "CONTROLE (BOTÃO Y)",
    "$x_rb": "CONTROLE (RB)",
    "$x_lb": "CONTROLE (LB)",
    "$x_rt": "CONTROLE (RT)",
    "$x_lt": "CONTROLE (LT)",

    # Nomes de Níveis no menu de Capítulos
    "$l02_exhibition": "EXPOSIÇÃO",
    "$l11_dry": "SECA",
    "$l14_cursed": "AMALDIÇOADA",
    "$l15_armory": "ARMARIA",
    "$l21_1": "Estação Negra",
    "$l21_task_1": "Estação Negra",
    "$l16_task_1": "Linha de Frente",
    "$l28_task_1": "Base dos Comandos",
    "l04_catacombs": "CATACUMBAS",
    "l07_tunnels_narration_NAME": "PERSEGUIÇÃO",
    "l03_camp_2": "INSTALAÇÃO",

    # Dicas e HUD
    "$gasmask_fast_hint": "<gasmask> Máscara de Gás",
    "$exchange_hint": "Você pode usar suas balas de padrão militar nos quiosques de troca para comprar mais munição para suas armas.",
    "change_filter": "TROCAR FILTRO",
    "$gp_filter": "TROCAR FILTRO",
    "$filter_name": "Filtro de máscara de gás",
    "inv_fastdrop": "SECUNDÁRIA",
    "hint_ingame_mask_xbox": "Pressione <gasmask> para colocar/tirar a máscara de gás. Pressione <filter> para trocar filtros.",
    "new_gasmask_hint": "Em muitos lugares, especialmente na superfície, é necessário usar máscara de gás. Se começar a sufocar, pressione <gasmask> para colocar a máscara. Para tirá-la, segure <gasmask>. Para verificar a duração dos filtros, olhe seu relógio segurando <time>.",
    "single_sign_on_later": "MAIS TARDE",
    "sso_email": "E-MAIL",
    "sso_birthdate": "DATA DE NASCIMENTO",
    "sso_existing": "EXISTENTE",
    "downloading": "BAIXANDO...",
}

for k, v in additions.items():
    expanded[k] = v

print(f"Total de traduções consolidadas: {len(expanded)}")

# Validar com a tabela da engine table_nl.json
with open('games/metro_2033_redux/data/table_nl.json', 'r', encoding='utf-8') as f:
    tbl_nl = json.load(f)

all_chars = set(''.join(expanded.values()))
missing = [c for c in all_chars if c not in tbl_nl]
print(f"Caracteres incompatíveis com a fonte da engine: {missing}")
assert len(missing) == 0, f"Caracteres incompatíveis encontrados: {missing}"

# Salvar dicionário expandido
with open('games/metro_2033_redux/menu_translations_ptbr.py', 'w', encoding='utf-8') as f:
    f.write('"""\nDicionário consolidado de traduções PT-BR para Menus, Opções, Modos e Interface do Metro 2033 Redux.\n"""\n\nMENU_TRANSLATIONS_PTBR = ')
    f.write(json.dumps(expanded, ensure_ascii=False, indent=4))
    f.write('\n')

print("Arquivo games/metro_2033_redux/menu_translations_ptbr.py atualizado com sucesso!")
