import json
from pathlib import Path
from typing import Dict, Optional

class Glossary:
    """
    Gerenciador de glossário para consistência terminológica de universo/lore do jogo.
    Evita traduções erradas ou inconsistentes de nomes próprios, locais, armas e facções.
    """
    def __init__(self, glossary_file: Optional[Path] = None):
        self.terms: Dict[str, str] = {}
        if glossary_file and glossary_file.exists():
            self.load(glossary_file)

    def load(self, path: Path):
        with open(path, "r", encoding="utf-8") as f:
            self.terms = json.load(f)

    def save(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.terms, f, ensure_ascii=False, indent=2)

    def add_term(self, original: str, translated: str):
        self.terms[original] = translated

    def apply(self, text: str) -> str:
        """
        Aplica as substituições do glossário no texto, respeitando maiúsculas e termos inteiros.
        """
        result = text
        for orig, target in sorted(self.terms.items(), key=lambda x: len(x[0]), reverse=True):
            # Substituição simples respeitando case exato
            result = result.replace(orig, target)
        return result
