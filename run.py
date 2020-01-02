from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flaskext.mysql import MySQL

app = Flask(__name__)
api = Api(app)

import views, models, resources
api.add_resource(resources.UserRegistration, '/registration')
api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.UserLogoutAccess, '/logout/access')
api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
api.add_resource(resources.TokenRefresh, '/token/refresh')
api.add_resource(resources.AllUsers, '/users')
api.add_resource(resources.SecretResource, '/secret')

mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root123'
app.config['MYSQL_DATABASE_DB'] = 'CanchasAlquiler'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'

mysql.init_app(app)
jwt = JWTManager(app)


