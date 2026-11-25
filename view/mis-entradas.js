'use strict';

// La API actual de US-007 usa X-Usuario-ID solo como mecanismo de demostración.
// En la integración final debe obtenerse la identidad de una sesión autenticada.
const API_URL = 'http://127.0.0.1:8000/api/mis-entradas';
const boton = document.getElementById('consultar');
const inputUsuario = document.getElementById('usuarioId');
const mensaje = document.getElementById('mensaje');
const tabla = document.getElementById('tablaContenedor');
const filas = document.getElementById('filasEntradas');

function mostrarMensaje(texto, error = false) {
  mensaje.textContent = texto;
  mensaje.className = error ? 'error' : 'vacio';
}

function pintarEntradas(entradas) {
  filas.replaceChildren();
  tabla.hidden = entradas.length === 0;
  for (const entrada of entradas) {
    const fila = document.createElement('tr');
    for (const valor of [entrada.id_entrada, entrada.tipo_entrada, entrada.fecha_adquisicion]) {
      const celda = document.createElement('td');
      celda.textContent = String(valor ?? '');
      fila.appendChild(celda);
    }
    const celdaEstado = document.createElement('td');
    const etiqueta = document.createElement('span');
    etiqueta.textContent = String(entrada.estado ?? 'Sin estado');
    etiqueta.className = 'estado ' + (String(entrada.estado).toLowerCase() === 'valida' ? 'valida' : String(entrada.estado).toLowerCase() === 'cancelada' ? 'cancelada' : '');
    celdaEstado.appendChild(etiqueta);
    fila.appendChild(celdaEstado);
    filas.appendChild(fila);
  }
}

async function consultarEntradas() {
  const usuarioId = inputUsuario.value.trim();
  if (!/^[1-9]\d*$/.test(usuarioId)) {
    pintarEntradas([]);
    mostrarMensaje('Introduce un ID de usuario válido.', true);
    return;
  }
  boton.disabled = true;
  pintarEntradas([]);
  mostrarMensaje('Cargando entradas...');
  try {
    const respuesta = await fetch(API_URL, {headers: {'X-Usuario-ID': usuarioId}});
    if (!respuesta.ok) {
      if (respuesta.status === 401 || respuesta.status === 403) throw new Error('No tienes permiso para consultar estas entradas.');
      throw new Error('No se pudo consultar el listado (error ' + respuesta.status + ').');
    }
    const datos = await respuesta.json();
    const entradas = Array.isArray(datos.entradas) ? datos.entradas : [];
    pintarEntradas(entradas);
    mostrarMensaje(entradas.length ? `Tienes ${entradas.length} entrada(s) adquirida(s).` : (datos.mensaje || 'No tienes entradas adquiridas.'));
  } catch (error) {
    pintarEntradas([]);
    mostrarMensaje(error instanceof TypeError ? 'No se pudo conectar con la API. Comprueba que esté iniciada.' : error.message, true);
  } finally {
    boton.disabled = false;
  }
}

boton.addEventListener('click', consultarEntradas);
