import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from .escritores import EscritorArquivos
from .leitores import LeitorArquivos


class ConversorEngine:
    def __init__(self):
        self.leitor = LeitorArquivos()
        self.escritor = EscritorArquivos()
        self.executor = ThreadPoolExecutor(max_workers=4)
    
    def converter(self, entrada: str, formato_saida: str, pasta_saida: str = "./output"):
        if not os.path.exists(entrada):
            raise FileNotFoundError(f"Arquivo não encontrado: {entrada}")
        
        Path(pasta_saida).mkdir(parents=True, exist_ok=True)
        
        # Carrega o arquivo
        arquivo_universal = self.leitor.ler(entrada)
        
        # Gera caminho de saída
        nome_base = Path(entrada).stem
        formato_limpo = formato_saida.lower().lstrip('.')
        caminho_saida = Path(pasta_saida) / f"{nome_base}.{formato_limpo}"
        
        # Evita sobrescrita
        contador = 1
        while caminho_saida.exists():
            caminho_saida = Path(pasta_saida) / f"{nome_base}_{contador}.{formato_limpo}"
            contador += 1
        
        # Escreve o arquivo
        return self.escritor.escrever(arquivo_universal, str(caminho_saida))
    
    def converter_lote(self, arquivos: list, formato_saida: str, pasta_saida: str = "./output"):
        resultados = []
        for arquivo in arquivos:
            try:
                resultado = self.converter(arquivo, formato_saida, pasta_saida)
                resultados.append(resultado)
            except Exception as e:
                resultados.append(f"❌ Erro em {arquivo}: {e}")
        return resultados