from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

class LoginPage:
    def __init__(self, driver, wait):
        self.driver, self.wait = driver, wait

    def open(self, base_url):
        self.driver.get(base_url + "/login.html")

    def login(self, email, senha):
        self.driver.find_element(By.ID, "login-email").send_keys(email)
        self.driver.find_element(By.ID, "login-senha").send_keys(senha)
        self.driver.find_element(By.ID, "btn-entrar").click()

    def error(self, id):
        return self.driver.find_element(By.ID, id).text

    def login_ok(self):
        self.wait.until(EC.url_contains("index.html"))
        return self.wait.until(EC.visibility_of_element_located((By.ID, "form-cadastro")))

class CadastroPage:
    def __init__(self, driver, wait):
        self.driver, self.wait = driver, wait

    def cadastrar(self, nome, email):
        d = self.driver
        d.find_element(By.ID, "nome").send_keys(nome)
        d.find_element(By.ID, "email").send_keys(email)
        d.find_element(By.ID, "telefone").send_keys("92999999999")
        Select(d.find_element(By.ID, "curso")).select_by_visible_text("Teste de Software")
        d.find_element(By.ID, "senha").send_keys("12345678")
        d.find_element(By.ID, "confirmar-senha").send_keys("12345678")
        d.find_element(By.ID, "termos").click()
        d.find_element(By.ID, "btn-cadastrar").click()

    def esperar_total(self, total):
        self.wait.until(EC.text_to_be_present_in_element((By.ID, "total-registros"), str(total)))

    def buscar(self, texto):
        busca = self.driver.find_element(By.ID, "busca")
        busca.clear()
        busca.send_keys(texto)

    def excluir(self):
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.delete"))).click()
