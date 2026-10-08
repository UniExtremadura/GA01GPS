# Definition of Ready (DoR) — Subsonic Festival 2026

**Equipo:** GPS01-2026 · **Versión:** 0.1 (borrador) ·

Responde a la pregunta: **¿tenemos información suficiente para aceptar esta historia como candidata a entrar en una iteración?**
No significa que sepamos todo, sino lo bastante para asumir el trabajo de forma razonable.

Una historia de usuario solo puede seleccionarse para un Sprint durante el Sprint Planning si cumple **todas** las condiciones aplicables. El Product Owner la propone y el equipo confirma que está lista (constitución, puerta de entrada a sprint).

## Identificación y trazabilidad
- [ ] Tiene un identificador único y estable (`US-XXX`) y está asociada a una épica (`EP-XXX`).
- [ ] Es trazable al menos a un objetivo de `goals.md` (G-XX).
- [ ] Encaja en el alcance incluido (S-XX) y no choca con ninguna exclusión (EX-XX).

## Valor y alcance
- [ ] El usuario está identificado: **cliente, proveedor o administrador**.
- [ ] La capacidad esperada está descrita con el formato *"Como [rol], quiero [capacidad], para [valor]"*.
- [ ] El valor o beneficio es comprensible para todo el equipo.
- [ ] Los límites del alcance están claros: qué entra y, especialmente, qué no entra.
- [ ] Los permisos por rol están definidos (qué puede y qué no puede hacer cada tipo de usuario en esta historia).

## Criterios de aceptación
- [ ] Hay criterios de aceptación definidos (`US-XXX-AC-NN`).
- [ ] Son observables y verificables por una revisión o prueba.
- [ ] Describen el comportamiento esperado, no una implementación concreta.
- [ ] Incluyen al menos un caso de error o caso límite relevante (por ejemplo, datos inválidos o acción no permitida para el rol).

## Planificación
- [ ] Tiene prioridad MoSCoW asignada y justificada (valor, riesgo, dependencias).
- [ ] Tiene una estimación en horas-persona, fruto del Planning Poker.
- [ ] Tiene el grado de incertidumbre identificado (baja, media, alta).
- [ ] Sus predecesores y dependencias (funcionales, técnicas y externas) son conocidos y están registrados.
- [ ] Es suficientemente pequeña para completarse dentro de **una iteración (1 semana)** con la capacidad efectiva del equipo. Si supera **[POR DEFINIR] h-p**, se divide antes de entrar.

## Restricciones
- [ ] Los requisitos no funcionales relevantes están identificados (seguridad, usabilidad, accesibilidad, rendimiento).
- [ ] Las restricciones técnicas, organizativas y de proyecto aplicables son conocidas.
- [ ] Los datos de prueba necesarios son **ficticios** y están identificados o se pueden generar.

## Cuestiones abiertas
- [ ] No quedan preguntas sin resolver que impidan entender o planificar la historia.
- [ ] Cualquier supuesto importante o cuestión no bloqueante está documentada explícitamente.

## Excepciones

Si excepcionalmente se propone aceptar una historia que no cumple alguna
condición del Definition of Ready, la decisión deberá ser acordada por el
equipo y registrada en la Wiki, indicando:

- La condición que no se cumple.
- La justificación de la excepción.
- El riesgo que supone.
- La persona responsable de resolverla.
- Cuándo deberá quedar resuelta.

## Historial de versiones

| Versión | Fecha | Cambios |
|---|---|---|
| 0.1 | 2026-10-01 | Borrador inicial. |
