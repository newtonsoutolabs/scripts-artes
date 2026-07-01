import os
import fitz  # PyMuPDF

pasta_raiz = '.' 

print("Iniciando a conversão mantendo os nomes originais...")

for raiz, pastas, arquivos in os.walk(pasta_raiz):
    for arquivo in arquivos:
        if arquivo.endswith('.pdf'):
            caminho_pdf = os.path.join(raiz, arquivo)
            
            try:
                doc = fitz.open(caminho_pdf)
                
                for i, pagina in enumerate(doc):
                    pix = pagina.get_pixmap()
                    
                    # Pega o nome do contrato (ex: 224844) e coloca .jpg
                    nome_sem_extensao = os.path.splitext(arquivo)[0]
                    
                    # Se tiver mais de uma página, ele ainda coloca o número 
                    # para não apagar o arquivo anterior. Se for só uma, fica o nome puro.
                    if len(doc) > 1:
                        nome_jpg = f"{nome_sem_extensao}_pag{i+1}.jpg"
                    else:
                        nome_jpg = f"{nome_sem_extensao}.jpg"
                        
                    caminho_final = os.path.join(raiz, nome_jpg)
                    pix.save(caminho_final)
                
                doc.close()
                print(f"Convertido: {nome_jpg}")
                
            except Exception as e:
                print(f"Erro em {arquivo}: {e}")

print("\nFinalizado! Agora os nomes dos JPGs são iguais aos dos PDFs.")