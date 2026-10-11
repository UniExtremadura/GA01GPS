# Revisión de requisitos — Subsonic Festival

## Fecha de revisión

2026-10-09

## Herramienta y modelo utilizados

- Herramienta: revisión documental del repositorio mediante lectura de artefactos en VS Code/Copilot SDK.
- Modelo: revisión asistida por IA; no se identificó un modelo externo concreto para la auditoría documental.

## Archivos analizados

- `constitution.md`
- `specs/EP-001-autenticacion-usuarios/spec.md`
- `specs/EP-002-entradas/spec.md`
- `specs/EP-003-espacios/spec.md`
- `specs/EP-004-servicios/spec.md`
- `specs/EP-005-proveedores/spec.md`
- `specs/EP-006-merchandising/spec.md`
- `specs/EP-007-incidencias/spec.md`
- `Organization/Planificacion.csv` (referencia de planificación, sin evidencia de objetivos, alcance ni DoR/DoD)

Se comprobó la estructura disponible del repositorio y se localizaron los siguientes artefactos formales en rutas reales del proyecto:

- `constitution.md`
- `docs/specs/product/mission.md`
- `docs/specs/product/goals.md`
- `docs/quality/definition-of-ready.md`
- `docs/quality/definition-of-done.md`

El alcance del proyecto no aparece en un archivo llamado `scope.md`, pero sí está formalizado en la sección “Alcance incluido” de `docs/specs/product/goals.md`.

## Resumen general

La base documental disponible permite identificar siete épicas y diecinueve historias de usuario con un patrón claro de negocio (autenticación, entradas, espacios, servicios, proveedores, merchandising e incidencias). El conjunto tiene una intención funcional consistente y una buena cobertura temática del festival, pero la trazabilidad entre las historias y los documentos base, así como la aplicación consistente del Definition of Ready y Definition of Done, requiere una revisión más explícita. Esto reduce la verificabilidad del conjunto y deja varios requisitos con ambigüedad, superposición y criterios de aceptación difíciles de validar de forma objetiva.

## Hallazgos

### RA-001 — Trazabilidad parcial al alcance y comprobación individual del DoR

- Historia o épica afectada: las 19 historias de usuario y su relación con los objetivos y el alcance del proyecto.
- Problema y evidencia concreta:
  - Los documentos de constitución, misión, objetivos, alcance, Definition of Ready y Definition of Done existen en el repositorio.
  - Las 19 historias tienen identificador, están asociadas a una épica y documentan prioridad MoSCoW, estimación en horas-persona y predecesores. Todas incluyen además un apartado de objetivos con referencias a códigos G.
  - Existe una relación conceptual entre las historias y el alcance S-01 a S-10 por sus áreas funcionales, aunque los códigos S-XX no se referencian explícitamente en cada historia.
  - S-11, relativo a documentación suficiente para instalar, ejecutar y evaluar el incremento, no tiene una historia específica entre las 19; su cobertura podría registrarse mediante tareas o entregables.
  - G-04 no aparece referenciado directamente en las historias, aunque puede abordarse mediante actividades transversales de integración y entrega.
  - Algunas historias presentan aspectos pendientes frente al DoR: US-011 y US-014 emplean el término ambiguo «usuario autorizado»; US-001 no concreta campos obligatorios y reglas de validación; US-009 no define los filtros; US-019 deja pendientes estados y reglas de negocio; y las justificaciones de prioridad MoSCoW no siempre están documentadas explícitamente.
  - La presencia de una estimación en cada historia no demuestra por sí sola que esté documentado el proceso de estimación individual y su consenso por el equipo, tal como pide el DoR.
  - El cumplimiento del DoR debe verificarse historia por historia antes de seleccionar cada una para una iteración, considerando las posibles excepciones acordadas y registradas. La revisión documental no demuestra por sí sola que las historias incumplan el DoR de forma generalizada.
  - No corresponde exigir evidencias de cumplimiento del Definition of Done en esta fase de especificación y planificación. El DoD incluye implementación, pruebas, integración, revisión y aceptación, y deberá comprobarse al implementar y cerrar cada historia.
