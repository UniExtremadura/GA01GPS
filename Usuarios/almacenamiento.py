"""Persistencia local de usuarios registrados con SQLite.

La base de datos se guarda en Usuarios/usuarios.sqlite3, o en la ruta indicada
por la variable de entorno SUBSONIC_USUARIOS_DB.
"""
import json
from contextlib import contextmanager
import os
import sqlite3
from pathlib import Path

RUTA_DB = Path(os.environ.get('SUBSONIC_USUARIOS_DB', Path(__file__).with_name('usuarios.sqlite3')))


@contextmanager
def _conexion():
    RUTA_DB.parent.mkdir(parents=True, exist_ok=True)
    conexion = sqlite3.connect(RUTA_DB, timeout=10)
    conexion.execute('PRAGMA busy_timeout = 10000')
    conexion.execute('''CREATE TABLE IF NOT EXISTS usuarios_registrados (
        id INTEGER PRIMARY KEY,
        email_normalizado TEXT NOT NULL UNIQUE,
        datos TEXT NOT NULL,
        salt TEXT NOT NULL,
        hash_password TEXT NOT NULL
    )''')
    try:
        with conexion:
            yield conexion
    finally:
        conexion.close()


def cargar_registros():
    """Devuelve pares (datos_del_usuario, salt_y_hash)."""
    with _conexion() as conexion:
        filas = conexion.execute(
            'SELECT datos, salt, hash_password FROM usuarios_registrados ORDER BY id'
        ).fetchall()
    return [(json.loads(datos), {'salt': salt, 'hash': hash_password})
            for datos, salt, hash_password in filas]


def guardar_registro(usuario, hash_password):
    """Guarda usuario y contraseña cifrada mediante hash en una única transacción."""
    with _conexion() as conexion:
        conexion.execute(
            '''INSERT INTO usuarios_registrados
               (id, email_normalizado, datos, salt, hash_password)
               VALUES (?, ?, ?, ?, ?)''',
            (usuario.id, usuario.email.strip().casefold(),
             usuario.model_dump_json(), hash_password['salt'], hash_password['hash'])
        )


def actualizar_usuario(usuario):
    with _conexion() as conexion:
        conexion.execute(
            '''UPDATE usuarios_registrados
               SET email_normalizado = ?, datos = ? WHERE id = ?''',
            (usuario.email.strip().casefold(), usuario.model_dump_json(), usuario.id)
        )


def borrar_usuario(id_usuario):
    with _conexion() as conexion:
        conexion.execute('DELETE FROM usuarios_registrados WHERE id = ?', (id_usuario,))
