# US-009 - Consulta y filtrado de espacios disponibles

Referencia: `docs/specs/EP-003-espacios/spec.md`, criterios US-009-AC-01 a AC-06.

## Archivos que se añaden

- `Espacios/`: microservicio FastAPI, modelos, catálogo ficticio y dependencias.
- `view/espacios.html`, `view/espacios.js`, `view/espacios.css`: interfaz de consulta.
- `tests/test_espacios.py`, `tests/test_api.py`: pruebas de consultas y HTTP.
- Este documento: ejecución, decisiones y comprobaciones manuales.

Copiar estas carpetas a la raíz del repositorio, conservando los archivos existentes.
No se modifica `Usuarios/main.py`, `view/style.css`, `view/registro.html` ni el README raíz.
Para enlazar esta página desde el menú existente, añadir un enlace a `espacios.html`
en los HTML del equipo. No se requiere ese cambio para abrir directamente la página.

## Decisiones de implementación

Se sigue el código de referencia de US-001 leído en el commit `4d64833`:
microservicio FastAPI, modelos Pydantic, CORS para 5500/8080,
errores `{codigo, mensaje}`, HTML y JavaScript sin frameworks, datos provisionales
en memoria. Ese commit se usa como referencia técnica; no se restaura su rama.
El servicio Espacios usa el puerto 8003, separado del 8001 de Usuarios.

La especificación deja los filtros por concretar: esta propuesta utiliza nombre
parcial (sin distinguir tildes ni mayúsculas), tipo, zona y capacidad mínima
inclusiva. Se combinan con AND. El equipo debe revisar esta elección al integrar.
El CSS mantiene la paleta de US-001: fondo oscuro, verde lima, rosa y tipografía
Segoe UI. Es independiente para no sustituir el CSS compartido del equipo.

Solo se muestran y permiten consultar detalles de espacios habilitados y disponibles.
El detalle vuelve a consultar el servicio para reflejar el estado actual.
Sin resultados, la API devuelve `[]` y la interfaz muestra un mensaje.
No se implementan reservas ni administración, correspondientes a US-010 y US-011.
La consulta es pública: US-009 no tiene dependencias de autenticación.

## Ejecutar desde Git Bash, en la raíz del repositorio

Requiere Python 3.10 o posterior. En Windows se usa `py`; si tu instalación se
ejecuta con `python`, sustituye `py` en los comandos de creación del entorno.

```bash
py -m venv .venv
source .venv/Scripts/activate
python -m pip install -r Espacios/requirements.txt
python -m uvicorn Espacios.main:app --reload --port 8003
```

Mantener esa terminal abierta. En otra terminal, también en la raíz:

```bash
source .venv/Scripts/activate
python -m http.server 5500 --bind 127.0.0.1 --directory view
```

Abrir http://127.0.0.1:5500/espacios.html

Documentación de la API: http://127.0.0.1:8003/docs

No abrir el HTML con doble clic: usar el servidor HTTP para respetar CORS.
Si el puerto 5500 está ocupado y se usa 8080, ambos están permitidos por la API.
El backend debe conservar el 8003 o actualizar `API_ESPACIOS` en `espacios.js`.
No subir `.venv/`, `__pycache__/` ni `.env` a Git; añadirlos al `.gitignore` existente.

## Pruebas automáticas

Con el entorno activado, desde la raíz:

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
```

Para ejecutar solo las consultas sin instalar FastAPI:

```bash
python -m unittest tests.test_espacios -v
```

## Comprobaciones manuales antes de la PR

| Criterio | Acción | Resultado esperado |
|---|---|---|
| AC-01 | Abrir la página sin filtros | Cinco espacios; no aparecen Camping Río ni Sala Auxiliar. |
| AC-02 | Revisar una tarjeta | Nombre, tipo, zona, capacidad y descripción legibles. |
| AC-03/04 | Tipo Escenario, zona Sur, capacidad 2000 | Solo Escenario Electrónica. |
| AC-04 | Buscar electronica sin tilde | Aparece Escenario Electrónica. |
| AC-05 | Buscar inexistente | Mensaje sin resultados y posibilidad de limpiar filtros. |
| AC-06 | Pulsar Ver detalle | Diálogo con información del espacio seleccionado. |
| Accesibilidad | Usar Tab, Enter y Escape | Controles alcanzables, foco visible y cierre del diálogo. |
| Error | Detener el backend y pulsar Filtrar | Mensaje comprensible y botón Reintentar consulta. |
| Recuperación | Arrancar backend y pulsar Reintentar | Se recuperan los resultados. |
| Validación | Capacidad negativa o decimal | El formulario rechaza el valor; la API rechaza filtros inválidos. |
| Pantalla pequeña | Reducir a 375 px de ancho | Filtros y tarjetas en una columna sin desbordamiento horizontal. |

## Límites y estado de validación

Los siete espacios son ficticios; cinco están disponibles. Los datos viven en memoria
y se reinician con el servidor. El almacenamiento persistente queda pendiente de la
arquitectura acordada por el equipo, como en el servicio Usuarios de referencia.

Durante la generación se verificaron 12 pruebas de la lógica de consultas,
la compilación de los archivos Python y la sintaxis de JavaScript.
Las pruebas HTTP y la revisión visual quedan pendientes de ejecución con las
dependencias instaladas. No se considera la historia Done hasta probar la interfaz,
superar las pruebas HTTP y realizar la revisión e integración que exige el equipo.

Para preparar el commit, comprobar primero que se está en la rama US-009 y usar
el ID real de la tarea Jira en el mensaje. No registrar tiempo ni marcar Done
automáticamente sin que corresponda al trabajo realizado.