- Propuesta de mejora justificada:
  - Reforzar las referencias explícitas de alcance cuando mejoren la trazabilidad, sin exigir cambios innecesarios en las especificaciones; registrar la cobertura de S-11 y el seguimiento de G-04 mediante tareas o entregables adecuados si el equipo lo considera pertinente.
  - Comprobar el DoR individualmente antes de planificar cada historia, incluyendo las cuestiones específicas identificadas y registrando cualquier excepción aprobada.
  - Verificar el cumplimiento del DoD en la fase de implementación y cierre de cada historia, no durante esta revisión de especificaciones.
- Supuestos e incertidumbres:
  - La asociación semántica entre historias y S-01 a S-10 se ha inferido por su contenido y agrupación en épicas; no se afirma que exista ya una matriz formal de trazabilidad S-XX.
  - La ausencia de historia específica para S-11 no implica necesariamente falta de cobertura si se gestiona mediante tareas o entregables.
  - No se dispone de evidencia suficiente para confirmar cómo se consensuaron las estimaciones ni si se aprobaron excepciones al DoR.
- Estado: Aceptado con modificaciones tras revisión humana.
- Justificación de la decisión: La revisión humana confirma que la documentación base y los principales campos de las 19 historias sí existen, así como sus referencias a objetivos G. Se mantiene el hallazgo únicamente por vacíos acotados de trazabilidad al alcance y cuestiones específicas del DoR, sin considerar incumplido el DoD antes de la implementación.

### RA-002 — La matriz consolidada de roles y permisos está pendiente y existen ambigüedades entre historias

- Historia o épica afectada:
  - EP-001 (US-001 a US-004)
  - EP-002 (US-005 a US-008)
  - EP-003 (US-009 a US-011)
  - EP-004 (US-012 a US-014)
  - EP-005 (US-015 y US-016)
  - EP-006 (US-017 y US-018)
  - EP-007 (US-019)
- Problema y evidencia concreta:
  - Los roles cliente, proveedor y administrador sí están definidos en la constitución y en los documentos de producto. Además, varias historias especifican permisos parciales, especialmente para usuarios autenticados y administradores. Sin embargo, no se localiza una matriz consolidada que asigne permisos concretos a cada rol de forma coherente para todas las capacidades.
  - No se concretan las operaciones que puede realizar el proveedor. La misión le atribuye gestión de información y operaciones que le correspondan, pero las historias de gestión de proveedores asignan esas tareas al administrador (US-016), sin definir capacidades de una cuenta de proveedor.
  - El término "usuario autorizado" no identifica qué rol o permiso otorga acceso a la gestión en US-011 y US-014; se alterna con "administrador" en los planes o justificaciones.
  - Las operaciones administrativas de US-004 son poco precisas: se alude a las operaciones "permitidas por el sistema" y a la información "necesaria", sin enumerar acciones ni límites de consulta o modificación.
  - US-001 indica que el registro normal no concede permisos de administrador, pero no se define cómo se asignan los roles de administrador y proveedor.
  - No se aclara si las consultas de catálogos requieren autenticación en US-005, US-009, US-012, US-015 y US-017, a diferencia de reservas y adquisiciones, donde sí se exige iniciar sesión.
  - US-019 no resuelve si registrar una incidencia requiere autenticación: la dependencia de US-002 solo lo condiciona para las operaciones que la requieran. Tampoco precisa si el usuario que la registra puede consultar su propia incidencia.
  - Hay diferencias de terminología entre documentos e historias —"cliente", "asistente", "usuario", "usuario registrado", "personal de administración", "administrador" y "usuario autorizado"— sin declarar equivalencias o límites entre esos términos.
- Propuesta de mejora justificada:
  - Consolidar en una matriz de roles y permisos las acciones permitidas y denegadas para cliente/asistente, proveedor y administrador, y referenciarla desde las historias afectadas.
  - Aclarar en las historias mencionadas qué rol puede realizar cada operación, qué operaciones requieren autenticación y cómo se asignan los roles, sin dar por decididas esas cuestiones hasta su validación por el equipo.
  - Alinear la terminología de actores y roles entre documentos, épicas e historias.
