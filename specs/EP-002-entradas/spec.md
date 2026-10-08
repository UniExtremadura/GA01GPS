EP-002 — Gestión de entradas

# Objetivo

Permitir la consulta y gestión de las entradas disponibles en Subsonic Festival, así como realizar una adquisición simulada de entradas y consultar las entradas asociadas a un usuario.

También se incluyen las funciones necesarias para que el personal administrador pueda mantener actualizada la información relacionada con las entradas del festival.

# Relación con los objetivos del proyecto

 G-01 — Gestión centralizada del festival.
 G-02 — Experiencia clara para el usuario.
 G-03 — Gestión diferenciada por roles.
 G-05 — Desarrollo organizado y trazable.

# Alcance de la épica

Esta épica incluye:

- Consulta de las entradas disponibles.
- Adquisición simulada de entradas.
- Consulta de las entradas adquiridas por un usuario.
- Gestión de entradas por parte del administrador.

No incluye pagos económicos reales, venta de entradas para un festival existente, integración con plataformas comerciales externas ni operaciones bancarias reales.


# Versión de referencia 

Catálogo de requisitos V0 — Práctica 1, Semana 2.

# Resultado esperado de la épica 

El resultado esperado sería permitir a los usuarios consultar las entradas disponibles para Subsonic Festival, realizar adquisiciones simuladas y visualizar las entradas asociadas a sus cuentas. Además, los administradores podrán gestionar los tipos de entradas y su disponibilidad, facilitando el control de la oferta del festival.


# Historias de usuario

## US-005 — CONSULTA DE ENTRADAS DISPONIBLES

# Necesidad

Los asistentes necesitan conocer las entradas disponibles para poder consultar las diferentes opciones ofrecidas por el festival antes de realizar una adquisición.

# Objetivo

Este requisito contribuye a los siguientes objetivos del proyecto:

 G-01 — Gestión centralizada del festival.
 G-02 — Experiencia clara para el usuario.

# Historia de usuario

Como asistente al festival, quiero consultar las entradas disponibles en Subsonic Festival para conocer las opciones existentes y poder elegir la que me interese.

# Información de planificación

- Prioridad MoSCoW: Must.
- Estimación: 5 horas-persona.
- Incertidumbre: Baja.
- Justificación de la incertidumbre: La funcionalidad consiste en mostrar los diferentes tipos de entradas disponibles, incluyendo su información principal, como el precio, las características y la disponibilidad. Es una operación de consulta con un comportamiento bien delimitado.
- Predecesores: Ninguno.
- Plan inicial: Se propone desarrollar durante las primeras fases del proyecto, ya que constituye la base para que los usuarios puedan consultar las entradas y posteriormente realizar su adquisición.


# Criterios de aceptación

 US-005-AC-01: El usuario puede consultar las entradas disponibles.
 US-005-AC-02: El sistema muestra la información necesaria para diferenciar los distintos tipos de entrada.
 US-005-AC-03: El usuario puede seleccionar una entrada para consultar su información.
 US-005-AC-04: Si no existen entradas disponibles, el sistema informa al usuario de forma comprensible.

# Reglas

- Solo se mostrarán como disponibles las entradas que puedan ser adquiridas.
- La información mostrada deberá corresponder con los datos registrados en el sistema.

# Restricciones

- Las entradas utilizadas durante el desarrollo y las pruebas serán ficticias.
- La plataforma no representará la venta real de entradas de un festival existente.

# Requisitos no funcionales

- La información de las entradas deberá mostrarse de forma clara y comprensible.
- La interfaz deberá permitir diferenciar fácilmente las distintas opciones disponibles.
- La consulta deberá respetar los criterios de usabilidad y accesibilidad establecidos para el proyecto.

# Dependencias

No presenta dependencias funcionales previas.

---


## US-006 — ADQUISICIÓN SIMULADA DE ENTRADAS

# Necesidad

Los asistentes necesitan poder adquirir una entrada dentro de Subsonic Festival para disponer de ella y asociarla a su cuenta, sin realizar pagos económicos reales.

# Objetivo

Este requisito contribuye a los siguientes objetivos del proyecto:

 G-01 — Gestión centralizada del festival.
 G-02 — Experiencia clara para el usuario.
 G-03 — Gestión diferenciada por roles.

# Historia de usuario

Como asistente registrado, quiero adquirir de forma simulada una entrada disponible para poder disponer de ella dentro de Subsonic Festival.


# Información de planificación

