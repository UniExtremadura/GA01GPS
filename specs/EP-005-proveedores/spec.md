EP-005 — GESTIÓN DE PROVEEDORES

# Objetivo

Permitir la consulta de la información de los proveedores asociados a Subsonic Festival y facilitar su gestión por parte de los usuarios autorizados.

# Relación con los objetivos del proyecto

 G-01 — Gestión centralizada del festival.
 G-02 — Experiencia clara para el usuario.
 G-03 — Gestión diferenciada por roles.
 G-05 — Desarrollo organizado y trazable.

# Alcance de la épica

Esta épica incluye:

- Consulta de la información de los proveedores.
- Gestión de los proveedores por parte de los usuarios autorizados.

Los proveedores y los datos utilizados durante el desarrollo y las pruebas serán ficticios y tendrán únicamente finalidad académica.

# Historias de usuario

## US-015 — CONSULTA DE INFORMACIÓN DE PROVEEDORES

# Necesidad

Los usuarios necesitan poder consultar la información disponible sobre los proveedores asociados a Subsonic Festival para conocer qué proveedores participan en la plataforma y los servicios relacionados con ellos.

# Objetivo

Este requisito contribuye a los siguientes objetivos del proyecto:

 G-01 — Gestión centralizada del festival.
 G-02 — Experiencia clara para el usuario.

# Historia de usuario

Como usuario de Subsonic Festival, quiero consultar la información disponible de los proveedores para conocer los proveedores asociados a la plataforma.

# Criterios de aceptación

 US-015-AC-01: El usuario puede consultar los proveedores registrados y disponibles en la plataforma.
 US-015-AC-02: El sistema muestra la información necesaria para identificar cada proveedor.
 US-015-AC-03: El usuario puede seleccionar un proveedor para consultar su información disponible.
 US-015-AC-04: La información mostrada corresponde con los datos registrados en el sistema.
 US-015-AC-05: Si no existen proveedores disponibles, el sistema informa al usuario de forma comprensible.

# Reglas

- Solo se mostrarán los proveedores que se encuentren habilitados en el sistema.
- La información mostrada deberá corresponder con los datos registrados para cada proveedor.
- No se mostrará información privada o reservada para las funciones administrativas.

# Restricciones

- Los proveedores utilizados durante el desarrollo y las pruebas serán ficticios.
- No se utilizarán datos personales o sensibles reales.
- La funcionalidad tendrá únicamente finalidad académica y demostrativa.

# Requisitos no funcionales

- La información de los proveedores deberá mostrarse de forma clara y comprensible.
- La consulta deberá ser sencilla para el usuario.
- La interfaz deberá respetar los criterios de usabilidad y accesibilidad establecidos para el proyecto.
- Si se produce un error durante la consulta, el sistema deberá informar al usuario de forma comprensible.

# Dependencias

No presenta dependencias funcionales previas.

---

## US-016 — GESTIÓN DE PROVEEDORES

# Necesidad

El personal autorizado necesita gestionar los proveedores asociados a Subsonic Festival para mantener actualizada y organizada la información de los proveedores de la plataforma.

# Objetivo

Este requisito contribuye a los siguientes objetivos del proyecto:

 G-01 — Gestión centralizada del festival.
 G-03 — Gestión diferenciada por roles.
 G-05 — Desarrollo organizado y trazable.

# Historia de usuario

Como administrador, quiero gestionar los proveedores de Subsonic Festival para mantener actualizada la información de los proveedores asociados a la plataforma.

# Criterios de aceptación

 US-016-AC-01: El administrador puede consultar los proveedores registrados en el sistema.
 US-016-AC-02: El administrador puede registrar nuevos proveedores.
 US-016-AC-03: El administrador puede modificar la información de los proveedores existentes.
 US-016-AC-04: El administrador puede eliminar o deshabilitar un proveedor cuando corresponda.
 US-016-AC-05: Un usuario sin permisos de administrador no puede acceder a las funciones de gestión de proveedores.
 US-016-AC-06: El sistema informa al administrador del resultado de cada operación realizada.
 US-016-AC-07: Los cambios realizados se reflejan correctamente en la información almacenada en la plataforma.

# Reglas

- Solo los usuarios con permisos de administrador pueden gestionar proveedores.
- Los datos obligatorios de un proveedor deberán estar completos antes de registrarlo.
- Las modificaciones deberán mantener la coherencia de la información almacenada.
- Un proveedor deshabilitado no deberá mostrarse como disponible para los usuarios.

# Restricciones

- El administrador deberá haber iniciado sesión previamente.
- Los proveedores utilizados durante el desarrollo y las pruebas serán ficticios.
- No se utilizarán datos personales o sensibles reales.

# Requisitos no funcionales

- El acceso a las funciones de gestión deberá estar protegido mediante control de permisos.
- La información deberá mostrarse de forma clara y comprensible.
- El sistema deberá informar de forma clara del resultado de cada operación.
- Los errores no deberán dejar los datos en un estado inconsistente.
- La interfaz deberá respetar los criterios de usabilidad y accesibilidad establecidos para el proyecto.

# Dependencias

 US-002 — Inicio y cierre de sesión.
 US-015 — Consulta de información de proveedores.
