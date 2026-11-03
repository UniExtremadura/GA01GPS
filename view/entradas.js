const API_ENTRADAS_DISPONIBLES = 'http://127.0.0.1:8000/api/entradas/disponibles';

const NOMBRES_ENTRADA = {
    vip: 'Abono VIP',
    abono_completo: 'Abono completo',
    abono_un_dia: 'Abono de un día'
};

const ICONOS_ENTRADA = {
    vip: '✧',
    abono_completo: '✦',
    abono_un_dia: '◷'
};

function crearElemento(etiqueta, clase, texto) {
    const elemento = document.createElement(etiqueta);
    if (clase) elemento.className = clase;
    if (texto !== undefined) elemento.textContent = texto;
    return elemento;
}

function formatoFecha(fecha) {
    if (!fecha) return 'No especificada';
    const valor = new Date(`${fecha}T00:00:00`);
    return Number.isNaN(valor.getTime())
        ? fecha
        : new Intl.DateTimeFormat('es-ES', { dateStyle: 'medium' }).format(valor);
}

function crearTarjetaEntrada(entrada) {
    const nombre = NOMBRES_ENTRADA[entrada.nombre] || entrada.nombre.replaceAll('_', ' ');
    const tarjeta = crearElemento('article', 'ticket-card');
    tarjeta.setAttribute('aria-labelledby', `ticket-title-${entrada.id}`);

    const lineaSuperior = crearElemento('div', 'ticket-topline');
    lineaSuperior.append(
        crearElemento('span', 'ticket-icon', ICONOS_ENTRADA[entrada.nombre] || '♫'),
        crearElemento('span', 'ticket-type', nombre.toLocaleUpperCase('es-ES'))
    );

    const titulo = crearElemento('h3', '', nombre);
    titulo.id = `ticket-title-${entrada.id}`;

    const descripcion = crearElemento(
        'p',
        'ticket-description',
        entrada.descripcion || 'Entrada disponible para el festival.'
    );

    const precioTexto = new Intl.NumberFormat('es-ES', { style: 'currency', currency: 'EUR' }).format(entrada.precio);
    const precio = crearElemento('div', 'ticket-price', precioTexto);
    precio.appendChild(crearElemento('span', '', 'Precio por entrada'));

    const disponibilidad = crearElemento(
        'p',
        'ticket-stock',
        `${entrada.stockDisponible} ${entrada.stockDisponible === 1 ? 'entrada disponible' : 'entradas disponibles'}`
    );

    const detalleId = `ticket-details-${entrada.id}`;
    const detalles = crearElemento('div', 'ticket-details');
    detalles.id = detalleId;
    detalles.hidden = true;
    detalles.append(
        crearElemento('p', '', `Tipo: ${nombre}`),
        crearElemento('p', '', `Precio: ${precioTexto}`),
        crearElemento('p', '', `Disponibilidad: ${entrada.stockDisponible} entradas`),
        crearElemento('p', '', `Válida desde: ${formatoFecha(entrada.fechaInicioValidez)}`),
        crearElemento('p', '', `Válida hasta: ${formatoFecha(entrada.fechaFinValidez)}`),
        crearElemento('p', '', `Estado: ${entrada.estado === 'disponible' ? 'Disponible' : entrada.estado}`)
    );

    const botonDetalle = crearElemento('button', 'btn ticket-button', 'Consultar detalles');
    botonDetalle.type = 'button';
    botonDetalle.setAttribute('aria-expanded', 'false');
    botonDetalle.setAttribute('aria-controls', detalleId);
    botonDetalle.addEventListener('click', () => {
        const mostrar = detalles.hidden;
        detalles.hidden = !mostrar;
        botonDetalle.setAttribute('aria-expanded', String(mostrar));
        botonDetalle.textContent = mostrar ? 'Ocultar detalles' : 'Consultar detalles';
    });

    tarjeta.append(lineaSuperior, titulo, descripcion, precio, disponibilidad, detalles, botonDetalle);
    return tarjeta;
}

async function cargarEntradasDisponibles() {
    const estado = document.getElementById('tickets-status');
    const error = document.getElementById('tickets-error');
    const lista = document.getElementById('ticket-grid');

    try {
        const respuesta = await fetch(API_ENTRADAS_DISPONIBLES, {
            headers: { Accept: 'application/json' }
        });
        if (!respuesta.ok) throw new Error(`El servidor respondió con estado ${respuesta.status}`);

        const entradas = await respuesta.json();
        if (!Array.isArray(entradas)) throw new Error('La respuesta del servidor no tiene el formato esperado.');

        lista.replaceChildren();
        estado.hidden = true;
        error.hidden = true;

        if (entradas.length === 0) {
            estado.textContent = 'En este momento no hay entradas disponibles para el festival.';
            estado.hidden = false;
            return;
        }

        entradas.forEach((entrada) => lista.appendChild(crearTarjetaEntrada(entrada)));
    } catch (fallo) {
        console.error('No se pudieron cargar las entradas disponibles:', fallo);
        estado.hidden = true;
        error.textContent = 'No se han podido cargar las entradas. Comprueba que el servicio de entradas esté activo e inténtalo de nuevo.';
        error.hidden = false;
    }
}

document.addEventListener('DOMContentLoaded', cargarEntradasDisponibles);
