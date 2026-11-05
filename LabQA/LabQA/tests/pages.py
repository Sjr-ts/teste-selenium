from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

class ChamadosPage:
    def __init__(self, driver, wait):
        self.driver, self.wait = driver, wait

    def abrir(self, titulo='Impressora sem conexão', solicitante='Ana Souza',
              categoria='Hardware', prioridade='Alta', descricao='Impressora não responde na rede.'):
        d = self.driver
        d.find_element(By.ID, 'titulo').send_keys(titulo)
        d.find_element(By.ID, 'solicitante').send_keys(solicitante)
        Select(d.find_element(By.ID, 'categoria')).select_by_visible_text(categoria)
        Select(d.find_element(By.ID, 'prioridade')).select_by_visible_text(prioridade)
        d.find_element(By.ID, 'descricao').send_keys(descricao)
        d.find_element(By.ID, 'btn-criar').click()

    def esperar_total(self, total):
        self.wait.until(EC.text_to_be_present_in_element((By.ID, 'total-chamados'), str(total)))

    def pesquisar(self, termo):
        campo = self.driver.find_element(By.ID, 'filtro-texto')
        campo.clear()
        campo.send_keys(termo)

    def filtrar_status(self, status):
        Select(self.driver.find_element(By.ID, 'filtro-status')).select_by_visible_text(status)

    def selecionar_status(self, status):
        seletor = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.ticket .status-select')))
        Select(seletor).select_by_visible_text(status)

    def excluir_primeiro(self):
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.ticket .delete'))).click()

    def cards(self):
        return self.driver.find_elements(By.CSS_SELECTOR, '.ticket')
