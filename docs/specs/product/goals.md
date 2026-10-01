# Subsonic — Objetivos

## Objetivos

| ID | Objetivo | Resultado esperado |
|---|---|---|
| G-01 | Gestión centralizada del festival | El personal autorizado puede gestionar desde una misma plataforma los principales elementos necesarios para la organización de Subsonic, como usuarios, entradas, espacios, servicios, proveedores, merchandising e incidencias. |
| G-02 | Experiencia clara para el usuario | Los usuarios pueden realizar las acciones principales de la plataforma de forma comprensible, sabiendo qué información deben introducir y cuál ha sido el resultado de cada operación. |
| G-03 | Gestión diferenciada por roles | La aplicación permite diferenciar las acciones disponibles según el tipo de usuario y restringir las operaciones administrativas al personal autorizado. |
| G-04 | Incremento funcional y revisable | El equipo produce una versión estable del proyecto que puede instalarse, ejecutarse y evaluarse siguiendo únicamente la documentación disponible. |
| G-05 | Desarrollo organizado y trazable | Las funcionalidades principales pueden relacionarse con los objetivos, las tareas realizadas, el código desarrollado y las pruebas o evidencias correspondientes. |



## Indicadores de éxito

| ID | Objetivo | Meta |
|---|---|---|
| M-01 | G-01 | Las operaciones esenciales de gestión incluidas en el alcance pueden demostrarse correctamente durante la revisión del proyecto. |
| M-02 | G-02 | Al menos cuatro de cinco participantes pueden completar un recorrido básico de la plataforma sin ayuda externa. |
| M-03 | G-02 | Al menos cuatro de cinco participantes identifican correctamente el resultado de las operaciones realizadas y comprenden los mensajes mostrados por el sistema. |
| M-04 | G-03 | Un usuario sin permisos administrativos no puede acceder a las operaciones reservadas al administrador. |
| M-05 | G-04 | Una persona que no haya desarrollado el proyecto puede instalarlo y ejecutarlo siguiendo el README, sin necesitar instrucciones adicionales no documentadas. |
| M-06 | G-05 | Cada funcionalidad principal desarrollada puede relacionarse con al menos un objetivo y con las tareas o evidencias correspondientes. |
| M-07 | Todos | No existe ningún defecto bloqueante conocido durante la revisión final del incremento. |



## Stakeholders

### Asistente al festival

Persona que utiliza Subsonic para interactuar con los servicios disponibles relacionados con el festival.

Necesita:

- Acceder a la plataforma de forma sencilla.
- Consultar información relevante del festival.
- Gestionar las acciones disponibles para su tipo de usuario.
- Recibir información clara sobre el resultado de sus acciones.

### Personal de organización y administración

Personas responsables de mantener la información necesaria para el funcionamiento del festival.

Necesitan:

- Gestionar usuarios.
- Gestionar entradas.
- Mantener la información de espacios.
- Gestionar servicios.
- Gestionar proveedores.
- Gestionar merchandising.
- Registrar y consultar incidencias.

### Proveedores

Entidades o personas encargadas de prestar determinados servicios durante el festival.

Necesitan que la información relacionada con sus servicios pueda mantenerse de forma organizada dentro de la plataforma.

### Equipo de desarrollo

Estudiantes de Ingeniería Informática responsables del análisis, planificación, desarrollo, pruebas y documentación del proyecto.

Necesitan:

- Disponer de un alcance asumible.
- Mantener una organización clara del trabajo.
- Registrar las decisiones importantes.
- Coordinar el desarrollo realizado por los distintos integrantes.
- Poder demostrar las decisiones y el trabajo realizado durante la asignatura.

### Profesorado

Actúa como stakeholder académico y responsable de evaluar el proyecto.

Necesita poder:

- Comprender los objetivos del producto.
- Revisar la planificación y las decisiones del equipo.
- Comprobar la evolución del proyecto.
- Instalar y ejecutar el incremento entregado.
- Revisar las evidencias y documentación asociadas.



## Alcance incluido

El proyecto incluye:

