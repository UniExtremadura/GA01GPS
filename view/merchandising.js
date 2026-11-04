/* US-017: consulta del catalogo y disponibilidad desde el servicio. */
(() => {
  'use strict';
  const API_URL = 'http://127.0.0.1:8004/api/productos';
  const grid = document.querySelector('#product-grid');
  const status = document.querySelector('#catalog-status');
  const search = document.querySelector('#product-search');
  const dialog = document.querySelector('#product-dialog');
  let products = [];
  let cargado = false;
  let ultimaConsulta = 0;
  let ultimoDetalle = 0;
  const actualizar = document.createElement('button');
  actualizar.type = 'button';
  actualizar.className = 'details-button';
  actualizar.textContent = 'Actualizar disponibilidad';
  status.after(actualizar);

  const escapeHTML = (value) => String(value ?? '').replace(/[&<>"']/g, (char) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[char]);
  const money = (value) => typeof value === 'number' && Number.isFinite(value)
    ? new Intl.NumberFormat('es-ES', { style: 'currency', currency: 'EUR' }).format(value)
    : 'Precio no indicado';

  function disponibilidad(producto) {
    // Un producto habilitado no implica que tenga existencias.
    if (producto.habilitado === false) return { clase: 'no-disponible', texto: 'No disponible', disponible: false };
    if (!Number.isInteger(producto.stockDisponible) || producto.stockDisponible < 0) {
      return { clase: 'sin-confirmar', texto: 'Disponibilidad no confirmada', disponible: false };
    }
    if (producto.stockDisponible === 0) return { clase: 'agotado', texto: 'Sin existencias', disponible: false };
    if (producto.disponible === false || (producto.estado && producto.estado !== 'disponible')) {
      return { clase: 'no-disponible', texto: 'No disponible', disponible: false };
    }
    return { clase: 'disponible', texto: `Disponible · ${producto.stockDisponible} unidad${producto.stockDisponible === 1 ? '' : 'es'}`, disponible: true };
  }

  async function consultar(url) {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 10000);
    try {
      const response = await fetch(url, { headers: { Accept: 'application/json' }, cache: 'no-store', signal: controller.signal });
      const datos = await response.json();
      if (!response.ok) throw new Error(datos.mensaje || datos.detail || 'No se pudo consultar el catálogo.');
      return datos;
    } finally { clearTimeout(timeout); }
  }

  function render() {
    if (!cargado) return;
    const query = search.value.trim().toLocaleLowerCase('es');
    const catalogo = products.filter(item => item.habilitado !== false);
    const visible = catalogo.filter(item => `${item.nombre || ''} ${item.descripcion || ''} ${item.categoria || ''}`.toLocaleLowerCase('es').includes(query));
    const disponibles = visible.filter(item => disponibilidad(item).disponible).length;
    grid.replaceChildren();
    status.classList.remove('error');
    if (!visible.length) {
      status.textContent = query ? 'No hay productos que coincidan con la búsqueda.' : 'Ahora mismo no hay productos de merchandising disponibles.';
    } else if (!disponibles) {
      status.textContent = 'No hay productos disponibles entre los resultados. Consulta el estado de cada artículo o actualiza la disponibilidad.';
    } else {
      status.textContent = `${disponibles} producto${disponibles === 1 ? '' : 's'} disponible${disponibles === 1 ? '' : 's'} de ${visible.length} mostrado${visible.length === 1 ? '' : 's'}.`;
    }
    visible.forEach(item => {
      const estado = disponibilidad(item);
      const card = document.createElement('article');
      card.className = `product-card ${estado.clase}`;
      card.innerHTML = `<div class="product-art" aria-hidden="true">${escapeHTML(item.icono || '♫')}</div><div class="product-content"><p class="eyebrow">${escapeHTML(item.categoria || 'MERCHANDISING')}</p><h3>${escapeHTML(item.nombre || 'Producto')}</h3><p>${escapeHTML(item.descripcion || 'Consulta los detalles del producto.')}</p><p class="availability ${estado.clase}">${escapeHTML(estado.texto)}</p><div class="card-bottom"><span class="price">${money(item.precio)}</span><button class="details-button" type="button">Ver detalles</button></div></div>`;
      card.querySelector('button').addEventListener('click', () => showDetails(item));
      grid.append(card);
    });
  }

  async function showDetails(producto) {
    const consulta = ++ultimoDetalle;
    document.querySelector('#detail-name').textContent = producto.nombre || 'Producto';
    document.querySelector('#detail-description').textContent = '';
    document.querySelector('#detail-price').textContent = '';
    const estado = document.querySelector('#detail-availability');
    estado.textContent = 'Consultando disponibilidad actual…';
    estado.className = 'detail-availability';
    if (!dialog.open) dialog.showModal();
    try {
      const actual = await consultar(`${API_URL}/${encodeURIComponent(producto.id)}`);
      if (consulta !== ultimoDetalle || !dialog.open) return;
      if (!actual || typeof actual !== 'object' || Array.isArray(actual) || actual.id !== producto.id) throw new Error('Respuesta incorrecta');
      products = products.map(item => item.id === actual.id ? actual : item);
      render();
      document.querySelector('#detail-name').textContent = actual.nombre || 'Producto';
      document.querySelector('#detail-description').textContent = actual.descripcion || 'No hay descripción adicional.';
      document.querySelector('#detail-price').textContent = money(actual.precio);
      const info = disponibilidad(actual);
      estado.textContent = info.texto;
      estado.className = `detail-availability ${info.clase}`;
    } catch {
      if (consulta !== ultimoDetalle || !dialog.open) return;
      // No conservar en pantalla una disponibilidad antigua como confirmada.
      products = products.map(item => item.id === producto.id ? { ...item, stockDisponible: null } : item);
      render();
      estado.textContent = 'No se pudo confirmar la disponibilidad. Cierra el detalle y vuelve a consultar, o actualiza el catálogo.';
      estado.className = 'detail-availability sin-confirmar';
    }
  }

  async function loadProducts() {
    const consulta = ++ultimaConsulta;
    ++ultimoDetalle;
    if (dialog.open) dialog.close();
    cargado = false;
    products = [];
    grid.replaceChildren();
    grid.setAttribute('aria-busy', 'true');
    status.classList.remove('error');
    status.textContent = 'Consultando disponibilidad de productos…';
    actualizar.disabled = true;
    try {
      const datos = await consultar(API_URL);
      if (consulta !== ultimaConsulta) return;
      const catalogo = Array.isArray(datos) ? datos : (datos?.productos || datos?.items);
      if (!Array.isArray(catalogo) || catalogo.some(item => !item || typeof item !== 'object' || !Number.isInteger(item.id))) throw new Error('Catálogo incorrecto');
      products = catalogo;
      cargado = true;
      actualizar.textContent = 'Actualizar disponibilidad';
      render();
    } catch {
      if (consulta !== ultimaConsulta) return;
      status.classList.add('error');
      status.textContent = 'No se pudo consultar la disponibilidad del servidor. Comprueba que el servicio Merchandising está iniciado y pulsa Reintentar.';
      actualizar.textContent = 'Reintentar';
    } finally {
      if (consulta === ultimaConsulta) {
        grid.setAttribute('aria-busy', 'false');
        actualizar.disabled = false;
      }
    }
  }

  actualizar.addEventListener('click', loadProducts);
  search.addEventListener('input', render);
  document.querySelector('#close-dialog').addEventListener('click', () => dialog.close());
  dialog.addEventListener('close', () => { ++ultimoDetalle; });
  dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
  loadProducts();
})();
