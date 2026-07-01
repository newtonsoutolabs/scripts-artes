# 1. Cria a pasta de destino
$destino = ".\Contratosdaplanilha"
if (!(Test-Path $destino)) { New-Item -ItemType Directory -Path $destino }

# 2. Carrega a lista de contratos da planilha (CSV)
# Se o seu CSV usa ponto-e-vírgula, mude o Delimiter para ";"
$listaContratos = Import-Csv -Path ".\contratos.csv" -Header "ID" | Select-Object -ExpandProperty ID

# 3. Pega todos os arquivos da pasta (exceto o script e o csv)
$todosArquivos = Get-ChildItem -File | Where-Object { $_.Name -notmatch "organizar.ps1|contratos.csv" }

# 4. Analisa cada arquivo
foreach ($arquivo in $todosArquivos) {
    foreach ($numero in $listaContratos) {
        # Verifica se o número do contrato existe em qualquer parte do nome do arquivo
        if ($arquivo.Name -like "*$numero*") {
            Write-Host "Localizado: $($arquivo.Name)" -ForegroundColor Yellow
            Move-Item -Path $arquivo.FullName -Destination $destino -Force
            break # Sai do laço interno para não tentar mover o mesmo arquivo duas vezes
        }
    }
}

Write-Host "Concluído! Verifique a pasta 'Contratosdaplanilha'." -ForegroundColor Green