/* Interfaz de compra simulada. Conectar API_BASE y las rutas acordadas cuando
   esté disponible el microservicio de Servicios. */
(() => {
  'use strict';

  const API_BASE = 'http://127.0.0.1:8004/api';
  const DEMO_USER_ID = 1;
  const DEMO_SERVICES = [
    { id: 1, nombre: 'Zona de descanso', categoria: 'Bienestar', descripcion: 'Acceso a un espacio tranquilo para descansar entre actuaciones.', precio: 12, disponible: true },
    { id: 2, nombre: 'Taquilla inteligente', categoria: 'Comodidad', descripcion: 'Guarda tus pertenencias de forma segura durante el festival.', precio: 8, disponible: true },
    { id: 3, nombre: 'Consigna premium', categoria: 'Comodidad', descripcion: 'Espacio de consigna ampliado con acceso durante toda la jornada.', precio: 18, disponible: true },
    { id: 4, nombre: 'Lanzadera nocturna', categoria: 'Transporte', descripcion: 'Traslado de vuelta al centro al finalizar los conciertos.', precio: 6, disponible: false }
  ];

  const $ = (selector) => document.querySelector(selector);
  const grid = $('#svc-grid');
  const status = $('#svc-status');
  const ownedStatus = $('#owned-status');
  const ownedList = $('#owned-list');
  const dialog = $('#svc-dialog');
  const search = $('#svc-search');
  const storageKey = `subsonic_servicios_usuario_${DEMO_USER_ID}`;
  let services = [];
  let selected = null;
  let owned = readOwned();

  function readOwned() {
    try { return JSON.parse(localStorage.getItem(storageKey) || '[]'); }
    catch { return []; }
  }

  function escapeHTML(value) {
    return String(value ?? '').replace(/[&<>"']/g, (char) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[char]));
  }

  function renderServices() {
    const query = search.value.trim().toLocaleLowerCase('es');
    const filtered = services.filter((item) => `${item.nombre} ${item.categoria} ${item.descripcion}`.toLocaleLowerCase('es').includes(query));
    grid.innerHTML = '';
    if (!filtered.length) {
      status.textContent = query ? 'No hay servicios que coincidan con la búsqueda.' : 'Ahora mismo no hay servicios disponibles.';
      return;
    }
    status.textContent = `${filtered.length} servicio${filtered.length === 1 ? '' : 's'} encontrado${filtered.length === 1 ? '' : 's'}.`;
    filtered.forEach((item) => {
      const available = item.disponible === true || item.estado === 'disponible' || item.habilitado === true;
      const card = document.createElement('article');
      card.className = 'svc-card';
      card.innerHTML = `<div class="svc-card-top"><span class="svc-tag">${escapeHTML(item.categoria || 'Festival')}</span><span class="${available ? 'svc-available' : 'svc-unavailable'}">${available ? 'Disponible' : 'No disponible'}</span></div><h3>${escapeHTML(item.nombre)}</h3><p>${escapeHTML(item.descripcion || 'Consulta los detalles de este servicio.')}</p><div class="svc-card-bottom"><span class="svc-price">${formatPrice(item.precio)}</span><button class="svc-button" type="button" ${available ? '' : 'disabled'}>Ver detalles</button></div>`;
      card.querySelector('button').addEventListener('click', () => openDetails(item, available));
      grid.append(card);
    });
  }

  function renderOwned() {
    ownedList.innerHTML = '';
    ownedStatus.textContent = owned.length ? `Tienes ${owned.length} servicio${owned.length === 1 ? '' : 's'} asociado${owned.length === 1 ? '' : 's'} a esta cuenta.` : 'Todavía no has añadido servicios.';
    owned.forEach((item) => {
      const li = document.createElement('li');
      li.innerHTML = `<span><strong>${escapeHTML(item.nombre)}</strong><small>Adquirido: ${new Date(item.fecha).toLocaleDateString('es-ES')}</small></span><span class="svc-tag">Activo</span>`;
      ownedList.append(li);
    });
  }

  function formatPrice(value) {
    const price = Number(value);
    return Number.isFinite(price) ? new Intl.NumberFormat('es-ES', { style: 'currency', currency: 'EUR' }).format(price) : 'Precio no indicado';
  }

  function openDetails(item, available) {
    selected = { item, available };
    $('#dialog-title').textContent = item.nombre;
    $('#dialog-description').textContent = item.descripcion || 'No hay descripción adicional.';
    $('#dialog-price').textContent = formatPrice(item.precio);
    $('#dialog-availability').textContent = available ? 'Disponible para añadir a tu cuenta.' : 'Este servicio no está disponible y no se puede adquirir.';
    $('#dialog-buy').disabled = !available;
    dialog.showModal();
  }

  async function acquire() {
    if (!selected?.available || !selected.item) return;
    const item = selected.item;
    const button = $('#dialog-buy');
    button.disabled = true;
    button.textContent = 'Comprobando…';
    try {
      // Se usa el backend si responde; en su ausencia la demo guarda la adquisición localmente.
      const response = await fetch(`${API_BASE}/servicios/adquirir`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ idUsuario: DEMO_USER_ID, idServicio: item.id })
      });
      if (!response.ok) {
        const payload = await response.json().catch(() => ({}));
        throw new Error(payload.detail || payload.mensaje || 'No se pudo completar la adquisición.');
      }
    } catch (error) {
      if (error instanceof TypeError) {
        // Fallback académico hasta que exista el microservicio/ruta acordados.
      } else {
        toast(error.message);
        button.disabled = false;
        button.textContent = 'Añadir a mi cuenta';
        return;
      }
    }
    if (!owned.some((entry) => String(entry.id) === String(item.id))) {
      owned.push({ id: item.id, nombre: item.nombre, fecha: new Date().toISOString() });
      localStorage.setItem(storageKey, JSON.stringify(owned));
      renderOwned();
    }
    dialog.close();
    toast('Servicio añadido correctamente a tu cuenta.');
    button.textContent = 'Añadir a mi cuenta';
  }

  function toast(message) {
    const element = $('#svc-toast');
    element.textContent = message;
    element.classList.add('is-visible');
    window.setTimeout(() => element.classList.remove('is-visible'), 3200);
  }

  async function loadServices() {
    try {
      const response = await fetch(`${API_BASE}/servicios`);
      if (!response.ok) throw new Error('API no disponible');
      const data = await response.json();
      services = Array.isArray(data) ? data : (data.servicios || data.items || []);
      services = services.filter((item) => item.disponible === true || item.estado === 'disponible' || item.habilitado === true);
    } catch {
      // Datos ficticios para que la interfaz pueda revisarse mientras se implementa la API.
      services = DEMO_SERVICES;
    }
    renderServices();
  }

  search.addEventListener('input', renderServices);
  $('#dialog-buy').addEventListener('click', acquire);
  $('#dialog-cancel').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', (event) => { if (event.target === dialog) dialog.close(); });
  renderOwned();
  loadServices();
})();
