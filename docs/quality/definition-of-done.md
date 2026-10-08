# Subsonic — Definition of Done

## Propósito

El **Definition of Done (DoD)** establece las condiciones mínimas que debe cumplir una historia de usuario para poder considerarse terminada.

Una funcionalidad no se considera terminada únicamente porque haya sido programada o funcione en condiciones ideales.

Para alcanzar el estado **Done**, la historia deberá estar implementada, verificada, integrada y documentada de acuerdo con las normas del proyecto.

---

## 1. Implementación

- [ ] La funcionalidad descrita en la historia de usuario ha sido completamente implementada.
- [ ] El comportamiento desarrollado corresponde con la historia aprobada.
- [ ] La implementación respeta la arquitectura y las convenciones técnicas acordadas por el equipo.
- [ ] No existen fragmentos de código temporal necesarios únicamente para que la funcionalidad funcione.
- [ ] No quedan errores críticos conocidos relacionados con la implementación.
- [ ] El código es suficientemente claro y mantenible para que pueda ser comprendido por otros integrantes del equipo.

---

## 2. Criterios de aceptación

- [ ] Se han comprobado todos los criterios de aceptación definidos en la historia de usuario.
- [ ] Todos los criterios obligatorios se cumplen correctamente.
- [ ] El comportamiento implementado coincide con el especificado.
- [ ] Se dispone de evidencias de la comprobación cuando sean necesarias.
- [ ] Los principales casos de error definidos en la historia han sido comprobados.

Una historia no podrá considerarse terminada si alguno de sus criterios de aceptación obligatorios no se cumple.

---

## 3. Pruebas

- [ ] Se han realizado las pruebas necesarias para comprobar la funcionalidad.
- [ ] Se ha probado el comportamiento esperado en los casos principales.
- [ ] Se han probado los errores y casos límite relevantes.
- [ ] Las pruebas existentes relacionadas con la funcionalidad continúan funcionando.
- [ ] No se han introducido regresiones críticas conocidas.
- [ ] Las pruebas manuales o automatizadas realizadas pueden identificarse o documentarse cuando sea necesario.

Siempre que resulte razonable, se favorecerá la automatización de las pruebas repetitivas.

---

## 4. Integración

- [ ] Los cambios están integrados en la rama correspondiente del proyecto.
- [ ] No existen conflictos pendientes con otros cambios del equipo.
- [ ] La versión integrada del proyecto puede ejecutarse correctamente.
- [ ] La nueva funcionalidad funciona también después de su integración con el resto del sistema.
- [ ] La integración no rompe funcionalidades principales que ya estaban operativas.
- [ ] Los cambios realizados están registrados correctamente mediante Git.

No se considerará terminada una historia que funcione únicamente en el entorno o rama individual de un integrante.

---

## 5. Seguridad y datos

Cuando sea aplicable a la historia:

- [ ] Las entradas del usuario son validadas.
- [ ] Se han comprobado los permisos correspondientes al tipo de usuario.
- [ ] Un usuario sin autorización no puede realizar operaciones restringidas.
- [ ] No se han incluido contraseñas, claves privadas, tokens u otras credenciales sensibles directamente en el código.
- [ ] Los datos utilizados para desarrollo y pruebas son ficticios o sintéticos.
- [ ] No se utilizan datos personales, bancarios o sensibles reales.

---

## 6. Usabilidad y accesibilidad

Cuando la historia incluya interacción con el usuario:

- [ ] La funcionalidad es comprensible para el usuario al que está destinada.
- [ ] Las acciones principales proporcionan una respuesta clara sobre su resultado.
- [ ] Los mensajes de error permiten comprender qué ha ocurrido.
- [ ] La interfaz mantiene coherencia con el resto de Subsonic.
- [ ] Se han tenido en cuenta los requisitos de accesibilidad aplicables.
- [ ] Los errores recuperables permiten al usuario continuar utilizando el sistema.

---

## 7. Requisitos no funcionales

- [ ] Se han comprobado los requisitos no funcionales asociados a la historia.
- [ ] Se han considerado las restricciones de seguridad aplicables.
- [ ] Se han considerado los requisitos de rendimiento cuando sean relevantes.
- [ ] Se han considerado usabilidad y accesibilidad cuando sean aplicables.
- [ ] La implementación respeta las restricciones establecidas en `goals.md` y `constitution.md`.

Una historia no necesitará cumplir requisitos no funcionales que no sean aplicables a su contexto, pero deberá quedar claro cuáles han sido considerados.

---

## 8. Documentación

- [ ] La documentación técnica relevante se ha actualizado cuando ha sido necesario.
- [ ] La documentación de usuario se ha actualizado si la funcionalidad modifica la forma de utilizar Subsonic.
- [ ] Cualquier nueva configuración necesaria para ejecutar el proyecto está documentada.
- [ ] El `README.md` se ha actualizado si han cambiado los pasos de instalación o ejecución.
- [ ] Las decisiones relevantes tomadas durante el desarrollo están registradas cuando corresponde.

La documentación deberá permitir que otro integrante del equipo pueda comprender el cambio realizado sin depender únicamente de quien lo implementó.

---

## 9. Trazabilidad

- [ ] La implementación puede relacionarse con su historia `US-XXX`.
- [ ] La historia continúa asociada a su épica `EP-XXX`.
- [ ] La historia puede relacionarse con al menos un objetivo de `goals.md`.
- [ ] Las tareas realizadas pueden relacionarse con la historia correspondiente.
- [ ] Las pruebas o evidencias realizadas pueden asociarse a la funcionalidad implementada.

La trazabilidad del trabajo seguirá, cuando corresponda:

**Misión → Objetivos → Épicas → Historias → Tareas → Código y pruebas → Evidencias**

---

## 10. Revisión

- [ ] El trabajo ha sido revisado siguiendo el proceso acordado por el equipo.
- [ ] Se han corregido los problemas bloqueantes encontrados durante la revisión.
- [ ] No existen cuestiones críticas pendientes.
- [ ] El equipo entiende suficientemente la solución implementada.
- [ ] El Product Owner puede comprobar que el resultado satisface el valor y los criterios de aceptación definidos.

---

## 11. Ejecución del proyecto

Antes de considerar terminada la historia:

- [ ] El proyecto puede iniciarse correctamente.
- [ ] La funcionalidad puede demostrarse desde la versión integrada.
- [ ] No requiere pasos manuales no documentados para poder funcionar.
- [ ] Las dependencias necesarias están correctamente declaradas.
- [ ] La funcionalidad puede ser evaluada por otro integrante del equipo.

---

## Criterio final

Una historia de usuario se considera **Done** cuando todas las condiciones aplicables de este documento han sido comprobadas y no existe ningún problema bloqueante conocido.

Si una historia:

- está programada pero no probada;
- cumple solo parte de sus criterios de aceptación;
- funciona únicamente en el entorno del desarrollador;
- no está integrada;
- introduce errores críticos;
- o requiere documentación pendiente;

**no se considerará Done** y deberá permanecer como trabajo pendiente.

La decisión se realizará de acuerdo con las responsabilidades del equipo:

- **Product Owner:** comprueba el valor aportado y los criterios de aceptación.
- **Tech Lead:** comprueba la coherencia técnica y la calidad de la implementación.
- **DevOps / QA:** comprueba pruebas, integración, entorno y requisitos no funcionales.
- **Scrum Master:** verifica que se ha seguido el proceso acordado y que no permanecen bloqueos sin gestionar.

El cumplimiento del Definition of Done será común para todas las historias del proyecto, salvo que alguna condición se indique explícitamente como no aplicable.
