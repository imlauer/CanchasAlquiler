from gen_ver_hash import *
from run import mysql


def filtrar_por(cosa,nombre):
    cursor = mysql.connection.cursor()

    sql = """SELECT * FROM Usuario WHERE %s="%s" """
    val = (cosa,nombre)

    sql_query = sql % val
    print(sql_query)

    cursor.execute(sql_query)
    row = cursor.fetchone()

    print(row)
    cursor.close()
    return row

def insert_usuario(nombre,clave,correo,apodo,telefono):
    cursor = mysql.connection.cursor()

    # Cambiar después
    clave_hash = generate_hash(clave)

    sql = """INSERT INTO Usuario (nombre,clave,correo,apodo,telefono,tipo_usuario,numero_reservas) VALUES (%s,%s,%s,%s,%s,1,0)"""
    
    cursor.execute(sql, (nombre,clave,correo,apodo,telefono))
    mysql.connection.commit()
