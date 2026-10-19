"""
Motor de tradução de legendas e textos de jogos.
Respeita tags de formatação do motor (<time=...>, códigos de escape, variáveis) e aplica glossário.
"""

import re
from typing import Dict, Optional, Callable
from core.translation.glossary import Glossary

class GameTranslator:
    def __init__(self, glossary: Optional[Glossary] = None):
        self.glossary = glossary or Glossary()

    def translate_text(self, text: str, translate_fn: Optional[Callable[[str], str]] = None) -> str:
        """
        Traduz o texto preservando tags temporais como <time=1234> e placeholders.
        Se translate_fn não for fornecido, aplica o glossário diretamente.
        """
        if not text or not text.strip():
            return text

        # Extrair e proteger tags <time=...>
        time_tag_pattern = re.compile(r'(<time=\d+>)')
        parts = time_tag_pattern.split(text)

        translated_parts = []
        for part in parts:
            if time_tag_pattern.match(part):
                # Mantém a tag intacta
                translated_parts.append(part)
            else:
                # Traduz o segmento de texto
                seg = part
                if translate_fn and seg.strip():
                    seg = translate_fn(seg)
                # Aplica termos canônicos do glossário
                seg = self.glossary.apply(seg)
                translated_parts.append(seg)

        return "".join(translated_parts)

    def translate_dictionary(
        self,
        source_dict: Dict[str, str],
        translate_fn: Optional[Callable[[str], str]] = None
    ) -> Dict[str, str]:
        """Traduz um dicionário completo de chaves -> textos."""
        result = {}
        for key, text in source_dict.items():
            result[key] = self.translate_text(text, translate_fn=translate_fn)
        return result
