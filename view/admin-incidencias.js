// US-019: seguimiento administrativo de incidencias.
const API_INCIDENCIAS = 'http://127.0.0.1:8000';
const filas = document.getElementById('filas');
const mensaje = document.getElementById('mensaje');
const filtro = document.getElementById('filtro');

function tokenActual() {
  try { return JSON.parse(localStorage.getItem('usuario_subsonic') || 'null')?.token; }
  catch { return null; }
}

async function solicitar(ruta, opciones = {}) {
  const token = tokenActual();
  if (!token) { window.location.replace('login.html'); throw new Error('Debes iniciar sesión'); }
  const respuesta = await fetch(API_INCIDENCIAS + ruta, {
    ...opciones,
    headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json', ...(opciones.headers || {}) }
  });
  const datos = await respuesta.json().catch(() => ({}));
  if (!respuesta.ok) {
    if (respuesta.status === 401) { localStorage.removeItem('usuario_subsonic'); window.location.replace('login.html'); }
    throw new Error(typeof datos.detail === 'string' ? datos.detail : `Error HTTP ${respuesta.status}`);
  }
  return datos;
}

function celda(fila, valor) {
  const td = document.createElement('td');
  td.textContent = String(valor);
  fila.appendChild(td);
  return td;
}

async function cargarIncidencias() {
  mensaje.textContent = '';
  filas.replaceChildren();
  try {
    const query = filtro.value ? `?estado=${encodeURIComponent(filtro.value)}` : '';
    const incidencias = await solicitar(`/api/admin/incidencias${query}`);
    if (!incidencias.length) {
      const tr = document.createElement('tr');
      const td = celda(tr, 'No hay incidencias para este filtro'); td.colSpan = 7;
      filas.appendChild(tr);
      return;
    }
    for (const incidencia of incidencias) {
      const tr = document.createElement('tr');
      celda(tr, incidencia.idIncidencia);
      celda(tr, incidencia.idUsuario);
      celda(tr, incidencia.titulo);
      celda(tr, incidencia.descripcion);
      celda(tr, incidencia.fechaRegistro);
      const estado = celda(tr, incidencia.estado);
      estado.className = incidencia.estado === 'Pendiente' ? 'pendiente' : 'resuelta';
      const accion = document.createElement('td');
      const boton = document.createElement('button');
      boton.type = 'button';
      const nuevoEstado = incidencia.estado === 'Pendiente' ? 'Resuelta' : 'Pendiente';
      boton.textContent = `Marcar como ${nuevoEstado.toLowerCase()}`;
      boton.addEventListener('click', async () => {
        boton.disabled = true;
        try {
          await solicitar(`/api/admin/incidencias/${incidencia.idIncidencia}`, {
            method: 'PATCH', body: JSON.stringify({ estado: nuevoEstado })
          });
          await cargarIncidencias();
          mensaje.textContent = 'Estado actualizado correctamente.';
        } catch (error) { mensaje.textContent = error.message; boton.disabled = false; }
      });
      accion.appendChild(boton); tr.appendChild(accion); filas.appendChild(tr);
    }
  } catch (error) { mensaje.textContent = error.message; }
}

filtro.addEventListener('change', cargarIncidencias);
document.getElementById('recargar').addEventListener('click', cargarIncidencias);
cargarIncidencias();
