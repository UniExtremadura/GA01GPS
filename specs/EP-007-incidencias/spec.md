EP-007 — GESTIÓN DE INCIDENCIAS

# Objetivo

Permitir que los usuarios puedan comunicar incidencias relacionadas con Subsonic Festival y que el personal autorizado pueda consultarlas y gestionarlas para mantener un control organizado de los problemas detectados en la plataforma.

# Relación con los objetivos del proyecto

 G-01 — Gestión centralizada del festival.
 G-02 — Experiencia clara para el usuario.
 G-03 — Gestión diferenciada por roles.
 G-05 — Desarrollo organizado y trazable.

# Alcance de la épica

Esta épica incluye:

- Registro de incidencias por parte de los usuarios.
- Consulta de las incidencias registradas.
- Gestión de las incidencias por parte de los usuarios autorizados.
- Actualización del estado de una incidencia.

Las incidencias utilizadas durante el desarrollo y las pruebas serán ficticias y tendrán únicamente finalidad académica.

# Historias de usuario

## US-019 — REGISTRO Y GESTIÓN DE INCIDENCIAS

# Necesidad

Los usuarios necesitan disponer de un mecanismo para comunicar los problemas o incidencias que puedan encontrar en Subsonic Festival, mientras que el personal autorizado necesita poder gestionarlos y realizar un seguimiento de su estado.

# Objetivo

Este requisito contribuye a los siguientes objetivos del proyecto:

 G-01 — Gestión centralizada del festival.
 G-02 — Experiencia clara para el usuario.
 G-03 — Gestión diferenciada por roles.
 G-05 — Desarrollo organizado y trazable.

# Historia de usuario

Como usuario de Subsonic Festival, quiero registrar una incidencia para comunicar un problema detectado en la plataforma.

Como administrador, quiero consultar y gestionar las incidencias registradas para realizar un seguimiento de los problemas comunicados por los usuarios.

# Criterios de aceptación

 US-019-AC-01: El usuario puede registrar una nueva incidencia.
 US-019-AC-02: El sistema solicita la información necesaria para describir la incidencia.
 US-019-AC-03: El sistema informa al usuario cuando la incidencia se ha registrado correctamente.
 US-019-AC-04: El administrador puede consultar las incidencias registradas.
 US-019-AC-05: El administrador puede consultar la información de una incidencia concreta.
 US-019-AC-06: El administrador puede modificar el estado de una incidencia.
 US-019-AC-07: Un usuario sin los permisos necesarios no puede acceder a las funciones administrativas de gestión de incidencias.
 US-019-AC-08: El sistema informa del resultado de las operaciones realizadas.
 US-019-AC-09: Si se produce un error durante una operación, el sistema informa al usuario y evita dejar los datos en un estado inconsistente.

# Reglas

- Cada incidencia deberá contener la información mínima necesaria para identificar el problema.
- Las incidencias registradas deberán disponer de un estado que permita realizar su seguimiento.
- Solo los usuarios con los permisos correspondientes podrán gestionar las incidencias.
- Los cambios realizados sobre una incidencia deberán quedar correctamente reflejados en el sistema.

# Restricciones

- Las incidencias utilizadas durante el desarrollo y las pruebas serán ficticias.
- No se utilizarán datos personales o sensibles reales.
- La funcionalidad tendrá únicamente finalidad académica y demostrativa.

# Requisitos no funcionales

- El proceso de registro de una incidencia deberá ser claro y comprensible.
- El sistema deberá proporcionar información sobre el resultado de las operaciones realizadas.
- Las funciones administrativas deberán estar protegidas mediante control de permisos.
- Los errores no deberán provocar estados inconsistentes en los datos.
- La interfaz deberá respetar los criterios de usabilidad y accesibilidad establecidos para el proyecto.

# Dependencias

 US-002 — Inicio y cierre de sesión, para las operaciones que requieran un usuario autenticado.
