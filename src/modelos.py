from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional


class TipoArquivo(Enum):
    IMAGEM = "imagem"
    DOCUMENTO = "documento"
    PLANILHA = "planilha"
    TEXTO = "texto"
    VIDEO = "video"
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
    caminho_origem: Optional[str] = None

    def __post_init__(self):
        if self.metadados.extensao:
            self.tipo = self._detectar_tipo(self.metadados.extensao)

    @staticmethod
    def _detectar_tipo(extensao: str) -> TipoArquivo:
        imagens = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp', 'svg'}
        documentos = {'pdf', 'docx', 'doc', 'odt', 'rtf', 'txt', 'md'}
        planilhas = {'xlsx', 'xls', 'csv', 'ods'}
        videos = {'mp4', 'mov', 'avi', 'mkv', 'webm', 'flv', 'wmv', 'm4v', '3gp'}

        ext = extensao.lower().lstrip('.')
        if ext in imagens: return TipoArquivo.IMAGEM
        if ext in documentos: return TipoArquivo.DOCUMENTO
        if ext in planilhas: return TipoArquivo.PLANILHA
        if ext in videos: return TipoArquivo.VIDEO
        return TipoArquivo.DESCONHECIDO