- Supuestos e incertidumbres:
  - La revisión confirma que los roles ya están definidos y que las historias contienen permisos parciales; el hallazgo se limita a la falta de consolidación y a las ambigüedades identificadas.
  - La política de acceso prevista para consultas y registro/consulta de incidencias no queda determinada por la documentación actual.
- Estado: Aceptado con modificaciones tras revisión humana.
- Justificación de la decisión: La revisión humana confirmó que los roles y parte de sus permisos sí están documentados, por lo que se descarta la afirmación inicial de que faltaba toda definición. Se mantiene el hallazgo, acotado a la ausencia de una matriz consolidada y a las ambigüedades concretas que aún requieren decisión del equipo.

### RA-003 — Algunos criterios de aceptación son ambiguos; otros ya son verificables

- Historia o épica afectada: las 19 historias de usuario (US-001 a US-019); los ejemplos concretos de ambigüedad se detallan a continuación.
- Problema y evidencia concreta:
  - La revisión de todos los criterios de aceptación confirma que ciertos enunciados dejan decisiones necesarias para la verificación sin especificar. Entre las expresiones recurrentes están «información necesaria», «de forma comprensible», «cuando corresponda» y «correctamente».
  - En US-001-AC-01 («El usuario puede introducir los datos necesarios para crear una cuenta»), US-001-AC-02 («El sistema informa al usuario si falta algún dato obligatorio») y US-001-AC-03 («El sistema valida los datos introducidos antes de crear la cuenta») no se enumeran los campos obligatorios ni las reglas de validación.
  - En US-009-AC-03 («El usuario puede aplicar los filtros disponibles para reducir los resultados mostrados») y US-009-AC-04 («Los resultados mostrados corresponden con los filtros seleccionados») no se identifican los filtros ni la regla de coincidencia o combinación entre ellos.
  - En US-019-AC-06 («El administrador puede modificar el estado de una incidencia») no se definen los estados ni las transiciones permitidas; otros criterios de la historia también dejan sin precisar los campos solicitados y el alcance de consulta.
  - En US-011-AC-01 a US-011-AC-04 y US-014-AC-01 a US-014-AC-04, «usuario autorizado» no identifica el rol habilitado. En estos criterios también hay aspectos que podrían requerir precisión —por ejemplo, qué campos pueden modificarse y cuándo eliminar o deshabilitar—, pero son cuestiones distintas a la ambigüedad del actor.
  - También se observaron expresiones como «de forma comprensible» y «correctamente» en criterios de comunicación de errores, resultados y actualización de datos. Si bien algunos criterios requieren precisión adicional, la revisión también identificó criterios cuyo comportamiento principal es observable y verificable, por ejemplo US-002-AC-05 («El usuario autenticado puede cerrar su sesión») y US-007-AC-03 («Un usuario únicamente puede consultar las entradas asociadas a su propia cuenta mediante esta funcionalidad»). Por tanto, el problema no afecta por igual a todos los criterios ni implica que deban reescribirse en bloque.
- Propuesta de mejora justificada:
  - Para los criterios ambiguos, acordar los datos, reglas de negocio, roles, estados, resultados y evidencias necesarios para que cada caso pueda comprobarse objetivamente.
  - Mantener los criterios que ya describen un resultado observable suficiente, salvo que una revisión del contexto o de dependencias revele una necesidad concreta de cambio.
  - Las propuestas de redacción y las decisiones pendientes deberán concretarse y validarse por el equipo antes de incorporarse a las historias; los ejemplos de este informe no son cambios aprobados.
- Supuestos e incertidumbres:
  - La evaluación distingue entre una intención funcional comprensible y un criterio suficientemente preciso para una prueba reproducible.
  - Algunos valores necesarios (como campos obligatorios, filtros, estados/transiciones y rol habilitado) son decisiones de producto que no deben inferirse durante esta revisión.
- Estado: Aceptado con modificaciones tras revisión humana.
- Justificación de la decisión: La revisión humana confirma que existen criterios ambiguos que deben precisarse, pero también criterios claros y verificables que no necesitan cambios. Se acota el hallazgo a los casos con una carencia demostrable y se evita proponer una reescritura indiscriminada.

