// static/js/socket-client.js
var socket = io();

socket.on('connect', function() {
  console.log('Socket conectado');
});

socket.on('update_fila', function(data) {
  // quando receber atualização, você pode atualizar a UI.
  // a forma mais simples: recarregar a parte necessária ou a página
  console.log('update_fila recebido', data);
  // se a página atual for lista-pacientes ou tela do paciente, recarrega
  if (window.location.pathname.includes('/lista-pacientes') || window.location.pathname.includes('/fila')) {
    location.reload();
  }
  // para tela-principal-estabelecimento recarrega tambem
  if (window.location.pathname.includes('/tela-principal-estabelecimento')) {
    location.reload();
  }
});
