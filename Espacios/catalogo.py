"""Datos ficticios y consultas de espacios para US-009."""

import unicodedata


# Almacenamiento provisional en memoria, como en el servicio Usuarios.
espacios = [
    {"id": 1, "nombre": "Escenario Principal", "tipo": "escenario", "zona": "Norte", "capacidad": 5000, "descripcion": "Escenario al aire libre para los conciertos principales.", "habilitado": True, "disponible": True},
    {"id": 2, "nombre": "Escenario Electrónica", "tipo": "escenario", "zona": "Sur", "capacidad": 2000, "descripcion": "Espacio de música electrónica con pista de baile.", "habilitado": True, "disponible": True},
    {"id": 3, "nombre": "Camping Encinas", "tipo": "camping", "zona": "Este", "capacidad": 600, "descripcion": "Zona de acampada con acceso a servicios comunes.", "habilitado": True, "disponible": True},
    {"id": 4, "nombre": "Zona VIP Mirador", "tipo": "zona_vip", "zona": "Norte", "capacidad": 150, "descripcion": "Zona de descanso con vistas al escenario principal.", "habilitado": True, "disponible": True},
    {"id": 5, "nombre": "Sala Encuentros", "tipo": "sala", "zona": "Oeste", "capacidad": 80, "descripcion": "Sala cubierta para encuentros y actividades.", "habilitado": True, "disponible": True},
    {"id": 6, "nombre": "Camping Río", "tipo": "camping", "zona": "Sur", "capacidad": 300, "descripcion": "Zona de acampada temporalmente no disponible.", "habilitado": True, "disponible": False},
    {"id": 7, "nombre": "Sala Auxiliar", "tipo": "sala", "zona": "Oeste", "capacidad": 40, "descripcion": "Sala deshabilitada por mantenimiento.", "habilitado": False, "disponible": True},
]


def normalizar(texto):
    return "".join(
        caracter for caracter in unicodedata.normalize("NFD", texto.strip().casefold())
        if unicodedata.category(caracter) != "Mn"
    )


def consultar_espacios(nombre="", tipo=None, zona=None, capacidad_minima=0):
    resultados = []
    for espacio in espacios:
        if not espacio["habilitado"] or not espacio["disponible"]:
            continue
        if normalizar(nombre) not in normalizar(espacio["nombre"]):
            continue
        if tipo and normalizar(tipo) != normalizar(espacio["tipo"]):
            continue
        if zona and normalizar(zona) != normalizar(espacio["zona"]):
            continue
        if espacio["capacidad"] < capacidad_minima:
            continue
        resultados.append(espacio.copy())
    return resultados


def consultar_espacio(id_espacio):
    return next((espacio for espacio in consultar_espacios() if espacio["id"] == id_espacio), None)
