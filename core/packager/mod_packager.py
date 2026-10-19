"""
Empacotador e instalador de mods para o jogo.
Suporta instalação direta como loose files ou exportação de pacote de distribuição (.zip).
"""

import shutil
import zipfile
from pathlib import Path
from typing import List, Tuple

class ModPackager:
    def __init__(self, game_root: Path):
        self.game_root = Path(game_root)
        self.content_dir = self.game_root / "content"

    def install_loose_files(self, mod_source_dir: Path) -> List[Path]:
        """
        Instala os arquivos do mod diretamente na pasta content/ do jogo como loose files.
        O motor da 4A Games prioriza automaticamente arquivos soltos sobre os arquivos .vfs0!
        """
        installed = []
        mod_source_dir = Path(mod_source_dir)
        for src_path in mod_source_dir.rglob("*"):
            if src_path.is_file():
                rel_path = src_path.relative_to(mod_source_dir)
                dest_path = self.content_dir / rel_path
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_path, dest_path)
                installed.append(dest_path)
        return installed

    def uninstall_loose_files(self, mod_source_dir: Path) -> List[Path]:
        """Remove os arquivos do mod previamente instalados."""
        removed = []
        mod_source_dir = Path(mod_source_dir)
        for src_path in mod_source_dir.rglob("*"):
            if src_path.is_file():
                rel_path = src_path.relative_to(mod_source_dir)
                dest_path = self.content_dir / rel_path
                if dest_path.exists():
                    dest_path.unlink()
                    removed.append(dest_path)
        return removed

    def create_distribution_zip(self, mod_source_dir: Path, output_zip: Path):
        """Cria um pacote .zip para distribuição pública do mod com script de instalação automática."""
        output_zip.parent.mkdir(parents=True, exist_ok=True)
        mod_source_dir = Path(mod_source_dir)

        # Criar script de instalação bat para o usuário final
        bat_content = """@echo off
echo ======================================================
echo   MOD DE TRADUCAO E DUBLAGEM PT-BR - METRO 2033 REDUX
echo   Desenvolvido com o framework narracao-pt-br
echo ======================================================
echo.
echo Copiando arquivos para a pasta do jogo...
xcopy /E /Y /I content "%~dp0\\content"
echo.
echo Mod instalado com sucesso! Inicie o jogo normalmente.
pause
"""
        with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file_path in mod_source_dir.rglob("*"):
                if file_path.is_file():
                    arcname = f"content/{file_path.relative_to(mod_source_dir)}"
                    zf.write(file_path, arcname=arcname)
            zf.writestr("instalar_mod.bat", bat_content)
