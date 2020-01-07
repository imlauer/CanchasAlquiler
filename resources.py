from flask_restful import Resource, reqparse
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from models import *
from datetime import datetime,timedelta

'''
  Debería haber alguna forma de que te confirmen el turno para estar 100% seguros de que esta reservado el lugar! 
  Ya veremos si funciona!


  Deberían dejar visualizar los turnos libres por lugar.
  EJEMPLO: abro el complejo plimplim y que me muestre los horarios q tienen libre
'''

class UserLogin(Resource):
  def post(self):
    parser = reqparse.RequestParser()
    parser.add_argument('nombre', help = 'Este campo no puede estar vacio', required = True)
    parser.add_argument('clave', help = 'Este campo no puede estar vacio', required = True)

    data = parser.parse_args()
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
    parser = reqparse.RequestParser()
    parser.add_argument('nombre', help = 'Este campo no puede estar vacio', required = True)
    parser.add_argument('clave1', help = 'Este campo no puede estar vacio', required = True)
    parser.add_argument('clave2', help = 'Este campo no puede estar vacio', required = True)
    parser.add_argument('correo', help = 'Este campo no puede estar vacio', required = True)
    parser.add_argument('apodo', help = 'Este campo no puede estar vacio', required = True)
    parser.add_argument('telefono', help = 'Este campo no puede estar vacio', required = False)

    data = parser.parse_args()
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

class LugarDescripcion(Resource):
  # TODO: Buscar por nombre
  def get(self,lugar_id):
    current_place = LugarModel.query.get(lugar_id)
    if not current_place:
      return {'message':'{} no existente'.format(lugar_id)}

    def to_json(x):
      return { 
        'lugar_id': x.id,
        'nombre': x.nombre,
        'owner': x.owner,
        'anunciada':x.anunciada,
        'bar':x.bar,
        'preciodia':x.preciodia,
        'precionoche':x.precionoche,
        'incluye':x.incluye,
        'fotoperfil':x.fotoperfil,
        'fotoportada':x.fotoportada,
        'estacionamiento':x.estacionamiento,
        'parrilla':x.parrilla,
        'ciudad':x.ciudad,
        'provincia':x.provincia,
        'total_likes':x.total_likes
      }
    return {'lugar': to_json(LugarModel.query.get(lugar_id))}

class SecretResource(Resource):
    @jwt_required      
    def get(self):
        return {
            'answer': 42
        }

class AddSport(Resource):
  #@jwt_required
  def post(self):
    parser = reqparse.RequestParser()
    parser.add_argument('lugar_id', help='Este campo no puede estar vacio', required=True)
    parser.add_argument('tipo_deporte', help='Este campo no puede estar vacio', required=True)

    data = parser.parse_args()

    if not LugarModel.query.get(data['lugar_id']):
      return {'message':'No existe ese lugar'}

    row = DeporteModel.find_by_lugar(data['lugar_id'])

    invalido = 0
    for i in range(0,len(row)):
      if row[i].tipo_deporte == data['tipo_deporte']:
        invalido = 1

    if invalido:
      return {'message':'Ese deporte ya existe'}

    nuevo_deporte = DeporteModel (
      id_lugar = data['lugar_id'],
      tipo_deporte = data['tipo_deporte']
    )

    try:
      nuevo_deporte.save()
      return {'message': 'El deporte {} se ha agregado'.format(data['tipo_deporte'])}
    except Exception as e:
      print(e)
      return {'message': "Algo fue mal"}, 500

