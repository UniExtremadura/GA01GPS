const API_ADMIN_ESPACIOS = 'http://127.0.0.1:8003/api/admin/espacios';

document.addEventListener('DOMContentLoaded', async () => {
    const lista = document.getElementById('lista-espacios');
    const estado = document.getElementById('estado-espacios');
    const actualizar = document.getElementById('actualizar-espacios');
    const detalle = document.getElementById('detalle-espacio');
    const baja = document.getElementById('baja-espacio');
    const confirmar = document.getElementById('confirmar-baja');
    const cancelar = document.getElementById('cancelar-baja');
    const estadoBaja = document.getElementById('estado-baja');
    const tipos = { escenario: 'Escenario', camping: 'Camping', zona_vip: 'Zona VIP', sala: 'Sala' };
    let espacioSeleccionado;
    let consultaDetalle = 0;

    function elemento(etiqueta, texto, clase) {
        const nodo = document.createElement(etiqueta);
        nodo.textContent = texto;
        if (clase) nodo.className = clase;
        return nodo;
    }

    function estadoEspacio(espacio) {
        if (!espacio.habilitado) return 'Dado de baja';
        return espacio.disponible ? 'Disponible' : 'No disponible';
    }

    async function pedir(ruta = '', method = 'GET') {
        const respuesta = await fetch(API_ADMIN_ESPACIOS + ruta, {
            method,
            headers: { Authorization: `Bearer ${obtenerSesion()?.token || ''}` },
            cache: 'no-store',
            signal: AbortSignal.timeout(10000),
        });
        const datos = await respuesta.json();
        if (respuesta.status === 401) window.location.replace('login.html');
        if (!respuesta.ok) throw new Error(datos.mensaje || 'No se pudo completar la operación.');
        return datos;
    }

    function mostrarError(destino, error) {
        destino.textContent = error instanceof TypeError || error.name === 'TimeoutError'
            ? 'No se pudo conectar con el servicio de espacios. Inténtalo de nuevo.'
            : error.message;
    }

    async function verDetalle(espacio) {
        const consulta = ++consultaDetalle;
        const datos = document.getElementById('datos-espacio');
        const titulo = document.getElementById('nombre-espacio');
        const aviso = document.getElementById('estado-detalle');
        titulo.textContent = espacio.nombre;
        datos.replaceChildren();
        aviso.textContent = 'Consultando detalle…';
        detalle.showModal();
        try {
            const actual = await pedir(`/${espacio.id}`);
            if (!detalle.open || consulta !== consultaDetalle) return;
            titulo.textContent = actual.nombre;
            for (const [campo, valor] of [
                ['Identificador', actual.id], ['Tipo', tipos[actual.tipo] || actual.tipo],
                ['Zona', actual.zona], ['Capacidad', `${actual.capacidad} personas`],
                ['Descripción', actual.descripcion], ['Estado', estadoEspacio(actual)],
            ]) {
                datos.append(elemento('dt', campo), elemento('dd', valor));
            }
            aviso.textContent = '';
        } catch (error) {
            if (detalle.open && consulta === consultaDetalle) mostrarError(aviso, error);
        }
    }

    function solicitarBaja(espacio) {
        espacioSeleccionado = espacio;
        document.getElementById('aviso-baja').textContent =
            `«${espacio.nombre}» dejará de aparecer como disponible en el catálogo público.`;
        estadoBaja.textContent = '';
        baja.showModal();
    }

    async function cargarEspacios(aviso = '') {
        actualizar.disabled = true;
        lista.replaceChildren();
        lista.setAttribute('aria-busy', 'true');
        estado.textContent = 'Consultando espacios…';
        try {
            const espacios = await pedir();
            for (const espacio of espacios) {
                const tarjeta = elemento('article', '', 'espacio-card');
                const ver = elemento('button', 'Ver detalle', 'btn secundaria');
                ver.type = 'button';
                ver.setAttribute('aria-label', `Ver detalle de ${espacio.nombre}`);
                ver.addEventListener('click', () => verDetalle(espacio));
                tarjeta.append(
                    elemento('span', estadoEspacio(espacio)),
                    elemento('h2', espacio.nombre),
                    elemento('p', `${tipos[espacio.tipo] || espacio.tipo} · Zona ${espacio.zona}`),
                    ver,
                );
                if (espacio.habilitado) {
                    const boton = elemento('button', 'Dar de baja', 'btn');
                    boton.type = 'button';
                    boton.style.marginTop = '.65rem';
                    boton.setAttribute('aria-label', `Dar de baja ${espacio.nombre}`);
                    boton.addEventListener('click', () => solicitarBaja(espacio));
                    tarjeta.append(boton);
                }
                lista.append(tarjeta);
            }
            estado.textContent = aviso || (espacios.length ? `Espacios registrados: ${espacios.length}.` : 'No hay espacios registrados.');
        } catch (error) {
            mostrarError(estado, error);
            if (aviso) estado.textContent = `${aviso} ${estado.textContent}`;
        } finally {
            actualizar.disabled = false;
            lista.setAttribute('aria-busy', 'false');
        }
    }

    actualizar.addEventListener('click', () => cargarEspacios());
    cancelar.addEventListener('click', () => baja.close());
    baja.addEventListener('cancel', (evento) => {
        if (confirmar.disabled) evento.preventDefault();
    });
    confirmar.addEventListener('click', async () => {
        confirmar.disabled = cancelar.disabled = true;
        estadoBaja.textContent = 'Guardando la baja…';
        try {
            const espacio = await pedir(`/${espacioSeleccionado.id}`, 'DELETE');
            baja.close();
            await cargarEspacios(`«${espacio.nombre}» se ha dado de baja.`);
        } catch (error) {
            mostrarError(estadoBaja, error);
        } finally {
            confirmar.disabled = cancelar.disabled = false;
        }
    });

    await comprobarAcceso('admin');
    if (!document.getElementById('contenido-privado').hidden) await cargarEspacios();
});
