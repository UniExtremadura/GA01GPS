 EP-003 — GESTIÓN DE ESPACIOS

# Objetivo

Permitir que los usuarios puedan consultar los espacios disponibles en Subsonic Festival y realizar las operaciones relacionadas con su uso, así como permitir su gestión por parte de los usuarios autorizados.

# Relación con los objetivos del proyecto

 G-01 — Gestión centralizada del festival.
 G-02 — Experiencia clara para el usuario.
 G-03 — Gestión diferenciada por roles.
 G-05 — Desarrollo organizado y trazable.

# Alcance de la épica

Esta épica incluye:

- Consulta de los espacios disponibles.
- Filtrado de los espacios para facilitar su localización.
- Reserva de espacios.
- Gestión de los espacios por parte de los usuarios autorizados.

Los espacios y reservas utilizados durante el desarrollo y las pruebas serán ficticios y tendrán únicamente finalidad académica.


# Versión de referencia 

Catálogo de requisitos V0 — Práctica 1, Semana 2.

# Resultado esperado de la épica 

Permitir a los usuarios consultar los espacios disponibles en Subsonic Festival, conocer sus características y realizar reservas según su disponibilidad. Además, los administradores podrán gestionar la información de los espacios, actualizar sus características y controlar su disponibilidad para facilitar la organización del festival.


# Historias de usuario

## US-009 — CONSULTA Y FILTRADO DE ESPACIOS DISPONIBLES

# Necesidad

Los usuarios necesitan consultar los espacios disponibles en Subsonic Festival y poder localizar aquellos que se ajusten a sus necesidades.

# Objetivo

Este requisito contribuye a los siguientes objetivos del proyecto:

 G-01 — Gestión centralizada del festival.
 G-02 — Experiencia clara para el usuario.

# Historia de usuario

Como usuario de Subsonic Festival, quiero consultar y filtrar los espacios disponibles para encontrar de forma sencilla aquellos que se ajusten a mis necesidades.


# Información de planificación

- Prioridad MoSCoW: Must.
- Estimación: 6 horas-persona.
- Incertidumbre: Baja.
- Justificación de la incertidumbre: La funcionalidad consiste en mostrar los espacios disponibles y permitir su filtrado según determinados criterios. Se trata de operaciones de consulta cuyo comportamiento está bien delimitado, aunque será necesario definir los filtros y comprobar que los resultados mostrados sean correctos.
- Predecesores: Ninguno.
- Plan inicial: Se propone desarrollar durante las primeras fases del proyecto, ya que permite a los usuarios conocer los espacios del festival y constituye la base para otras funcionalidades relacionadas con su utilización.


# Criterios de aceptación

 US-009-AC-01: El usuario puede consultar los espacios registrados y disponibles en la plataforma.
 US-009-AC-02: El sistema muestra la información necesaria para identificar cada espacio.
 US-009-AC-03: El usuario puede aplicar los filtros disponibles para reducir los resultados mostrados.
 US-009-AC-04: Los resultados mostrados corresponden con los filtros seleccionados.
 US-009-AC-05: Si no existen espacios que cumplan los criterios seleccionados, el sistema informa al usuario de forma comprensible.
 US-009-AC-06: El usuario puede consultar la información disponible de un espacio seleccionado.

# Reglas

- Solo se mostrarán como disponibles los espacios que se encuentren habilitados en el sistema.
- Los filtros deberán aplicarse sobre la información registrada de los espacios.
- La información mostrada deberá corresponder con el estado actual almacenado en el sistema.

# Restricciones

- Los espacios utilizados durante el desarrollo y las pruebas serán ficticios.
- La funcionalidad tendrá únicamente finalidad académica y demostrativa.

# Requisitos no funcionales

- La información de los espacios deberá mostrarse de forma clara y comprensible.
- Los filtros deberán ser fáciles de utilizar.
- La interfaz deberá respetar los criterios de usabilidad y accesibilidad establecidos para el proyecto.
- Si se produce un error durante la consulta, el sistema deberá informar al usuario de forma comprensible.

# Dependencias

No presenta dependencias funcionales previas.

---

## US-010 — RESERVA DE UN ESPACIO

# Necesidad

Los usuarios necesitan poder reservar un espacio disponible en Subsonic Festival para utilizarlo dentro de las condiciones establecidas por la plataforma.

# Objetivo

Este requisito contribuye a los siguientes objetivos del proyecto:

 G-01 — Gestión centralizada del festival.
 G-02 — Experiencia clara para el usuario.
 G-03 — Gestión diferenciada por roles.

# Historia de usuario

Como usuario registrado, quiero reservar un espacio disponible en Subsonic Festival para poder hacer uso de él según las condiciones establecidas.


# Información de planificación

- Prioridad MoSCoW: Should.
- Estimación: 9 horas-persona.
- Incertidumbre: Alta.
- Justificación de la incertidumbre: La reserva requiere comprobar la disponibilidad de los espacios, registrar correctamente la operación y evitar conflictos cuando varios usuarios intenten reservar un mismo espacio. También deben contemplarse situaciones como la cancelación de la operación, los errores durante el proceso o los cambios de disponibilidad.
- Predecesores: US-002 y US-009.
- Plan inicial: Se propone desarrollar después de implementar la autenticación y la consulta de espacios, ya que el usuario debe iniciar sesión, seleccionar un espacio y comprobar su disponibilidad antes de confirmar una reserva.


