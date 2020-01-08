'''
This is actually a simple, yet frustrating issue. The problem is you are importing main BEFORE you are creating the instance of db in your __init__.py
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

app.config['JWT_SECRET_KEY'] = 'KZPsLNpcsWWS&MY&is7gV6h!7s2E6UuQ@!d%2'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

jwt = JWTManager(app)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return models.RevokedTokenModel.is_jti_blacklisted(jti)


##### Autenticación
api.add_resource(resources.UserRegistration, '/registration')
api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.UserLogoutAccess, '/logout/access')
api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
api.add_resource(resources.TokenRefresh, '/token/refresh')

###### General
api.add_resource(resources.Reservas,'/misreservas')
api.add_resource(resources.Reservas,'/info')
api.add_resource(resources.LugarDescripcion, '/lugar/<int:lugar_id>')
api.add_resource(resources.AllUsers, '/lista_usuarios')
api.add_resource(resources.SecretResource, '/secret')

####### Acciones de usuario (faltan implementar)
#api.add_resource(resources.SecretResource, '/<string:usuario>/me_gusta')
#api.add_resource(resources.SecretResource, '/<string:usuario>/denuncias')
#api.add_resource(resources.SecretResource, '/<int:lugar>/denunciar')
#api.add_resource(resources.SecretResource, '/<int:lugar>/corazon')
api.add_resource(resources.AddRent, '/agregar_alquiler')
# Lo voy a cambiar por este:
#api.add_resource(resources.AddRent, '/<int:lugar_id>/alquilar')

###### Acciones administrador
api.add_resource(resources.AddSport, '/agregar_deporte')
# Lo voy a cambiar por este:
#api.add_resource(resources.AddSport, '/<int:lugar>/agregar_deporte')

#api.add_resource(resources.AgregarCancha, '/<int:lugar>/agregar_cancha')
api.add_resource(resources.AddHorario,'/agregar_horario')
# Lo voy a cambiar por:
#api.add_resource(resources.AddHorario,'/<int:lugar>/agregar_horario')