- Prioridad MoSCoW: Must.
- Estimación: 9 horas-persona.
- Incertidumbre: Alta.
- Justificación de la incertidumbre: La adquisición requiere comprobar la disponibilidad de las entradas, asociarlas correctamente al usuario y evitar registros inconsistentes. También deben contemplarse situaciones como la cancelación de la operación, los errores durante el proceso o la falta de disponibilidad.
- Predecesores: US-002 y US-005.
- Plan inicial: Se propone desarrollar después de implementar la autenticación de usuarios y la consulta de entradas, ya que el usuario debe iniciar sesión y seleccionar una entrada disponible antes de confirmar su adquisición.


# Criterios de aceptación

 US-006-AC-01: El usuario puede seleccionar una entrada disponible.
 US-006-AC-02: El sistema muestra la información de la entrada seleccionada antes de confirmar la adquisición.
 US-006-AC-03: El usuario puede confirmar o cancelar la operación.
 US-006-AC-04: Si la adquisición se completa correctamente, la entrada queda asociada al usuario.
 US-006-AC-05: El sistema informa al usuario cuando la operación se ha realizado correctamente.
 US-006-AC-06: Si la entrada no está disponible, el sistema impide la adquisición e informa al usuario.
 US-006-AC-07: La operación no implica ningún pago económico real.

# Reglas

- El usuario debe estar autenticado para adquirir una entrada.
- Solo se pueden adquirir entradas disponibles.
- Una adquisición completada deberá quedar asociada al usuario que la realiza.
- La operación será únicamente una simulación dentro del sistema.

# Restricciones

- No se realizarán pagos económicos reales.
- No se utilizarán datos bancarios o financieros reales.
- No se integrará la plataforma con sistemas comerciales externos de venta de entradas.
- Las entradas utilizadas durante el desarrollo y las pruebas serán ficticias.

# Requisitos no funcionales

- El proceso de adquisición deberá mostrar de forma clara la entrada seleccionada y el resultado de la operación.
- Los errores deberán comunicarse mediante mensajes comprensibles.
- La operación no deberá dejar información inconsistente si se produce un error.
- La interfaz deberá respetar los criterios de usabilidad y accesibilidad establecidos para el proyecto.

# Dependencias

 US-002 — Inicio y cierre de sesión.
 US-005 — Consulta de entradas disponibles.


Este requisito vamos a detallarlo como se pide en la sesión 2:

# Ejemplos

- Un usuario autenticado selecciona una entrada disponible, confirma la operación y la entrada queda asociada a su cuenta.
- Un usuario selecciona una entrada pero cancela la operación antes de confirmarla.
- Un usuario intenta adquirir una entrada que ya no está disponible y el sistema rechaza la operación.

# Casos límite

- La entrada deja de estar disponible entre el momento de la consulta y la confirmación de la adquisición.
- El usuario intenta confirmar una adquisición sin haber iniciado sesión.
- Se produce un error durante la operación antes de que la entrada quede asociada al usuario.
- El usuario intenta realizar la operación sobre una entrada deshabilitada.

# Supuestos

- El usuario dispone de una cuenta válida y ha iniciado sesión.
- Existen entradas previamente registradas en el sistema.
- La información de disponibilidad se encuentra actualizada antes de confirmar la operación.
- La adquisición es únicamente simulada y no implica pagos económicos reales.
 


## US-007 — CONSULTA DE ENTRADAS ADQUIRIDAS

# Necesidad

Los usuarios que hayan adquirido una entrada necesitan poder consultar las entradas asociadas a su cuenta para conocer y revisar la información de sus adquisiciones.

# Objetivo

Este requisito contribuye a los siguientes objetivos del proyecto:

 G-01 — Gestión centralizada del festival.
 G-02 — Experiencia clara para el usuario.
 G-03 — Gestión diferenciada por roles.

# Historia de usuario

Como asistente registrado, quiero consultar las entradas asociadas a mi cuenta para poder revisar las entradas que he adquirido en Subsonic Festival.

# Información de planificación

- Prioridad MoSCoW: Should.
- Estimación: 5 horas-persona.
- Incertidumbre: Baja.
- Justificación de la incertidumbre: La funcionalidad consiste en recuperar y mostrar las entradas que han sido adquiridas previamente por un usuario. La principal consideración es garantizar que cada usuario únicamente pueda consultar las entradas asociadas a su propia cuenta.
- Predecesores: US-002 y US-006.
- Plan inicial: Se propone desarrollar después de implementar la adquisición simulada de entradas, ya que es necesario disponer de entradas asociadas a los usuarios para poder consultarlas.


