const API_REGISTRO = 'http://127.0.0.1:8001/api/usuarios';

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('registro-form');
    const feedback = document.getElementById('registro-feedback');
    const submitButton = document.getElementById('registro-submit');

    if (!form || !feedback || !submitButton) return;

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        feedback.textContent = '';
        feedback.className = 'registro-feedback';

        if (!form.reportValidity()) return;

        const datos = new FormData(form);
        const nombre = String(datos.get('nombre') || '').trim();
        const apellidos = String(datos.get('apellidos') || '').trim();
        const email = String(datos.get('email') || '').trim().toLowerCase();
        const password = String(datos.get('password') || '');

        if (!nombre || !apellidos || !email || !password.trim()) {
            mostrarError('Completa todos los campos obligatorios.');
            return;
        }

        const solicitud = {
            nombre,
            apellidos,
            email,
            password,
            tipo: 'cliente'
        };

        const telefono = String(datos.get('telefono') || '').trim();
        const fechaNacimiento = String(datos.get('fechaNacimiento') || '').trim();

        if (telefono) solicitud.telefono = telefono;
        if (fechaNacimiento) solicitud.fechaNacimiento = fechaNacimiento;

        submitButton.disabled = true;
        submitButton.textContent = 'Creando cuenta…';

        try {
            const respuesta = await fetch(API_REGISTRO, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(solicitud)
            });

            const resultado = await respuesta.json().catch(() => ({}));

            if (respuesta.status === 409) {
                mostrarError('Ese correo electrónico ya está registrado.');
                return;
            }

            if (!respuesta.ok) {
                mostrarError(resultado.mensaje || 'No se pudo crear la cuenta. Revisa los datos e inténtalo de nuevo.');
                return;
            }

            feedback.textContent = 'La cuenta se ha creado correctamente.';
            feedback.classList.add('registro-exito');
            form.reset();
        } catch (error) {
            mostrarError('No se pudo conectar con el servicio de registro. Inténtalo de nuevo más tarde.');
        } finally {
            submitButton.disabled = false;
            submitButton.textContent = 'Crear cuenta';
        }
    });

    function mostrarError(mensaje) {
        feedback.textContent = mensaje;
        feedback.classList.add('registro-error');
    }
});
