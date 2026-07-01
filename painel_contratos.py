import os
import re
import fitz  # PyMuPDF
import shutil
import pdfplumber
import sys
import customtkinter as ctk
from tkinter import filedialog, messagebox

# --- CONFIGURAÇÃO DO VISUAL MODERNO ---
ctk.set_appearance_mode("dark")       # Opções: "dark", "light", "system"
ctk.set_default_color_theme("blue")   # Opções: "blue", "dark-blue", "green"

# --- 0. CLASSE PARA REDIRECIONAR OS PRINTS ---
class Redirecionador:
    def __init__(self, widget_texto):
        self.widget_texto = widget_texto

    def write(self, texto):
        self.widget_texto.insert("end", texto)
        self.widget_texto.see("end")
        self.widget_texto.update()

    def flush(self):
        pass

# --- 1. FUNÇÕES DOS SEUS SCRIPTS ---

def converter_pdf_jpg():
    pasta_raiz = var_caminho.get()
    if not pasta_raiz:
        messagebox.showwarning("Atenção", "Por favor, selecione a pasta primeiro!")
        return
        
    print("\n--- Iniciando a conversão para JPG ---")
    try:
        for raiz, pastas, arquivos in os.walk(pasta_raiz):
            for arquivo in arquivos:
                if arquivo.endswith('.pdf'):
                    caminho_pdf = os.path.join(raiz, arquivo)
                    
                    doc = fitz.open(caminho_pdf)
                    for i, pagina in enumerate(doc):
                        pix = pagina.get_pixmap()
                        nome_sem_extensao = os.path.splitext(arquivo)[0]
                        
                        if len(doc) > 1:
                            nome_jpg = f"{nome_sem_extensao}_pag{i+1}.jpg"
                        else:
                            nome_jpg = f"{nome_sem_extensao}.jpg"
                            
                        caminho_final = os.path.join(raiz, nome_jpg)
                        pix.save(caminho_final)
                    
                    doc.close()
                    print(f"Convertido: {nome_jpg}")
        
        print(">>> Conversão finalizada com sucesso! <<<")
        messagebox.showinfo("Concluído", "Conversão de PDF para JPG finalizada!")
    except Exception as e:
        print(f"ERRO: {e}")
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")


def organizar_por_consultor():
    diretorio_origem = var_caminho.get()
    if not diretorio_origem:
        messagebox.showwarning("Atenção", "Por favor, selecione a pasta primeiro!")
        return

    print("\n--- Iniciando organização por Consultor ---")
    if not os.path.exists(diretorio_origem):
        print("ERRO: Diretório não encontrado!")
        return

    try:
        os.chdir(diretorio_origem)
        arquivos_pdf = [f for f in os.listdir() if f.lower().endswith('.pdf')]

        for nome_arquivo in arquivos_pdf:
            nome_base = os.path.splitext(nome_arquivo)[0]
            caminho_jpg = f"{nome_base}.jpg"

            doc = fitz.open(nome_arquivo)
            texto_completo = ""
            for pagina in doc:
                texto_completo += pagina.get_text()
            doc.close()

            padrao = r"Consultor responsável:.*?-\s*(.*)"
            match = re.search(padrao, texto_completo, re.IGNORECASE)

            if match:
                nome_bruto = match.group(1).strip()
                nome_escritorio = nome_bruto.split('\n')[0].replace("/", "-").strip()
                
                pasta_escritorio = nome_escritorio
                pasta_jpgs = os.path.join(pasta_escritorio, "jpgs")
                
                if not os.path.exists(pasta_jpgs):
                    os.makedirs(pasta_jpgs)

                shutil.move(nome_arquivo, os.path.join(pasta_escritorio, nome_arquivo))
                
                if os.path.exists(caminho_jpg):
                    shutil.move(caminho_jpg, os.path.join(pasta_jpgs, caminho_jpg))
                
                print(f"Sucesso: {nome_base} -> {nome_escritorio}")
            else:
                print(f"Aviso: Padrão não encontrado no arquivo {nome_arquivo}")
                
        print(">>> Organização finalizada com sucesso! <<<")
        messagebox.showinfo("Concluído", "Organização por consultor finalizada!")
    except Exception as e:
        print(f"ERRO: {e}")
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")


