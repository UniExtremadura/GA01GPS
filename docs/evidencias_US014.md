# Evidencias de validación — US-014

## Subtarea
Validación de permisos y gestión de servicios.

## Objetivo
Comprobar que solo los administradores pueden gestionar servicios, que los datos se validan y que las modificaciones se reflejan en el catálogo.

## Código revisado
- `serviciosUS013.py`: rutas `/api/admin/servicios`, validación de token y rol, creación, modificación y deshabilitación.
- `view/admin-servicios.js`: interfaz administrativa.
- `tests/test_validacion_us014.py`: pruebas específicas de esta subtarea.

## Comprobaciones automatizadas

| Requisito | Comprobación |
|---|---|
| Permisos de administrador | Se bloquea a visitantes, clientes, tokens inválidos y cabeceras de rol falsificadas |
| Validación de datos | Se rechazan campos vacíos, precio negativo, nombres duplicados y campos no admitidos |
| Modificaciones | Un administrador puede crear, editar y consultar; los cambios aparecen en el catálogo |
| Disponibilidad | Un servicio deshabilitado aparece como no disponible y no puede adquirirse |
| Errores | Un servicio inexistente devuelve 404 y un fallo del verificador de sesión deniega la operación |

## Ejecución local

Desde la carpeta raíz `GA01GPS`:

```bash
python -m unittest discover -s tests -p "test_validacion_us014.py" -v
```

- Fecha: **pendiente de completar**.
- Resultado obtenido en el equipo: **pendiente de ejecutar y registrar**.
- Incidencias encontradas: **pendiente de completar**.

## Alcance y limitaciones
Las pruebas simulan las respuestas del servicio de autenticación de US-002; no sustituyen una prueba de integración real con ese servicio. El catálogo utiliza una lista en memoria y los cambios no persisten después de reiniciar el proceso. La prueba de deshabilitación verifica que no se puede adquirir un servicio deshabilitado, aunque permanezca visible en el listado público.

## Conclusión
Completar tras ejecutar las pruebas en el equipo y registrar cualquier incidencia. No declarar la subtarea terminada si hay fallos sin resolver.