### RA-004 — US-018 y US-019 agrupan responsabilidades de actores diferentes

- Historia o épica afectada:
  - US-018 — adquisición de merchandising por el usuario y gestión administrativa del catálogo.
  - US-019 — registro de incidencias por el usuario y consulta y gestión por el administrador.
- Problema y evidencia concreta:
  - US-018 contiene dos historias bajo un mismo identificador: una para que el usuario registrado adquiera productos de merchandising y otra para que el administrador gestione el catálogo. Sus criterios de aceptación abarcan ambos flujos y roles.
  - US-019 también contiene dos historias bajo un mismo identificador: una para registrar incidencias y otra para que el administrador consulte incidencias y gestione su estado.
  - La agrupación puede dificultar la estimación, la planificación por iteración y la verificación separada de los permisos y resultados de cada actor. La división es una posibilidad a valorar, no una decisión tomada por esta revisión.
  - Repetir patrones funcionales entre épicas distintas —por ejemplo, consulta, adquisición o administración de entidades diferentes— no constituye por sí mismo una duplicidad. Solo debe considerarse un problema si produce inconsistencias o contradicciones entre requisitos.
- Propuesta de mejora justificada:
  - Valorar si conviene dividir US-018 y US-019 en historias independientes por actor y flujo. La decisión deberá validarse por el equipo según el Definition of Ready, la capacidad disponible en las iteraciones y las necesidades de planificación.
  - Si se decide dividir ambas historias, el backlog pasaría de 19 a 21 historias. Antes de incorporarlas, deberán revisarse los identificadores y sus referencias, estimaciones, prioridades y dependencias; las estimaciones actuales no deben repartirse automáticamente entre las historias resultantes.
  - Mantener la repetición de patrones entre épicas cuando refleje funcionalidades distintas; revisar esos patrones únicamente cuando se detecten inconsistencias o contradicciones concretas.
- Supuestos e incertidumbres:
  - La revisión confirma que US-018 y US-019 agrupan responsabilidades asociadas a actores diferentes.
  - No se ha determinado si la división ofrece una ventaja suficiente frente al coste de ampliar y reorganizar el backlog; corresponde al equipo decidirlo.
- Estado: Aceptado con modificaciones tras revisión humana.
- Justificación de la decisión: La revisión humana confirma la mezcla de actores y responsabilidades en US-018 y US-019, pero la división depende de la capacidad y planificación del equipo. También se reconoce que la repetición de patrones entre épicas no es una duplicidad por sí sola, por lo que el hallazgo queda acotado a las dos historias y a sus posibles efectos de planificación y verificación.

### RA-005 — No se formaliza un modelo de datos ni una definición de estados de negocio reutilizable para disponibilidad, reservas, adquisiciones y incidencias

- Historia o épica afectada:
  - EP-002, EP-003, EP-004, EP-006 y EP-007
- Problema y evidencia concreta:
  - Las historias ya contienen reglas parciales de disponibilidad, habilitación y deshabilitación para entradas (US-005, US-006 y US-008), espacios (US-009 a US-011), servicios (US-012 a US-014), proveedores (US-015 y US-016) y productos de merchandising (US-017 y US-018). US-019 también establece que cada incidencia debe tener un estado para su seguimiento y que el administrador puede modificarlo.
  - Estas reglas parciales no resuelven algunos aspectos necesarios para verificar los flujos:
    - US-010 requiere comprobar la disponibilidad del espacio y contempla intentos simultáneos, pero no define la regla de disponibilidad aplicable ni el resultado esperado cuando varias reservas concurrentes compiten por el mismo espacio.
    - US-019 no enumera los estados posibles de una incidencia ni las transiciones permitidas.
    - Para entradas, servicios y merchandising, las historias condicionan la adquisición a la disponibilidad, pero no concretan todas las condiciones que determinan esa disponibilidad.
    - US-016 y US-018 permiten eliminar o deshabilitar proveedores y productos “cuando corresponda”, sin definir la diferencia entre ambas acciones ni sus consecuencias.
    - No se explican los efectos de cambios de disponibilidad, deshabilitación o eliminación sobre reservas, adquisiciones u otras operaciones ya registradas.
  - Por tanto, no es correcto afirmar que no exista ninguna definición de estados o reglas de negocio. El problema es que las definiciones existentes son parciales y no determinan algunos resultados y casos límite relevantes, lo que puede dar lugar a implementaciones o pruebas con interpretaciones diferentes.
