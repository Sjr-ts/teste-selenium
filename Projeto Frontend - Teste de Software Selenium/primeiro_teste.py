
from selenium import webdriver # Biblioteca para automação de testes
from selenium.webdriver.common.by import By

### 
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
####

# 1. Iniciar o Chrome
driver = webdriver.Chrome()

try:
    
    # 2. Abrir o formulário
    driver.get("http://127.0.0.1:5500/frontend/index.html")
    
    driver.maximize_window() # Maximizar a janela do navegador

    # 3. Consultar o título
    print("Título:", driver.title)

    # 4. Preencher o nome
    nome = driver.find_element(By.ID, "nome")
    nome.send_keys("Ana Oliveira")

    # 5. Preencher e-mail
    email = driver.find_element(By.ID, "email")
    email.send_keys("ana@exemplo.com")

    # 6. Preencher telefone
    telefone = driver.find_element(By.ID, "telefone")
    telefone.send_keys("92999999999")

    # 7. Selecionar curso
    curso = Select(driver.find_element(By.ID, "curso"))
    curso.select_by_visible_text("Teste de Software")

    # 8. Preencher senhas
    driver.find_element(By.ID, "senha").send_keys("12345678")
    driver.find_element(By.ID, "confirmar-senha").send_keys("12345678")

    # 9. Aceitar termos
    driver.find_element(By.ID, "termos").click()

    # 10. Clicar em cadastrar
    driver.find_element(By.ID, "btn-cadastrar").click()

    # 11. Aguardar o resultado
    wait = WebDriverWait(driver, 10)
    wait.until(
        lambda d: d.find_element(
            By.ID, "total-registros"
        ).text == "1"
    )

    # 12. Validar o cadastro
    total = driver.find_element(By.ID, "total-registros").text
    lista = driver.find_element(By.ID, "lista-registros").text

    assert total == "1"
    assert "Ana Oliveira" in lista

    print("TESTE APROVADO: participante cadastrado!")

finally:
    # 13. Encerrar navegador
    driver.quit()
