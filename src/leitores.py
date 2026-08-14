from datetime import datetime
from pathlib import Path

from docx import Document
from PIL import Image
from PyPDF2 import PdfReader

from .modelos import ArquivoUniversal, Metadados  # ← IMPORTANTE!


class LeitorArquivos:
    def ler(self, caminho: str) -> ArquivoUniversal:
        path = Path(caminho)
        
        metadados = Metadados(
            nome_arquivo=path.name,
            tamanho_bytes=path.stat().st_size,
            extensao=path.suffix.lstrip('.'),
            data_criacao=datetime.fromtimestamp(path.stat().st_ctime),
            data_modificacao=datetime.fromtimestamp(path.stat().st_mtime)
        )
        
        ext = metadados.extensao.lower()
        
        if ext in ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp']:
            return self._ler_imagem(caminho, metadados)
        elif ext == 'pdf':
            return self._ler_pdf(caminho, metadados)
        elif ext in ['docx', 'doc']:
            return self._ler_docx(caminho, metadados)
        elif ext == 'txt':
            return self._ler_txt(caminho, metadados)
        else:
            raise ValueError(f"Formato não suportado: {ext}")
    
    def _ler_imagem(self, caminho: str, metadados: Metadados):
        imagem = Image.open(caminho)
        props = {
            'largura': imagem.width,
            'altura': imagem.height,
            'modo': imagem.mode,
            'formato': imagem.format
        }
        return ArquivoUniversal(imagem, metadados, propriedades=props)  # ← 'propriedades' corrigido
    
    def _ler_pdf(self, caminho: str, metadados: Metadados):
        reader = PdfReader(caminho)
        texto = ""
        for pagina in reader.pages:
            texto += pagina.extract_text() + "\n"
        props = {'paginas': len(reader.pages)}
        return ArquivoUniversal(texto, metadados, propriedades=props)  # ← 'propriedades' corrigido
    
    def _ler_docx(self, caminho: str, metadados: Metadados):
        doc = Document(caminho)
        texto = "\n".join([p.text for p in doc.paragraphs])
        return ArquivoUniversal(texto, metadados, propriedades={'estilos': 'preservado'})  # ← 'propriedades' corrigido
    
    def _ler_txt(self, caminho: str, metadados: Metadados):
        with open(caminho, 'r', encoding='utf-8') as f:
            texto = f.read()
        return ArquivoUniversal(texto, metadados, propriedades={})  # ← 'propriedades' corrigido