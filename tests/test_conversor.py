import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

# Adiciona o src ao path para importar
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.engine import ConversorEngine
from src.escritores import EscritorArquivos
from src.leitores import LeitorArquivos
from src.modelos import ArquivoUniversal, Metadados, TipoArquivo


class TestModelos(unittest.TestCase):
    """Testes para os modelos de dados"""
    
    def test_deteccao_tipo_imagem(self):
        """Testa detecção de tipos de imagem"""
        extensoes = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp']
        for ext in extensoes:
            metadados = Metadados(
                nome_arquivo=f"teste.{ext}",
                tamanho_bytes=1000,
                extensao=ext,
                data_criacao=None,
                data_modificacao=None
            )
            arquivo = ArquivoUniversal(conteudo=None, metadados=metadados)
            self.assertEqual(arquivo.tipo, TipoArquivo.IMAGEM)
    
    def test_deteccao_tipo_documento(self):
        """Testa detecção de tipos de documento"""
        extensoes = ['pdf', 'docx', 'doc', 'odt', 'rtf', 'txt', 'md']
        for ext in extensoes:
            metadados = Metadados(
                nome_arquivo=f"teste.{ext}",
                tamanho_bytes=1000,
                extensao=ext,
                data_criacao=None,
                data_modificacao=None
            )
            arquivo = ArquivoUniversal(conteudo=None, metadados=metadados)
            self.assertEqual(arquivo.tipo, TipoArquivo.DOCUMENTO)
    
    def test_deteccao_tipo_planilha(self):
        """Testa detecção de tipos de planilha"""
        extensoes = ['xlsx', 'xls', 'csv', 'ods']
        for ext in extensoes:
            metadados = Metadados(
                nome_arquivo=f"teste.{ext}",
                tamanho_bytes=1000,
                extensao=ext,
                data_criacao=None,
                data_modificacao=None
            )
            arquivo = ArquivoUniversal(conteudo=None, metadados=metadados)
            self.assertEqual(arquivo.tipo, TipoArquivo.PLANILHA)
    
    def test_deteccao_tipo_desconhecido(self):
        """Testa detecção de tipo desconhecido"""
        metadados = Metadados(
            nome_arquivo="teste.xyz",
            tamanho_bytes=1000,
            extensao="xyz",
            data_criacao=None,
            data_modificacao=None
        )
        arquivo = ArquivoUniversal(conteudo=None, metadados=metadados)
        self.assertEqual(arquivo.tipo, TipoArquivo.DESCONHECIDO)


class TestLeitores(unittest.TestCase):
    """Testes para leitores de arquivos"""
    
    def setUp(self):
        """Configura arquivos de teste"""
        self.temp_dir = tempfile.mkdtemp()
        self.leitor = LeitorArquivos()
        
        # Cria arquivo TXT de teste
        self.txt_path = os.path.join(self.temp_dir, "teste.txt")
        with open(self.txt_path, 'w', encoding='utf-8') as f:
            f.write("Este é um arquivo de teste\nLinha 2\nLinha 3")
        
        # Cria arquivo de imagem de teste (1x1 pixel)
        self.img_path = os.path.join(self.temp_dir, "teste.png")
        from PIL import Image
        img = Image.new('RGB', (1, 1), color='red')
        img.save(self.img_path)
    
    def tearDown(self):
        """Limpa arquivos de teste"""
        shutil.rmtree(self.temp_dir)
    
    def test_ler_txt(self):
        """Testa leitura de arquivo TXT"""
        arquivo = self.leitor.ler(self.txt_path)
        self.assertEqual(arquivo.tipo, TipoArquivo.DOCUMENTO)
        self.assertIn("Este é um arquivo de teste", arquivo.conteudo)
    
    def test_ler_imagem(self):
        """Testa leitura de arquivo de imagem"""
        arquivo = self.leitor.ler(self.img_path)
        self.assertEqual(arquivo.tipo, TipoArquivo.IMAGEM)
        self.assertEqual(arquivo.propriedades.get('largura'), 1)
        self.assertEqual(arquivo.propriedades.get('altura'), 1)
    
    def test_arquivo_nao_encontrado(self):
        """Testa erro ao ler arquivo inexistente"""
        with self.assertRaises(FileNotFoundError):
            self.leitor.ler("arquivo_inexistente.txt")
    
    def test_formato_nao_suportado(self):
        """Testa erro ao ler formato não suportado"""
        arquivo_estranho = os.path.join(self.temp_dir, "teste.xyz")
        with open(arquivo_estranho, 'w') as f:
            f.write("conteudo qualquer")
        
        with self.assertRaises(ValueError):
            self.leitor.ler(arquivo_estranho)


