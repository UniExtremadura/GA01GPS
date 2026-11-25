# US-007 — Verificación de criterios de aceptación

## Alcance
Subtarea «Verificar criterios de aceptación» (US-007-AC-01 a US-007-AC-04). Revisión basada en `mainEntradasAdquiridas.py` y las pruebas del listado. Ejecutar las pruebas sobre la rama actual y registrar la salida real antes de cerrar la subtarea.

| Criterio | Prueba | Resultado esperado |
|---|---|---|
| AC-01: consulta de entradas propias | `test_ac01_consulta_con_identificador` | HTTP 200 y entradas del usuario 2 |
| AC-02: información por entrada | `test_ac02_informacion_de_cada_entrada` | Tipo, fecha y estado presentes |
| AC-03: solo entradas propias | `test_ac03_filtrado_por_identificador` | No aparecen entradas de otro ID *en el filtrado* |
| AC-04: mensaje sin entradas | `test_ac04_mensaje_si_no_hay_entradas` | Lista vacía y mensaje informativo |

## Ejecución

```bash
python -m pip install fastapi httpx pydantic
python -m unittest discover -s tests -p "test_criterios_aceptacion_us007.py" -v
```

## Evidencia de ejecución

- Fecha de ejecución: **por completar**.
- Equipo y rama: **por completar**.
- Resultado de la ejecución: **por completar; pegar salida real o adjuntar captura**.
- Resultado de la prueba visual de `view/mis-entradas.html`: **por completar**.

## Incidencia de seguridad pendiente

El endpoint identifica al usuario únicamente mediante `X-Usuario-ID`, un valor controlado por quien realiza la petición. El filtrado por ID funciona, pero **AC-03 no puede considerarse verificado como control de seguridad**: un usuario puede indicar el ID de otro y consultar sus entradas. La prueba `test_seguridad_pendiente_no_suplantar_identidad` se marca `expectedFailure` para documentar esta limitación, no para ocultarla. Se requiere integrar la autenticación real de US-002 y obtener el ID de la sesión validada, no de una cabecera arbitraria.

Además, la especificación del proyecto contiene **AC-05** (correspondencia con adquisiciones registradas), fuera del alcance explícito AC-01 a AC-04 de esta subtarea; queda pendiente verificarlo con US-006.

## Conclusión

Las pruebas funcionales de AC-01, AC-02 y AC-04 pueden verificarse con los datos ficticios existentes. AC-03 solo verifica el filtrado funcional; su seguridad requiere integración adicional. No declarar la historia totalmente aceptada hasta resolver esta incidencia y completar las evidencias de ejecución.
