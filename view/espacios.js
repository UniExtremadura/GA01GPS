const API_ESPACIOS = 'http://127.0.0.1:8003/api/espacios';

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('espacios-form');
    const lista = document.getElementById('espacios-lista');
    const feedback = document.getElementById('espacios-feedback');
    const filtrar = document.getElementById('filtrar');
    const reintentar = document.getElementById('reintentar');
    const dialog = document.getElementById('espacio-detalle');
    const tipos = { escenario: 'Escenario', camping: 'Camping', zona_vip: 'Zona VIP', sala: 'Sala' };
    let consultaActual = 0;

    function mensaje(texto, error = false) {
        feedback.textContent = texto;
        feedback.classList.toggle('error', error);
    }

    async function pedir(url, opciones = {}) {
        const controller = new AbortController();
        const timeout = setTimeout(() => controller.abort(), 10000);
        try {
            const respuesta = await fetch(url, { ...opciones, cache: 'no-store', signal: controller.signal });
            const datos = await respuesta.json();
            if (!respuesta.ok) {
                const error = new Error(datos.mensaje || 'No se pudo completar la operación.');
                error.status = respuesta.status;
                throw error;
            }
            return datos;
        } catch (error) {
            if (error.name === 'AbortError' || error instanceof TypeError) {
                throw new Error('No se pudo conectar con el servicio de espacios. Comprueba que está iniciado y reintenta.');
            }
            throw error;
        } finally {
            clearTimeout(timeout);
        }
    }

    function crearElemento(etiqueta, texto, clase) {
        const elemento = document.createElement(etiqueta);
        elemento.textContent = texto;
        if (clase) elemento.className = clase;
        return elemento;
    }

    const reservaDialogo = document.getElementById('espacio-reserva');
    const reservaForm = document.getElementById('reserva-form');
    const franja = document.getElementById('reserva-franja');
    const estadoReserva = document.getElementById('reserva-feedback');
    const accesoReserva = document.getElementById('reserva-acceso');
    const consultar = document.getElementById('reserva-consultar');
    const confirmar = document.getElementById('reserva-confirmar');
    const cerrar = document.getElementById('reserva-cerrar');
    let espacioReserva;

    function abrirReserva(espacio) {
        espacioReserva = espacio;
        reservaForm.reset();
        franja.disabled = false;
        consultar.hidden = confirmar.hidden = false;
        confirmar.disabled = true;
        accesoReserva.hidden = true;
        cerrar.textContent = 'Cancelar';
        estadoReserva.textContent = '';
        document.getElementById('reserva-espacio').textContent =
            `${espacio.nombre} · Zona ${espacio.zona} · ${espacio.capacidad} personas`;
        reservaDialogo.showModal();
    }

    async function tramitarReserva(esConfirmacion) {
        if (cerrar.disabled || !reservaForm.reportValidity()) return;
        const datos = Object.fromEntries(new FormData(reservaForm));
        if (datos.horaInicio >= datos.horaFin) {
            estadoReserva.textContent = 'La hora de fin debe ser posterior a la de inicio.';
            confirmar.disabled = true;
            return;
        }
        const token = obtenerSesion()?.token;
        if (esConfirmacion && !token) {
            estadoReserva.textContent = 'Inicia sesión para confirmar la reserva.';
            accesoReserva.hidden = false;
            return;
        }

        franja.disabled = consultar.disabled = confirmar.disabled = cerrar.disabled = true;
        accesoReserva.hidden = true;
        estadoReserva.textContent = esConfirmacion ? 'Confirmando reserva…' : 'Consultando disponibilidad…';
        const url = `${API_ESPACIOS}/${espacioReserva.id}`;
        let guardada = false;
        try {
            if (esConfirmacion) {
                const reserva = await pedir(`${url}/reservas`, {
                    method: 'POST',
                    headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
                    body: JSON.stringify(datos)
                });
                guardada = true;
                estadoReserva.textContent =
                    `Reserva #${reserva.idReserva} confirmada: ${reserva.nombreEspacio}, ${reserva.fecha} de ${reserva.horaInicio} a ${reserva.horaFin}.`;
                consultar.hidden = confirmar.hidden = true;
                cerrar.textContent = 'Cerrar';
            } else {
                const { disponible } = await pedir(`${url}/disponibilidad?${new URLSearchParams(datos)}`);
                confirmar.disabled = !disponible;
                estadoReserva.textContent = disponible
                    ? 'Franja disponible. Ya puedes confirmar la reserva.'
                    : 'El espacio ya está reservado en esa franja. Elige otro horario.';
            }
        } catch (error) {
            estadoReserva.textContent = error.message;
            accesoReserva.hidden = error.status !== 401;
        } finally {
            franja.disabled = guardada;
            consultar.disabled = cerrar.disabled = false;
        }
    }

    reservaForm.addEventListener('input', () => {
        confirmar.disabled = true;
        accesoReserva.hidden = true;
        estadoReserva.textContent = '';
    });
    consultar.addEventListener('click', () => tramitarReserva(false));
    reservaForm.addEventListener('submit', (evento) => {
        evento.preventDefault();
        if (!confirmar.disabled) tramitarReserva(true);
    });
    cerrar.addEventListener('click', () => reservaDialogo.close());
    reservaDialogo.addEventListener('cancel', (evento) => {
        if (cerrar.disabled) evento.preventDefault();
    });

    async function abrirDetalle(id, boton) {
        boton.disabled = true;
        boton.textContent = 'Cargando…';
        try {
            // Se consulta de nuevo: no se reutiliza una disponibilidad antigua.
            const espacio = await pedir(`${API_ESPACIOS}/${id}`);
            document.getElementById('detalle-titulo').textContent = espacio.nombre;
            document.getElementById('detalle-descripcion').textContent = espacio.descripcion;
            const datos = document.getElementById('detalle-datos');
            datos.replaceChildren();
            for (const [titulo, valor] of [
                ['Identificador', espacio.id], ['Tipo', tipos[espacio.tipo] || espacio.tipo],
                ['Zona', espacio.zona], ['Capacidad', `${espacio.capacidad} personas`],
                ['Estado', 'Disponible']
            ]) {
                datos.append(crearElemento('dt', titulo), crearElemento('dd', valor));
            }
            dialog.showModal();
        } catch (error) {
            mensaje(error.message, true);
            reintentar.hidden = false;
        } finally {
            boton.disabled = false;
            boton.textContent = 'Ver detalle';
        }
    }

    async function cargarEspacios() {
        if (!form.reportValidity()) return;
        const consulta = ++consultaActual;
        lista.replaceChildren();
        lista.setAttribute('aria-busy', 'true');
        filtrar.disabled = true;
        reintentar.hidden = true;
        mensaje('Consultando espacios…');
        const parametros = new URLSearchParams();
        for (const [campo, valor] of new FormData(form)) {
            if (String(valor).trim()) parametros.set(campo, String(valor).trim());
        }
        try {
            const espacios = await pedir(`${API_ESPACIOS}?${parametros}`);
            if (consulta !== consultaActual) return;
            if (!Array.isArray(espacios)) throw new Error('La respuesta del servicio no es válida.');
            mensaje(espacios.length ? `${espacios.length} espacio(s) disponible(s).` : 'No hay espacios disponibles que cumplan los filtros seleccionados. Puedes limpiar los filtros.');
            for (const espacio of espacios) {
                const tarjeta = crearElemento('article', '', 'espacio-card');
                const boton = crearElemento('button', 'Ver detalle', 'btn secundaria');
                boton.type = 'button';
                boton.setAttribute('aria-label', `Ver detalle de ${espacio.nombre}`);
                boton.addEventListener('click', () => abrirDetalle(espacio.id, boton));
                const reservar = crearElemento('button', 'Reservar', 'btn');
                reservar.type = 'button';
                reservar.setAttribute('aria-label', `Reservar ${espacio.nombre}`);
                reservar.addEventListener('click', () => abrirReserva(espacio));
                tarjeta.append(
                    crearElemento('span', 'DISPONIBLE', 'disponible'),
                    crearElemento('h2', espacio.nombre),
                    crearElemento('p', `${tipos[espacio.tipo] || espacio.tipo} · Zona ${espacio.zona}`),
                    crearElemento('p', `Capacidad: ${espacio.capacidad} personas`),
                    crearElemento('p', espacio.descripcion), boton, reservar
                );
                lista.append(tarjeta);
            }
        } catch (error) {
            if (consulta !== consultaActual) return;
            lista.replaceChildren();
            mensaje(error.message, true);
            reintentar.hidden = false;
        } finally {
            if (consulta === consultaActual) {
                lista.setAttribute('aria-busy', 'false');
                filtrar.disabled = false;
            }
        }
    }

    form.addEventListener('submit', (evento) => { evento.preventDefault(); cargarEspacios(); });
    form.addEventListener('reset', () => setTimeout(cargarEspacios, 0));
    reintentar.addEventListener('click', cargarEspacios);
    cargarEspacios();
});