class TestEscritores(unittest.TestCase):
    """Testes para escritores de arquivos"""
    
    def setUp(self):
        """Configura arquivos de teste"""
        self.temp_dir = tempfile.mkdtemp()
        self.escritor = EscritorArquivos()
        
        # Cria um arquivo universal de texto
        metadados = Metadados(
            nome_arquivo="teste.txt",
            tamanho_bytes=0,
            extensao="txt",
            data_criacao=None,
            data_modificacao=None
        )
        self.arquivo_texto = ArquivoUniversal(
            conteudo="Texto de teste para escrita",
            metadados=metadados
        )
        
        # Cria um arquivo universal de imagem
        from PIL import Image
        img = Image.new('RGB', (100, 100), color='blue')
        metadados_img = Metadados(
            nome_arquivo="teste.png",
            tamanho_bytes=0,
            extensao="png",
            data_criacao=None,
            data_modificacao=None
        )
        self.arquivo_imagem = ArquivoUniversal(
            conteudo=img,
            metadados=metadados_img,
            propriedades={'largura': 100, 'altura': 100}
        )
    
    def tearDown(self):
        """Limpa arquivos de teste"""
        shutil.rmtree(self.temp_dir)
    
    def test_escrever_txt(self):
        """Testa escrita de arquivo TXT"""
        caminho = os.path.join(self.temp_dir, "saida.txt")
        resultado = self.escritor.escrever(self.arquivo_texto, caminho)
        
        self.assertTrue(os.path.exists(resultado))
        with open(resultado, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        self.assertEqual(conteudo, "Texto de teste para escrita")
    
    def test_escrever_md(self):
        """Testa escrita de arquivo Markdown"""
        caminho = os.path.join(self.temp_dir, "saida.md")
        resultado = self.escritor.escrever(self.arquivo_texto, caminho)
        
        self.assertTrue(os.path.exists(resultado))
        with open(resultado, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        self.assertIn("# Documento convertido", conteudo)
        self.assertIn("Texto de teste para escrita", conteudo)
    
    def test_escrever_imagem(self):
        """Testa escrita de arquivo de imagem"""
        caminho = os.path.join(self.temp_dir, "saida.jpg")
        resultado = self.escritor.escrever(self.arquivo_imagem, caminho)
        
        self.assertTrue(os.path.exists(resultado))
        from PIL import Image
        img = Image.open(resultado)
        self.assertEqual(img.width, 100)
        self.assertEqual(img.height, 100)
    
    def test_formato_nao_suportado(self):
        """Testa erro ao escrever em formato não suportado"""
        caminho = os.path.join(self.temp_dir, "saida.xyz")
        with self.assertRaises(ValueError):
            self.escritor.escrever(self.arquivo_texto, caminho)


class TestEngine(unittest.TestCase):
    """Testes para o motor de conversão"""
    
    def setUp(self):
        """Configura arquivos de teste"""
        self.temp_dir = tempfile.mkdtemp()
        self.output_dir = os.path.join(self.temp_dir, "output")
        self.engine = ConversorEngine()
        
        # Cria arquivo TXT de teste
        self.txt_path = os.path.join(self.temp_dir, "teste.txt")
        with open(self.txt_path, 'w', encoding='utf-8') as f:
            f.write("Conteúdo para teste de conversão")
        
        # Cria arquivo de imagem de teste
        from PIL import Image
        self.img_path = os.path.join(self.temp_dir, "teste.png")
        img = Image.new('RGB', (10, 10), color='green')
        img.save(self.img_path)
    
    def tearDown(self):
        """Limpa arquivos de teste"""
        shutil.rmtree(self.temp_dir)
    
    def test_converter_txt_para_md(self):
        """Testa conversão de TXT para MD"""
        resultado = self.engine.converter(
            self.txt_path, "md", self.output_dir
        )
        
        self.assertTrue(os.path.exists(resultado))
        self.assertTrue(resultado.endswith('.md'))
        with open(resultado, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        self.assertIn("Conteúdo para teste de conversão", conteudo)
    
    def test_converter_imagem_para_jpg(self):
        """Testa conversão de PNG para JPG"""
        resultado = self.engine.converter(
            self.img_path, "jpg", self.output_dir
        )
        
        self.assertTrue(os.path.exists(resultado))
        self.assertTrue(resultado.endswith('.jpg'))
    
    def test_converter_lote(self):
        """Testa conversão em lote"""
        arquivos = [self.txt_path, self.img_path]
        resultados = self.engine.converter_lote(
            arquivos, "txt", self.output_dir
        )
        
        self.assertEqual(len(resultados), 2)
        for r in resultados:
            self.assertTrue(os.path.exists(r))
    
    def test_arquivo_nao_encontrado(self):
        """Testa erro ao converter arquivo inexistente"""
        with self.assertRaises(FileNotFoundError):
            self.engine.converter("arquivo_inexistente.txt", "txt")
    
    def test_evitar_sobrescrita(self):
        """Testa que não sobrescreve arquivos existentes"""
        # Primeira conversão
        resultado1 = self.engine.converter(
            self.txt_path, "txt", self.output_dir
        )
        
        # Segunda conversão (mesmo arquivo)
        resultado2 = self.engine.converter(
            self.txt_path, "txt", self.output_dir
        )
        
        # Deve ser diferente (não sobrescreveu)
        self.assertNotEqual(resultado1, resultado2)
        self.assertTrue(os.path.exists(resultado1))
        self.assertTrue(os.path.exists(resultado2))


class TestIntegracao(unittest.TestCase):
    """Testes de integração - fluxo completo"""
    
    def setUp(self):
        """Configura arquivos de teste"""
        self.temp_dir = tempfile.mkdtemp()
        self.output_dir = os.path.join(self.temp_dir, "output")
        self.engine = ConversorEngine()
        
        # Cria vários arquivos para teste
        self.arquivos = []
        
        # TXT
        txt_path = os.path.join(self.temp_dir, "documento.txt")
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write("Documento de teste para integração")
        self.arquivos.append(txt_path)
        
        # PNG (imagem 5x5)
        from PIL import Image
        img_path = os.path.join(self.temp_dir, "imagem.png")
        img = Image.new('RGB', (5, 5), color='purple')
        img.save(img_path)
        self.arquivos.append(img_path)
    
    def tearDown(self):
        """Limpa arquivos de teste"""
        shutil.rmtree(self.temp_dir)
    
    def test_fluxo_completo_lote(self):
        """Testa fluxo completo de conversão em lote"""
        resultados = self.engine.converter_lote(
            self.arquivos, "txt", self.output_dir
        )
        
        # Verifica que todos foram convertidos
        self.assertEqual(len(resultados), len(self.arquivos))
        
        # Verifica que os arquivos de saída existem
        for r in resultados:
            self.assertTrue(os.path.exists(r))
            self.assertTrue(r.endswith('.txt'))
    
    def test_fluxo_completo_formatos_diferentes(self):
        """Testa fluxo completo com formatos diferentes"""
        # TXT -> MD
        txt_result = self.engine.converter(
            self.arquivos[0], "md", self.output_dir
        )
        self.assertTrue(txt_result.endswith('.md'))
        
        # PNG -> JPG
        img_result = self.engine.converter(
            self.arquivos[1], "jpg", self.output_dir
        )
        self.assertTrue(img_result.endswith('.jpg'))
        
        # Verifica os arquivos
        self.assertTrue(os.path.exists(txt_result))
        self.assertTrue(os.path.exists(img_result))


def suite():
    """Cria suite de testes"""
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestModelos))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestLeitores))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestEscritores))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestEngine))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestIntegracao))
    return suite


if __name__ == "__main__":
    # Roda os testes com detalhes
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())