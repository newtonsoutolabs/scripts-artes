# 📂 Automação e Gerenciamento de Documentos

Este repositório contém um conjunto de ferramentas focadas em manipulação de arquivos físicos, extração de texto, conversão de formatos e organização de diretórios em massa. O ecossistema abrange desde scripts locais e macros até uma Interface Gráfica (GUI) moderna.

## 🛠️ Tecnologias Utilizadas
* **Python 3:** Lógica principal de extração e conversão.
* **Bibliotecas Python:** `PyMuPDF` (fitz), `pdfplumber` (leitura de texto em PDFs), `customtkinter` (Interface Gráfica) e `shutil` (manipulação de sistema).
* **PowerShell:** Triagem de arquivos no Windows.
* **VBA:** Macro para Microsoft Word.

---

## 🚀 Como Executar o Painel Gráfico

O projeto conta com uma interface amigável para executar as principais automações sem precisar usar o terminal de comandos.

1. Instale as dependências: `pip install PyMuPDF pdfplumber customtkinter`
2. Dê um duplo clique no arquivo `iniciar_painel.bat`. Ele executará o comando `pythonw painel_contratos.py` e abrirá a interface silenciosamente, sem manter a tela preta do console de fundo[cite: 14].
3. Selecione a pasta de trabalho e clique no botão da automação desejada.

---

## 📂 Documentação das Ferramentas

### 1. Painel de Automação de Contratos (`painel_contratos.py`)
* **Visão Geral:** Interface gráfica centralizadora construída com tema escuro via `customtkinter`[cite: 11].
* **Funcionalidades:** Permite selecionar um diretório visualmente e executar três ações com um clique: renomear PDFs baseando-se no "Nº Serviço" extraído do texto, converter arquivos PDF para JPG, e organizar arquivos físicos agrupando-os pelo nome do consultor[cite: 11]. O painel inclui uma caixa de texto que redireciona e exibe o log de operações em tempo real[cite: 11].

### 2. Organizador de Diretórios por Regex (`organizar_contratos.py`)
* **Visão Geral:** Script de organização física de arquivos[cite: 9].
* **Funcionalidades:** Varre uma pasta atrás de PDFs, lê o texto de todas as páginas usando a biblioteca `fitz`, e utiliza expressões regulares (Regex) para localizar o padrão "Consultor responsável:"[cite: 9]. Em seguida, cria pastas dinamicamente com os nomes extraídos e move o PDF e seu correspondente `.jpg` para dentro delas[cite: 9].

### 3. Conversor de PDF para JPG (`converter_pdf_jpg.py`)
* **Visão Geral:** Utilitário de rasterização de imagens[cite: 13].
* **Funcionalidades:** Utiliza o método `get_pixmap()` para transformar páginas de documentos em imagens JPG, preservando o nome original do arquivo[cite: 13]. Caso o PDF possua múltiplas páginas, o script automaticamente adiciona uma paginação sequencial (ex: `nome_pag1.jpg`, `nome_pag2.jpg`) para não sobrescrever os dados[cite: 13].

### 4. Filtro de Arquivos via CSV (`organizar_por_planilha.ps1`)
* **Visão Geral:** Script em PowerShell para triagem rápida em sistemas Windows[cite: 10].
* **Funcionalidades:** Lê um arquivo chamado `contratos.csv`, captura a coluna "ID", e compara com todos os arquivos da pasta atual[cite: 10]. Se o nome do arquivo contiver o número do contrato, o arquivo é movido forçadamente (`-Force`) para uma pasta destino chamada "Contratosdaplanilha"[cite: 10]. 

### 5. Divisor de Páginas do Word (`SalvarPaginasComoPDF.vba`)
* **Visão Geral:** Macro desenvolvida em VBA (Visual Basic for Applications) para automação dentro do Microsoft Word[cite: 12].
* **Funcionalidades:** Realiza a contagem total de páginas do documento ativo e faz um loop (laço de repetição) para exportar cada página, uma a uma, gerando arquivos PDF individuais sequenciais (ex: `Pagina_1.pdf`) no mesmo diretório do documento original[cite: 12].