# Criterios de aceptación

 US-007-AC-01: El usuario autenticado puede consultar las entradas asociadas a su cuenta.
 US-007-AC-02: El sistema muestra la información correspondiente a cada entrada adquirida.
 US-007-AC-03: Un usuario únicamente puede consultar las entradas asociadas a su propia cuenta mediante esta funcionalidad.
 US-007-AC-04: Si el usuario no tiene ninguna entrada asociada, el sistema muestra un mensaje informativo.
 US-007-AC-05: La información mostrada debe corresponder con las adquisiciones registradas en el sistema.

# Reglas

- El usuario debe estar autenticado para consultar sus entradas.
- Solo se mostrarán las entradas asociadas a la cuenta del usuario autenticado.
- Las entradas mostradas deberán corresponder con adquisiciones registradas correctamente en el sistema.

# Restricciones

- Las entradas y adquisiciones utilizadas durante el desarrollo y las pruebas serán ficticias.
- La funcionalidad no supondrá la validación de entradas reales para acceder a un festival.
- No se utilizarán datos personales o financieros reales.

# Requisitos no funcionales

- La información de las entradas deberá mostrarse de forma clara y comprensible.
- El acceso deberá respetar los permisos y la información asociada a cada usuario.
- La interfaz deberá respetar los criterios de usabilidad y accesibilidad establecidos para el proyecto.
- Si se produce un error al consultar la información, el sistema deberá informar al usuario de forma comprensible.

# Dependencias

 US-002 — Inicio y cierre de sesión.
 US-006 — Adquisición simulada de entradas.


## US-008 — GESTIÓN DE ENTRADAS POR ADMINISTRADOR

# Necesidad

El personal de administración necesita gestionar la información de las entradas disponibles en Subsonic Festival para mantener actualizada la oferta de entradas del festival.

# Objetivo

Este requisito contribuye a los siguientes objetivos del proyecto:

 G-01 — Gestión centralizada del festival.
 G-03 — Gestión diferenciada por roles.
 G-05 — Desarrollo organizado y trazable.

# Historia de usuario

Como administrador, quiero gestionar las entradas de Subsonic Festival para mantener actualizada la información y disponibilidad de los diferentes tipos de entrada.


# Información de planificación

- Prioridad MoSCoW: Must.
- Estimación: 8 horas-persona.
- Incertidumbre: Media.
- Justificación de la incertidumbre: La gestión administrativa requiere implementar operaciones para crear, modificar y deshabilitar tipos de entradas, validar la información introducida y controlar que estas acciones únicamente puedan realizarlas usuarios con permisos de administración.
- Predecesores: US-002.
- Plan inicial: Se propone desarrollar una vez implementado el sistema de autenticación y control de acceso. Esta funcionalidad permitirá mantener actualizada la información de las entradas ofrecidas en el festival.


# Criterios de aceptación

 US-008-AC-01: El administrador puede consultar las entradas registradas en el sistema.
 US-008-AC-02: El administrador puede crear nuevos tipos de entrada.
 US-008-AC-03: El administrador puede modificar la información de las entradas existentes.
 US-008-AC-04: El administrador puede eliminar o deshabilitar una entrada cuando corresponda.
 US-008-AC-05: Un usuario sin permisos de administrador no puede acceder a las funciones de gestión de entradas.
 US-008-AC-06: El sistema informa al administrador del resultado de las operaciones realizadas.
 US-008-AC-07: Los cambios realizados se reflejan correctamente en la información de entradas disponible para los usuarios.

# Reglas

- Solo los usuarios con permisos de administrador pueden acceder a la gestión de entradas.
- La información obligatoria de una entrada deberá estar completa antes de poder registrarla.
- Las modificaciones deberán mantener la coherencia de la información almacenada.
- Solo las entradas disponibles podrán mostrarse a los asistentes como opciones de adquisición.

# Restricciones

- El administrador deberá haber iniciado sesión previamente.
- Las entradas utilizadas durante el desarrollo y las pruebas serán ficticias.
- No se realizarán operaciones económicas reales ni se gestionarán pagos bancarios.
- No se integrará la plataforma con servicios comerciales externos de venta de entradas.

# Requisitos no funcionales

- El acceso a las funciones de gestión deberá estar protegido mediante control de permisos.
- Las operaciones realizadas deberán proporcionar información clara sobre su resultado.
- Los errores no deberán provocar estados inconsistentes en los datos.
- La interfaz deberá respetar los criterios de usabilidad y accesibilidad establecidos para el proyecto.

# Dependencias

 US-002 — Inicio y cierre de sesión.
 US-005 — Consulta de entradas disponibles.
