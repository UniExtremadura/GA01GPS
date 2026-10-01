# Constitución del proyecto — Subsonic Festival 2026
 
**Equipo:** GPS01-2026
**Versión:** 1.0.0 (borrador) · **Fecha:** 2026-10-01
**Ubicación en el repo:** `.specify/memory/constitution.md`
 
Esta constitución es la norma superior y estable del proyecto. Define los principios no negociables que deben respetarse en todas las funcionalidades, especificaciones, planes, tareas e implementaciones. No describe qué funcionalidades se construyen ni cómo se implementan.
 
---
 
## Core Principles
 
### 1. Especificación y trazabilidad
 
Toda funcionalidad debe estar especificada antes de implementarse. Debe poder seguirse la cadena:
 
**Necesidad → requisito → plan → tareas → código → pruebas → evidencias**
 
- No se implementa ninguna funcionalidad que no esté justificada por una especificación aprobada.
- Todo elemento tiene un identificador estable que se mantiene igual en Git, Excel, ProjectLibre y Jira: épicas `EP-XXX`, historias `US-XXX`, tareas `TK-XXX`, subtareas `ST-XXXX` e iteraciones `ITXXX`.
- Una épica que no contribuya a ningún objetivo de `goals.md` se considera fuera de alcance hasta que se apruebe un cambio.
### 2. Disciplina de alcance del MVP
 
El equipo se centra en las funcionalidades necesarias para obtener un producto mínimo viable que ofrezca valor a los usuarios definidos en `mission.md`.
 
Toda ampliación de alcance debe:
- Estar justificada por valor, riesgo o dependencia.
- Ser priorizada mediante MoSCoW.
- Evaluar su impacto en plazo, coste y capacidad del equipo.
- Quedar documentada como una decisión humana del Product Owner.
### 3. Calidad y comportamiento verificable
 
Los requisitos deben ser claros, medibles y comprobables. Cada historia incluye:
- Criterios de aceptación observables.
- Tratamiento de errores y casos límite relevantes.
- Pruebas adecuadas a su riesgo.
- Cumplimiento de la Definition of Done.
Una funcionalidad no se considera terminada porque el código funcione en condiciones ideales.
 
### 4. Seguridad, privacidad y datos sintéticos
 
El proyecto utiliza exclusivamente datos ficticios o sintéticos. La solución debe:
- Evitar cualquier dato personal, bancario o de pago real. Los saldos, compras y pagos son simulados.
- Validar todas las entradas y controlar el acceso según el rol de cada usuario (cliente, proveedor, administrador).
- Proteger la información y las operaciones sensibles, como cambios de estado de cuentas, aprobaciones y cancelaciones.
- **No almacenar en el repositorio claves, credenciales, archivos de configuración con secretos ni archivos `.env` reales.** Los secretos se gestionan fuera del control de versiones, y si alguno se expone, se revoca de inmediato.
- Considerar la seguridad desde la especificación hasta las pruebas.
### 5. Usabilidad y accesibilidad
 
Las funcionalidades deben ser comprensibles, consistentes y fáciles de utilizar. Los flujos principales, los mensajes de error y las interfaces se diseñan teniendo en cuenta la accesibilidad y la diversidad de usuarios, y ofrecen siempre una forma clara de continuar ante un error recuperable.
 
---
 
## Development and Documentation Standards
 
**Responsabilidad de cada artefacto**
 
| Artefacto | Responde a |
|---|---|
| `mission.md` | Por qué existe el producto, para quién y qué valor aporta. |
| `goals.md` | Qué se quiere conseguir, cómo se medirá y dónde están los límites del alcance. |
| `spec.md` | Qué se necesita y por qué (por épica). |
| `plan.md` | Cómo se abordará técnicamente. |
| `tasks.md` | Qué trabajo concreto y ejecutable se deriva del plan. |
 
**Reglas**
- Se mantiene la separación entre *qué/por qué* (especificación) y *cómo* (plan). Las especificaciones no prescriben implementación.
- Las decisiones importantes quedan documentadas en la Wiki con fecha, motivo y elementos afectados. Las decisiones técnicas relevantes se registran como ADR.
- Los artefactos mantienen la trazabilidad entre sí y se actualizan cuando cambia alguno de ellos.
- El Product Owner es responsable del contenido de negocio; el Tech Lead, del técnico. Ambos responden de que sus artefactos sean coherentes con esta constitución.
- Las decisiones de definición del producto las toman personas. Si se usan herramientas de IA, su salida es una propuesta que el equipo revisa y aprueba, nunca una decisión.
---
 
## Quality Gates and Delivery Workflow
 
Antes de aprobar una especificación, un plan o una implementación debe comprobarse que:
 
- [ ] Cumple los principios de esta constitución.
- [ ] Respeta el alcance acordado en `goals.md`.
- [ ] Mantiene la trazabilidad (identificadores y enlaces entre artefactos).
- [ ] Define criterios de aceptación verificables.
- [ ] Considera calidad, pruebas, seguridad y accesibilidad.
- [ ] No contiene decisiones importantes sin justificar.
- [ ] No incluye datos reales ni secretos.
**Puertas de entrada y salida**
- **Entrada a sprint:** la historia cumple la Definition of Ready.
- **Cierre de historia:** la historia cumple la Definition of Done, y al menos una persona distinta de su autor ha revisado el cambio.
- **Integración:** nada se fusiona con el pipeline de integración en rojo.
---
 
## Governance
 
- La constitución tiene prioridad sobre el resto de los documentos del proyecto.
- Cualquier modificación debe:
  1. Estar justificada.
  2. Ser aprobada explícitamente por el equipo, con decisión final del Product Owner.
  3. Registrar la fecha y la nueva versión.
  4. Indicar qué documentos o decisiones resultan afectados.
- **Versionado:** cambio mayor (X.0.0) si se añade, elimina o redefine un principio; menor (0.X.0) si se amplía una sección; parche (0.0.X) para correcciones de redacción.
- **Excepciones:** deben ser explícitas, justificadas, aprobadas y, cuando sea posible, temporales, con fecha de revisión.
### Historial de versiones
 
| Versión | Fecha | Cambios |
|---|---|---|
| 1.0.0 | 2026-10-01 | Versión inicial adaptada a Subsonic Festival 2026. |
 
