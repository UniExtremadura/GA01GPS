// US-002: comprobar sesión, proteger la vista y cerrar sesión.
const API_SESION = 'http://127.0.0.1:8000';

function obtenerSesion() {
  try { return JSON.parse(localStorage.getItem('usuario_subsonic') || 'null'); }
  catch { return null; }
}

async function comprobarAcceso(rolNecesario) {
  const sesion = obtenerSesion();
  if (!sesion?.token) { window.location.replace('login.html'); return; }
  try {
    const respuesta = await fetch(`${API_SESION}/api/privado`, {
      headers: { Authorization: `Bearer ${sesion.token}` }
    });
    if (!respuesta.ok) throw new Error('Sesión no válida');
    const datos = await respuesta.json();
    if (rolNecesario && datos.rol !== rolNecesario) {
      window.location.replace(datos.rol === 'admin' ? 'admin-dashboard.html' : 'perfil.html');
      return;
    }
    document.getElementById('bienvenida').textContent = `Bienvenido, ${datos.nombre}`;
    document.getElementById('contenido-privado').hidden = false;
  } catch {
    localStorage.removeItem('usuario_subsonic');
    window.location.replace('login.html');
  }
}

async function cerrarSesion() {
  const sesion = obtenerSesion();
  try {
    if (sesion?.token) {
      await fetch(`${API_SESION}/api/logout`, {
        method: 'POST', headers: { Authorization: `Bearer ${sesion.token}` }
      });
    }
  } finally {
    localStorage.removeItem('usuario_subsonic');
    window.location.replace('login.html');
  }
}
