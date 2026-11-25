# US-011 — Validación de permisos y disponibilidad de espacios

## Objetivo
Comprobar los permisos administrativos, la validación de los datos y la actualización de disponibilidad en la API de espacios.

## Código revisado
- `Espacios/main.py`: operaciones administrativas y validación de datos.
- `Espacios/catalogo.py`: consulta pública de espacios disponibles.
- `mainUsuario002.py`: servicio de sesiones utilizado por la API.

## Pruebas automatizadas
Archivo: `tests/test_validacion_us011.py`.

Comando desde la raíz del repositorio:

```bash
python -m unittest discover -s tests -p "test_validacion_us011.py" -v
```

| Caso | Resultado esperado |
| --- | --- |
| Operaciones sin sesión | 401; sin cambios |
| Operaciones de usuario cliente | 403; sin cambios |
| Token no válido | 401 |
| Alta y consulta por administrador | 201 y 200 |
| Capacidad inválida | 400; sin cambios |
| Campos y valores inválidos | 400 |
| Nombre duplicado | 409; sin cambios |
| Cambiar disponibilidad | Actualiza ficha y catálogo público |
| Deshabilitar espacio | Oculto del catálogo y conservado para admin |
| ID inexistente | 404 |
| Servicio de sesiones caído | 503; sin cambios |

## Evidencia de ejecución local
- Fecha: **pendiente de completar**.
- Resultado real de las pruebas: **pendiente de ejecutar y registrar**.
- Captura o registro de salida: **pendiente**.

## Alcance y limitaciones
Las pruebas de permisos simulan la respuesta del servicio de autenticación, por lo que verifican el control de acceso del microservicio de espacios, pero no sustituyen una prueba de integración real con US-002. Los espacios se guardan en memoria y se reinician al reiniciar el servidor; no se demuestra persistencia en base de datos. No marcar esta comprobación como superada en el entorno local sin ejecutar las pruebas.
