// US-014: administración del catálogo de servicios.
(async () => {
  'use strict';
  const api = 'http://127.0.0.1:8004/api/admin/servicios';
  const $ = (selector) => document.querySelector(selector);
  const form = $('#service-form');
  const feedback = $('#feedback');
  const rows = $('#service-rows');
  const status = $('#list-status');
  const save = $('#save-button');
  const reload = $('#reload-button');
  const cancel = $('#cancel-edit');
  const title = $('#form-title');
  const money = new Intl.NumberFormat('es-ES', { style: 'currency', currency: 'EUR' });
  const field = (name) => form.elements.namedItem(name);
  let editingId = null;
  let busy = false;

  function message(text, error = false) {
    feedback.textContent = text;
    feedback.classList.toggle('error', error);
  }

  async function request(path = '', method = 'GET', data) {
    const response = await fetch(api + path, {
      method, cache: 'no-store', signal: AbortSignal.timeout(10000),
      headers: {
        Authorization: 'Bearer ' + (obtenerSesion()?.token || ''),
        ...(data && { 'Content-Type': 'application/json' }),
      },
      body: data && JSON.stringify(data),
    });
    const body = await response.json().catch(() => ({}));
    if (response.status === 401) window.location.replace('login.html');
    if (!response.ok) {
      const details = body.errores?.map((item) => item.campo + ': ' + item.mensaje).join(' · ');
      throw new Error(details || body.detail || body.mensaje || 'No se pudo completar la operación.');
    }
    return body;
  }

  function node(tag, text) {
    const element = document.createElement(tag);
    element.textContent = text;
    return element;
  }

  function resetForm() {
    editingId = null;
    form.reset();
    title.textContent = save.textContent = 'Registrar servicio';
    cancel.hidden = true;
  }

  async function act(operation) {
    if (busy) return;
    busy = save.disabled = reload.disabled = cancel.disabled = true;
    try {
      await operation();
    } catch (error) {
      message(error.message, true);
    } finally {
      busy = save.disabled = reload.disabled = cancel.disabled = false;
    }
  }

  async function viewDetail(id) {
    const service = await request('/' + id);
    $('#detail-title').textContent = service.nombre;
    const data = $('#detail-data');
    data.replaceChildren();
    for (const [key, value] of [
      ['ID', service.id], ['Categoría', service.categoria], ['Descripción', service.descripcion],
      ['Precio', money.format(service.precio)], ['Estado', service.disponible ? 'Disponible' : 'No disponible'],
    ]) data.append(node('dt', key), node('dd', value));
    $('#service-detail').showModal();
  }

  async function startEdit(id) {
    const service = await request('/' + id);
    editingId = id;
    for (const key of ['nombre', 'categoria', 'descripcion', 'precio']) field(key).value = service[key];
    field('disponible').checked = service.disponible;
    title.textContent = 'Editar: ' + service.nombre;
    save.textContent = 'Guardar cambios';
    cancel.hidden = false;
    message('');
    field('nombre').focus();
  }

  async function disableService(service) {
    if (!window.confirm('¿Dar de baja «' + service.nombre + '»? Dejará de ofrecerse en el catálogo público.')) return;
    const updated = await request('/' + service.id, 'DELETE');
    if (editingId === service.id) resetForm();
    message('Servicio «' + updated.nombre + '» dado de baja.');
    await loadServices();
  }

  function action(label, service, operation) {
    const button = node('button', label);
    button.type = 'button';
    button.className = 'secondary';
    button.setAttribute('aria-label', label + ': ' + service.nombre);
    button.addEventListener('click', () => act(operation));
    return button;
  }

  async function loadServices() {
    rows.replaceChildren();
    status.textContent = 'Cargando servicios…';
    try {
      const services = await request();
      for (const service of services) {
        const row = document.createElement('tr');
        const state = node('td', service.disponible ? 'Disponible' : 'No disponible');
        state.className = service.disponible ? 'availability' : 'unavailable';
        const actions = document.createElement('td');
        actions.append(
          action('Ver detalle', service, () => viewDetail(service.id)),
          action('Editar', service, () => startEdit(service.id)),
        );
        if (service.disponible) actions.append(action('Dar de baja', service, () => disableService(service)));
        row.append(node('td', service.nombre), node('td', service.categoria), node('td', money.format(service.precio)), state, actions);
        rows.append(row);
      }
      status.textContent = services.length ? 'Servicios registrados: ' + services.length : 'No hay servicios registrados.';
    } catch (error) {
      status.textContent = 'No se pudo cargar el catálogo: ' + error.message;
    }
  }

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    if (busy) return;
    const id = editingId;
    const data = {
      nombre: field('nombre').value.trim(),
      categoria: field('categoria').value.trim(),
      descripcion: field('descripcion').value.trim(),
      precio: field('precio').valueAsNumber,
      disponible: field('disponible').checked,
    };
    act(async () => {
      message('');
      const service = await request(id === null ? '' : '/' + id, id === null ? 'POST' : 'PUT', data);
      resetForm();
      message('Servicio «' + service.nombre + '» ' + (id === null ? 'registrado' : 'actualizado') + ' correctamente.');
      await loadServices();
    });
  });
  reload.addEventListener('click', () => act(loadServices));
  cancel.addEventListener('click', () => { resetForm(); message(''); });
  await comprobarAcceso('admin');
  if (!$('#contenido-privado').hidden) await act(loadServices);
})();
