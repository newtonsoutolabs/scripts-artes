import os
import fitz  # PyMuPDF
import shutil
import re

def organizar_contratos(diretorio_origem):
    if not os.path.exists(diretorio_origem):
        print("Diretório não encontrado!")
        return

    os.chdir(diretorio_origem)
    arquivos_pdf = [f for f in os.listdir() if f.lower().endswith('.pdf')]

    for nome_arquivo in arquivos_pdf:
        nome_base = os.path.splitext(nome_arquivo)[0]
        caminho_jpg = f"{nome_base}.jpg"

        try:
            doc = fitz.open(nome_arquivo)
            texto_completo = ""
            for pagina in doc:
                texto_completo += pagina.get_text()
            doc.close()

            # REGEX MELHORADO:
            # Procuro "Consultor responsável:", pulo até o "-", 
            # e pego tudo até encontrar uma "/" OU uma ","
            padrao = r"Consultor responsável:.*?-\s*(.*?)[/,]"
            match = re.search(padrao, texto_completo, re.IGNORECASE)

            if match:
                nome_escritorio = match.group(1).strip()
                
                # Criar pastas
                pasta_escritorio = nome_escritorio
                pasta_jpgs = os.path.join(pasta_escritorio, "jpgs")
                
                if not os.path.exists(pasta_jpgs):
                    os.makedirs(pasta_jpgs)

                # Mover arquivos
                shutil.move(nome_arquivo, os.path.join(pasta_escritorio, nome_arquivo))
                if os.path.exists(caminho_jpg):
                    shutil.move(caminho_jpg, os.path.join(pasta_jpgs, caminho_jpg))
                
                print(f"Sucesso: {nome_base} -> {nome_escritorio}")
            else:
                print(f"Aviso: Padrão não encontrado no arquivo {nome_arquivo}")

        except Exception as e:
            print(f"Erro ao processar {nome_arquivo}: {e}")

# Lembre-se do 'r' antes das aspas para evitar o erro de unicode!
diretorio = r"C:\Users\Newton solto\Documents\Artes\FEVEREIRO\PDFS FEVEREIRO LINHAS 18 A 146"
organizar_contratos(diretorio)