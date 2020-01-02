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
        try:
          row = filtrar_por("nombre",data['nombre'])

          if not row:
            return {'message':"El usuario {} no existe".format(data['nombre'])}
          else:
            if verify_hash(data['clave'],row['clave']):
              access_token = create_access_token(identify = data['nombre'])
              refresh_token = create_refresh_token(identify = data['nombre'])
              return {
                'message': 'Te has logueado como {}'.format(row['nombre']),
                'access_token': access_token,
                'refresh_token': refresh_token
              }
            else:
              return {'message',"Datos incorrectos"}
        except Exception as e:
          print(e)
          return {'message': 'Algo falló'}, 500
        
class UserRegistration(Resource):
    def post(self):
        data = parser_reg.parse_args()
        if data['clave1'] != data['clave2']:
          return {'message':'Las claves no coinciden'}
        if not data['telefono']:
          data['telefono'] = "0"

        try:
          row_user = filtrar_por("nombre",data['nombre'])
          row_email = filtrar_por("correo",data['correo'])

          #current_user = row_user['nombre']
          #current_email = row_email['correo']

          if row_user or row_email:
            return {'message':"El usuario o el correo ha sido usado"}

          insert_usuario(data['nombre'],data['clave1'],data['correo'],data['apodo'],data['telefono'])

          access_token = create_access_token(identity = data['nombre'])
          refresh_token = create_refresh_token(identity = data['nombre'])
          return {
              'message': 'El usuario {} se creó'.format(data['nombre']),
              'access_token': access_token,
              'refresh_token': refresh_token
          }
        except Exception as e:
          print(e)
          return {'message': 'Algo falló'}, 500

class UserLogoutAccess(Resource):
    def post(self):
        return {'message': 'User logout'}
      
      
class UserLogoutRefresh(Resource):
    def post(self):
        return {'message': 'User logout'}
      
      
class TokenRefresh(Resource):
    def post(self):
        return {'message': 'Token refresh'}
      
      
class AllUsers(Resource):
    def get(self):
        return {'message': 'List of users'}

    def delete(self):
        return {'message': 'Delete all users'}
      
class SecretResource(Resource):
    @jwt_required      
    def get(self):
        return {
            'answer': 42
        }
