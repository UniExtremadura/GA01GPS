EP-001 — Autenticación y usuarios

# Objetivo

Permitir que los usuarios puedan identificarse y acceder de forma controlada a Subsonic Festival, utilizando las funcionalidades correspondientes a su rol.

También se incluye la gestión de las cuentas de usuario por parte del personal administrador.

# Relación con los objetivos del proyecto

 G-01 — Gestión centralizada del festival.
 G-02 — Experiencia clara para el usuario.
 G-03 — Gestión diferenciada por roles.
 G-05 — Desarrollo organizado y trazable.

# Alcance de la épica

Esta épica incluye:

- Registro de usuarios.
- Inicio y cierre de sesión.
- Consulta y modificación del perfil.
- Gestión de usuarios por parte del administrador.

No incluye sistemas de autenticación mediante plataformas externas ni el uso de datos personales reales.



# Historias de usuario

### US-001 — REGISTRO DE USUARIO

# Necesidad

Los asistentes al festival necesitan disponer de una cuenta para poder identificarse en Subsonic Festival y acceder a las funcionalidades destinadas a usuarios registrados.

# Objetivo

Este requisito contribuye a los siguientes objetivos del proyecto:

- G-02 — Experiencia clara para el usuario.
- G-03 — Gestión diferenciada por roles.

# Historia de usuario

Como asistente al festival, quiero registrarme en Subsonic Festival para disponer de una cuenta con la que acceder a las funcionalidades disponibles para usuarios registrados.

# Criterios de aceptación

- US-001-AC-01: El usuario puede introducir los datos necesarios para crear una cuenta.
- US-001-AC-02: El sistema informa al usuario si falta algún dato obligatorio.
- US-001-AC-03: El sistema valida los datos introducidos antes de crear la cuenta.
- US-001-AC-04: Si el registro se completa correctamente, el sistema informa al usuario de que la cuenta ha sido creada.
- US-001-AC-05: Si se produce un error durante el registro, el sistema informa al usuario de forma comprensible.

# Reglas

- Cada cuenta debe estar asociada a un identificador único.
- Todos los campos definidos como obligatorios deben completarse para finalizar el registro.
- Un usuario registrado mediante el proceso normal no obtiene permisos de administrador.

# Restricciones

- Durante el desarrollo y las pruebas no se utilizarán datos personales o sensibles reales.
- El registro deberá respetar las reglas de seguridad y privacidad establecidas para el proyecto.

# Requisitos no funcionales

- Los mensajes mostrados durante el registro deben ser claros y comprensibles.
- Los datos introducidos deben validarse antes de almacenarse.
- La interfaz de registro debe respetar los criterios de usabilidad y accesibilidad establecidos para el proyecto.

# Dependencias

No presenta dependencias funcionales previas.



### US-002 — INICIO Y CIERRE DE SESIÓN

# Necesidad

Los usuarios registrados necesitan identificarse en Subsonic Festival para acceder de forma segura a las funcionalidades disponibles según su tipo de usuario.

# Objetivo

Este requisito contribuye a los siguientes objetivos del proyecto:

 G-02 — Experiencia clara para el usuario.
 G-03 — Gestión diferenciada por roles.

# Historia de usuario

Como usuario registrado, quiero iniciar y cerrar sesión en Subsonic Festival para acceder de forma controlada a las funcionalidades correspondientes a mi rol.

# Criterios de aceptación

 US-002-AC-01: El usuario puede introducir sus credenciales para iniciar sesión.
 US-002-AC-02: Si las credenciales son correctas, el sistema permite el acceso a la plataforma.
 US-002-AC-03: Si las credenciales son incorrectas, el sistema rechaza el acceso e informa al usuario mediante un mensaje comprensible.
 US-002-AC-04: Una vez autenticado, el usuario únicamente puede acceder a las funcionalidades permitidas para su rol.
 US-002-AC-05: El usuario autenticado puede cerrar su sesión.
 US-002-AC-06: Una vez cerrada la sesión, el usuario deja de tener acceso a las funcionalidades que requieren autenticación.

# Reglas

 Solo los usuarios con una cuenta válida pueden iniciar sesión.
 Las funcionalidades disponibles dependerán del rol asociado a cada usuario.
 Las operaciones administrativas estarán disponibles únicamente para usuarios con permisos de administrador.

# Restricciones

- Durante el desarrollo y las pruebas se utilizarán únicamente cuentas y datos ficticios.
- El acceso a las funcionalidades deberá respetar el sistema de roles definido para Subsonic Festival.

# Requisitos no funcionales

- Las credenciales deberán tratarse de forma segura.
- Los mensajes de error no deberán mostrar información sensible.
- El sistema deberá informar de forma clara del resultado del inicio y cierre de sesión.
- El control de acceso deberá impedir que un usuario sin autorización acceda a funciones administrativas.

