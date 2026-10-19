"""
Extrator nativo de arquivos de Metro 2033 Redux (.vfx e .vfs0).
Lê a tabela de índices e extrai arquivos individuais (textos, áudios, etc.) ou em lote.
"""

import os
import struct
from pathlib import Path
from typing import Dict, List, Optional
import lz4.block

class MetroFileEntry:
    def __init__(self, idx: int, flags: int, is_dir: bool, name: str):
        self.idx = idx
        self.flags = flags
        self.is_dir = is_dir
        self.name = name
        
        # Arquivo
        self.pak_idx: int = 0
        self.offset: int = 0
        self.size_uncompressed: int = 0
        self.size_compressed: int = 0
        
        # Diretório
        self.num_children: int = 0
        self.first_child_idx: int = 0

        # Caminho completo resolvido
        self.full_path: str = ""

    def __repr__(self):
        type_str = "DIR" if self.is_dir else "FILE"
        return f"<{type_str} {self.full_path} (uncompressed={self.size_uncompressed})>"

class VFXReader:
    def __init__(self, vfx_path: Path):
        self.vfx_path = Path(vfx_path)
        self.base_dir = self.vfx_path.parent
        self.paks: List[str] = []
        self.entries: List[MetroFileEntry] = []
        self.path_map: Dict[str, MetroFileEntry] = {}

    def _read_string_z(self, f) -> str:
        chars = bytearray()
        while True:
            b = f.read(1)
            if not b or b == b'\x00':
                break
            chars.extend(b)
        return chars.decode('utf-8', errors='ignore')

    def _read_xored_string(self, f) -> str:
        raw_header = f.read(2)
        if len(raw_header) < 2:
            return ""
        header = struct.unpack('<H', raw_header)[0]
        string_len = header & 0xFF
        xor_mask = (header >> 8) & 0xFF
        if string_len <= 1:
            f.read(1)  # lê byte nulo final
            return ""
        raw_bytes = f.read(string_len - 1)
        f.read(1)      # lê byte nulo final
        decoded = bytes([b ^ xor_mask for b in raw_bytes])
        return decoded.decode('utf-8', errors='ignore')

    def load(self):
        with open(self.vfx_path, 'rb') as f:
            version, compression = struct.unpack('<II', f.read(8))
            guid = f.read(16)
            num_paks, num_files, unknown_0 = struct.unpack('<III', f.read(12))

            # Carregar pacotes (.vfs0)
            self.paks = []
            for _ in range(num_paks):
                pak_name = self._read_string_z(f)
                num_strings = struct.unpack('<I', f.read(4))[0]
                for _ in range(num_strings):
                    self._read_string_z(f)
                chunk = struct.unpack('<I', f.read(4))[0]
                self.paks.append(pak_name)

            # Carregar inodes / arquivos
            self.entries = []
            for idx in range(num_files):
                flags = struct.unpack('<H', f.read(2))[0]
                is_dir = (flags & 8) != 0

                if not is_dir:
                    pak_idx, offset, size_uncompressed, size_compressed = struct.unpack('<HIII', f.read(14))
                    name = self._read_xored_string(f)
                    entry = MetroFileEntry(idx, flags, is_dir=False, name=name)
                    entry.pak_idx = pak_idx
                    entry.offset = offset
                    entry.size_uncompressed = size_uncompressed
                    entry.size_compressed = size_compressed
                else:
                    num_children, first_child_idx = struct.unpack('<HI', f.read(6))
                    name = self._read_xored_string(f)
                    entry = MetroFileEntry(idx, flags, is_dir=True, name=name)
                    entry.num_children = num_children
                    entry.first_child_idx = first_child_idx

                self.entries.append(entry)

        self._resolve_paths()

    def _resolve_paths(self):
        """Reconstrói a árvore de diretórios e mapeia caminhos completos."""
        if not self.entries:
            return

        def walk(entry: MetroFileEntry, current_dir: str):
            for i in range(entry.first_child_idx, entry.first_child_idx + entry.num_children):
                if i >= len(self.entries):
                    break
                child = self.entries[i]
                child_path = f"{current_dir}/{child.name}".strip("/")
                child.full_path = child_path
                self.path_map[child_path.lower()] = child
                if child.is_dir:
                    walk(child, child_path)

        root = self.entries[0]
        root.full_path = ""
        walk(root, "")

    def find_files(self, pattern: str) -> List[MetroFileEntry]:
        """Busca arquivos por padrão (case-insensitive)."""
        pattern_lower = pattern.lower().replace('\\', '/')
        matches = []
        for path_lower, entry in self.path_map.items():
            if not entry.is_dir and pattern_lower in path_lower:
                matches.append(entry)
        return matches

    def extract_file(self, entry: MetroFileEntry, output_path: Optional[Path] = None) -> bytes:
        """Descomprime e extrai um arquivo específico da respectiva archive .vfs0."""
        if entry.is_dir:
            raise ValueError(f"{entry.full_path} é um diretório, não um arquivo.")

        pak_name = self.paks[entry.pak_idx]
        pak_path = self.base_dir / pak_name

        if not pak_path.exists():
            raise FileNotFoundError(f"Arquivo VFS {pak_path} não encontrado.")

        with open(pak_path, 'rb') as f:
            f.seek(entry.offset)
            compressed_bytes = f.read(entry.size_compressed)

        if entry.size_compressed == entry.size_uncompressed:
            uncompressed = compressed_bytes
        else:
            uncompressed = bytearray()
            pos = 0
            while pos < len(compressed_bytes):
                block_size, block_uncompressed_size = struct.unpack('<II', compressed_bytes[pos:pos+8])
                pos += 8
                payload_size = block_size - 8
                block_payload = compressed_bytes[pos:pos+payload_size]
                pos += payload_size

                dict_buf = bytes(uncompressed[-65536:]) if len(uncompressed) > 0 else b""
                decompressed_block = lz4.block.decompress(
                    block_payload,
                    uncompressed_size=block_uncompressed_size,
                    dict=dict_buf
                )
                uncompressed.extend(decompressed_block)

        data = bytes(uncompressed)
        if output_path:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'wb') as out_f:
                out_f.write(data)

        return data
