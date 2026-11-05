import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .pages import ChamadosPage


def test_CT01_abertura_valida(browser, wait):
    p = ChamadosPage(browser, wait)
    p.abrir()
    p.esperar_total(1)
    assert 'Impressora sem conexão' in p.cards()[0].text
    assert browser.find_element(By.ID, 'total-abertos').text == '1'


def test_CT02_campos_vazios(browser):
    browser.find_element(By.ID, 'btn-criar').click()
    assert 'pelo menos 5' in browser.find_element(By.ID, 'erro-titulo').text
    assert 'Selecione' in browser.find_element(By.ID, 'erro-categoria').text


@pytest.mark.parametrize('titulo', ['A', 'ABCD', '   '])
def test_CT03_titulo_curto_parametrizado(browser, titulo):
    browser.find_element(By.ID, 'titulo').send_keys(titulo)
    browser.find_element(By.ID, 'btn-criar').click()
    assert 'pelo menos 5' in browser.find_element(By.ID, 'erro-titulo').text


def test_CT04_pesquisa_por_titulo(browser, wait):
    p = ChamadosPage(browser, wait)
    p.abrir()
    p.esperar_total(1)
    p.pesquisar('Impressora')
    assert len(p.cards()) == 1
    p.pesquisar('Inexistente')
    assert len(p.cards()) == 0


def test_CT05_pesquisa_por_solicitante(browser, wait):
    p = ChamadosPage(browser, wait)
    p.abrir()
    p.pesquisar('Ana Souza')
    assert len(p.cards()) == 1


def test_CT06_alterar_status(browser, wait):
    p = ChamadosPage(browser, wait)
    p.abrir()
    p.selecionar_status('Em andamento')
    wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '.ticket .badge'), 'Em andamento'))
    p.selecionar_status('Concluído')
    assert browser.find_element(By.ID, 'total-concluidos').text == '1'
    assert browser.find_element(By.ID, 'total-abertos').text == '0'


def test_CT07_filtrar_por_status(browser, wait):
    p = ChamadosPage(browser, wait)
    p.abrir()
    p.filtrar_status('Concluído')
    assert len(p.cards()) == 0
    p.filtrar_status('Aberto')
    assert len(p.cards()) == 1


def test_CT08_excluir_chamado(browser, wait):
    p = ChamadosPage(browser, wait)
    p.abrir()
    p.excluir_primeiro()
    p.esperar_total(0)
    assert 'Nenhum chamado cadastrado' in browser.find_element(By.ID, 'lista-chamados').text


def test_CT09_persistencia_apos_reload(browser, wait):
    p = ChamadosPage(browser, wait)
    p.abrir()
    browser.refresh()
    assert browser.find_element(By.ID, 'total-chamados').text == '1'


def test_CT10_limpar_formulario(browser):
    titulo = browser.find_element(By.ID, 'titulo')
    titulo.send_keys('Título temporário')
    browser.find_element(By.ID, 'btn-limpar').click()
    assert titulo.get_attribute('value') == ''


def test_CT11_html_escapado(browser, wait):
    p = ChamadosPage(browser, wait)
    p.abrir(titulo='<script>alert(1)</script>')
    p.esperar_total(1)
    assert '<script>alert(1)</script>' in p.cards()[0].text
    assert len(browser.find_elements(By.CSS_SELECTOR, '.ticket script')) == 0


def test_CT12_erro_descricao_curta(browser):
    browser.find_element(By.ID, 'descricao').send_keys('curta')
    browser.find_element(By.ID, 'btn-criar').click()
    assert 'pelo menos 10' in browser.find_element(By.ID, 'erro-descricao').text
