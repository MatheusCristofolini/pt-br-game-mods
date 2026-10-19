"""
Script simples para checar o status e progresso da tradução do Metro 2033 Redux.
Pode ser executado a qualquer momento no terminal com:
    python status_traducao.py
"""

import json
import sys
from pathlib import Path

# Configura saída UTF-8 para o terminal
sys.stdout.reconfigure(encoding='utf-8')

JSON_FILE = Path("workspace/traducao/textos_completos_jogo.json")

def verificar_progresso():
    if not JSON_FILE.exists():
        print(f"Erro: Arquivo {JSON_FILE} não encontrado.")
        return

    print("=" * 60)
    print("📊 STATUS DA TRADUÇÃO - METRO 2033 REDUX")
    print("=" * 60)

    with open(JSON_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    total = len(data)
    traduzidos = 0
    categorias = {
        "História / Campanha (2033)": {"total": 0, "pronto": 0},
        "Falas / NPCs / Combate (Voices)": {"total": 0, "pronto": 0},
        "Interface / Menus / Diários (Outros)": {"total": 0, "pronto": 0}
    }

    for k, v in data.items():
        is_done = bool(v.get("traducao_ptbr") and v["traducao_ptbr"].strip())
        if is_done:
            traduzidos += 1

        if k.startswith("2033"):
            cat = "História / Campanha (2033)"
        elif k.startswith("voices"):
            cat = "Falas / NPCs / Combate (Voices)"
        else:
            cat = "Interface / Menus / Diários (Outros)"

        categorias[cat]["total"] += 1
        if is_done:
            categorias[cat]["pronto"] += 1

    pct = (traduzidos / total) * 100 if total > 0 else 0

    # Barra visual de progresso
    bar_len = 30
    filled = int(bar_len * (traduzidos / total)) if total > 0 else 0
    bar = "█" * filled + "░" * (bar_len - filled)

    print(f"\nProgresso Geral: [{bar}] {pct:.2f}%\n")
    print(f"  • Total de textos:      {total:,}")
    print(f"  • Já traduzidos:        {traduzidos:,}")
    print(f"  • Faltam:               {total - traduzidos:,}\n")

    print("Detalhamento por Área:")
    for nome, stat in categorias.items():
        cat_pct = (stat["pronto"] / stat["total"]) * 100 if stat["total"] > 0 else 0
        print(f"  - {nome:<38}: {stat['pronto']:>5} / {stat['total']:<5} ({cat_pct:>5.1f}%)")

    print("\n" + "=" * 60)
    if traduzidos == total:
        print("🎉 TRADUÇÃO COMPLETA! Você já pode rodar:")
        print("    python aplicar_traducao.py")
    else:
        print("💡 Para aplicar os textos que já estão prontos no jogo agora:")
        print("    python aplicar_traducao.py")
    print("=" * 60)

if __name__ == "__main__":
    verificar_progresso()