def renomear_por_numero():
    pasta_raiz = var_caminho.get()
    if not pasta_raiz:
        messagebox.showwarning("Atenção", "Por favor, selecione a pasta primeiro!")
        return

    print(f"\n--- Iniciando renomeação (Nº Serviço) ---")
    try:
        for raiz, pastas, arquivos in os.walk(pasta_raiz):
            for arquivo in arquivos:
                if arquivo.endswith('.pdf'):
                    caminho_completo = os.path.join(raiz, arquivo)
                    
                    with pdfplumber.open(caminho_completo) as pdf:
                        texto = pdf.pages[0].extract_text()
                        busca = re.search(r'SERVIÇO:\s*N°\s*(\d+)', texto, re.IGNORECASE)
                        
                        if busca:
                            numero_contrato = busca.group(1)
                            novo_nome = f"{numero_contrato}.pdf"
                            novo_caminho = os.path.join(raiz, novo_nome)
                        pdf.close()
                        
                        if busca:
                            if not os.path.exists(novo_caminho):
                                os.rename(caminho_completo, novo_caminho)
                                print(f"OK: {arquivo} -> {novo_nome}")
                            elif caminho_completo != novo_caminho:
                                print(f"Conflito: {novo_nome} já existe.")
        
        print(">>> Renomeação finalizada com sucesso! <<<")
        messagebox.showinfo("Concluído", "Renomeação finalizada!")
    except Exception as e:
        print(f"ERRO: {e}")
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")


def selecionar_pasta():
    pasta_selecionada = filedialog.askdirectory()
    if pasta_selecionada:
        var_caminho.set(pasta_selecionada)
        print(f"Pasta selecionada: {pasta_selecionada}")


# --- 2. CONFIGURAÇÃO DA INTERFACE GRÁFICA ---

janela = ctk.CTk()
janela.title("Painel de Automação de Contratos")
janela.geometry("500x650") # Um pouco maior para acomodar o novo design

var_caminho = ctk.StringVar()

# Título
lbl_titulo = ctk.CTkLabel(janela, text="Selecione a pasta de trabalho:", font=("Arial", 16, "bold"))
lbl_titulo.pack(pady=(20, 5))

# Caminho selecionado
lbl_caminho = ctk.CTkLabel(janela, textvariable=var_caminho, text_color="#1E90FF", wraplength=450)
lbl_caminho.pack(pady=(0, 15))

# Botão Selecionar
btn_selecionar = ctk.CTkButton(janela, text="📂 Selecionar Pasta", command=selecionar_pasta, width=200, height=35)
btn_selecionar.pack(pady=5)

# Linha separadora
separador = ctk.CTkFrame(janela, height=2, width=400, fg_color="gray20")
separador.pack(pady=20)

# Botões de Ação
btn_script3 = ctk.CTkButton(janela, text="1. Renomear PDFs (Nº Serviço)", command=renomear_por_numero, width=300, height=40)
btn_script3.pack(pady=5)

btn_script1 = ctk.CTkButton(janela, text="2. Converter PDFs para JPG", command=converter_pdf_jpg, width=300, height=40)
btn_script1.pack(pady=5)

btn_script2 = ctk.CTkButton(janela, text="3. Organizar por Consultor", command=organizar_por_consultor, width=300, height=40)
btn_script2.pack(pady=5)

# Título do Log
lbl_log = ctk.CTkLabel(janela, text="Progresso das tarefas:", font=("Arial", 12, "bold"))
lbl_log.pack(pady=(20, 5), anchor="w", padx=40)

# Caixa de Texto
caixa_texto = ctk.CTkTextbox(janela, height=150, width=420, fg_color="black", text_color="#00FF00", font=("Consolas", 12))
caixa_texto.pack(pady=5)

# Redirecionamento
sys.stdout = Redirecionador(caixa_texto)
sys.stderr = Redirecionador(caixa_texto)

# Inicia o programa
janela.mainloop()