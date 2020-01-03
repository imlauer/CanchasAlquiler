from passlib.hash import pbkdf2_sha256 as sha256
from run import mysql


class UsuarioModel(db.Model):
  __table_args__ = {'extend_existing': True}
  __tablename__ = 'Usuario'

  id =     Column(Integer, primary_key=True, nullable=False, autoincrement=True)
  nombre = Column(String(length=60), nullable=False, unique=False)
  clave =  Column(String(length=100), nullable=False, unique=False)
  correo = Column(String(length=100), nullable=False, unique=False)
  apodo =  Column(String(length=50), nullable=False, unique=False)
  tipo_usuario = Column(Integer, nullable=False, unique=False)
  telefono = Column(String(length=100), nullable=False, unique=False)
  numero_reservas = Column(Integer, nullable=True, unique=False)

  @classmethod
  def find_by_nombre(cls, nombre):
      return cls.query.filter_by(nombre = nombre).first()


  @staticmethod
  def generate_hash(password):
    return sha256.hash(password)
  
  @staticmethod
  def verify_hash(password, hash):
    return sha256.verify(password, hash)

  def save_to_db(self):
    db.session.add(self)
    db.session.commit() # this needed to write the changes to database

  def __repr__(self):
    return "<User(name='{0}', fullname='{1}', nickname='{2}')>".format(
                        self.nombre, self.correo, self.clave)


class RevokedTokenModel(db.Model):
    # Creala si tira error
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key = True)
    jti = db.Column(db.String(120))
    
    def add(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti = jti).first()
        return bool(query)


def todos_los_usuarios():
  cursor = mysql.connection.cursor()

  sql = "SELECT * FROM Usuario"
  
  cursor.execute(sql)
  record = cursor.fetchall()

  cursor.close()
  return record

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
    
    cursor.execute(sql, (nombre,clave_hash,correo,apodo,telefono))
    mysql.connection.commit()

def insert_revoked_token(jti):
  cursor = mysql.connection.cursor()

  sql = """INSERT INTO revoked_tokens (jdi) VALUES (%s)"""
  cursor.execute(sql,(jdi))

  mysql.connection.commit()

def filtrar_por_general(tabla,cosa,nombre):
  cursor = mysql.connection.cursor()

  sql = """SELECT * FROM %s WHERE %s="%s" """
  val = (tabla,cosa,nombre)

  sql_query = sql % val
  print(sql_query)

  cursor.execute(sql_query)
  row = cursor.fetchone()

  print(row)
  cursor.close()
  return row
