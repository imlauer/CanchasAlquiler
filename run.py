'''
This is actually a simple, yet frustrating issue. The problem 
is you are importing main BEFORE you are creating the instance of db in your __init__.py
'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root123@localhost/CanchasAlquiler'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  

db = SQLAlchemy(app)

from flask_restful import Api
from flask_jwt_extended import JWTManager
api = Api(app)

import views, models, resources

app.config['JWT_SECRET_KEY'] = 'cambiarlo'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

jwt = JWTManager(app)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return models.RevokedTokenModel.is_jti_blacklisted(jti)


''' Autenticación '''
api.add_resource(resources.UserRegistration, '/registration')
api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.UserLogoutAccess, '/logout/access')
api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
api.add_resource(resources.TokenRefresh, '/token/refresh')

''' General '''
api.add_resource(resources.Reservas,'/info/misreservas')
api.add_resource(resources.LugarDescripcion,'/info/lugar/<int:lugar_id>')
api.add_resource(resources.InfoUsuario,'/info/usuario/<string:nombre>')

''' Acciones de usuario (faltan implementar) '''
api.add_resource(resources.Denunciar, '/denunciar/<int:lugar_id>')
api.add_resource(resources.MeGusta, '/corazon/<int:lugar_id>')
api.add_resource(resources.AddRent, '/alquilar')

''' Acciones administrador '''
api.add_resource(resources.AddSport, '/agregar/deporte')
api.add_resource(resources.AddCancha, '/agregar/cancha')
api.add_resource(resources.AddHorario, '/agregar/horario')
api.add_resource(resources.AddAddress, '/agregar/direccion')