class AddRent(Resource):
  '''
    Agregar campo para agregar si están o no de vacaciones en la tabla de Horarios.
    la lógica del horario anulado, todavía no está implementada.
    En vez de buscar por horario, directamente mostrar los turnos disponibles y que
    se pueda elegir de ahí.
  '''
  #@jwt_required
  def post(self):
    parser = reqparse.RequestParser()
    parser.add_argument('id_lugar', type=int, help='Este campo no puede estar vacio', required=True)
    parser.add_argument('diadelasemana', type=int, help='Este campo no puede estar vacio', required=True)
    parser.add_argument('fechaalquiler', help='Este campo no puede estar vacio', required=True)
    # type=datetime significa que va a ejecutar datetime(horacomienzo) al argumento
    parser.add_argument('horacomienzo', type=int,help='Este campo no puede estar vacio', required=True)
    parser.add_argument('senado',type=int, help='Este campo no puede estar vacio', required=True)
    # Tiempo en horas.
    parser.add_argument('tiempo',type=int, help='Este campo no puede estar vacio', required=True)

    data = parser.parse_args()

    if not LugarModel.query.get(data['id_lugar']):
      return {'message':'No existe ese lugar'}

    if data['horacomienzo'] > 1440 or data['horacomienzo'] < 0:
      return {'message':'Hora invalida'}

    # Sólo acepto horas sin minutos.
    if data['horacomiezo'] % 60 != 0:
      return {'message':'Hora invalida'}

    def hora_from_int_to_string(hora_representacion_int):
      hora = 0
      if hora_representacion_int >= 60:
        hora_representacion_int -= 60
        hora += 1
      horacomienzo = timedelta(hours=hora, minutes=hora_representacion_int)
      return horacomienzo


    if data['diadelasemana'] <0 or data['diadelasemana']>6:
      return {'message':'Dia de la semana no válido'},500

    now = datetime.now()
    # Nombre cliente.
    #current_user = get_jwt_identity()
    current_user = "Acer_"
    current_user_id = UsuarioModel.find_by_nombre(current_user).id

    # Antes de agregar el alquiler, tengo que verificar si el local está abierto en ese
    # horario y además TENGO que verificar si ya está alquilado
    DataHorario = HorarioModel.query.gets(id_lugar)

    horario_invalido = 0
    if data['horacomienzo'] >= DataHorario.horadeapertura_dia and data['horacomienzo'] <= DataHorario.horadeapertura_dia:
      horario_invalido = 1
    elif data['horacomienzo'] >= DataHorario.hora_apertura_noche and data['horacomienzo'] <= DataHorario.horadeapertura_noche:
      horario_invalido = 1

    if horario_invalido:
      return {'message':'Horario invalido'},500

    # Verifico si ya está alquilado, probablemente estén mal los tipos después los corrijo.
    if AlquilaLugarModel.verificar_alquiler(id_lugar,data['fechaalquilar'],data['horacomienzo']):
      return {'message':'Horario no disponible'},500

    nuevo_alquiler = AlquilaLugarModel (
      id_lugar = data['id_lugar'],
      id_persona_alquila = current_user_id,
      diadelasemana = data['diadelasemana'],
      fecha_peticion_realizada = now.strftime("%Y-%m-%d %H:%M:%S"),
      fechaalquiler = data['fechaalquiler'],
      horacomienzo = data['horacomienzo'],
      senado = data['senado'],
      tiempo = data['tiempo'],
      # Desde el sistema de gestión del club te lo tienen que confirmar.
      confirmado = 0
    )

    try:
      nuevo_alquiler.save()
      # Cambiar todo a una lista, con sus correspondientes variables. 
      return {'message': 'El lugar {} se ha alquilado a las {} horas hasta las {} horas, espera la confirmacion porque capaz que sos un hijo de puta y nos queres hacer quedar mal, y por gente como vos tenemos que hacer un sistema de confirmacion.'.format(data['id_lugar'],hora_from_int_to_string(data['horacomienzo']),str(hora_from_int_to_string(data['horacomienzo'])+timedelta(hours=data['tiempo'])))}

    except Exception as e:
      print(e)
      return {'message': "Algo exploto"}, 500

class AddPlace(Resource):
  #jwt_required
  def post(self):
    parser = reqparse.RequestParser()
    parser.add_argument('lugar_nombre', help='Este campo no puede estar vacio', required=True)
    parser.add_argument('owner', help='Este campo no puede estar vacio', required=True)
    parser.add_argument('telefono', help='Este campo no puede estar vacio', required=True)
    parser.add_argument('correo_owner', help='Este campo no puede estar vacio', required=True)
    parser.add_argument('anunciada', help='Este campo no puede estar vacio', required=False)
    parser.add_argument('bar', help='Este campo no puede estar vacio', required=True)
    parser.add_argument('preciodia', help='Este campo no puede estar vacio', required=True)
    parser.add_argument('precionoche', help='Este campo no puede estar vacio', required=True)
    parser.add_argument('incluye', help='Este campo no puede estar vacio', required=True)
    parser.add_argument('fotoperfil', help='Este campo no puede estar vacio', required=True)
    parser.add_argument('fotoportada', help='Este campo no puede estar vacio', required=True)
    parser.add_argument('estacionamiento', help='Este campo no puede estar vacio', required=True)
    parser.add_argument('parrilla', help='Este campo no puede estar vacio', required=True)
    parser.add_argument('ciudad', help='Este campo no puede estar vacio', required=True)
    parser.add_argument('provincia', help='Este campo no puede estar vacio', required=True)

    data = parser.parse_args()   

    if LugarModel.find_by_nombre(data['lugar_nombre']):
      return {'message': 'Ese lugar ya existe'}
    
    nuevo_lugar = LugarModel (
      nombre = data['lugar_nombre'],
      owner = data['owner'],
      anunciada = data['anunciada'],
      bar = data['bar'],
      preciodia = data['preciodia'],
      precionoche = data['precionoche'],
      incluye = data['incluye'],
      fotoperfil = data['fotoperfil'],
      fotoportada = data['fotoportada'],
      estacionamiento = data['estacionamiento'],
      parrilla = data['parrilla'],
      telefono = data['telefono'],
      correo_owner = data['correo_owner'],
      ciudad = data['ciudad'],
      provincia = data['provincia'],
      total_likes = 0
    )
    # Agregar el horario

    try:
      nuevo_lugar.save_to_db()
      return {
        'message': 'El lugar {} se ha guardado'.format(data['lugar_nombre'])
      }
    except Exception as e:
      print(e)
      return {'message':'Algo falló al agregar el lugar'},500
