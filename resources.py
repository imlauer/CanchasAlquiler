from flask_restful import Resource, reqparse
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from gen_ver_hash import *
from models import *

#Login
parser_log = reqparse.RequestParser()
parser_log.add_argument('nombre', help = 'Este campo no puede estar vacio', required = True)
parser_log.add_argument('clave', help = 'Este campo no puede estar vacio', required = True)
#Register
parser_reg = reqparse.RequestParser()
parser_reg.add_argument('nombre', help = 'Este campo no puede estar vacio', required = True)
parser_reg.add_argument('clave1', help = 'Este campo no puede estar vacio', required = True)
parser_reg.add_argument('clave2', help = 'Este campo no puede estar vacio', required = True)
parser_reg.add_argument('correo', help = 'Este campo no puede estar vacio', required = True)
parser_reg.add_argument('apodo', help = 'Este campo no puede estar vacio', required = True)
parser_reg.add_argument('telefono', help = 'Este campo no puede estar vacio', required = False)

class UserLogin(Resource):
  def post(self):
    data = parser_log.parse_args()
    current_user = UsuarioModel.find_by_nombre(data['nombre'])

    if not current_user:
      return {'message':"El usuario {} no existe".format(data['nombre'])}

    if UsuarioModel.verify_hash(data['password'], current_user.clave):
      access_token = create_access_token(identify = data['nombre'])
      refresh_token = create_refresh_token(identify = data['nombre'])
      return {
        'message': 'Te has logueado como {}'.format(row['nombre']),
        'access_token': access_token,
        'refresh_token': refresh_token
      }
    else:
      return {'message',"Datos incorrectos"}

class UserRegistration(Resource):
  def post(self):

    data = parser_reg.parse_args()
    if data['clave1'] != data['clave2']:
      return {'message':'Las claves no coinciden'}
    if UsuarioModel.find_by_nombre(data['nombre']) or UsuarioModel.find_by_correo(data['correo']):
      return {'message': 'El usuario o el correo han sido usados.'}

    nuevo_usuario = UsuarioModel (
      nombre = data['nombre'],
      clave = UsuarioModel.generate_hash(data['clave1']),
      correo = data['correo'],
      apodo = data['apodo'],
      tipo_usuario = 1,
      numero_reservas = 0
    )
    try:
      nuevo_usuario.save_to_db()
      access_token = create_access_token(identity = data['nombre'])
      refresh_token = create_refresh_token(identity = data['nombre'])
      return {
          'message': 'El usuario {} se ha creado'.format(data['nombre']),
          'access_token': access_token,
          'refresh_token': refresh_token
      }
    except Exception as e:
      print(e)
      return {'message': 'Algo falló'}, 500

class UserLogoutAccess(Resource):
  @jwt_required
  def post(self):
    jti = get_raw_jwt()['jti']
    try:
      revoked_token = RevokedTokenModel(jti = jti)
      revoked_token.add()
      return {'message': 'Access token has been revoked'}
    except:
      return {'message': 'Something went wrong'}, 500

class UserLogoutRefresh(Resource):
  @jwt_refresh_token_required
  def post(self):
    jti = get_raw_jwt()['jti']
    try:
      revoked_token = RevokedTokenModel(jti = jti)
      revoked_token.add()
      return {'message': 'Refresh token has been revoked'}
    except:
      return {'message': 'Something went wrong'}, 500


class TokenRefresh(Resource):
  @jwt_refresh_token_required
  def post(self):
    current_user = get_jwt_identity()
    access_token = create_access_token(identity = current_user)
    return {'access_token': access_token}


class AllUsers(Resource):
  def get(self):
    def to_json(x):
      return {
        'nombre': x.nombre,
        'correo': x.correo
      }   
    return {'nombre': list(map(lambda x: to_json(x), UsuarioModel.query.all()))}
  
      
class SecretResource(Resource):
    @jwt_required      
    def get(self):
        return {
            'answer': 42
        }
