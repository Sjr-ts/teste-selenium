# LabQA Aula 03 — Central de Chamados

Aplicação didática HTML/CSS/JavaScript com testes de interface Selenium + pytest. Sem backend: localStorage apenas para demonstração. Não inserir dados pessoais reais.

## Executar no Windows

Terminal 1 (na pasta `LabQA_Aula3_Chamados`):

```powershell
py -m pip install -r requirements.txt
py -m http.server 8000
```

Abra http://127.0.0.1:8000/index.html

Terminal 2 (na mesma pasta):

```powershell
py -m pytest --html=relatorio.html --self-contained-html
```

Caso a porta 8000 esteja em uso, inicie `py -m http.server 8080` e defina `$env:LABQA_URL="http://127.0.0.1:8080"` no terminal de testes.

`HEADLESS=1` opcional para execução sem janela de navegador. O Chrome deve estar instalado. Selenium Manager normalmente configura o ChromeDriver.

## Organização

- `index.html`: formulário, indicadores e fila de chamados
- `style.css`: aparência responsiva
- `app.js`: validação, criação, pesquisa, filtros, atualização, exclusão e localStorage
- `tests/conftest.py`: fixture de navegador isolado e espera explícita
- `tests/pages.py`: Page Object dos chamados
- `tests/test_chamados.py`: 14 casos executados (12 funções, incluindo 3 variações parametrizadas)
- `docs/Apostila_Aula03_Selenium_Chamados.docx`: guia de aprendizagem

Documentação: https://www.selenium.dev/pt-br/documentation/webdriver/ ; https://docs.pytest.org/en/stable/
