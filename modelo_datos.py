import sqlite3
import os

BASE_DATOS = os.path.join(os.path.dirname(__file__),'personas.db')

creacion = """
        create table persona(
            id integer primary key autoincrement,
            nombre text,
            apellidos text,
            dni text)
"""
def crear_bd():
    cnx = sqlite3.connect(BASE_DATOS)
    cnx.execute(creacion)
    cnx.close()

crear_bd()