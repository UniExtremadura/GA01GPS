/* US-017: catálogo y consulta de detalles. El backend puede configurarse en API_URL. */
(() => {
  'use strict';

  // Ajusta esta URL a la ruta real del microservicio cuando esté disponible.
  const API_URL = '/api/productos';
  const DEMO_PRODUCTS = [
    { id: 1, nombre: 'Camiseta Subsonic', descripcion: 'Camiseta oficial del festival, algodón cómodo y diseño edición 2026.', precio: 22.5, disponible: true, categoria: 'Ropa', icono: '👕' },
    { id: 2, nombre: 'Tote bag del festival', descripcion: 'Bolsa reutilizable con ilustración exclusiva de Subsonic Festival.', precio: 9.9, disponible: true, categoria: 'Accesorios', icono: '👜' },
    { id: 3, nombre: 'Vaso reutilizable', descripcion: 'Vaso oficial reutilizable para disfrutar de los conciertos.', precio: 4.5, disponible: true, categoria: 'Accesorios', icono: '🥤' },
    { id: 4, nombre: 'Sudadera Subsonic', descripcion: 'Sudadera edición festival, ideal para las noches de conciertos.', precio: 38, disponible: true, categoria: 'Ropa', icono: '🧥' }
  ];

  const grid = document.querySelector('#product-grid');
  const status = document.querySelector('#catalog-status');
  const search = document.querySelector('#product-search');
  const dialog = document.querySelector('#product-dialog');
  let products = [];

  const escapeHTML = (value) => String(value ?? '').replace(/[&<>"']/g, (char) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[char]);
  const money = (value) => {
    const amount = Number(value);
    return Number.isFinite(amount) ? new Intl.NumberFormat('es-ES', { style: 'currency', currency: 'EUR' }).format(amount) : 'Precio no indicado';
  };
  const isAvailable = (item) => item.disponible === true || item.habilitado === true || item.estado === 'disponible';

  function showDetails(product) {
    document.querySelector('#detail-name').textContent = product.nombre || 'Producto';
    document.querySelector('#detail-description').textContent = product.descripcion || 'No hay descripción adicional.';
    document.querySelector('#detail-price').textContent = money(product.precio);
    document.querySelector('#detail-availability').textContent = isAvailable(product) ? 'Disponible en el catálogo.' : 'Actualmente no está disponible.';
    dialog.showModal();
  }

  function render() {
    const query = search.value.trim().toLocaleLowerCase('es');
    const visible = products.filter((item) => isAvailable(item) && `${item.nombre} ${item.descripcion} ${item.categoria || ''}`.toLocaleLowerCase('es').includes(query));
    grid.replaceChildren();
    if (!visible.length) {
      status.textContent = query ? 'No hay productos disponibles que coincidan con la búsqueda.' : 'Ahora mismo no hay productos de merchandising disponibles.';
      const empty = document.createElement('p');
      empty.className = 'empty-state';
      empty.textContent = query ? 'Prueba con otro término de búsqueda.' : 'Vuelve a consultar más adelante.';
      grid.append(empty);
      return;
    }
    status.textContent = `${visible.length} producto${visible.length === 1 ? '' : 's'} disponible${visible.length === 1 ? '' : 's'}.`;
    visible.forEach((item) => {
      const card = document.createElement('article');
      card.className = 'product-card';
      card.innerHTML = `<div class="product-art" aria-hidden="true">${escapeHTML(item.icono || '🎁')}</div><div class="product-content"><p class="eyebrow">${escapeHTML(item.categoria || 'MERCHANDISING')}</p><h3>${escapeHTML(item.nombre || 'Producto')}</h3><p>${escapeHTML(item.descripcion || 'Consulta los detalles del producto.')}</p><div class="card-bottom"><span class="price">${money(item.precio)}</span><button class="details-button" type="button">Ver detalles</button></div></div>`;
      card.querySelector('button').addEventListener('click', () => showDetails(item));
      grid.append(card);
    });
  }

  async function loadProducts() {
    status.textContent = 'Cargando productos…';
    try {
      const response = await fetch(API_URL, { headers: { Accept: 'application/json' } });
      if (!response.ok) throw new Error(`Respuesta ${response.status}`);
      const data = await response.json();
      products = Array.isArray(data) ? data : (data.productos || data.items || []);
    } catch {
      // Datos ficticios: permiten revisar la interfaz mientras el equipo implementa la API.
      products = DEMO_PRODUCTS;
      status.textContent = 'Mostrando productos de demostración; no se pudo consultar el catálogo del servidor.';
    }
    render();
  }

  search.addEventListener('input', render);
  document.querySelector('#close-dialog').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', (event) => { if (event.target === dialog) dialog.close(); });
  loadProducts();
})();
