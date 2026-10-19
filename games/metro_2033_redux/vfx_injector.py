"""
Injetor de arquivos no Virtual File System (VFX/VFS) do Metro 2033 Redux.
Permite criar um pacote de mod (ex: content99.vfs0) e registrar/redirecionar arquivos no content.vfx.
"""

import shutil
import struct
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import lz4.block

from games.metro_2033_redux.vfx_unpacker import VFXReader

class VFXInjector:
    def __init__(self, vfx_path: Path):
        self.vfx_path = Path(vfx_path)
        self.base_dir = self.vfx_path.parent
        self.reader = VFXReader(self.vfx_path)
        self.reader.load()

    def create_vfs_package(self, files_dict: Dict[str, bytes], vfs_filename: str = "content99.vfs0") -> Tuple[Path, Dict[str, Tuple[int, int, int]]]:
        """
        Cria um arquivo .vfs0 contendo os arquivos fornecidos em raw uncompressed.
        Retorna o caminho do .vfs0 e um dicionario {nome: (offset, size_u, size_c)}.
        """
        vfs_path = self.base_dir / vfs_filename
        offsets = {}
        current_offset = 0

        with open(vfs_path, "wb") as f:
            for name, data in files_dict.items():
                size = len(data)
                f.write(data)
                offsets[name] = (current_offset, size, size)
                current_offset += size

        return vfs_path, offsets

    def inject_mod_package(
        self,
        files_to_replace: Dict[str, bytes],
        mod_pak_name: str = "content99.vfs0",
        output_vfx_path: Optional[Path] = None
    ) -> Path:
        """
        Gera um content99.vfs0 e um novo content.vfx com os arquivos redirecionados.
        """
        if output_vfx_path is None:
            output_vfx_path = self.vfx_path

        # 1. Criar o pacote content99.vfs0
        vfs_path, file_offsets = self.create_vfs_package(files_to_replace, mod_pak_name)
        vfs_size = vfs_path.stat().st_size

        # 2. Ler os bytes brutos do VFX original
        with open(self.vfx_path, "rb") as f:
            vfx_raw = f.read()

        # Desempacotar cabeçalho original
        version, compression = struct.unpack_from("<II", vfx_raw, 0)
        guid = vfx_raw[8:24]
        num_paks, num_files, unknown_0 = struct.unpack_from("<III", vfx_raw, 24)

        # Reconstruir seção de pacotes
        # Lê a lista de paks existentes
        paks_data = bytearray()
        pos = 36
        for _ in range(num_paks):
            # Ler pak original
            start_pak = pos
            while vfx_raw[pos] != 0:
                pos += 1
            pos += 1 # nulo
            n_strings = struct.unpack_from("<I", vfx_raw, pos)[0]
            pos += 4
            for _ in range(n_strings):
                while vfx_raw[pos] != 0:
                    pos += 1
                pos += 1
            pos += 4 # size
            paks_data.extend(vfx_raw[start_pak:pos])

        # Adicionar o novo pak ao final da lista de paks
        new_pak_idx = num_paks
        new_pak_bytes = bytearray()
        new_pak_bytes.extend(mod_pak_name.encode("utf-8") + b"\x00")
        new_pak_bytes.extend(struct.pack("<I", 0)) # 0 strings de levels
        new_pak_bytes.extend(struct.pack("<I", vfs_size)) # tamanho do vfs
        paks_data.extend(new_pak_bytes)

        # 3. Ler e atualizar os inodes
        inodes_data = bytearray()
        for idx in range(num_files):
            flags = struct.unpack_from("<H", vfx_raw, pos)[0]
            is_dir = (flags & 8) != 0

            if is_dir:
                # Diretório: 2 (flags) + 2 (n_children) + 4 (first_child) = 8 bytes
                start_dir = pos
                pos += 8
                # Nome xored: 2 bytes header + (s_len-1) + 1 byte nulo
                h = struct.unpack_from("<H", vfx_raw, pos)[0]
                s_len = h & 0xFF
                name_bytes_len = (s_len - 1) if s_len > 1 else 0
                pos += 2 + name_bytes_len + 1
                inodes_data.extend(vfx_raw[start_dir:pos])
            else:
                # Arquivo: 2 (flags) + 2 (pak_idx) + 4 (offset) + 4 (sz_u) + 4 (sz_c) = 16 bytes
                start_file = pos
                pak_idx, offset, sz_u, sz_c = struct.unpack_from("<HIII", vfx_raw, pos + 2)
                pos += 16
                h = struct.unpack_from("<H", vfx_raw, pos)[0]
                s_len = h & 0xFF
                xor_mask = (h >> 8) & 0xFF
                name_len = max(0, s_len - 1)
                raw_name = vfx_raw[pos+2 : pos+2+name_len]
                pos += 2 + name_len + 1 # consome header + string + nulo
                decoded_name = bytes([b ^ xor_mask for b in raw_name]).decode("utf-8", errors="ignore")

                # Checar se este arquivo deve ser substituído pelo mod (por nome, caminho ou índice)
                target_key = None
                for k in file_offsets:
                    if k == decoded_name or k.endswith("/" + decoded_name) or k == str(idx):
                        target_key = k
                        break

                if target_key:
                    new_offset, new_sz_u, new_sz_c = file_offsets[target_key]
                    # Grava flags originais
                    inodes_data.extend(struct.pack("<H", flags))
                    # Grava novo pak_idx, novo offset, novo sz_u, novo sz_c (raw uncompressed)
                    inodes_data.extend(struct.pack("<HIII", new_pak_idx, new_offset, new_sz_u, new_sz_c))
                    # Grava o nome xored original intacto
                    inodes_data.extend(vfx_raw[start_file + 16 : pos])
                else:
                    inodes_data.extend(vfx_raw[start_file:pos])

        # 4. Preservar a seção final (tail / tabela de hash e blocos)
        tail_data = vfx_raw[pos:]

        # 5. Gravar novo VFX completo
        with open(output_vfx_path, "wb") as f:
            f.write(struct.pack("<II", version, compression))
            f.write(guid)
            f.write(struct.pack("<III", num_paks + 1, num_files, unknown_0))
            f.write(paks_data)
            f.write(inodes_data)
            f.write(tail_data)

        return output_vfx_path

