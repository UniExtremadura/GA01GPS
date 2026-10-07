EP-004 — GESTIÓN DE SERVICIOS

# Objetivo

Permitir que los usuarios puedan consultar y acceder a los servicios disponibles en Subsonic Festival, así como permitir que los usuarios autorizados gestionen la información relacionada con dichos servicios.

# Relación con los objetivos del proyecto

 G-01 — Gestión centralizada del festival.
 G-02 — Experiencia clara para el usuario.
 G-03 — Gestión diferenciada por roles.
 G-05 — Desarrollo organizado y trazable.

# Alcance de la épica

Esta épica incluye:

- Consulta de los servicios disponibles.
- Adquisición de servicios por parte de los usuarios.
- Gestión de los servicios por parte de los usuarios autorizados.

Los servicios y operaciones utilizados durante el desarrollo y las pruebas serán ficticios y tendrán únicamente finalidad académica.

# Historias de usuario

## US-012 — CONSULTA DE SERVICIOS

# Necesidad

Los usuarios necesitan conocer los servicios disponibles en Subsonic Festival para poder consultar sus características y elegir aquellos que sean de su interés.

# Objetivo

Este requisito contribuye a los siguientes objetivos del proyecto:

 G-01 — Gestión centralizada del festival.
 G-02 — Experiencia clara para el usuario.

# Historia de usuario

Como usuario de Subsonic Festival, quiero consultar los servicios disponibles para conocer las diferentes opciones ofrecidas dentro de la plataforma.

# Criterios de aceptación

 US-012-AC-01: El usuario puede consultar los servicios disponibles en la plataforma.
 US-012-AC-02: El sistema muestra la información necesaria para identificar cada servicio.
 US-012-AC-03: El usuario puede seleccionar un servicio para consultar su información.
 US-012-AC-04: Solo se muestran como disponibles los servicios que se encuentren habilitados.
 US-012-AC-05: Si no existen servicios disponibles, el sistema informa al usuario de forma comprensible.

# Reglas

- Solo se mostrarán como disponibles los servicios que se encuentren habilitados en el sistema.
- La información mostrada deberá corresponder con los datos registrados para cada servicio.
- Los servicios deberán estar correctamente identificados dentro de la plataforma.

# Restricciones

- Los servicios utilizados durante el desarrollo y las pruebas serán ficticios.
- La funcionalidad tendrá únicamente finalidad académica y demostrativa.

# Requisitos no funcionales

- La información de los servicios deberá mostrarse de forma clara y comprensible.
- La consulta deberá ser sencilla para el usuario.
- La interfaz deberá respetar los criterios de usabilidad y accesibilidad establecidos para el proyecto.
- Si se produce un error durante la consulta, el sistema deberá informar al usuario de forma comprensible.

# Dependencias

No presenta dependencias funcionales previas.

---

## US-013 — ADQUISICIÓN DE UN SERVICIO

# Necesidad

Los usuarios necesitan poder seleccionar y adquirir los servicios disponibles en Subsonic Festival para acceder a las prestaciones ofrecidas a través de la plataforma.

# Objetivo

Este requisito contribuye a los siguientes objetivos del proyecto:

 G-01 — Gestión centralizada del festival.
 G-02 — Experiencia clara para el usuario.
 G-03 — Gestión diferenciada por roles.

# Historia de usuario

Como usuario registrado, quiero adquirir un servicio disponible en Subsonic Festival para poder acceder a las prestaciones asociadas a dicho servicio.

# Criterios de aceptación

 US-013-AC-01: El usuario puede seleccionar un servicio disponible.
 US-013-AC-02: El sistema muestra la información del servicio antes de confirmar la operación.
 US-013-AC-03: El usuario puede confirmar o cancelar la operación.
 US-013-AC-04: El sistema comprueba que el servicio se encuentra disponible antes de completar la operación.
 US-013-AC-05: Si la operación se completa correctamente, el sistema informa al usuario.
 US-013-AC-06: Si el servicio no está disponible, el sistema impide la operación e informa al usuario.

# Reglas

- El usuario deberá estar autenticado para adquirir un servicio.
- Solo podrán adquirirse servicios que se encuentren disponibles.
- La operación deberá quedar asociada al usuario que la realiza.

# Restricciones

- El usuario deberá haber iniciado sesión previamente.
- No se realizarán pagos económicos reales.
- No se utilizarán datos bancarios o financieros reales.
- Los servicios utilizados durante el desarrollo y las pruebas serán ficticios.

# Requisitos no funcionales

- El proceso deberá ser claro y comprensible para el usuario.
- El sistema deberá informar del resultado de la operación.
- Los errores no deberán provocar estados inconsistentes en los datos.
- La interfaz deberá respetar los criterios de usabilidad y accesibilidad establecidos para el proyecto.

# Dependencias

 US-002 — Inicio y cierre de sesión.
 US-012 — Consulta de servicios.

---

## US-014 — GESTIÓN DE SERVICIOS

# Necesidad

Los usuarios autorizados necesitan gestionar los servicios de Subsonic Festival para mantener actualizada la información y disponibilidad de los servicios ofrecidos en la plataforma.

# Objetivo

Este requisito contribuye a los siguientes objetivos del proyecto:

 G-01 — Gestión centralizada del festival.
 G-03 — Gestión diferenciada por roles.
 G-05 — Desarrollo organizado y trazable.

# Historia de usuario

Como usuario autorizado, quiero gestionar los servicios de Subsonic Festival para mantener actualizada su información y disponibilidad.

# Criterios de aceptación

 US-014-AC-01: El usuario autorizado puede consultar los servicios registrados.
 US-014-AC-02: El usuario autorizado puede crear nuevos servicios.
 US-014-AC-03: El usuario autorizado puede modificar la información de los servicios existentes.
 US-014-AC-04: El usuario autorizado puede eliminar o deshabilitar un servicio cuando corresponda.
 US-014-AC-05: Un usuario sin los permisos necesarios no puede acceder a las funciones de gestión de servicios.
 US-014-AC-06: El sistema informa del resultado de las operaciones realizadas.
 US-014-AC-07: Los cambios realizados se reflejan correctamente en la información disponible para los usuarios.

# Reglas

- Solo los usuarios con los permisos correspondientes pueden gestionar servicios.
- Los datos obligatorios de un servicio deberán estar completos antes de registrarlo.
- Las modificaciones deberán mantener la coherencia de la información almacenada.
- Un servicio deshabilitado no deberá mostrarse como disponible para su adquisición.

# Restricciones

- El usuario encargado de la gestión deberá haber iniciado sesión previamente.
- Los servicios utilizados durante el desarrollo y las pruebas serán ficticios.
- No se gestionarán pagos económicos reales.

# Requisitos no funcionales

- El acceso a las funciones de gestión deberá estar protegido mediante control de permisos.
- La información deberá mostrarse de forma clara y comprensible.
- Los errores no deberán dejar los datos en un estado inconsistente.
- El sistema deberá informar de forma clara del resultado de cada operación.
- La interfaz deberá respetar los criterios de usabilidad y accesibilidad establecidos para el proyecto.

# Dependencias

 US-002 — Inicio y cierre de sesión.
 US-012 — Consulta de servicios.
