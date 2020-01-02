from db import mysql

def filtrar_por(cosa,nombre): 
    conn = mysql.connect()
    cursor = conn.cursor()

    sql = "SELECT * FROM Usuario WHERE %s=%s"
    sql_where = (sql,cosa,nombre)
    row = cursor.fetchone()

    current_user = row['nombre']

    cursor.close()
    conn.close()
    return current_user

def insert_usuario(nombre,clave,correo,apodo):
    conn = mysql.connect()
    cursor = conn.cursor()

    # Cambiar después
    clave = str.encode(clave1)
    hash_object = hashlib.sha512(clave)
    hex_dig = hash_object.hexdigest()

    sql = "INSERTO INTO Usuario (nombre,clave,correo,apodo,tipo_usuario,numero_reservas) VALUES ('%s','%s','%s','%s',1,0)"
    sql_where = (nombre,clave_hash,correo,apodo,)
    
    cursor.execute(sql, sql_where) 
    cursor.close()
    conn.close()
