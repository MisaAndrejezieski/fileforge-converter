"""
Conversor de vídeo usando FFmpeg.

Tenta usar o FFmpeg do sistema primeiro (mais novo e rápido).
Se não encontrar, usa o FFmpeg embutido do imageio-ffmpeg.
"""

import subprocess
import sys
from pathlib import Path


class ConversorVideo:
    """Converte vídeos usando FFmpeg."""

    FORMATOS_ENTRADA = {'mp4', 'mov', 'avi', 'mkv', 'webm', 'flv', 'wmv', 'm4v', '3gp'}
    FORMATOS_SAIDA = {'webm', 'mp4', 'gif'}

    def __init__(self, crf: int = 35, preset: str = "good"):
        self.crf = crf
        self.preset = preset
        self.ffmpeg_path = self._encontrar_ffmpeg()

    def _encontrar_ffmpeg(self) -> str:
        # 1. Tenta o FFmpeg do sistema (PATH)
        try:
            subprocess.run(
                ["ffmpeg", "-version"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True
            )
            return "ffmpeg"
        except (FileNotFoundError, subprocess.CalledProcessError):
            pass

        # 2. Fallback: FFmpeg embutido do imageio-ffmpeg
        try:
            import imageio_ffmpeg
            return imageio_ffmpeg.get_ffmpeg_exe()
        except ImportError:
            raise RuntimeError(
                "FFmpeg não encontrado. Instale com:\n"
                "  pip install imageio-ffmpeg\n"
                "Ou adicione o FFmpeg do sistema ao PATH."
            )

    def converter(self, entrada: str, saida: str) -> str:
        ext_saida = Path(saida).suffix.lstrip('.').lower()

        if ext_saida == 'webm':
            return self._para_webm(entrada, saida)
        elif ext_saida == 'mp4':
            return self._para_mp4(entrada, saida)
        elif ext_saida == 'gif':
            return self._para_gif(entrada, saida)
        else:
            raise ValueError(f"Formato de vídeo não suportado: {ext_saida}")

    def _para_webm(self, entrada: str, saida: str) -> str:
        cmd = [
            self.ffmpeg_path, "-y",
            "-i", str(entrada),
            "-c:v", "libvpx-vp9",
            "-crf", str(self.crf),
            "-b:v", "0",
            "-deadline", self.preset,
            "-cpu-used", "2",
            "-an",
            str(saida)
        ]
        self._executar(cmd, entrada, saida)
        return saida

    def _para_mp4(self, entrada: str, saida: str) -> str:
        cmd = [
            self.ffmpeg_path, "-y",
            "-i", str(entrada),
            "-c:v", "libx264",
            "-crf", str(self.crf),
            "-preset", "medium",
            "-an",
            str(saida)
        ]
        self._executar(cmd, entrada, saida)
        return saida

    def _para_gif(self, entrada: str, saida: str) -> str:
        cmd = [
            self.ffmpeg_path, "-y",
            "-i", str(entrada),
            "-vf", "fps=15,scale=480:-1:flags=lanczos",
            "-loop", "0",
            str(saida)
        ]
        self._executar(cmd, entrada, saida)
        return saida

    def _executar(self, cmd: list, entrada: str, saida: str):
        flags = subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
        try:
            subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                creationflags=flags
            )
        except subprocess.CalledProcessError as e:
            erro = e.stderr.decode('utf-8', errors='ignore')
            linhas = erro.strip().split('\n')
            ultimas = '\n'.join(linhas[-5:])
            raise RuntimeError(f"FFmpeg falhou:\n{ultimas}")

        if not Path(saida).exists():
            raise RuntimeError(f"FFmpeg não gerou o arquivo: {saida}")