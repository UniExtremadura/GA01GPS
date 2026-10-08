# Subsonic — Definition of Done

**Equipo:** GPS01-2026 · **Versión:** 1.1.0 (propuesta de revisión) · 

## Propósito

El **Definition of Done (DoD)** establece las condiciones mínimas que debe cumplir una historia de usuario para poder considerarse terminada.

Una funcionalidad no se considera terminada únicamente porque haya sido programada o funcione en condiciones ideales. Para alcanzar el estado **Done**, la historia deberá estar implementada, verificada, integrada, documentada y aceptada de acuerdo con las normas del proyecto.

**Definición de "problema crítico".** A efectos de este documento, es todo defecto que impide cumplir un criterio de aceptación obligatorio, rompe una funcionalidad ya operativa, expone datos o credenciales, o impide ejecutar la demo.

Todas las condiciones se aplican a cada historia, salvo que se marquen *(si aplica)*. Cuando una condición *(si aplica)* no se cumple por no ser aplicable, se anota en la PR cuál y por qué.

---

## Implementación

- [ ] La funcionalidad descrita en la historia `US-XXX` está completamente implementada.
- [ ] La implementación respeta la arquitectura y las convenciones técnicas acordadas por el equipo.
- [ ] No quedan fragmentos de código temporal, depuración ni código comentado necesario para que funcione.
- [ ] No quedan problemas críticos conocidos.

## Criterios de aceptación

- [ ] Se han comprobado **todos** los criterios de aceptación de la historia (`US-XXX-AC-NN`) y todos se cumplen.
- [ ] Se han comprobado los casos de error y casos límite definidos en la historia.
- [ ] Hay evidencia de la comprobación enlazada en la PR (resultado de pruebas, captura o registro).

Una historia no puede considerarse terminada si algún criterio de aceptación obligatorio no se cumple.

## Pruebas

- [ ] Existen pruebas (automáticas o manuales documentadas) que cubren cada criterio de aceptación.
- [ ] Las pruebas cubren el comportamiento principal y, al menos, un error o caso límite relevante.
- [ ] Todas las pruebas existentes siguen pasando y no se han introducido regresiones críticas.
- [ ] Las pruebas repetitivas se automatizan siempre que sea razonable.

## Integración y ejecución

- [ ] El cambio se ha integrado mediante una Pull Request desde la rama `feature/US-XXX`, sin conflictos pendientes.
- [ ] El pipeline de integración está en verde.
- [ ] El proyecto se inicia correctamente desde la versión integrada, y la funcionalidad se puede demostrar desde ella.
- [ ] No hay pasos manuales sin documentar y las dependencias nuevas están declaradas.
- [ ] El cambio no rompe funcionalidades principales que ya estaban operativas.

No se considera terminada una historia que funcione solo en el entorno o rama individual de un integrante.

## Requisitos no funcionales

Cuando la historia los afecte (si aplica), se han comprobado y se deja constancia de cuáles se consideraron:

**Seguridad y datos**
- [ ] Las entradas del usuario se validan.
- [ ] Se comprueban los permisos del rol (cliente, proveedor, administrador): un usuario sin autorización no puede realizar operaciones restringidas.
- [ ] No hay contraseñas, claves, tokens ni archivos `.env` reales en el código ni en el repositorio.
- [ ] Los datos de desarrollo y pruebas son ficticios. No hay datos personales, bancarios ni sensibles reales.

**Usabilidad y accesibilidad**
- [ ] Las acciones principales informan claramente de su resultado.
- [ ] Los mensajes de error explican qué ha ocurrido y los errores recuperables permiten continuar.
- [ ] La interfaz es coherente con el resto de Subsonic y respeta los requisitos de accesibilidad aplicables.

**Rendimiento y restricciones**
- [ ] Se han considerado los requisitos de rendimiento cuando son relevantes.
- [ ] La implementación respeta las restricciones de `goals.md` y los principios de `constitution.md`.

## Documentación

- [ ] La documentación técnica relevante está actualizada.
- [ ] La documentación de usuario está actualizada *(si aplica)*.
- [ ] El `README.md` está actualizado si cambian la instalación, la configuración o la ejecución.
- [ ] Las decisiones o desviaciones relevantes están registradas en la Wiki.

La documentación debe permitir que otro integrante comprenda el cambio sin depender de quien lo implementó.

## Trazabilidad

- [ ] Los commits y la rama referencian el ID de la historia (`US-XXX`).
- [ ] La historia sigue asociada a su épica (`EP-XXX`) y al menos a un objetivo de `goals.md`.
- [ ] Las tareas (`TK-XXX`) y las pruebas o evidencias se pueden relacionar con la historia.

Cadena de trazabilidad: **Misión → Objetivos → Épicas → Historias → Tareas → Código y pruebas → Evidencias**

## Revisión y aceptación

- [ ] La PR ha sido aprobada por **al menos una persona distinta del autor**.
- [ ] Se han resuelto los problemas bloqueantes detectados en la revisión.
- [ ] El Product Owner ha aceptado la historia, normalmente en la Sprint Review, tras comprobar el valor aportado y los criterios de aceptación.

---

## Criterio final y decisión

Una historia es **Done** cuando todas las condiciones aplicables han sido comprobadas y no existe ningún problema crítico conocido.

**No es Done** una historia que: esté programada pero no probada, cumpla solo parte de sus criterios de aceptación, funcione solo en el entorno del desarrollador, no esté integrada, introduzca problemas críticos o tenga documentación pendiente. Permanece como trabajo pendiente.

**Quién comprueba y quién cierra**

| Quién | Qué hace |
|---|---|
| **Autor** | Hace una autocomprobación de este documento antes de abrir la PR. |
| **Revisor de la PR** (cualquier otro integrante) | Verifica la implementación, las pruebas y la integración. |
| **Tech Lead** | Resuelve las dudas sobre coherencia técnica y arquitectura. |
| **DevOps / QA** | Resuelve las dudas sobre pruebas, pipeline, entorno y requisitos no funcionales. |
| **Scrum Master** | Comprueba que se siguió el proceso y que no hay bloqueos sin gestionar. |
| **Product Owner** | Acepta la historia y es quien la cierra como Done. |

Si el PO rechaza una historia, vuelve al backlog con el motivo registrado en la Wiki.

## Historial de versiones

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0.0 | 2026-10-01 | Versión inicial del equipo. |
| 1.1.0 | 2026-10-01 | Propuesta de revisión: alineada con el team charter (acuerdos 14 y 17) y la constitución, condiciones verificables, secciones fusionadas (11 → 8) y responsabilidades de cierre. |
