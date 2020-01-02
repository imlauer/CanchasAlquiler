from gen_ver_hash import *
from run import mysql


def filtrar_por(cosa,nombre):
    conn = mysql.connect
    cursor = conn.cursor()

    sql = "SELECT * FROM Usuario WHERE %s=%s"
    val = (cosa,nombre)

    cursor.execute(sql,val)    
    row = cursor.fetchone()

    return row

def insert_usuario(nombre,clave,correo,apodo):
    conn = mysql.connect()
    cursor = conn.cursor()

    # Cambiar después
    clave_hash = generate_hash(clave)

    sql = "INSERTO INTO Usuario (nombre,clave,correo,apodo,tipo_usuario,numero_reservas) VALUES ('%s','%s','%s','%s',1,0)"
    sql_where = (nombre,clave_hash,correo,apodo,)
    
    cursor.execute(sql, sql_where) 
    cursor.close()
    conn.close()
