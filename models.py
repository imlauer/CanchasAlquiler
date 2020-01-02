from db import mysql

def filtrar_por_nombre(nombre): 
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        sql = "SELECT * FROM Usuario WHERE nombre=%s"
        sql_where = (sql,nombre)
        row = cursor.fetchone()

        current_user = row['nombre']

        return current_user 
        
    except Error as error:
        print(error)
 
    finally:
        cursor.close()
        conn.close()

def insert_usuario(data,...):
  try:
    conn = mysql.connect()
    cursor = conn.cursor()

    # Cambiar después
    clave = str.encode(clave1)
    hash_object = hashlib.sha512(clave)
    hex_dig = hash_object.hexdigest()

    sql = "INSERTO INTO Usuario (nombre,clave,correo,apodo,tipo_usuario,numero_reservas) VALUES ('%s','%s','%s','%s',0,1)"
    sql_where = (_nombre,hex_dig,_correo,_apodo,)
    
    # Como verifico que se ejecutó bien la consulta? 
    cursor.execute(sql, sql_where)

    cursor.commit()
