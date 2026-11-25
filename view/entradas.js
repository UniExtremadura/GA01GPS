(() => {
  'use strict';
  const API = 'http://127.0.0.1:8000/api/entradas';
  const API_USUARIOS = 'http://127.0.0.1:8001/api';
  const NOMBRES = { vip: 'Abono VIP', abono_completo: 'Abono completo', abono_un_dia: 'Abono de un día' };
  const $ = (selector) => document.querySelector(selector);
  let entradas = [];
  let seleccionada = null;
  let mediosPago = [];

  function money(value) { return new Intl.NumberFormat('es-ES', { style: 'currency', currency: 'EUR' }).format(Number(value) || 0); }
  function text(tag, className, value) { const node = document.createElement(tag); if (className) node.className = className; node.textContent = value ?? ''; return node; }
  function session() { try { return JSON.parse(localStorage.getItem('usuario_subsonic') || 'null'); } catch { return null; } }
  function errorMessage(payload, fallback) { return payload?.detail || payload?.mensaje || payload?.message || fallback; }

  function renderTickets() {
    const grid = $('#ticket-grid'); grid.replaceChildren();
    if (!entradas.length) { $('#tickets-status').hidden = false; $('#tickets-status').textContent = 'No hay entradas disponibles ahora mismo.'; return; }
    $('#tickets-status').hidden = true;
    entradas.forEach((entry) => {
      const card = text('article', 'ticket-card');
      card.append(text('span', 'ticket-type', (NOMBRES[entry.nombre] || entry.nombre).toLocaleUpperCase('es-ES')));
      card.append(text('h3', '', NOMBRES[entry.nombre] || entry.nombre));
      card.append(text('p', 'ticket-description', entry.descripcion || 'Entrada válida para el festival.'));
      card.append(text('p', 'ticket-price', money(entry.precio)));
      card.append(text('p', 'ticket-stock', `${entry.stockDisponible} disponibles · ${entry.estado === 'agotada' ? 'Agotada' : 'Disponible'}`));
      const qty = document.createElement('label'); qty.className = 'purchase-quantity-label'; qty.textContent = 'Cantidad';
      const input = document.createElement('input'); input.type = 'number'; input.min = '1'; input.max = String(entry.stockDisponible); input.value = '1'; input.className = 'ticket-quantity'; input.setAttribute('aria-label', `Cantidad de ${NOMBRES[entry.nombre] || entry.nombre}`);
      qty.append(input); card.append(qty);
      const buy = text('button', 'btn purchase-button', 'Adquirir entrada'); buy.type = 'button'; buy.disabled = !entry.stockDisponible;
      buy.addEventListener('click', () => openPurchase(entry, input)); card.append(buy); grid.append(card);
    });
  }

  async function loadTickets() {
    $('#tickets-error').hidden = true;
    try {
      const response = await fetch(`${API}/disponibles`, { headers: { Accept: 'application/json' } });
      const payload = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(errorMessage(payload, `Error ${response.status}`));
      if (!Array.isArray(payload)) throw new Error('La respuesta del servicio no tiene el formato esperado.');
      entradas = payload.filter((entry) => Number(entry.stockDisponible) > 0);
      renderTickets();
    } catch (error) {
      $('#tickets-status').hidden = true; $('#tickets-error').textContent = `No se pudieron cargar las entradas: ${error.message}`; $('#tickets-error').hidden = false;
    }
  }

  async function loadPaymentMethods(userId) {
    const response = await fetch(`${API_USUARIOS}/usuarios/${encodeURIComponent(userId)}/metodos-pago`, { headers: { Accept: 'application/json' } });
    const payload = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(errorMessage(payload, `No se pudieron consultar los métodos de pago (${response.status}).`));
    if (!Array.isArray(payload) || !payload.length) throw new Error('La cuenta no tiene métodos de pago registrados.');
    mediosPago = payload;
  }

  async function openPurchase(entry, quantityInput) {
    const user = session();
    if (!user?.id) { $('#purchase-message').textContent = 'Inicia sesión para adquirir entradas.'; $('#purchase-confirm').disabled = true; seleccionada = entry; updateDialog(entry, 1); $('#purchase-dialog').showModal(); return; }
    seleccionada = entry;
    const quantity = Number(quantityInput.value);
    $('#purchase-confirm').disabled = true;
    $('#purchase-message').textContent = 'Comprobando métodos de pago…';
    updateDialog(entry, quantity);
    $('#purchase-dialog').showModal();
    try {
      await loadPaymentMethods(user.id);
      $('#purchase-message').textContent = `Se usará el método de pago predeterminado de tu cuenta (${mediosPago.find((m) => m.predeterminado)?.tipo || mediosPago[0].tipo}). No se realizará ningún cobro real.`;
      $('#purchase-confirm').disabled = false;
    } catch (error) {
      $('#purchase-message').textContent = `${error.message} Pide que se habilite la consulta de métodos de pago en el microservicio Usuarios.`;
    }
  }

  function updateDialog(entry, quantity) {
    $('#purchase-title').textContent = `Adquirir ${NOMBRES[entry.nombre] || entry.nombre}`;
    $('#purchase-description').textContent = entry.descripcion || 'Entrada para Subsonic Festival.';
    $('#purchase-quantity').value = Number.isInteger(quantity) && quantity > 0 ? quantity : 1;
    $('#purchase-quantity').max = String(entry.stockDisponible);
    $('#purchase-stock').textContent = `Disponibles: ${entry.stockDisponible}`;
    $('#purchase-total').textContent = money(entry.precio * Number($('#purchase-quantity').value));
  }

  async function confirmPurchase() {
    if (!seleccionada) return;
    const user = session();
    const quantity = Number($('#purchase-quantity').value);
    if (!Number.isInteger(quantity) || quantity < 1 || quantity > seleccionada.stockDisponible) {
      $('#purchase-message').textContent = `Indica una cantidad entre 1 y ${seleccionada.stockDisponible}.`; return;
    }
    const method = mediosPago.find((item) => item.predeterminado) || mediosPago[0];
    if (!user?.id || !method?.id) { $('#purchase-message').textContent = 'Falta la sesión o un método de pago válido.'; return; }
    const button = $('#purchase-confirm'); button.disabled = true; button.textContent = 'Procesando…';
    $('#purchase-message').textContent = 'Comprobando disponibilidad y registrando la adquisición…';
    try {
      const response = await fetch(`${API}/comprar`, { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify({ idUsuario: user.id, idTipoEntrada: seleccionada.id, cantidad: quantity, idMetodoPago: method.id }) });
      const result = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(errorMessage(result, `No se pudo completar la compra (${response.status}).`));
      $('#purchase-dialog').close(); showReceipt(result, quantity); await loadTickets();
    } catch (error) { $('#purchase-message').textContent = error.message; }
    finally { button.disabled = false; button.textContent = 'Confirmar adquisición'; }
  }

  function showReceipt(order, quantity) {
    const box = $('#my-purchase'); box.replaceChildren(); box.hidden = false;
    box.append(text('h2', '', '¡Adquisición completada!'));
    box.append(text('p', '', `${quantity} × ${NOMBRES[order.tipoEntrada] || order.tipoEntrada}. Total: ${money(order.precioTotal)}.`));
    box.append(text('p', '', `Compra #${order.idCompra} · ${new Date(order.fechaCompra).toLocaleString('es-ES')}`));
    box.append(text('p', '', 'Las entradas se han asociado a tu cuenta.'));
    box.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }

  $('#purchase-quantity').addEventListener('input', () => { if (seleccionada) { updateDialog(seleccionada, Number($('#purchase-quantity').value)); $('#purchase-confirm').disabled = !mediosPago.length; } });
  $('#purchase-confirm').addEventListener('click', confirmPurchase);
  $('#purchase-cancel').addEventListener('click', () => $('#purchase-dialog').close());
  $('#purchase-dialog').addEventListener('click', (event) => { if (event.target === $('#purchase-dialog')) $('#purchase-dialog').close(); });
  document.addEventListener('DOMContentLoaded', loadTickets);
})();
