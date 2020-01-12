from passlib.hash import pbkdf2_sha256 as sha256
from run import db
from flask_sqlalchemy import *

class DenunciarModel(db.Model):
  __tablename__ = 'Denuncias'
  __table_args__ = {
      'autoload': True,
      'schema': 'CanchasAlquiler',
      'autoload_with': db.engine
  }
  @classmethod
  def find_by_lugar_persona(cls, id_lugar, id_persona):
    return cls.query.filter_by(id_lugar=id_lugar, id_persona=id_persona).first()

  def save(self):
    db.session.add(self)
    db.session.commit() 

class CanchaModel(db.Model):
  __tablename__ = 'Cancha'
  __table_args__ = {
      'autoload': True,
      'schema': 'CanchasAlquiler',
      'autoload_with': db.engine
  }
  def save(self):
    db.session.add(self)
    db.session.commit() 

class LeGustaModel(db.Model):
  __tablename__ = 'LeGusta'
  __table_args__ = {
      'autoload': True,
      'schema': 'CanchasAlquiler',
      'autoload_with': db.engine
  }

  @classmethod
  def find_by_lugar_nombre(cls,id_lugar,id_persona):
    return cls.query.filter_by(id_lugar=id_lugar, id_persona=id_persona).first()

  def save(self):
    db.session.add(self)
    db.session.commit() 

class DireccionModel(db.Model):
  __tablename__ = 'HorarioNormal'
  __table_args__ = {
      'autoload': True,
      'schema': 'CanchasAlquiler',
      'autoload_with': db.engine
  }
  
  @classmethod
  def find_by_ID(cls,lugar_id):
    return cls.query.filter_by(id_lugar=lugar_id).first()

  def save_to_db(self):
    db.session.add(self)
    db.session.commit()


class HorarioModel(db.Model):
  __tablename__ = 'HorarioNormal'
  __table_args__ = {
      'autoload': True,
      'schema': 'CanchasAlquiler',
      'autoload_with': db.engine
  }
  def save_to_db(self):
    db.session.add(self)
    db.session.commit()
  @classmethod
  def find_by_lugar(cls,lugar_id):
    return cls.query.filter_by(id_lugar=lugar_id).first()

class LugarModel(db.Model):
  __tablename__ = 'Lugar'
  __table_args__ = { 
      'autoload': True,
      'schema': 'CanchasAlquiler',
      'autoload_with': db.engine
  }

  @classmethod
  def find_by_nombre(cls, nombre):
    return cls.query.filter_by(nombre = nombre).first()

  def save_to_db(self):
    db.session.add(self)
    db.session.commit() 


class UsuarioModel(db.Model):
  __tablename__ = 'Usuario'
  __table_args__ = { 
      'autoload': True,
      'schema': 'CanchasAlquiler',
      'autoload_with': db.engine
  }

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

class AlquilaLugarModel(db.Model):
  __tablename__ = 'AlquilaLugar'
  __table_args__ = {
      'autoload': True,
      'schema': 'CanchasAlquiler',
      'autoload_with': db.engine
  }

  @classmethod
  def find_by_id_usuario(cls, id_persona_alquila):
    return cls.query.filter_by(id_persona_alquila = id_persona_alquila).all()

  @classmethod
  def find_by_lugar(cls, id_lugar):
    return cls.query.filter_by(id_lugar = id_lugar).all()
  @classmethod
  def verificar_alquiler(cls, id_lugar, fecha, hora):
    return cls.query.filter_by(id_lugar=id_lugar, fechaalquiler=fecha, horacomienzo=hora).first()

  def save(self):
    db.session.add(self)
    db.session.commit()


class DeporteModel(db.Model):
  __table_args__ = {'extend_existing': True}
  __tablename__ = 'Deportes'

  id = db.Column(db.Integer, primary_key=True) 
  tipo_deporte = db.Column(db.String(50), nullable=False)
  id_lugar = db.Column(db.Integer, db.ForeignKey('Lugar.id'), nullable=True)

  @classmethod
  def find_by_lugar(cls, id_lugar):
    return cls.query.filter_by(id_lugar = id_lugar).all()

  def save(self):
    db.session.add(self)
    db.session.commit()

class RevokedTokenModel(db.Model):
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
