const API_ENTRADAS = 'http://127.0.0.1:8000/api/entradas';

const NOMBRES_ENTRADA = {
    vip: 'Abono VIP',
    abono_completo: 'Abono completo',
    abono_un_dia: 'Abono de un día'
};

function crearElemento(etiqueta, clase, texto) {
    const elemento = document.createElement(etiqueta);

    if (clase) elemento.className = clase;
    if (texto !== undefined) elemento.textContent = texto;

    return elemento;
}

function nombreEntrada(entrada) {
    return NOMBRES_ENTRADA[entrada.nombre]
        || entrada.nombre.replaceAll('_', ' ');
}

function formatoPrecio(precio) {
    return new Intl.NumberFormat('es-ES', {
        style: 'currency',
        currency: 'EUR'
    }).format(precio);
}

function formatoFecha(fecha) {
    if (!fecha) return 'No especificada';

    const valor = new Date(`${fecha}T00:00:00`);

    return Number.isNaN(valor.getTime())
        ? fecha
        : new Intl.DateTimeFormat('es-ES', {
            dateStyle: 'medium'
        }).format(valor);
}

function estaDisponible(entrada) {
    return entrada.estado === 'disponible'
        && entrada.stockDisponible > 0;
}

async function consultarAPI(ruta) {
    const controlador = new AbortController();
    const tiempo = setTimeout(() => controlador.abort(), 10000);

    try {
        const respuesta = await fetch(`${API_ENTRADAS}${ruta}`, {
            headers: { Accept: 'application/json' },
            cache: 'no-store',
            signal: controlador.signal
        });

        const datos = await respuesta.json();

        if (!respuesta.ok) {
            throw new Error(
                datos.mensaje
                || datos.detail
                || 'No se pudo consultar la información.'
            );
        }

        return datos;
    } finally {
        clearTimeout(tiempo);
    }
}

function crearTarjetaEntrada(entrada) {
    const tarjeta = crearElemento('article', 'ticket-card');

    const titulo = crearElemento('h3', '', nombreEntrada(entrada));
    const descripcion = crearElemento(
        'p', 'ticket-description', entrada.descripcion
    );
    const precio = crearElemento(
        'div', 'ticket-price', formatoPrecio(entrada.precio)
    );
    const disponibilidad = crearElemento(
        'p',
        'ticket-stock',
        `${entrada.stockDisponible} entradas disponibles`
    );

    const detalles = crearElemento('div', 'ticket-details');
    detalles.id = `detalle-entrada-${entrada.id}`;
    detalles.hidden = true;
    detalles.setAttribute('role', 'status');
    detalles.setAttribute('aria-live', 'polite');

    const boton = crearElemento(
        'button', 'btn ticket-button', 'Consultar detalles'
    );
    boton.type = 'button';
    boton.setAttribute('aria-expanded', 'false');
    boton.setAttribute('aria-controls', detalles.id);

    let detalleAbierto = false;

    boton.addEventListener('click', async () => {
        if (detalleAbierto) {
            detalles.hidden = true;
            detalleAbierto = false;
            boton.textContent = 'Consultar detalles';
            boton.setAttribute('aria-expanded', 'false');
            return;
        }

        boton.disabled = true;
        boton.textContent = 'Consultando…';

        try {
            // Recuperar los datos actuales de la entrada seleccionada.
            const actual = await consultarAPI(`/${entrada.id}`);

            titulo.textContent = nombreEntrada(actual);
            descripcion.textContent = actual.descripcion;
            precio.textContent = formatoPrecio(actual.precio);
            disponibilidad.textContent = estaDisponible(actual)
                ? `${actual.stockDisponible} entradas disponibles`
                : 'Entrada no disponible actualmente';

            detalles.replaceChildren(
                crearElemento('p', '', `Tipo: ${nombreEntrada(actual)}`),
                crearElemento('p', '', `Descripción: ${actual.descripcion}`),
                crearElemento('p', '', `Precio: ${formatoPrecio(actual.precio)}`),
                crearElemento(
                    'p', '',
                    `Disponibilidad: ${actual.stockDisponible} entradas`
                ),
                crearElemento(
                    'p', '',
                    `Válida desde: ${formatoFecha(actual.fechaInicioValidez)}`
                ),
                crearElemento(
                    'p', '',
                    `Válida hasta: ${formatoFecha(actual.fechaFinValidez)}`
                ),
                crearElemento(
                    'p', '',
                    `Estado: ${estaDisponible(actual) ? 'Disponible' : 'No disponible'}`
                )
            );

            detalleAbierto = true;
            boton.textContent = 'Ocultar detalles';
        } catch (error) {
            detalles.replaceChildren(
                crearElemento(
                    'p',
                    'tickets-error',
                    'No se pudo consultar el detalle. Inténtalo de nuevo.'
                )
            );
            boton.textContent = 'Reintentar detalle';
        } finally {
            detalles.hidden = false;
            boton.setAttribute('aria-expanded', 'true');
            boton.disabled = false;
        }
    });

    tarjeta.append(
        titulo, descripcion, precio,
        disponibilidad, detalles, boton
    );

    return tarjeta;
}

async function cargarEntradasDisponibles() {
    const estado = document.getElementById('tickets-status');
    const error = document.getElementById('tickets-error');
    const lista = document.getElementById('ticket-grid');

    lista.replaceChildren();
    lista.setAttribute('aria-busy', 'true');
    estado.textContent = 'Cargando entradas disponibles…';
    estado.hidden = false;
    error.hidden = true;

    try {
        const entradas = await consultarAPI('/disponibles');

        if (!Array.isArray(entradas)) {
            throw new Error('Respuesta no válida');
        }

        const disponibles = entradas.filter(estaDisponible);

        if (disponibles.length === 0) {
            estado.textContent =
                'En este momento no hay entradas disponibles para el festival.';
            return;
        }

        disponibles.forEach(entrada => {
            lista.appendChild(crearTarjetaEntrada(entrada));
        });

        estado.textContent =
            `${disponibles.length} tipos de entrada disponibles.`;
    } catch (fallo) {
        estado.hidden = true;
        error.textContent =
            'No se han podido cargar las entradas. Comprueba que el servicio está activo. ';
        error.hidden = false;

        const reintentar = crearElemento(
            'button', 'btn', 'Reintentar'
        );
        reintentar.type = 'button';
        reintentar.addEventListener('click', cargarEntradasDisponibles);
        error.appendChild(reintentar);
    } finally {
        lista.setAttribute('aria-busy', 'false');
    }
}

document.addEventListener(
    'DOMContentLoaded', cargarEntradasDisponibles
);