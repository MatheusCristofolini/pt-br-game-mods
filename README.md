# PT-BR Game Mods (Tradução e Narração em Português)

Framework modular para criação de mods de localização, tradução e dublagem/narração em Português do Brasil (PT-BR) para jogos de PC.

---

## 🎮 Jogos Suportados

### 1. Metro 2033 Redux (4A Engine)
- **Status Atual:** 
  - [x] Extração e descompressão completa do formato de pacotes nativos (`.vfx` e `.vfs0` LZ4 em streaming).
  - [x] Compilador e descompilador de arquivos de texto/legendas (`.lng` Huffman/tabela de caracteres) com preservação de acentuação e integridade de fontes.
  - [x] Injeção dinâmica no Virtual File System (VFS) com pacote isolado (`content99.vfs0`), preservando tabelas de hash e streaming da 4A Engine.
  - [x] Adição do idioma **"Português (BR)"** no menu nativo de opções sem sobrescrever nenhum dos 10 idiomas originais do jogo (English, Russian, Español, Deutsch, Français, Italiano, Nederlands, Polski, Čeština, Українська).
  - [x] Tradução funcional do Menu Principal e Menus de Configurações.
  - [x] Pipeline de áudio DSP (reverberação de túnel, rádio, máscara de gás) e conversão para `.vba` (Ogg Vorbis 44.1 kHz).

---

## 🏗️ Arquitetura do Projeto

```text
├── core/
│   ├── dubbing/            # Pipeline de dublagem e áudio
│   │   ├── audio_dsp.py    # Efeitos de áudio (rádio, máscara, reverberação de metrô)
│   │   ├── tts_engine.py   # Síntese neural de voz e alinhamento de duração
│   │   └── voice_caster.py # Atribuição de vozes aos personagens
│   ├── packager/           # Empacotadores genéricos de mods
│   └── translation/        # Glossários e tradutores
├── games/
│   └── metro_2033_redux/   # Suporte nativo ao Metro 2033 Redux
│       ├── data/           # Tabelas oficiais de caracteres e fontes da engine
│       ├── characters.yaml # Mapeamento de personagens e casting de vozes
│       ├── config.yaml     # Configurações do jogo
│       ├── glossary_ptbr.json # Glossário de lore e termos do Metro
│       ├── lng_tool.py     # Compilador e descompilador de .lng (4A Engine)
│       ├── vfx_injector.py # Injetor de pacotes VFS e recompilador de content.vfx
│       └── vfx_unpacker.py # Leitor e extrator nativo de .vfx / .vfs0
├── build_language_test.py  # Script de compilação e teste do seletor de idioma PT-BR
├── cli.py                  # Interface de linha de comando unificada
├── config.yaml             # Configuração global do framework
└── requirements.txt        # Dependências Python
```

---

## 🚀 Como Executar

### Pré-requisitos
- Python 3.10+
- FFmpeg instalado no sistema e acessível no PATH

### Instalação
```bash
# Criar e ativar ambiente virtual
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell

# Instalar dependências
pip install -r requirements.txt
```

### Testar a Localização no Metro 2033 Redux
Para gerar o pacote de mod e injetar a opção de **Português (BR)** no jogo:
```bash
python build_language_test.py
```
Abra o jogo pela Steam, vá em **Opções** -> **Jogo** -> **Idioma do Texto** e selecione **Português (BR)**.

---

## 🛠️ Tecnologias Utilizadas
- **Python 3.12**
- **lz4** (Descompressão e streaming de blocos VFS da 4A Engine)
- **pydub** & **scipy** (DSP e processamento de sinal acústico)
- **edge-tts** (Síntese neural de voz multilíngue em português brasileiro)
- **PyYAML** (Configuração e perfil de casting de personagens)

---

## 📄 Licença
Distribuído sob licença MIT. Criado para fins educacionais e de preservação de jogos em língua portuguesa.
