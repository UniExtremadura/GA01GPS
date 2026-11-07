// US-014 / SCRUM-69: formulario de alta de servicios.
(() => {
  'use strict';
  const API_BASE = 'http://127.0.0.1:8004/api/admin/servicios';
  const form = document.querySelector('#service-form');
  const feedback = document.querySelector('#feedback');
  const rows = document.querySelector('#service-rows');
  const listStatus = document.querySelector('#list-status');
  const saveButton = document.querySelector('#save-button');
  const fields = {
    nombre: document.querySelector('#name'),
    categoria: document.querySelector('#category'),
    descripcion: document.querySelector('#description'),
    precio: document.querySelector('#price'),
  };
  const errors = {
    nombre: document.querySelector('#name-error'),
    categoria: document.querySelector('#category-error'),
    descripcion: document.querySelector('#description-error'),
    precio: document.querySelector('#price-error'),
  };

  function session() {
    try { return JSON.parse(localStorage.getItem('usuario_subsonic') || 'null'); }
    catch { return null; }
  }
  const currentSession = session();
  if (!currentSession?.token) window.location.replace('login.html');
  else if (currentSession.rol !== 'admin') window.location.replace('perfil.html');

  function headers() {
    return { 'Content-Type': 'application/json', rol_usuario: currentSession?.rol || '' };
  }
  function showMessage(message, isError = false) {
    feedback.textContent = message;
    feedback.classList.toggle('error', isError);
  }
  function validate() {
    let valid = true;
    for (const [key, input] of Object.entries(fields)) {
      errors[key].textContent = '';
      input.removeAttribute('aria-invalid');
      const value = input.value.trim();
      if (!value) {
        errors[key].textContent = 'Este campo es obligatorio.';
        input.setAttribute('aria-invalid', 'true'); valid = false;
      } else if (key === 'nombre' && value.length < 2) {
        errors[key].textContent = 'Introduce al menos 2 caracteres.';
        input.setAttribute('aria-invalid', 'true'); valid = false;
      } else if (key === 'descripcion' && value.length < 5) {
        errors[key].textContent = 'Introduce al menos 5 caracteres.';
        input.setAttribute('aria-invalid', 'true'); valid = false;
      } else if (key === 'precio' && (!Number.isFinite(Number(value)) || Number(value) < 0)) {
        errors[key].textContent = 'Introduce un precio igual o superior a 0.';
        input.setAttribute('aria-invalid', 'true'); valid = false;
      }
    }
    return valid;
  }
  async function request(url, options = {}) {
    const response = await fetch(url, { ...options, headers: headers() });
    const body = await response.json().catch(() => ({}));
    if (!response.ok) {
      const details = body.errores?.map((error) => `${error.campo}: ${error.mensaje}`).join(' · ');
      throw new Error(details || body.detail || body.mensaje || `Error HTTP ${response.status}`);
    }
    return body;
  }
  function euro(value) {
    return new Intl.NumberFormat('es-ES', { style: 'currency', currency: 'EUR' }).format(Number(value));
  }
  async function loadServices() {
    rows.replaceChildren(); listStatus.textContent = 'Cargando servicios…';
    try {
      const services = await request(API_BASE);
      listStatus.textContent = services.length ? `${services.length} servicio(s) registrado(s).` : 'Todavía no hay servicios registrados.';
      for (const service of services) {
        const row = document.createElement('tr');
        for (const value of [service.nombre, service.categoria, euro(service.precio)]) {
          const cell = document.createElement('td'); cell.textContent = value; row.appendChild(cell);
        }
        const state = document.createElement('td');
        state.textContent = service.disponible ? 'Disponible' : 'No disponible';
        state.className = service.disponible ? 'availability' : 'unavailable';
        row.appendChild(state); rows.appendChild(row);
      }
    } catch (error) { listStatus.textContent = `No se pudo cargar el catálogo: ${error.message}`; }
  }
  form.addEventListener('submit', async (event) => {
    event.preventDefault(); showMessage('');
    if (!validate()) { showMessage('Revisa los campos marcados antes de guardar.', true); return; }
    const payload = {
      nombre: fields.nombre.value.trim(),
      categoria: fields.categoria.value.trim(),
      descripcion: fields.descripcion.value.trim(),
      precio: Number(fields.precio.value),
      disponible: document.querySelector('#available').checked,
    };
    saveButton.disabled = true; saveButton.textContent = 'Guardando…';
    try {
      const created = await request(API_BASE, { method: 'POST', body: JSON.stringify(payload) });
      form.reset(); document.querySelector('#available').checked = true;
      showMessage(`Servicio «${created.nombre}» registrado correctamente (ID ${created.id}).`);
      await loadServices();
    } catch (error) { showMessage(error.message, true); }
    finally { saveButton.disabled = false; saveButton.textContent = 'Registrar servicio'; }
  });
  document.querySelector('#reload-button').addEventListener('click', loadServices);
  for (const input of Object.values(fields)) input.addEventListener('input', () => {
    if (input.value.trim()) { input.removeAttribute('aria-invalid'); }
  });
  loadServices();
})();
