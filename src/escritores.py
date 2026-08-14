from pathlib import Path

from PIL import Image

from .modelos import ArquivoUniversal


class EscritorArquivos:
    def escrever(self, arquivo_universal: ArquivoUniversal, caminho_saida: str):
        ext = Path(caminho_saida).suffix.lstrip('.').lower()
        
        if arquivo_universal.tipo.value == 'imagem':
            return self._escrever_imagem(arquivo_universal, caminho_saida, ext)
        else:
            return self._escrever_texto(arquivo_universal, caminho_saida, ext)
    
    def _escrever_imagem(self, arquivo: ArquivoUniversal, caminho: str, ext: str):
        imagem = arquivo.conteudo
        
        # Converte modo se necessário
        if ext in ['jpg', 'jpeg'] and imagem.mode in ['RGBA', 'P']:
            imagem = imagem.convert('RGB')
        
        # CORREÇÃO: Mapeia extensão para formato PIL
        formato_pil = self._mapear_formato_pil(ext)
        
        imagem.save(caminho, format=formato_pil, quality=85, optimize=True)
        return caminho
    
    def _mapear_formato_pil(self, ext: str) -> str:
        """Mapeia extensão para formato suportado pelo Pillow"""
        mapa = {
            'jpg': 'JPEG',
            'jpeg': 'JPEG',
            'png': 'PNG',
            'gif': 'GIF',
            'bmp': 'BMP',
            'webp': 'WEBP',
            'tiff': 'TIFF',
            'tif': 'TIFF'
        }
        formato = mapa.get(ext.lower(), ext.upper())
        if formato == 'JPG':
            formato = 'JPEG'  # Correção importante!
        return formato
    
    def _escrever_texto(self, arquivo: ArquivoUniversal, caminho: str, ext: str):
        texto = arquivo.conteudo
        
        if ext == 'txt':
            with open(caminho, 'w', encoding='utf-8') as f:
                f.write(texto)
        elif ext == 'md':
            with open(caminho, 'w', encoding='utf-8') as f:
                f.write(f"# Documento convertido\n\n{texto}")
        else:
            raise ValueError(f"Formato de texto não suportado: {ext}")
        
        return caminho