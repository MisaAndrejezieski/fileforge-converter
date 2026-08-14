🔥 FileForge Converter

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.2+-green?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)
![Tests](https://img.shields.io/badge/Tests-19%20passing-brightgreen?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Stable-success?style=for-the-badge)

**Um conversor de arquivos universal com interface gráfica moderna**

[Recursos](#-recursos) • [Instalação](#-instalação) • [Como Usar](#-como-usar) • [Testes](#-testes) • [Contribuição](#-contribuição)

</div>

---

## 📸 Preview

![FileForge Converter Interface](https://via.placeholder.com/800x500/1a1a2e/ffffff?text=FileForge+Converter+Interface)

> *Interface moderna com tema escuro e design intuitivo*

---

## 🎯 Recursos

### ✨ Principais Funcionalidades

- 📁 **Conversão entre múltiplos formatos** (imagens, documentos, textos)
- 🎨 **Interface gráfica moderna** com CustomTkinter
- ⚡ **Processamento em lote** - converta vários arquivos de uma vez
- 🔄 **Detecção automática de tipo** de arquivo
- 🛡️ **Proteção contra sobrescrita** - renomeia automaticamente arquivos duplicados
- 📊 **Suporte a múltiplos formatos**:
  - Imagens: PNG, JPG, JPEG, GIF, BMP, WebP
  - Documentos: TXT, MD, PDF (leitura), DOCX (leitura)
- 🧪 **Suite completa de testes** (19 testes unitários)
- 🚀 **Processamento paralelo** para conversões em lote

### 🎨 Interface

- Tema escuro moderno
- Drag & Drop (clique para selecionar)
- Lista de arquivos com remoção individual
- Indicador de status em tempo real
- Design responsivo

---

## 📦 Formatos Suportados

| Tipo | Formatos de Entrada | Formatos de Saída |
|------|-------------------|-------------------|
| 📷 Imagens | PNG, JPG, JPEG, GIF, BMP, WebP | PNG, JPG, JPEG, WebP |
| 📄 Documentos | TXT, PDF (leitura), DOCX (leitura) | TXT, MD |
| 📊 Planilhas | *Em desenvolvimento* | *Em desenvolvimento* |
| 🎵 Áudio | *Em desenvolvimento* | *Em desenvolvimento* |
| 🎬 Vídeo | *Em desenvolvimento* | *Em desenvolvimento* |

---

## 🚀 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- Git (opcional, para clonar o repositório)

### Passo a Passo

#### 1. Clone o repositório

```bash
git clone https://github.com/MisaAndrejezieski/fileforge-converter
cd fileforge-converter
2. Crie e ative o ambiente virtual
Windows:

bash
python -m venv venv
.\venv\Scripts\activate
Linux/Mac:

bash
python3 -m venv venv
source venv/bin/activate
3. Instale as dependências
bash
pip install -r requirements.txt
4. Execute o programa
bash
python main.py


🎮 Como Usar
Interface Gráfica
Selecionar arquivos:

Clique em "📁 Selecionar Arquivos"

Ou arraste arquivos para a área indicada (em breve)

Escolher formato de saída:

Selecione o formato desejado no dropdown

Opções: jpg, png, webp, pdf, txt, md

Converter:

Clique em "⚡ Converter"

Acompanhe o progresso no status

Gerenciar arquivos:

Remova arquivos individualmente com o botão ✕

Limpe toda a lista com "🗑️ Limpar"

Linha de Comando (Modo Programático)
python
from src.engine import ConversorEngine

# Inicializa o motor
engine = ConversorEngine()

# Converte um arquivo
resultado = engine.converter(
    entrada="documento.txt",
    formato_saida="md",
    pasta_saida="./output"
)
print(f"Arquivo convertido: {resultado}")

# Converte múltiplos arquivos
arquivos = ["foto1.png", "foto2.jpg"]
resultados = engine.converter_lote(
    arquivos,
    formato_saida="webp",
    pasta_saida="./output"
)
for r in resultados:
    print(f"✓ {r}")
🧪 Testes
O projeto inclui uma suite completa de testes unitários.

Executar todos os testes:
bash
python -m unittest discover tests -v
Executar testes específicos:
bash
# Testes de modelo
python -m unittest tests.test_conversor.TestModelos -v

# Testes do motor
python -m unittest tests.test_conversor.TestEngine -v

# Testes de integração
python -m unittest tests.test_conversor.TestIntegracao -v
Cobertura de Testes:
text
✅ 19 testes unitários
✅ Modelos de dados
✅ Leitores de arquivos
✅ Escritores de arquivos
✅ Motor de conversão
✅ Integração completa


📁 Estrutura do Projeto
text
fileforge-converter/
├── src/                      # Código fonte
│   ├── __init__.py
│   ├── modelos.py           # Modelos de dados (ArquivoUniversal, Metadados)
│   ├── leitores.py          # Leitores de arquivos (TXT, PNG, PDF, DOCX)
│   ├── escritores.py        # Escritores de arquivos (TXT, MD, JPG, PNG)
│   ├── engine.py            # Motor principal de conversão
│   └── interface.py         # Interface gráfica (CustomTkinter)
├── tests/                    # Testes unitários
│   └── test_conversor.py    # Suite de testes (19 testes)
├── output/                   # Arquivos convertidos (criado automaticamente)
├── main.py                   # Ponto de entrada
├── requirements.txt          # Dependências do projeto
├── README.md                 # Esta documentação
└── .gitignore               # Arquivos ignorados pelo Git


🛠️ Tecnologias Utilizadas
Tecnologia	Versão	Descrição
Python	3.8+	Linguagem principal
Pillow	10.0+	Manipulação de imagens
CustomTkinter	5.2+	Interface gráfica moderna
PyPDF2	3.0+	Leitura de PDFs
python-docx	0.8+	Leitura de DOCX
unittest	Built-in	Testes unitários
🤝 Contribuição
Contribuições são bem-vindas! Siga estes passos:

Fork o projeto

Clone seu fork:

bash
git clone https://github.com/MisaAndrejezieski/fileforge-converter
Crie uma branch para sua feature:

bash
git checkout -b feature/nova-funcionalidade
Faça commit das alterações:

bash
git commit -m "Adiciona nova funcionalidade"
Push para a branch:

bash
git push origin feature/nova-funcionalidade
Abra um Pull Request

Áreas para Contribuição
📦 Adicionar novos formatos (vídeo, áudio, planilhas)

🎨 Melhorar a interface (temas, animações)

🧪 Aumentar cobertura de testes

📚 Melhorar documentação

🌍 Internacionalização (i18n)

📝 Licença
Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

text
MIT License

Copyright (c) 2024 FileForge Converter

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions...


🙏 Agradecimentos
Pillow - Manipulação de imagens

CustomTkinter - Interface gráfica

PyPDF2 - Leitura de PDFs

python-docx - Leitura de DOCX

📞 Contato
Autor: Misael Andrejezieski

Email: mandrejezieski@gmail.com

GitHub: https://github.com/MisaAndrejezieski

LinkedIn: https://www.linkedin.com/in/misael-andrejezieski-b4996720a/

<div align="center">
Feito com ❤️ por Misael Andrejezieski.

⭐ Se este projeto te ajudou, considere dar uma estrela no GitHub!

</div> ```