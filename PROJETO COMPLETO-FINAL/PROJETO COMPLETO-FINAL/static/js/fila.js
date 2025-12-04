// static/js/fila.js
(() => {
  // conecta ao namespace /fila
  const socket = io({ path: '/socket.io' , transports: ['websocket'] , // configuração padrão
                      // opcional: adicionar query/token se precisar autenticar
                    , autoConnect: true, });

  // Se você estiver usando namespaces explicitamente:
  const ns = io('/fila');

  // melhor usar o namespace object
  const s = ns;

  s.on('connect', () => {
    console.log('Socket conectado, id:', s.id);
  });

  s.on('disconnect', (reason) => {
    console.log('Socket desconectado:', reason);
  });

  s.on('unauthorized', (data) => {
    console.warn('Não autenticado:', data);
    // redireciona para login
    window.location.href = '/login_cadastro_paciente';
  });

  s.on('fila_update', (payload) => {
    // payload: { paciente_nome, empresa_nome, posicao, paciente_id, paciente_classificacao, tempo_medio, ultimos }
    try {
      if (payload.error) {
        console.error('Erro recebido do servidor:', payload);
        return;
      }

      const setText = (id, value) => {
        const el = document.getElementById(id);
        if (el) el.textContent = value ?? '-';
      };

      setText('paciente_nome', payload.paciente_nome ?? '-');
      setText('posicao', payload.posicao ?? '-');
      setText('tempo_medio', payload.tempo_medio ?? '-');
      setText('classificacao', payload.paciente_classificacao ?? '-');

      // ultimos
      const ul = document.getElementById('ultimos_list');
      if (ul && Array.isArray(payload.ultimos)) {
        ul.innerHTML = '';
        payload.ultimos.forEach(u => {
          const li = document.createElement('li');
          li.innerHTML = `<strong>${escapeHtml(u.nome)}</strong> — ${escapeHtml(u.classificacao || '-')} <span class="saida">${escapeHtml(u.saida || '-')}</span>`;
          ul.appendChild(li);
        });
      }
    } catch (e) {
      console.error('Erro ao aplicar update:', e);
    }
  });

  // helper para evitar XSS ao inserir strings
  function escapeHtml(text) {
    if (!text && text !== 0) return '';
    return String(text)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }
})();
