/* Gestión de tipos de entrada usando GET/PUT /api/entradas del microservicio existente. */
(() => {
  'use strict';
  const API = 'http://127.0.0.1:8000/api/entradas';
  const $ = (selector) => document.querySelector(selector);
  const rows = $('#ticket-rows');
  const listStatus = $('#list-status');
  const editStatus = $('#edit-status');
  const panel = $('#admin-panel');
  const editor = $('#edit-section');
  let entradas = [];

  function hasAdminAccess() {
    try {
      const session = JSON.parse(localStorage.getItem('usuario_subsonic') || 'null');
      const role = String(session?.rol || session?.tipo || '').toLowerCase();
      return Boolean(session?.token) && ['admin', 'administrador'].includes(role);
    } catch { return false; }
  }

  function escapeHTML(value) {
    return String(value ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  }
  function nombreTipo(value) { return ({ vip: 'Abono VIP', abono_completo: 'Abono completo', abono_un_dia: 'Abono de un día' })[value] || value; }
  function euros(value) { return new Intl.NumberFormat('es-ES', { style: 'currency', currency: 'EUR' }).format(Number(value) || 0); }
  function message(element, text, isError = false) { element.textContent = text; element.classList.toggle('error', isError); }
  function notify(text) {
    const toast = $('#ae-toast'); toast.textContent = text; toast.classList.add('visible');
    window.setTimeout(() => toast.classList.remove('visible'), 3000);
  }

  async function api(path = '', options = {}) {
    const response = await fetch(`${API}${path}`, {
      ...options,
      headers: { Accept: 'application/json', ...(options.body ? { 'Content-Type': 'application/json' } : {}), ...options.headers }
    });
    if (!response.ok) {
      const body = await response.json().catch(() => ({}));
      throw new Error(body.detail || body.mensaje || `Error del servidor (${response.status}).`);
    }
    return response.status === 204 ? null : response.json();
  }

  function renderList() {
    rows.replaceChildren();
    if (!entradas.length) { listStatus.textContent = 'No hay entradas registradas.'; return; }
    listStatus.textContent = `${entradas.length} tipo${entradas.length === 1 ? '' : 's'} de entrada registrado${entradas.length === 1 ? '' : 's'}.`;
    entradas.forEach((entry) => {
      const row = document.createElement('tr');
      const estado = entry.estado === 'disponible' ? 'Disponible' : 'Agotada';
      row.innerHTML = `<td><strong>${escapeHTML(nombreTipo(entry.nombre))}</strong><br><small>${escapeHTML(entry.descripcion || '')}</small></td><td>${euros(entry.precio)}</td><td>${Number(entry.stockTotal)}</td><td>${Number(entry.stockDisponible)}</td><td><span class="ae-pill ${entry.estado === 'disponible' ? '' : 'off'}">${estado}</span></td><td><button type="button" class="ae-button ae-secondary" data-id="${Number(entry.id)}">Ver / editar</button></td>`;
      row.querySelector('button').addEventListener('click', () => openEditor(entry.id));
      rows.append(row);
    });
  }

  async function loadEntries() {
    listStatus.textContent = 'Cargando entradas…';
    $('#reload').disabled = true;
    try { entradas = await api(); renderList(); }
    catch (error) { listStatus.textContent = `No se pudieron cargar las entradas: ${error.message}`; listStatus.classList.add('error'); }
    finally { $('#reload').disabled = false; }
  }

  async function openEditor(id) {
    message(editStatus, 'Cargando información…');
    editor.hidden = false;
    editor.scrollIntoView({ behavior: 'smooth', block: 'start' });
    try {
      const entry = await api(`/${encodeURIComponent(id)}`);
      $('#ticket-id').value = entry.id;
      $('#ticket-name').value = entry.nombre;
      $('#ticket-description').value = entry.descripcion || '';
      $('#ticket-price').value = entry.precio;
      $('#ticket-stock').value = entry.stockTotal;
      $('#ticket-start').value = entry.fechaInicioValidez;
      $('#ticket-end').value = entry.fechaFinValidez;
      $('#stock-hint').textContent = `Disponibles ahora: ${entry.stockDisponible}. El sistema conservará las entradas ya vendidas y recalculará el estado.`;
      $('#edit-title').textContent = `Editar ${nombreTipo(entry.nombre)}`;
      message(editStatus, `Estado actual: ${entry.estado === 'disponible' ? 'disponible' : 'agotada'}.`);
    } catch (error) { message(editStatus, `No se pudo abrir el detalle: ${error.message}`, true); }
  }

  function validForm() {
    const price = Number($('#ticket-price').value);
    const stock = Number($('#ticket-stock').value);
    if (!Number.isFinite(price) || price < 0) throw new Error('El precio debe ser un número igual o superior a cero.');
    if (!Number.isInteger(stock) || stock < 1) throw new Error('El stock total debe ser un entero mayor que cero.');
    if (!$('#ticket-start').value || !$('#ticket-end').value) throw new Error('Indica las fechas de validez.');
    if ($('#ticket-end').value < $('#ticket-start').value) throw new Error('La fecha final no puede ser anterior a la inicial.');
    return { nombre: $('#ticket-name').value, descripcion: $('#ticket-description').value.trim(), precio: price, stockTotal: stock,
      fechaInicioValidez: $('#ticket-start').value, fechaFinValidez: $('#ticket-end').value };
  }

  $('#ticket-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    try {
      const data = validForm();
      const button = $('#ticket-form button[type="submit"]');
      button.disabled = true; message(editStatus, 'Guardando cambios…');
      try {
        await api(`/${encodeURIComponent($('#ticket-id').value)}`, { method: 'PUT', body: JSON.stringify(data) });
        message(editStatus, 'Cambios guardados. Se ha actualizado el stock disponible y el estado.');
        notify('Entrada actualizada correctamente.');
        await loadEntries();
      } finally { button.disabled = false; }
    } catch (error) { message(editStatus, error.message, true); }
  });

  $('#reload').addEventListener('click', loadEntries);
  $('#close-editor').addEventListener('click', () => { editor.hidden = true; });
  document.addEventListener('DOMContentLoaded', () => {
    if (!hasAdminAccess()) { $('#access-denied').hidden = false; return; }
    panel.hidden = false;
    loadEntries();
  });
})();
