from selenium.webdriver.common.by import By
from .pages import LoginPage, CadastroPage


def acessar(browser, wait):
    login = LoginPage(browser, wait)
    login.login("professor@labqa.test", "LabQA@1234")
    login.login_ok()
    return CadastroPage(browser, wait)

def test_cadastrar_e_buscar_participante(browser, wait):
    pagina = acessar(browser, wait)
    pagina.cadastrar("Ana Oliveira", "ana@exemplo.com")
    pagina.esperar_total(1)
    pagina.buscar("Ana")
    assert "Ana Oliveira" in browser.find_element(By.ID, "lista-registros").text

def test_impedir_email_duplicado(browser, wait):
    pagina = acessar(browser, wait)
    pagina.cadastrar("Ana Oliveira", "ana@exemplo.com")
    pagina.esperar_total(1)
    pagina.cadastrar("Outra Pessoa", "ana@exemplo.com")
    assert browser.find_element(By.ID, "erro-email").text == "Este e-mail já está cadastrado."
    assert browser.find_element(By.ID, "total-registros").text == "1"

def test_excluir_participante(browser, wait):
    pagina = acessar(browser, wait)
    pagina.cadastrar("Ana Oliveira", "ana@exemplo.com")
    pagina.esperar_total(1)
    pagina.excluir()
    pagina.esperar_total(0)
    assert "Nenhum participante cadastrado" in browser.find_element(By.ID, "lista-registros").text
