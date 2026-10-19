"""
Motor de Síntese de Voz (TTS) para dublagem de jogos.
Suporta síntese neural multi-personagem, controle de tom/velocidade e pós-processamento de áudio.
"""

import asyncio
from pathlib import Path
from typing import Dict, Any, Optional
import edge_tts
from core.dubbing.audio_dsp import AudioProcessor

class TTSEngine:
    def __init__(self, voice_configs: Dict[str, Any]):
        self.voice_configs = voice_configs
        self.processor = AudioProcessor()

    async def synthesize(
        self,
        text: str,
        character_key: str,
        output_vba_path: Path,
        target_max_duration: Optional[float] = None,
        custom_effect: Optional[str] = None
    ) -> Path:
        """
        Sintetiza uma fala de personagem em português e converte para o formato de áudio do jogo (.vba).
        """
        char_conf = self.voice_configs.get(character_key, self.voice_configs.get("default_male", {}))
        voice_name = char_conf.get("voice", "pt-BR-AntonioNeural")
        rate = char_conf.get("rate", "+0%")
        if not rate.startswith(("+", "-")):
            rate = f"+{rate}"
        pitch = char_conf.get("pitch", "+0Hz")
        if not pitch.startswith(("+", "-")):
            pitch = f"+{pitch}"
        effect = custom_effect if custom_effect is not None else char_conf.get("effect")

        # Arquivo temporário intermediário
        temp_mp3 = output_vba_path.with_suffix(".temp.mp3")
        temp_mp3.parent.mkdir(parents=True, exist_ok=True)

        # Síntese neural
        communicate = edge_tts.Communicate(text, voice_name, rate=rate, pitch=pitch)
        await communicate.save(str(temp_mp3))

        # Pós-processamento DSP e conversão para o formato do jogo
        self.processor.process_voice_line(
            input_file=temp_mp3,
            output_file=output_vba_path,
            target_sample_rate=44100,
            channels=1,
            bitrate="64k",
            target_max_duration=target_max_duration,
            effect=effect
        )

        # Limpeza do temporário
        if temp_mp3.exists():
            temp_mp3.unlink()

        return output_vba_path

    def synthesize_sync(self, *args, **kwargs) -> Path:
        return asyncio.run(self.synthesize(*args, **kwargs))
