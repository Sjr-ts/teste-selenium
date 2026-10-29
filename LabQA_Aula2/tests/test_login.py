from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .pages import LoginPage

VALID_EMAIL = "professor@labqa.test"
VALID_PASSWORD = "LabQA@1234"

def test_login_valido_redireciona(browser, wait):
    pagina = LoginPage(browser, wait)
    pagina.login(VALID_EMAIL, VALID_PASSWORD)
    assert pagina.login_ok().is_displayed()
    assert browser.execute_script("return sessionStorage.getItem('labqa_auth_demo_v2')") == "autenticado"

def test_login_senha_incorreta(browser, wait):
    pagina = LoginPage(browser, wait)
    pagina.login(VALID_EMAIL, "senha_errada")
    wait.until(EC.text_to_be_present_in_element((By.ID, "login-mensagem"), "incorretos"))
    assert "login.html" in browser.current_url

def test_login_campos_vazios(browser, wait):
    browser.find_element(By.ID, "btn-entrar").click()
    pagina = LoginPage(browser, wait)
    assert pagina.error("erro-login-email") == "Informe o e-mail."
    assert pagina.error("erro-login-senha") == "Informe a senha."

def test_email_formato_invalido(browser, wait):
    pagina = LoginPage(browser, wait)
    pagina.login("nao-e-email", "qualquer")
    assert pagina.error("erro-login-email") == "Informe um e-mail válido."

def test_mostrar_ocultar_senha(browser, wait):
    senha = browser.find_element(By.ID, "login-senha")
    botao = browser.find_element(By.ID, "btn-mostrar-senha")
    assert senha.get_attribute("type") == "password"
    botao.click()
    assert senha.get_attribute("type") == "text"
    botao.click()
    assert senha.get_attribute("type") == "password"

def test_logout(browser, wait):
    pagina = LoginPage(browser, wait)
    pagina.login(VALID_EMAIL, VALID_PASSWORD)
    pagina.login_ok()
    browser.find_element(By.ID, "btn-sair").click()
    wait.until(EC.url_contains("login.html"))
    assert browser.execute_script("return sessionStorage.getItem('labqa_auth_demo_v2')") is None
