"""
Voice Caster: Mapeia caminhos de arquivos de áudio do jogo para personagens e atores de voz correspondentes.
"""

from typing import List, Dict, Any

class VoiceCaster:
    def __init__(self, rules: List[Dict[str, str]], default_character: str = "default_male"):
        self.rules = rules
        self.default_character = default_character

    def resolve_character(self, audio_path: str) -> str:
        """Determina qual personagem está falando baseado na chave/caminho do arquivo."""
        path_lower = audio_path.lower().replace('\\', '/')
        for rule in self.rules:
            pattern = rule["pattern"].lower()
            if pattern in path_lower:
                return rule["character"]
        return self.default_character
