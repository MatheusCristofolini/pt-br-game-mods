"""
Processamento de sinal de áudio (DSP) para dublagens de jogos.
Converte formatos, ajusta durações e aplica efeitos imersivos (rádio, máscara de gás, túnel).
"""

import subprocess
import shutil
from pathlib import Path
from typing import Optional

def get_ffmpeg_path() -> str:
    """Retorna o executável do ffmpeg."""
    path = shutil.which("ffmpeg")
    if path:
        return path
    # Checagem em caminhos padrão do Winget
    winget_paths = list(Path.home().glob("AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg*/**/ffmpeg.exe"))
    if winget_paths:
        return str(winget_paths[0])
    return "ffmpeg"

def get_ffprobe_path() -> str:
    """Retorna o executável do ffprobe."""
    path = shutil.which("ffprobe")
    if path:
        return path
    winget_paths = list(Path.home().glob("AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg*/**/ffprobe.exe"))
    if winget_paths:
        return str(winget_paths[0])
    return "ffprobe"

def get_audio_duration(file_path: Path) -> float:
    """Retorna a duração em segundos de um arquivo de áudio usando ffprobe."""
    ffprobe = get_ffprobe_path()
    cmd = [
        ffprobe, "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(file_path)
    ]
    try:
        output = subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL).strip()
        return float(output)
    except Exception:
        return 0.0

class AudioProcessor:
    def __init__(self):
        self.ffmpeg = get_ffmpeg_path()

    def process_voice_line(
        self,
        input_file: Path,
        output_file: Path,
        target_sample_rate: int = 44100,
        channels: int = 1,
        bitrate: str = "64k",
        target_max_duration: Optional[float] = None,
        effect: Optional[str] = None
    ) -> Path:
        """
        Processa e converte o áudio sintetizado para o padrão do motor do jogo (ex: Vorbis .vba).
        
        Efeitos suportados:
        - 'radio': Filtro de rádio/walkie-talkie militar (bandpass 300-3400Hz).
        - 'gasmask': Filtro abafado de máscara de gás (lowpass 1800Hz + boost nos médios-graves).
        - 'tunnel': Leve reverberação de túnel subterrâneo.
        - None: Voz limpa normal.
        """
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Filtros de áudio
        filters = []

        # Ajuste de velocidade se necessário (tempo-stretch sem mudar o tom)
        current_dur = get_audio_duration(input_file)
        if target_max_duration and current_dur > target_max_duration and current_dur > 0:
            speed_ratio = current_dur / target_max_duration
            # Limita a aceleração a no máximo 1.4x para não soar artificial
            speed_ratio = min(speed_ratio, 1.4)
            if speed_ratio > 1.05:
                filters.append(f"atempo={speed_ratio:.3f}")

        # Efeitos atmosféricos de Metro
        if effect == "radio":
            filters.append("highpass=f=300,lowpass=f=3400,volume=1.2")
        elif effect == "gasmask":
            filters.append("lowpass=f=1900,equalizer=f=350:t=q:w=1:g=3")
        elif effect == "tunnel":
            filters.append("aecho=0.8:0.88:40:0.4")

        # Normalização de volume
        filters.append("loudnorm=I=-16:TP=-1.5:LRA=11")

        filter_str = ",".join(filters)

        cmd = [
            self.ffmpeg, "-y",
            "-i", str(input_file),
            "-ar", str(target_sample_rate),
            "-ac", str(channels),
            "-c:a", "libvorbis",
            "-b:a", bitrate
        ]

        if filter_str:
            cmd.extend(["-af", filter_str])

        if str(output_file).endswith(".vba") or str(output_file).endswith(".ogg"):
            cmd.extend(["-f", "ogg"])

        cmd.append(str(output_file))

        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return output_file
