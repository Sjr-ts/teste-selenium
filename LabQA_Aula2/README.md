# LabQA — Aula 02: Login + Selenium

## Iniciar (Windows, PowerShell)
```powershell
cd LabQA_Aula2
py -m pip install -r requirements.txt
py -m http.server 8000
```
Em outro terminal, na mesma pasta:
```powershell
$env:LABQA_URL="http://127.0.0.1:8000"
py -m pytest --html=relatorio.html --self-contained-html
```
Abra `http://127.0.0.1:8000/login.html` no Chrome.

**Credenciais didáticas:** `professor@labqa.test` / `LabQA@1234`.

Selenium 4 tenta gerenciar o ChromeDriver automaticamente (Selenium Manager); mantenha o Chrome instalado. O navegador aparece durante os testes. Não use `file://` nem a extensão Live Server em porta diferente sem atualizar `LABQA_URL`.

> Sistema de ensino: autenticação somente no JavaScript, sem backend. Não armazene dados pessoais reais nem reutilize esse modelo em produção.

Arquivos: `login.html` (nova interface), `index.html` (cadastro original), `style.css` (visual separado), `app.js` (lógica dos dois fluxos), `tests/conftest.py` (fixtures), `tests/pages.py` (Page Object), `tests/test_login.py` e `tests/test_cadastro.py`.
