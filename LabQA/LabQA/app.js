'use strict';
// Laboratório didático: armazenamento local no browser, sem autenticação ou servidor.
const STORAGE_KEY = 'helpdesk_lab_chamados_v3';
const $ = id => document.getElementById(id);
const fields = ['titulo', 'solicitante', 'categoria', 'prioridade', 'descricao'];

function obterChamados() {
  try {
    const dados = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
    return Array.isArray(dados) ? dados : [];
  } catch { return []; }
}
function salvarChamados(chamados) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(chamados));
}
function mostrarMensagem(texto, tipo = '') {
  $('mensagem').textContent = texto;
  $('mensagem').className = 'message ' + tipo;
}
function definirErro(campo, texto = '') {
  $('erro-' + campo).textContent = texto;
  $(campo).classList.toggle('invalid', Boolean(texto));
}
function validarChamado() {
  fields.forEach(campo => definirErro(campo));
  let valido = true;
  const falhar = (campo, texto) => { definirErro(campo, texto); valido = false; };
  if ($('titulo').value.trim().length < 5) falhar('titulo', 'O título deve ter pelo menos 5 caracteres.');
  if ($('solicitante').value.trim().length < 3) falhar('solicitante', 'Informe um solicitante com pelo menos 3 caracteres.');
  if (!$('categoria').value) falhar('categoria', 'Selecione uma categoria.');
  if (!$('prioridade').value) falhar('prioridade', 'Selecione uma prioridade.');
  if ($('descricao').value.trim().length < 10) falhar('descricao', 'A descrição deve ter pelo menos 10 caracteres.');
  return valido;
}
function criarChamado(evento) {
  evento.preventDefault();
  mostrarMensagem('');
  if (!validarChamado()) { mostrarMensagem('Corrija os campos destacados.', 'fail'); return; }
  const chamados = obterChamados();
  const id = String(Date.now()) + '-' + String(Math.floor(Math.random() * 100000));
  chamados.push({
    id,
    titulo: $('titulo').value.trim(), solicitante: $('solicitante').value.trim(),
    categoria: $('categoria').value, prioridade: $('prioridade').value,
    descricao: $('descricao').value.trim(), status: 'Aberto'
  });
  salvarChamados(chamados);
  $('form-chamado').reset();
  fields.forEach(campo => definirErro(campo));
  mostrarMensagem('Chamado aberto com sucesso!', 'ok');
  renderizarChamados();
}
function renderizarChamados() {
  const chamados = obterChamados();
  $('total-chamados').textContent = String(chamados.length);
  $('total-abertos').textContent = String(chamados.filter(c => c.status === 'Aberto').length);
  $('total-concluidos').textContent = String(chamados.filter(c => c.status === 'Concluído').length);
  const termo = $('filtro-texto').value.trim().toLowerCase();
  const status = $('filtro-status').value;
  const filtrados = chamados.filter(c =>
    (c.titulo.toLowerCase().includes(termo) || c.solicitante.toLowerCase().includes(termo)) &&
    (status === 'Todos' || c.status === status)
  );
  const lista = $('lista-chamados');
  lista.replaceChildren();
  if (filtrados.length === 0) {
    const p = document.createElement('p'); p.className = 'empty';
    p.textContent = chamados.length ? 'Nenhum chamado corresponde aos filtros.' : 'Nenhum chamado cadastrado.';
    lista.appendChild(p); return;
  }
  filtrados.forEach(chamado => {
    const card = document.createElement('article'); card.className = 'ticket'; card.dataset.id = chamado.id;
    const titulo = document.createElement('h3'); titulo.textContent = chamado.titulo;
    const info = document.createElement('div'); info.className = 'meta';
    info.textContent = `${chamado.solicitante} • ${chamado.categoria} • Prioridade ${chamado.prioridade}`;
    const descricao = document.createElement('p'); descricao.textContent = chamado.descricao;
    const estado = document.createElement('span'); estado.className = 'badge'; estado.textContent = chamado.status;
    const acoes = document.createElement('div'); acoes.className = 'ticket-actions';
    const seletor = document.createElement('select'); seletor.className = 'status-select';
    seletor.setAttribute('aria-label', 'Status de ' + chamado.titulo);
    ['Aberto','Em andamento','Concluído'].forEach(s => {
      const op = document.createElement('option'); op.value = s; op.textContent = s; seletor.appendChild(op);
    });
    seletor.value = chamado.status;
    const excluir = document.createElement('button'); excluir.type = 'button'; excluir.className = 'delete';
    excluir.textContent = 'Excluir'; excluir.setAttribute('aria-label', 'Excluir ' + chamado.titulo);
    acoes.append(seletor, excluir); card.append(titulo, info, descricao, estado, acoes); lista.appendChild(card);
  });
}
function alterarStatus(id, novoStatus) {
  const chamados = obterChamados();
  const chamado = chamados.find(c => c.id === id);
  if (!chamado || !['Aberto','Em andamento','Concluído'].includes(novoStatus)) return;
  chamado.status = novoStatus; salvarChamados(chamados); renderizarChamados();
}
function excluirChamado(id) {
  salvarChamados(obterChamados().filter(c => c.id !== id));
  mostrarMensagem('Chamado excluído com sucesso.', 'ok');
  renderizarChamados();
}
$('form-chamado').addEventListener('submit', criarChamado);
$('form-chamado').addEventListener('reset', () => {
  setTimeout(() => { fields.forEach(campo => definirErro(campo)); mostrarMensagem(''); }, 0);
});
$('filtro-texto').addEventListener('input', renderizarChamados);
$('filtro-status').addEventListener('change', renderizarChamados);
$('lista-chamados').addEventListener('change', evento => {
  if (evento.target.matches('select.status-select')) {
    alterarStatus(evento.target.closest('.ticket').dataset.id, evento.target.value);
  }
});
$('lista-chamados').addEventListener('click', evento => {
  if (evento.target.matches('button.delete')) excluirChamado(evento.target.closest('.ticket').dataset.id);
});
renderizarChamados();
