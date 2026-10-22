'use strict';
const KEY = 'labqa_participantes_v1';
const $ = (id) => document.getElementById(id);
const form = $('form-cadastro');
const required = ['nome','email','curso','senha','confirmar-senha','termos'];
function registros() { try {const data = JSON.parse(localStorage.getItem(KEY) || '[]');return Array.isArray(data) ? data : [];} catch {return [];} }
function salvar(data) {localStorage.setItem(KEY, JSON.stringify(data));}
function erro(id, mensagem='') {$('erro-'+id).textContent=mensagem;const el=$(id); if(el && el.type !== 'checkbox') el.classList.toggle('invalid',Boolean(mensagem));}
function aviso(texto, classe='') {const el=$('mensagem'); el.textContent=texto;el.className='message '+classe;}
function validar() {
  [...required,'telefone'].forEach(id=>erro(id)); let valido=true;
  function falha(id,msg) {erro(id,msg);valido=false;}
  const nome=$('nome').value.trim(),email=$('email').value.trim(),tel=$('telefone').value.trim();
  if(!nome) falha('nome','Informe o nome completo.'); else if(nome.length<3) falha('nome','O nome deve ter pelo menos 3 caracteres.');
  if(!email) falha('email','Informe o e-mail.'); else if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) falha('email','Informe um e-mail válido.');
  else if(registros().some(r=>r.email.toLowerCase()===email.toLowerCase())) falha('email','Este e-mail já está cadastrado.');
  if(tel && !/^[\d\s()+-]{8,20}$/.test(tel)) falha('telefone','Informe um telefone válido.');
  if(!$('curso').value) falha('curso','Selecione um curso.');
  if($('senha').value.length<8) falha('senha','A senha deve conter pelo menos 8 caracteres.');
  if($('confirmar-senha').value!==$('senha').value || !$('confirmar-senha').value) falha('confirmar-senha','As senhas devem ser iguais.');
  if(!$('termos').checked) falha('termos','É necessário aceitar os termos.');
  return valido;
}
function desenhar() {
  const dados=registros();$('total-registros').textContent=String(dados.length);
  const termo=$('busca').value.trim().toLowerCase();const filtrados=dados.filter(p=>p.nome.toLowerCase().includes(termo)||p.email.toLowerCase().includes(termo));
  const lista=$('lista-registros');lista.replaceChildren();
  if(!filtrados.length){const p=document.createElement('p');p.className='empty';p.textContent=termo?'Nenhum resultado encontrado.':'Nenhum participante cadastrado.';lista.append(p);return;}
  filtrados.forEach(p=>{const row=document.createElement('div');row.className='person';row.dataset.email=p.email;const info=document.createElement('div');const strong=document.createElement('strong');strong.textContent=p.nome;const sm=document.createElement('small');sm.textContent=`${p.email} · ${p.curso}`;info.append(strong,sm);const del=document.createElement('button');del.className='delete';del.type='button';del.dataset.delete=p.email;del.textContent='Excluir';del.setAttribute('aria-label','Excluir '+p.nome);row.append(info,del);lista.append(row);});
}
form.addEventListener('submit', e=>{e.preventDefault();aviso('');if(!validar()){aviso('Corrija os campos destacados antes de continuar.','failure');return;}
const p={nome:$('nome').value.trim(),email:$('email').value.trim(),telefone:$('telefone').value.trim(),curso:$('curso').value,criadoEm:new Date().toISOString()};const dados=registros();dados.push(p);salvar(dados);form.reset();required.forEach(id=>erro(id));aviso('Participante cadastrado com sucesso!','success');desenhar();});
form.addEventListener('reset',()=>{setTimeout(()=>{[...required,'telefone'].forEach(id=>erro(id));aviso('');},0);});
$('busca').addEventListener('input',desenhar);
$('lista-registros').addEventListener('click',e=>{const btn=e.target.closest('button[data-delete]');if(!btn)return;const email=btn.dataset.delete;salvar(registros().filter(p=>p.email!==email));aviso('Participante excluído com sucesso.','success');desenhar();});
desenhar();
