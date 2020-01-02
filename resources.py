from flask_restful import Resource, reqparse
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from models import *
from db import mysql


parser = reqparse.RequestParser()
parser.add_argument('nombre', help = 'This field cannot be blank', required = True)
parser.add_argument('clave', help = 'This field cannot be blank', required = True)

def generate_hash(password):
  return sha256.hash(password) 
def verify_hash(password, hash):
  return sha256.verify(password, hash)

class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        try:
          # filtrar_por_nombre(data['nombre'])
          conn = mysql.connect()
          cursor = conn.cursor()

          sql = "SELECT * FROM Usuario WHERE nombre=%s"
          sql_where = (sql,data['nombre'])
          row = cursor.fetchone()

          current_user = row['nombre']

          if not current_user:
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

        finally:
          if cursor and conn:
            cursor.close()
            conn.close()
        
# Filtrar por nombre
# Insert usuario 

class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()
        try:
          current_user = filtrar_por("nombre",data['nombre'])
          current_email = filtrar_por("correo",data['correo'])
          
          if current_user or current_email:
            return {'message':"El usuario o el correo están en uso"}

          insert_usuario(data['nombre'],data['clave'],data['correo'],data['apodo'])
          return {
              'message': 'El usuario {} se creó'.format(data['username'])
          }
        except:
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
    def get(self):
        return {
            'answer': 42
        }
