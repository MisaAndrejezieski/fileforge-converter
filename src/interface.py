from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk

from .engine import ConversorEngine

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class FileForgeUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("FileForge Converter 🔥")
        self.geometry("800x500")
        
        self.engine = ConversorEngine()
        self.arquivos = []
        
        self._setup_ui()
    
    def _setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Frame principal
        frame = ctk.CTkFrame(self)
        frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        
        # Título
        titulo = ctk.CTkLabel(frame, text="FileForge Converter", 
                             font=ctk.CTkFont(size=28, weight="bold"))
        titulo.grid(row=0, column=0, pady=(0, 20))
        
        # Botão selecionar
        self.btn_selecionar = ctk.CTkButton(frame, text="📁 Selecionar Arquivos",
                                           command=self.selecionar_arquivos,
                                           height=50, font=ctk.CTkFont(size=14))
        self.btn_selecionar.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        # Frame formato
        frame_formato = ctk.CTkFrame(frame)
        frame_formato.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")
        frame_formato.grid_columnconfigure((0,1), weight=1)
        
        ctk.CTkLabel(frame_formato, text="Converter para:").grid(row=0, column=0, padx=5)
        
        self.combo_formato = ctk.CTkComboBox(
            frame_formato,
            values=["jpg", "png", "webp", "pdf", "txt", "md"],
            width=150
        )
        self.combo_formato.grid(row=0, column=1, padx=5)
        
        # Lista de arquivos
        self.lista_frame = ctk.CTkScrollableFrame(frame, height=150)
        self.lista_frame.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.lista_frame.grid_columnconfigure(0, weight=1)
        
        self.lbl_lista = ctk.CTkLabel(self.lista_frame, text="Nenhum arquivo selecionado")
        self.lbl_lista.grid(row=0, column=0, padx=10, pady=10)
        
        # Botões ação
        frame_botoes = ctk.CTkFrame(frame)
        frame_botoes.grid(row=4, column=0, padx=20, pady=(0, 10), sticky="ew")
        frame_botoes.grid_columnconfigure((0,1,2), weight=1)
        
        self.btn_converter = ctk.CTkButton(frame_botoes, text="⚡ Converter",
                                          command=self.converter,
                                          fg_color="#2ecc71", hover_color="#27ae60")
        self.btn_converter.grid(row=0, column=1, padx=5)
        
        self.btn_limpar = ctk.CTkButton(frame_botoes, text="🗑️ Limpar",
                                       command=self.limpar,
                                       fg_color="#e74c3c", hover_color="#c0392b")
        self.btn_limpar.grid(row=0, column=2, padx=5)
        
        # Status
        self.lbl_status = ctk.CTkLabel(frame, text="✅ Pronto", font=ctk.CTkFont(size=12))
        self.lbl_status.grid(row=5, column=0)
    
    def selecionar_arquivos(self):
        arquivos = filedialog.askopenfilenames(
            title="Selecione arquivos",
            filetypes=[
                ("Todos", "*.*"),
                ("Imagens", "*.png *.jpg *.jpeg *.gif *.bmp *.webp"),
                ("Documentos", "*.pdf *.docx *.txt *.md"),
            ]
        )
        
        for arq in arquivos:
            if arq not in self.arquivos:
                self.arquivos.append(arq)
                self.atualizar_lista()
    
    def atualizar_lista(self):
        # Limpa
        for widget in self.lista_frame.winfo_children():
            widget.destroy()
        
        if not self.arquivos:
            lbl = ctk.CTkLabel(self.lista_frame, text="Nenhum arquivo selecionado")
            lbl.grid(row=0, column=0, padx=10, pady=10)
            return
        
        for i, arq in enumerate(self.arquivos):
            frame = ctk.CTkFrame(self.lista_frame)
            frame.grid(row=i, column=0, padx=5, pady=2, sticky="ew")
            frame.grid_columnconfigure(0, weight=1)
            
            nome = Path(arq).name
            ctk.CTkLabel(frame, text=f"📄 {nome}").grid(row=0, column=0, padx=5, sticky="w")
            
            btn_remover = ctk.CTkButton(frame, text="✕", width=30, height=30,
                                       fg_color="transparent", text_color="#e74c3c",
                                       command=lambda a=arq: self.remover_arquivo(a))
            btn_remover.grid(row=0, column=1, padx=5)
        
        self.lbl_status.configure(text=f"{len(self.arquivos)} arquivo(s) selecionado(s)")
    
    def remover_arquivo(self, arquivo):
        if arquivo in self.arquivos:
            self.arquivos.remove(arquivo)
            self.atualizar_lista()
    
    def limpar(self):
        self.arquivos.clear()
        self.atualizar_lista()
        self.lbl_status.configure(text="🗑️ Lista limpa")
    
    def converter(self):
        if not self.arquivos:
            messagebox.showwarning("Aviso", "Nenhum arquivo selecionado!")
            return
        
        formato = self.combo_formato.get()
        self.btn_converter.configure(state="disabled", text="⏳ Convertendo...")
        
        try:
            resultados = self.engine.converter_lote(
                self.arquivos, formato, pasta_saida="./output"
            )
            
            mensagem = f"✅ {len(resultados)} arquivo(s) convertido(s)!\n\n"
            for r in resultados[:5]:
                mensagem += f"  • {r}\n"
            if len(resultados) > 5:
                mensagem += f"  ... e mais {len(resultados)-5} arquivo(s)"
            
            messagebox.showinfo("Sucesso", mensagem)
            self.limpar()
            self.lbl_status.configure(text=f"✅ Última conversão: {len(resultados)} arquivo(s)")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro: {str(e)}")
        
        finally:
            self.btn_converter.configure(state="normal", text="⚡ Converter")