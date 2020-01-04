from passlib.hash import pbkdf2_sha256 as sha256
from run import db
from flask_sqlalchemy import *

class LugarModel(db.Model):
  __table_args__ = {'extend_existing': True}
  __tablename__ = 'Lugar'
  #__table__ = db.Table('Lugar', db.metadata)

  id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
  owner = db.Column(db.String(length=60), nullable=False, unique=False)
  nombre =  db.Column(db.String(length=100), nullable=False, unique=False)
  anunciada = db.Column(db.String(length=100), nullable=True, unique=False)
  bar =  db.Column(db.String(length=50), nullable=True, unique=False)
  preciodia = db.Column(db.Integer, nullable=False, unique=False)
  precionoche = db.Column(db.Integer, nullable=False, unique=False)
  incluye = db.Column(db.String(length=250), nullable=False, unique=False)
  fotoperfil = db.Column(db.String, nullable=False, unique=False)
  fotoportada = db.Column(db.String, nullable=False, unique=False)
  estacionamiento = db.Column(db.Integer, nullable=True, unique=False)
  parrilla = db.Column(db.Integer, nullable=True, unique=False)
  ciudad = db.Column(db.String(length=100), nullable=False, unique=False)
  provincia = db.Column(db.String(length=100), nullable=False, unique=False)
  total_likes = db.Column(db.Integer, nullable=True, unique=False)

  @classmethod
  def find_by_id(cls,lugar_id):
    try:
      lugar = cls.query.get(lugar_id)
      return {'lugar_nombre' : lugar.nombre}
    except Exception as e:
      print(e)
      return {'message':'Algo falló'}

  def save_to_db(self):
    db.session.add(self)
    db.session.commit() # this needed to write the changes to database


class UsuarioModel(db.Model):
  __table_args__ = {'extend_existing': True}
  __tablename__ = 'Usuario'

  id =     db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
  nombre = db.Column(db.String(length=60), nullable=False, unique=False)
  clave =  db.Column(db.String(length=100), nullable=False, unique=False)
  correo = db.Column(db.String(length=100), nullable=False, unique=False)
  apodo =  db.Column(db.String(length=50), nullable=False, unique=False)
  tipo_usuario = db.Column(db.Integer, nullable=False, unique=False)
  telefono = db.Column(db.String(length=100), nullable=False, unique=False)
  numero_reservas = db.Column(db.Integer, nullable=True, unique=False)

  @classmethod
  def find_by_nombre(cls, nombre):
      return cls.query.filter_by(nombre = nombre).first()

  @classmethod
  def find_by_correo(cls, correo):
      return cls.query.filter_by(correo = correo).first()

  @staticmethod
  def generate_hash(password):
    return sha256.hash(password)
  
  @staticmethod
  def verify_hash(password, hash):
    return sha256.verify(password, hash)

  @classmethod
  def return_all(cls):
    def to_json(x):
      return {
          'nombre': x.nombre,
          'correo': x.correo
      }
      return {'nombre': list(map(lambda x: to_json(x), UsuarioModel.query.all()))}

  def save_to_db(self):
    db.session.add(self)
    db.session.commit() # this needed to write the changes to database

  def __repr__(self):
    return "<Usuario(nombre='{0}', correo='{1}', clave='{2}')>".format(
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
