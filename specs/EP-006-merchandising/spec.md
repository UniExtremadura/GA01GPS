EP-006 — GESTIÓN DE MERCHANDISING

# Objetivo

Permitir que los usuarios puedan consultar los productos de merchandising disponibles en Subsonic Festival y realizar una adquisición simulada de los mismos, así como permitir su gestión por parte de los usuarios autorizados.

# Relación con los objetivos del proyecto

 G-01 — Gestión centralizada del festival.
 G-02 — Experiencia clara para el usuario.
 G-03 — Gestión diferenciada por roles.
 G-05 — Desarrollo organizado y trazable.

# Alcance de la épica

Esta épica incluye:

- Consulta de los productos de merchandising disponibles.
- Adquisición simulada de productos de merchandising.
- Gestión de los productos por parte de los usuarios autorizados.

No incluye pagos económicos reales, operaciones bancarias ni integración con plataformas comerciales externas.


# Versión de referencia 

Catálogo de requisitos V0 — Práctica 1, Semana 2.

# Resultado esperado de la épica 

Permitir a los usuarios consultar los productos de merchandising disponibles en Subsonic Festival, conocer sus características y realizar adquisiciones simuladas. Además, los administradores podrán gestionar los productos, modificar su información y controlar su disponibilidad para mantener actualizado el catálogo de merchandising del festival.


# Historias de usuario

## US-017 — CONSULTA DE PRODUCTOS DE MERCHANDISING

# Necesidad

Los usuarios necesitan consultar los productos de merchandising disponibles en Subsonic Festival para conocer los diferentes artículos ofrecidos a través de la plataforma.

# Objetivo

Este requisito contribuye a los siguientes objetivos del proyecto:

 G-01 — Gestión centralizada del festival.
 G-02 — Experiencia clara para el usuario.

# Historia de usuario

Como usuario de Subsonic Festival, quiero consultar los productos de merchandising disponibles para conocer los artículos ofrecidos y su información.


# Información de planificación

- Prioridad MoSCoW: Could.
- Estimación: 5 horas-persona.
- Incertidumbre: Baja.
- Justificación de la incertidumbre: La funcionalidad consiste en mostrar los productos de merchandising disponibles, incluyendo información como su nombre, descripción, precio y disponibilidad. Se trata de una operación de consulta con un comportamiento bien delimitado, aunque será necesario comprobar que los datos mostrados sean correctos y estén actualizados.
- Predecesores: Ninguno.
- Plan inicial: Se propone desarrollar en una fase posterior a las funcionalidades principales del festival, ya que el merchandising tiene una prioridad menor. Su implementación permitirá que los usuarios consulten los productos antes de realizar una adquisición simulada.


# Criterios de aceptación

 US-017-AC-01: El usuario puede consultar los productos de merchandising disponibles.
 US-017-AC-02: El sistema muestra la información necesaria para identificar cada producto.
 US-017-AC-03: El usuario puede seleccionar un producto para consultar su información.
 US-017-AC-04: Solo se muestran como disponibles los productos que se encuentren habilitados.
 US-017-AC-05: Si no existen productos disponibles, el sistema informa al usuario de forma comprensible.

# Reglas

- Solo se mostrarán como disponibles los productos que se encuentren habilitados en el sistema.
- La información mostrada deberá corresponder con los datos registrados para cada producto.
- Los productos deberán estar correctamente identificados dentro de la plataforma.

# Restricciones

- Los productos utilizados durante el desarrollo y las pruebas serán ficticios.
- La plataforma no representará una tienda comercial real.
- No se utilizarán datos financieros reales.

# Requisitos no funcionales

- La información de los productos deberá mostrarse de forma clara y comprensible.
- La consulta de productos deberá ser sencilla para el usuario.
- La interfaz deberá respetar los criterios de usabilidad y accesibilidad establecidos para el proyecto.
- Si se produce un error durante la consulta, el sistema deberá informar al usuario de forma comprensible.

# Dependencias

No presenta dependencias funcionales previas.

---

## US-018 — ADQUISICIÓN SIMULADA Y GESTIÓN DE MERCHANDISING 

# Necesidad

Los usuarios necesitan poder realizar una adquisición simulada de los productos disponibles, mientras que el personal autorizado necesita gestionar el catálogo de merchandising para mantener actualizada la información de los productos.

# Objetivo

Este requisito contribuye a los siguientes objetivos del proyecto:

 G-01 — Gestión centralizada del festival.
 G-02 — Experiencia clara para el usuario.
 G-03 — Gestión diferenciada por roles.
 G-05 — Desarrollo organizado y trazable.

# Historia de usuario

Como usuario registrado, quiero realizar una adquisición simulada de productos de merchandising para poder utilizar esta funcionalidad dentro de Subsonic Festival.

Como administrador, quiero gestionar los productos de merchandising para mantener actualizado el catálogo disponible en la plataforma.


# Información de planificación

- Prioridad MoSCoW: Could.
- Estimación: 10 horas-persona.
- Incertidumbre: Alta.
- Justificación de la incertidumbre: La funcionalidad incluye tanto la adquisición simulada de productos como su gestión administrativa. Es necesario comprobar la disponibilidad de los productos, registrar correctamente las adquisiciones, asociarlas a los usuarios y controlar los permisos de administración. También deben contemplarse posibles errores durante las operaciones y cambios en la disponibilidad de los productos.
- Predecesores: US-002 y US-017.
- Plan inicial: Se propone desarrollar después de implementar la autenticación y la consulta de merchandising. Al tratarse de una funcionalidad con prioridad Could, su incorporación dependerá de la capacidad efectiva del equipo y del avance de los requisitos considerados más importantes.


# Criterios de aceptación

 US-018-AC-01: El usuario registrado puede seleccionar un producto disponible.
 US-018-AC-02: El sistema muestra la información del producto antes de confirmar la adquisición.
 US-018-AC-03: El usuario puede confirmar o cancelar la operación.
 US-018-AC-04: La adquisición realizada queda asociada al usuario.
 US-018-AC-05: La operación no implica ningún pago económico real.
 US-018-AC-06: El administrador puede crear nuevos productos de merchandising.
 US-018-AC-07: El administrador puede modificar la información de los productos existentes.
 US-018-AC-08: El administrador puede eliminar o deshabilitar productos cuando corresponda.
 US-018-AC-09: Un usuario sin permisos de administrador no puede acceder a las funciones de gestión del catálogo.
 US-018-AC-10: El sistema informa del resultado de las operaciones realizadas.

# Reglas

- El usuario deberá estar autenticado para realizar una adquisición.
- Solo podrán adquirirse productos que se encuentren disponibles.
- Las adquisiciones realizadas serán simuladas.
- Solo los usuarios con permisos de administrador podrán gestionar el catálogo de merchandising.
- Los productos deshabilitados no deberán mostrarse como disponibles.

# Restricciones

- No se realizarán pagos económicos reales.
- No se utilizarán datos bancarios o financieros reales.
- No se integrará la plataforma con sistemas comerciales externos.
- Los productos y operaciones utilizados durante el desarrollo y las pruebas serán ficticios.

# Requisitos no funcionales

- El proceso de adquisición deberá ser claro y comprensible.
- Las funciones de administración deberán estar protegidas mediante control de permisos.
- El sistema deberá informar de forma clara del resultado de las operaciones.
- Los errores no deberán dejar los datos en un estado inconsistente.
- La interfaz deberá respetar los criterios de usabilidad y accesibilidad establecidos para el proyecto.

# Dependencias

 US-002 — Inicio y cierre de sesión.
 US-017 — Consulta de productos de merchandising.
