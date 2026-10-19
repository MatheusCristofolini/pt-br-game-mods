"""
Ferramenta para descompactar e compactar arquivos de localização (.lng) da 4A Engine (Metro 2033 Redux).
Permite exportar todas as legendas e textos para JSON/TXT e recompilar para .lng.
"""

import json
import struct
from pathlib import Path
from typing import Dict, List, Optional, Tuple

MAGIC = 0x0000000400000000
UNK1  = 0x0000000100000000
UNK2  = 0x00000002

class LNGTool:
    @staticmethod
    def read_to_null(f) -> bytes:
        res = bytearray()
        while True:
            b = f.read(1)
            if not b or b == b'\x00':
                break
            res.extend(b)
        return bytes(res)

    @classmethod
    def unpack(cls, lng_file: Path) -> Dict[str, str]:
        """Lê um arquivo .lng binário e retorna um dicionário chave -> texto traduzido."""
        with open(lng_file, 'rb') as f:
            magic = struct.unpack('<Q', f.read(8))[0]
            unk1 = struct.unpack('<Q', f.read(8))[0]
            ch_tbl_size = struct.unpack('<I', f.read(4))[0]
            ch_count = ch_tbl_size // 2
            ch_table = [chr(struct.unpack('<H', f.read(2))[0]) for _ in range(ch_count)]
            unk2 = struct.unpack('<I', f.read(4))[0]
            str_tbl_size = struct.unpack('<I', f.read(4))[0]

            def decode_val(buf: bytes, table: List[str]) -> str:
                res = []
                i = 0
                while i < len(buf):
                    b = buf[i]
                    if (b & 0xE0) == 0xE0:
                        page = b & 0x0F
                        offset = buf[i + 1]
                        idx = 223 + (255 * page) + offset
                        if idx < len(table):
                            res.append(table[idx])
                        else:
                            res.append('?')
                        i += 2
                    else:
                        res.append(table[b])
                        i += 1
                return ''.join(res)

            entries = {}
            bytes_read = 0
            while bytes_read < str_tbl_size:
                raw_key = cls.read_to_null(f)
                bytes_read += len(raw_key) + 1
                raw_val = cls.read_to_null(f)
                bytes_read += len(raw_val) + 1

                key = raw_key.decode('ascii', errors='ignore')
                val = decode_val(raw_val, ch_table)
                entries[key] = val

            return entries

    @classmethod
    def export_json(cls, lng_file: Path, output_json: Path) -> Dict[str, str]:
        entries = cls.unpack(lng_file)
        output_json.parent.mkdir(parents=True, exist_ok=True)
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(entries, f, ensure_ascii=False, indent=2)
        return entries

    @classmethod
    def get_char_table(cls, lng_file: Path) -> List[str]:
        """Extrai a tabela de caracteres oficial de um arquivo .lng binário."""
        with open(lng_file, 'rb') as f:
            f.seek(16)
            ch_tbl_size = struct.unpack('<I', f.read(4))[0]
            ch_count = ch_tbl_size // 2
            return [chr(struct.unpack('<H', f.read(2))[0]) for _ in range(ch_count)]

    @classmethod
    def pack(
        cls,
        entries: Dict[str, str],
        output_lng: Path,
        base_table: Optional[List[str]] = None,
        reference_lng: Optional[Path] = None
    ):
        """
        Compila um dicionário de textos de volta para o formato .lng binário.
        Preserva rigorosamente a tabela de caracteres da engine para compatibilidade total.
        """
        if reference_lng and Path(reference_lng).exists():
            base_table = cls.get_char_table(Path(reference_lng))
        elif base_table is None:
            data_dir = Path(__file__).parent / "data"
            ref_path = data_dir / "table_us.json"
            if not ref_path.exists():
                ref_path = Path("workspace/extracted/localization/table_us.json")
            if ref_path.exists():
                with open(ref_path, "r", encoding="utf-8") as f:
                    base_table = json.load(f)

        ch_map: Dict[str, int] = {}
        ch_list: List[str] = []
        if base_table:
            for ch in base_table:
                if ch not in ch_map:
                    ch_map[ch] = len(ch_list)
                    ch_list.append(ch)

        # Adicionar novos caracteres estritamente no final, sem deslocar os originais
        for text in entries.values():
            for ch in text:
                if ch not in ch_map:
                    ch_map[ch] = len(ch_list)
                    ch_list.append(ch)

        # 2. Codificar todos os pares (chave, valor)
        encoded_data = bytearray()
        for key, text in entries.items():
            # Chave em ASCII nulo-terminada
            encoded_data.extend(key.encode('ascii', errors='ignore'))
            encoded_data.append(0x00)

            # Valor codificado com a tabela
            val_bytes = bytearray()
            for ch in text:
                idx = ch_map[ch]
                if idx < 223:
                    val_bytes.append(idx)
                else:
                    adj = idx - 223
                    page = (adj // 255) & 0x0F
                    offset = adj % 255
                    val_bytes.append(0xE0 | page)
                    val_bytes.append(offset)
            val_bytes.append(0x00)  # nulo terminal do valor
            encoded_data.extend(val_bytes)

        # 3. Gravar arquivo binário
        output_lng.parent.mkdir(parents=True, exist_ok=True)
        with open(output_lng, 'wb') as f:
            f.write(struct.pack('<Q', MAGIC))
            f.write(struct.pack('<Q', UNK1))

            ch_tbl_bytes = bytearray()
            for ch in ch_list:
                ch_tbl_bytes.extend(struct.pack('<H', ord(ch)))
            f.write(struct.pack('<I', len(ch_tbl_bytes)))
            f.write(ch_tbl_bytes)

            f.write(struct.pack('<I', UNK2))
            f.write(struct.pack('<I', len(encoded_data)))
            f.write(encoded_data)
