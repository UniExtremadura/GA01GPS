# US-010 — Evidencias de validación de disponibilidad de espacios

Subtarea: Validación de disponibilidad de espacios.

## Código existente revisado

- `Espacios/reservas.py`: consulta disponibilidad, valida fechas y horarios, comprueba sesión y guarda reservas en SQLite.
- `Espacios/main.py`: publica los endpoints del servicio de espacios.
- `view/espacios.js`: muestra los mensajes de disponibilidad y errores de reserva.

## Pruebas automatizadas

Ejecutar desde la raíz de GA01GPS:

```bash
python -m unittest discover -s tests -p "test_reservas_us010.py" -v
```

Comprobaciones incluidas:

1. Disponibilidad de una franja libre.
2. Confirmación y guardado de reserva.
3. Rechazo de reserva duplicada.
4. Rechazo de horarios solapados.
5. Permiso de franjas contiguas.
6. Independencia entre espacios diferentes.
7. Rechazo de usuario sin sesión.
8. Rechazo de horas de inicio y fin inválidas.
9. Rechazo de fechas pasadas.
10. Rechazo de espacios inexistentes.
11. Persistencia de la reserva entre consultas.

## Resultado en el equipo del desarrollador

- Fecha: **[completar]**
- Resultado de ejecución: **[copiar salida real del terminal]**
- Resultado de comprobación visual del formulario: **[completar]**
- Incidencias encontradas: **[completar, o indicar ninguna]**

## Limitaciones

Las pruebas automatizadas sustituyen la dependencia de autenticación por un usuario simulado en las pruebas de éxito. El caso sin sesión usa la dependencia real. Para verificar la integración completa, iniciar el servicio de autenticación de US-002 y el servicio de espacios, iniciar sesión desde la web y comprobar la reserva con un token real. No afirmar que esta integración ha sido validada hasta ejecutarla.
