from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional


class TipoArquivo(Enum):
    IMAGEM = "imagem"
    DOCUMENTO = "documento"
    PLANILHA = "planilha"
    TEXTO = "texto"
    DESCONHECIDO = "desconhecido"

@dataclass
class Metadados:
    nome_arquivo: str
    tamanho_bytes: int
    extensao: str
    data_criacao: datetime
    data_modificacao: datetime

@dataclass
class ArquivoUniversal:
    conteudo: Any
    metadados: Metadados
    tipo: TipoArquivo = TipoArquivo.DESCONHECIDO
    propriedades: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if self.metadados.extensao:
            self.tipo = self._detectar_tipo(self.metadados.extensao)
    
    @staticmethod
    def _detectar_tipo(extensao: str) -> TipoArquivo:
        imagens = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp', 'svg'}
        documentos = {'pdf', 'docx', 'doc', 'odt', 'rtf', 'txt', 'md'}
        planilhas = {'xlsx', 'xls', 'csv', 'ods'}
        
        ext = extensao.lower().lstrip('.')
        if ext in imagens: return TipoArquivo.IMAGEM
        if ext in documentos: return TipoArquivo.DOCUMENTO
        if ext in planilhas: return TipoArquivo.PLANILHA
        return TipoArquivo.DESCONHECIDO