- Propuesta de mejora justificada:
  - Concretar y validar con el equipo las reglas de negocio y los estados necesarios para comprobar los criterios de aceptación, en particular los aspectos pendientes identificados para US-010 y US-019 y el significado operativo de disponibilidad, eliminación y deshabilitación.
  - No se considera necesario exigir en esta fase un modelo de datos técnico completo. La mejora se limita a especificar el comportamiento de negocio verificable, sin prescribir una implementación ni inventar estados o transiciones.
- Supuestos e incertidumbres:
  - Se reconoce que las historias ya documentan reglas parciales de disponibilidad, habilitación y deshabilitación y referencias al estado de las incidencias.
  - Los estados, transiciones y efectos concretos pendientes son decisiones de producto que deben ser acordadas por el equipo; no se presuponen en este hallazgo.
- Estado: Aceptado con modificaciones tras revisión humana.
- Justificación de la decisión: La revisión humana confirma que ya existen reglas parciales, por lo que se descarta la afirmación de ausencia total. Se mantiene el hallazgo, acotado a las reglas y estados necesarios que aún faltan para verificar los criterios de aceptación, sin exigir un modelo de datos técnico completo.

### RA-006 — No se identifica explícitamente qué historias componen el MVP mínimo

- Historia o épica afectada: las 19 historias de usuario, con especial atención a las clasificadas como Should y Could.
- Problema y evidencia concreta:
  - La documentación de misión, objetivos y alcance sí existe: `constitution.md` establece la orientación al MVP; `docs/specs/product/mission.md` define la misión; y `docs/specs/product/goals.md` contiene los objetivos G-01 a G-05, el alcance incluido S-01 a S-11 y las exclusiones EX-01 a EX-09.
  - Las 19 historias tienen prioridad MoSCoW documentada: 11 Must, 6 Should y 2 Could.
  - Aun así, no se identifica explícitamente qué historias forman la primera entrega mínima ni se documenta con claridad cómo las prioridades MoSCoW delimitan esa entrega y se relacionan con dependencias y capacidad del equipo.
  - Esta falta de precisión no demuestra que las prioridades actuales sean incorrectas. En particular, US-017 y US-018 (merchandising), clasificadas como Could, pueden formar parte del alcance general del proyecto sin ser imprescindibles para el MVP.
- Propuesta de mejora justificada:
  - Completar `docs/specs/product/goals.md` con una definición explícita del MVP y su relación con las prioridades MoSCoW, las dependencias y la capacidad del equipo.
  - La definición y selección de funcionalidades para el MVP debe ser validada por el Product Owner. No deben asumirse funcionalidades como aprobadas para esa primera entrega sin dicha validación.
- Supuestos e incertidumbres:
  - La documentación revisada identifica el alcance general, pero no determina qué historias componen el MVP mínimo.
  - No se presume una selección de historias ni una decisión de producto no registrada.
- Estado: Aceptado con modificaciones tras revisión humana.
- Justificación de la decisión: La revisión humana confirma que existen la misión, los objetivos, el alcance y las prioridades MoSCoW. Se mantiene el hallazgo únicamente por no explicitar qué historias integran el MVP mínimo ni cómo se delimitan con esas prioridades, dependencias y capacidad.

## Conclusión

El repositorio disponible presenta una especificación funcional extensa y bastante estructurada. Los documentos de misión, objetivos, alcance, Definition of Ready y Definition of Done sí existen; la mejora pendiente consiste en reforzar la trazabilidad entre esos documentos y las historias, y comprobar la aplicación consistente del DoR y el DoD. Los principales puntos de atención son la ausencia de una matriz de roles/permisos, la ambigüedad de los criterios de aceptación y la necesidad de revisar historias que mezclan varios actores o flujos de negocio.

Las propuestas anteriores no deben tomarse como decisiones de diseño; quedan pendientes de revisión humana y validación del equipo.