# Dependencias

 US-001 — Registro de usuario, para las cuentas creadas mediante el proceso de registro de la plataforma.

 

### US-003 — CONSULTA Y MODIFICACIÓN DEL PERFIL.


# Necesidad

Los usuarios registrados necesitan poder consultar la información asociada a su cuenta y modificar los datos permitidos para mantener su perfil actualizado.

# Objetivo

Este requisito contribuye a los siguientes objetivos del proyecto:

 G-01 — Gestión centralizada del festival.
 G-02 — Experiencia clara para el usuario.
 G-03 — Gestión diferenciada por roles.

# Historia de usuario

Como usuario registrado, quiero consultar y modificar los datos permitidos de mi perfil para mantener actualizada la información asociada a mi cuenta.

# Criterios de aceptación

 US-003-AC-01: El usuario autenticado puede consultar la información disponible en su perfil.
 US-003-AC-02: El usuario puede modificar los campos que estén habilitados para edición.
 US-003-AC-03: El sistema valida los nuevos datos antes de guardar los cambios.
 US-003-AC-04: Si los datos introducidos no son válidos, el sistema informa al usuario y no guarda los cambios incorrectos.
 US-003-AC-05: Si la modificación se realiza correctamente, el sistema informa al usuario del resultado.
 US-003-AC-06: Un usuario no puede modificar el perfil de otro usuario mediante las funciones destinadas a la gestión de su propio perfil.

# Reglas

- El usuario solo podrá modificar los campos de su perfil que estén habilitados para edición.
- Los datos modificados deberán cumplir las mismas reglas de validación establecidas para dichos campos.
- Cada usuario únicamente podrá gestionar su propio perfil mediante esta funcionalidad.

# Restricciones

- El usuario deberá haber iniciado sesión previamente.
- Durante el desarrollo y las pruebas no se utilizarán datos personales o sensibles reales.
- La modificación del perfil deberá respetar los permisos asociados al usuario.

# Requisitos no funcionales

- La información del perfil deberá mostrarse de forma clara y comprensible.
- El sistema deberá proporcionar información sobre el resultado de las modificaciones realizadas.
- Los datos deberán tratarse de forma segura.
- La interfaz deberá mantener los criterios de usabilidad y accesibilidad establecidos para el proyecto.

# Dependencias

- US-002 — Inicio y cierre de sesión.



### US-004 — GESTIÓN DE USUARIO POR ADMINISTRADOR.

# Necesidad

El personal de administración necesita poder consultar y gestionar las cuentas de usuario de Subsonic Festival para mantener organizada y controlada la información de los usuarios de la plataforma.

# Objetivo

Este requisito contribuye a los siguientes objetivos del proyecto:

 G-01 — Gestión centralizada del festival.
 G-03 — Gestión diferenciada por roles.
 G-05 — Desarrollo organizado y trazable.

# Historia de usuario

Como administrador, quiero consultar y gestionar los usuarios registrados en Subsonic Festival para mantener controladas las cuentas utilizadas en la plataforma.

# Criterios de aceptación

 US-004-AC-01: El administrador puede consultar los usuarios registrados en la plataforma.
 US-004-AC-02: El administrador puede acceder a la información necesaria de cada usuario para realizar las operaciones de gestión previstas.
 US-004-AC-03: El administrador puede realizar las operaciones de gestión de usuarios permitidas por el sistema.
 US-004-AC-04: Un usuario sin permisos de administrador no puede acceder a las funciones de gestión de usuarios.
 US-004-AC-05: El sistema informa del resultado de las operaciones realizadas.
 US-004-AC-06: Si se produce un error durante una operación, el sistema informa al administrador y evita dejar los datos en un estado inconsistente.

# Reglas

- Solo los usuarios con permisos de administrador pueden acceder a la gestión de usuarios.
- Las operaciones realizadas deberán respetar los permisos definidos para cada tipo de usuario.
- Las modificaciones realizadas deberán mantener la integridad de la información almacenada.

# Restricciones

- El administrador deberá haber iniciado sesión previamente.
- Durante el desarrollo y las pruebas se utilizarán únicamente cuentas y datos ficticios.
- Las operaciones administrativas deberán respetar las reglas de seguridad y privacidad establecidas para el proyecto.

# Requisitos no funcionales

- El acceso a las funciones administrativas deberá estar protegido mediante control de permisos.
- La información deberá mostrarse de forma clara y comprensible.
- Las operaciones deberán proporcionar información sobre su resultado.
- Los errores no deberán provocar estados inconsistentes en los datos.

# Dependencias

 US-002 — Inicio y cierre de sesión.
