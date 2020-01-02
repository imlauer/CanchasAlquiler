'''
This is actually a simple, yet frustrating issue. The problem is you are importing main BEFORE you are creating the instance of db in your __init__.py


'''

from flask import Flask
#from flask_restful import Api
#from flask_jwt_extended import JWTManager
from flask_mysqldb import MySQL

app = Flask(__name__)
# MySQL configurations
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root123'
app.config['MYSQL_DB'] = 'CanchasAlquiler'

mysql = MySQL(app)

from flask_restful import Api
from flask_jwt_extended import JWTManager

api = Api(app)

import views, models, resources

app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'

jwt = JWTManager(app)

api.add_resource(resources.UserRegistration, '/registration')
api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.UserLogoutAccess, '/logout/access')
api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
api.add_resource(resources.TokenRefresh, '/token/refresh')
api.add_resource(resources.AllUsers, '/users')
api.add_resource(resources.SecretResource, '/secret')

