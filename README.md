🔥 FileForge Converter

<div align="center">

![Status](https://img.shields.io/badge/Status-Funcionando-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Tests](https://img.shields.io/badge/Tests-19%20passing-success)
![License](https://img.shields.io/badge/License-MIT-yellow)

**Conversor de arquivos com interface gráfica moderna**

</div>

---

## 📋 Sobre o Projeto

FileForge Converter é um conversor de arquivos desenvolvido em Python com interface gráfica (CustomTkinter). O projeto foi criado para ser simples, rápido e eficiente, permitindo converter arquivos entre diferentes formatos com apenas alguns cliques.

Este projeto faz parte do meu portfólio como **Analista e Desenvolvedor de Sistemas** e demonstra habilidades em:
- Desenvolvimento Python
- Interface gráfica com CustomTkinter
- Manipulação de arquivos e imagens
- Testes unitários
- Controle de versão com Git

---

## ✨ Funcionalidades

### Atualmente Funcionando

- ✅ **Interface gráfica moderna** com tema escuro
- ✅ **Conversão de imagens**: PNG, JPG, JPEG, GIF, BMP, WebP
- ✅ **Conversão de documentos**: TXT para MD, extração de texto de PDF e DOCX
- ✅ **Processamento em lote**: converta vários arquivos de uma vez
- ✅ **Detecção automática** do tipo de arquivo
- ✅ **Proteção contra sobrescrita** (renomeia automaticamente)
- ✅ **Seleção múltipla** de arquivos via interface
- ✅ **Lista de arquivos** com remoção individual
- ✅ **19 testes unitários** para garantir qualidade

### Em Desenvolvimento (Futuro)

- 🔄 Conversão de vídeos
- 🔄 Conversão de áudio
- 🔄 Conversão de planilhas
- 🔄 Barra de progresso
- 🔄 Drag & Drop nativo

---

## 📦 Formatos Suportados

| Entrada | Saída |
|---------|-------|
| PNG, JPG, JPEG, GIF, BMP, WebP | PNG, JPG, JPEG, WebP |
| TXT | MD, TXT |
| PDF (extrai texto) | TXT |
| DOCX (extrai texto) | TXT |

---

## 🚀 Instalação

### Pré-requisitos

- Python 3.8 ou superior instalado
- Git (opcional, para clonar)

### Passo a Passo

#### 1. Clone ou baixe o projeto

```bash
git clone https://github.com/MisaAndrejezieski/fileforge-converter.git
cd fileforge-converter
2. Crie o ambiente virtual
bash
python -m venv venv
3. Ative o ambiente virtual
Windows:

bash
.\venv\Scripts\activate
Linux/Mac:

bash
source venv/bin/activate
4. Instale as dependências
bash
pip install -r requirements.txt
5. Execute
bash
python main.py
🎮 Como Usar
Interface Gráfica
Selecione os arquivos

Clique em "📁 Selecionar Arquivos"

Escolha um ou mais arquivos (Ctrl+Click para múltiplos)

Escolha o formato de saída

No dropdown, selecione o formato desejado

Opções disponíveis: jpg, png, webp, txt, md

Converta

Clique em "⚡ Converter"

Aguarde a mensagem de sucesso

Encontre os arquivos

Os arquivos convertidos estarão na pasta output/

Nomes são auto-renomeados para evitar duplicação

Via Código (Programático)
python
from src.engine import ConversorEngine

engine = ConversorEngine()

# Converte um arquivo
resultado = engine.converter(
    "foto.png",        # arquivo de entrada
    "jpg",             # formato de saída
    "./output"         # pasta de destino
)
print(f"Convertido: {resultado}")

# Converte vários arquivos
arquivos = ["doc1.txt", "doc2.txt"]
resultados = engine.converter_lote(arquivos, "md", "./output")
🧪 Testes
O projeto inclui testes unitários para garantir o funcionamento correto.

Executar todos os testes:
bash
python -m unittest discover tests -v
Resultado esperado:
text
Ran 19 tests in 0.085s
OK
📁 Estrutura do Projeto
text
fileforge-converter/
├── src/
│   ├── modelos.py          # Modelos de dados
│   ├── leitores.py         # Leitores de arquivos
│   ├── escritores.py       # Escritores de arquivos
│   ├── engine.py           # Motor principal
│   └── interface.py        # Interface gráfica
├── tests/
│   └── test_conversor.py   # Testes unitários (19 testes)
├── output/                 # Arquivos convertidos (criado automaticamente)
├── main.py                 # Ponto de entrada
├── requirements.txt        # Dependências
├── .gitignore             # Arquivos ignorados
└── README.md              # Este arquivo
🛠️ Tecnologias Usadas
Biblioteca	Versão	Para que serve
Python	3.8+	Linguagem principal
Pillow	10.0+	Manipulação de imagens
CustomTkinter	5.2+	Interface gráfica
PyPDF2	3.0+	Leitura de PDFs
python-docx	0.8+	Leitura de DOCX
📊 Estatísticas do Projeto
Total de testes: 19

Cobertura de testes: 100% (modelos, leitores, escritores, engine, integração)

Linhas de código: ~400 (src) + ~200 (tests)

Tempo médio dos testes: 0.085 segundos

📝 Licença
Este projeto está sob a licença MIT.

text
MIT License

Copyright (c) 2024 Misael Andrejezieski

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
🤝 Contribuindo
Contribuições são bem-vindas!

Faça um Fork do projeto

Crie sua branch: git checkout -b minha-feature

Commit: git commit -m "Adiciona algo"

Push: git push origin minha-feature

Abra um Pull Request

📬  Contato
Misael Andrejezieski
Analista e Desenvolvedor de Sistemas

https://img.shields.io/badge/GitHub-MisaAndrejezieski-181717?style=for-the-badge&logo=github
https://img.shields.io/badge/LinkedIn-Misael_Andrejezieski-0A66C2?style=for-the-badge&logo=linkedin

Feito com Python e ☕

⭐ Se este projeto te ajudou, considere dar uma estrela no GitHub!

</div>