# Criterios de aceptación

 US-010-AC-01: El usuario puede seleccionar un espacio disponible para realizar una reserva.
 US-010-AC-02: El sistema muestra la información necesaria del espacio antes de confirmar la reserva.
 US-010-AC-03: El usuario puede confirmar o cancelar la operación.
 US-010-AC-04: El sistema comprueba que el espacio se encuentra disponible antes de registrar la reserva.
 US-010-AC-05: Si la reserva se realiza correctamente, queda asociada al usuario que la ha realizado.
 US-010-AC-06: Si el espacio no está disponible, el sistema impide realizar la reserva e informa al usuario.
 US-010-AC-07: El sistema informa al usuario del resultado de la operación.

# Reglas

- El usuario deberá estar autenticado para realizar una reserva.
- Solo podrán reservarse espacios que se encuentren disponibles.
- Una reserva confirmada deberá quedar asociada al usuario que la realiza.
- No se podrá confirmar una reserva si el espacio ha dejado de estar disponible.

# Restricciones

- El usuario deberá haber iniciado sesión previamente.
- Los espacios y reservas utilizados durante el desarrollo y las pruebas serán ficticios.
- La funcionalidad tendrá únicamente finalidad académica y demostrativa.

# Requisitos no funcionales

- El proceso de reserva deberá ser claro y comprensible para el usuario.
- El sistema deberá informar del resultado de la operación.
- Los errores no deberán provocar reservas duplicadas ni estados inconsistentes.
- La interfaz deberá respetar los criterios de usabilidad y accesibilidad establecidos para el proyecto.

# Dependencias

 US-002 — Inicio y cierre de sesión.
 US-009 — Consulta y filtrado de espacios disponibles.


Este requisito vamos a detallarlo:

# Ejemplos

- Un usuario autenticado consulta los espacios, selecciona uno disponible y confirma su reserva.
- Un usuario selecciona un espacio pero cancela la operación antes de confirmarla.
- Un usuario intenta reservar un espacio que ya no está disponible y el sistema rechaza la reserva.

# Casos límite

- Dos usuarios intentan reservar el mismo espacio para la misma disponibilidad.
- El espacio deja de estar disponible entre la consulta y la confirmación.
- El usuario intenta realizar una reserva sin haber iniciado sesión.
- Se produce un error durante el proceso y la reserva no llega a completarse.

# Supuestos

- El usuario está correctamente autenticado.
- Los espacios han sido previamente registrados en el sistema.
- La disponibilidad de los espacios se encuentra actualizada.
- Las reservas realizadas durante las pruebas son ficticias.

 

## US-011 — GESTIÓN DE ESPACIOS

# Necesidad

Los usuarios autorizados necesitan gestionar los espacios de Subsonic Festival para mantener actualizada la información y disponibilidad de los espacios registrados en la plataforma.

# Objetivo

Este requisito contribuye a los siguientes objetivos del proyecto:

 G-01 — Gestión centralizada del festival.
 G-03 — Gestión diferenciada por roles.
 G-05 — Desarrollo organizado y trazable.

# Historia de usuario

Como usuario autorizado, quiero gestionar los espacios de Subsonic Festival para mantener actualizada su información y disponibilidad.


# Información de planificación

- Prioridad MoSCoW: Must.
- Estimación: 8 horas-persona.
- Incertidumbre: Media.
- Justificación de la incertidumbre: La gestión administrativa requiere implementar operaciones para crear, modificar y deshabilitar espacios, validar los datos introducidos y garantizar que únicamente los usuarios con permisos de administración puedan realizar estas acciones. También será necesario mantener actualizada la información sobre las características y la disponibilidad de los espacios.
- Predecesores: US-002.
- Plan inicial: Se propone desarrollar una vez implementado el sistema de autenticación y control de acceso. Esta funcionalidad permitirá mantener actualizada la información de los espacios y facilitará su posterior consulta y utilización.


# Criterios de aceptación

 US-011-AC-01: El usuario autorizado puede consultar los espacios registrados en el sistema.
 US-011-AC-02: El usuario autorizado puede crear nuevos espacios.
 US-011-AC-03: El usuario autorizado puede modificar la información de los espacios existentes.
 US-011-AC-04: El usuario autorizado puede eliminar o deshabilitar un espacio cuando corresponda.
 US-011-AC-05: Los usuarios sin los permisos necesarios no pueden acceder a las funciones de gestión de espacios.
 US-011-AC-06: El sistema informa del resultado de cada operación realizada.
 US-011-AC-07: Los cambios realizados se reflejan correctamente en la información de espacios disponible en la plataforma.

# Reglas

- Solo los usuarios con los permisos correspondientes pueden gestionar espacios.
- Los datos obligatorios de un espacio deberán estar completos antes de registrarlo.
- Las modificaciones deberán mantener la coherencia de la información almacenada.
- Un espacio deshabilitado no deberá mostrarse como disponible para los usuarios.

# Restricciones

- El usuario encargado de la gestión deberá haber iniciado sesión previamente.
- Los espacios utilizados durante el desarrollo y las pruebas serán ficticios.
- Las operaciones realizadas tendrán únicamente finalidad académica y demostrativa.

# Requisitos no funcionales

- El acceso a las funciones de gestión deberá estar protegido mediante control de permisos.
- La información de los espacios deberá mostrarse de forma clara y comprensible.
- Los errores no deberán dejar la información en un estado inconsistente.
- El sistema deberá informar de forma clara del resultado de las operaciones realizadas.
- La interfaz deberá respetar los criterios de usabilidad y accesibilidad establecidos para el proyecto.

# Dependencias

 US-002 — Inicio y cierre de sesión.
 US-009 — Consulta y filtrado de espacios disponibles.
