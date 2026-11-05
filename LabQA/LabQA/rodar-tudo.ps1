# Roda tudo do laboratório em um único comando:
# servidor HTTP + pytest (relatorio.html) + abertura do relatório.
# Não altera nenhum arquivo de código do projeto.

$ErrorActionPreference = 'Stop'
$Base = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Base

$py = Join-Path $Base '.venv\Scripts\python.exe'
if (-not (Test-Path $py)) {
    Write-Host '[1/4] Criando ambiente virtual...' -ForegroundColor Cyan
    py -m venv .venv
    & $py -m pip install --upgrade pip -q
    & $py -m pip install -r requirements.txt -q
} else {
    Write-Host '[1/4] Ambiente virtual encontrado.' -ForegroundColor Cyan
}

$port = 8000
$serverStartedHere = $false

Write-Host '[2/4] Verificando servidor HTTP na porta 8000...' -ForegroundColor Cyan
$inUse = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
if (-not $inUse) {
    Start-Process -FilePath $py -ArgumentList '-m', 'http.server', $port -WorkingDirectory $Base -WindowStyle Minimized
    $serverStartedHere = $true
    $deadline = (Get-Date).AddSeconds(30)
    do {
        Start-Sleep -Milliseconds 500
        $ok = Test-NetConnection -ComputerName 127.0.0.1 -Port $port -InformationLevel Quiet -WarningAction SilentlyContinue
    } until ($ok -or (Get-Date) -gt $deadline)
    if (-not $ok) { throw 'Servidor HTTP nao subiu na porta 8000.' }
    Write-Host '       Servidor iniciado.' -ForegroundColor Green
} else {
    Write-Host '       Porta 8000 ja em uso (servidor reutilizado).' -ForegroundColor Green
}

$relatorio = Join-Path $Base 'relatorio.html'
if (Test-Path $relatorio) { Remove-Item $relatorio -Force }

try {
    Write-Host '[3/4] Executando pytest...' -ForegroundColor Cyan
    $args = @('-m', 'pytest', '--html=relatorio.html', '--self-contained-html')
    if ($env:HEADLESS -eq '1') { Write-Host '       (HEADLESS=1)' -ForegroundColor DarkGray }
    & $py @args
    $exit = $LASTEXITCODE
} finally {
    if ($serverStartedHere) {
        Get-CimInstance Win32_Process -Filter "Name='python.exe'" |
            Where-Object { $_.CommandLine -like '*http.server*' } |
            ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
        Write-Host '       Servidor encerrado.' -ForegroundColor DarkGray
    }
}

Write-Host '[4/4] Abrindo relatorio.html...' -ForegroundColor Cyan
if (Test-Path $relatorio) {
    $wsh = New-Object -ComObject WScript.Shell
    [void]$wsh.Run("cmd.exe /c start `"`"$relatorio`"`"", 0, $false)
}

exit $exit