- **S-01:** autenticación de usuarios y control básico de acceso.
- **S-02:** gestión de los usuarios necesarios para la demostración.
- **S-03:** gestión de entradas del festival.
- **S-04:** gestión de espacios.
- **S-05:** gestión de servicios.
- **S-06:** gestión de proveedores.
- **S-07:** gestión de merchandising.
- **S-08:** gestión de incidencias.
- **S-09:** funciones administrativas necesarias para mantener la información utilizada por la plataforma.
- **S-10:** almacenamiento de un conjunto controlado de datos ficticios necesarios para demostrar el funcionamiento del sistema.
- **S-11:** documentación suficiente para instalar, ejecutar y evaluar el incremento desarrollado.

El equipo se centrará en obtener primero un recorrido funcional y estable de estas capacidades antes de incorporar ampliaciones.



## Exclusiones

Quedan expresamente fuera del alcance inicial:

- **EX-01:** pagos económicos reales.
- **EX-02:** venta y validación de entradas reales para un festival existente.
- **EX-03:** integración con plataformas comerciales externas de venta de entradas.
- **EX-04:** operaciones bancarias, facturación o gestión económica real.
- **EX-05:** utilización de datos personales o financieros reales.
- **EX-06:** despliegue de la plataforma como servicio comercial en producción.
- **EX-07:** garantía de funcionamiento para grandes volúmenes de usuarios concurrentes.
- **EX-08:** desarrollo de aplicaciones móviles nativas.
- **EX-09:** funcionalidades adicionales que no contribuyan directamente a ninguno de los objetivos establecidos en este documento.



## Supuestos

El proyecto parte de los siguientes supuestos:

- **A-01:** los miembros del equipo disponen de los conocimientos técnicos básicos necesarios para desarrollar el proyecto con el apoyo de los contenidos de la asignatura.
- **A-02:** todos los integrantes participarán activamente en las tareas asignadas.
- **A-03:** el equipo dispondrá de acceso a las herramientas de desarrollo, repositorio y gestión utilizadas durante la asignatura.
- **A-04:** las tecnologías seleccionadas permiten implementar el alcance previsto.
- **A-05:** los datos necesarios para desarrollar y probar la plataforma pueden representarse mediante información ficticia o sintética.
- **A-06:** el alcance podrá ajustarse durante el proyecto si aparecen nuevas restricciones, feedback del profesorado o cambios en la capacidad disponible del equipo.



## Restricciones

El proyecto deberá cumplir las siguientes condiciones:

- **R-01:** debe desarrollarse dentro de los plazos establecidos por la asignatura de Gestión de Proyectos Software.
- **R-02:** el alcance deberá ser asumible por el equipo dentro del tiempo disponible.
- **R-03:** no se utilizarán datos personales, bancarios o sensibles reales.
- **R-04:** se utilizarán las tecnologías y convenciones aprobadas por el equipo.
- **R-05:** el código y la documentación deberán mantenerse en el repositorio Git del proyecto.
- **R-06:** los cambios importantes de alcance deberán quedar justificados y registrados.
- **R-07:** una ampliación de alcance no deberá comprometer las funcionalidades esenciales ya definidas.
- **R-08:** el incremento entregado deberá poder ejecutarse siguiendo la documentación del repositorio.



## Trazabilidad

La cadena de trazabilidad utilizada en Subsonic será:

**Misión → objetivos → épicas → historias → tareas → código y pruebas → evidencias**

Toda épica o funcionalidad relevante deberá contribuir al menos a uno de los objetivos definidos en este documento.

Si una nueva propuesta no contribuye a ningún objetivo, se considerará fuera del alcance hasta que se apruebe una modificación de `goals.md`.



## Gestión de cambios

Cualquier modificación de un objetivo, una métrica, el alcance, una exclusión, un supuesto o una restricción requerirá:

1. Revisión de la propuesta por parte del equipo.
2. Evaluación del impacto sobre el tiempo y la capacidad disponible.
3. Decisión explícita del responsable correspondiente del proyecto.
4. Registro de la decisión tomada.
5. Revisión de las especificaciones, tareas y planificación afectadas.
6. Actualización de las referencias y documentos correspondientes.

Las ampliaciones de alcance deberán estar justificadas y priorizadas. Si una nueva funcionalidad pone en riesgo el cumplimiento de los objetivos principales, se priorizará completar y estabilizar el alcance ya acordado.
