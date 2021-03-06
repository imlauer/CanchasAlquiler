from flask_restful import Resource, reqparse
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from models import *
from datetime import datetime,timedelta

'''
  Debería haber alguna forma de que te 
  confirmen el turno para estar 100% seguros de que esta reservado el lugar! 
  Ya veremos si funciona!

  Deberían dejar visualizar los turnos libres por lugar.
  EJEMPLO: abro el complejo plimplim y que me muestre los horarios q tienen libre
'''

class UserLogin(Resource):
  def post(self):
    parser = reqparse.RequestParser()
    parser.add_argument('nombre',
          help = 'Este campo no puede estar vacio',
          required = True)
    parser.add_argument('clave',
          help = 'Este campo no puede estar vacio',
          required = True)

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
    parser.add_argument('nombre',
        help = 'Este campo no puede estar vacio',
        required = True)
    parser.add_argument('clave1',
        help = 'Este campo no puede estar vacio',
        required = True)
    parser.add_argument('clave2',
        help = 'Este campo no puede estar vacio',
        required = True)
    parser.add_argument('correo',
        help = 'Este campo no puede estar vacio',
        required = True)
    parser.add_argument('apodo',
        help = 'Este campo no puede estar vacio',
        required = True)
    parser.add_argument('telefono',
        help = 'Este campo no puede estar vacio',
        required = False)

    data = parser.parse_args()
    if data['clave1'] != data['clave2']:
      return {'message':'Las claves no coinciden'}

    if(
      UsuarioModel.find_by_nombre(data['nombre']) or
      UsuarioModel.find_by_correo(data['correo']) 
      ):
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



class Denunciar(Resource):
  #@jwt_required
  def get(self,lugar_id):
    Lugar = LugarModel.query.get(lugar_id)
    if not Lugar:
      return {'message':'No existe ese lugar'}

    # Solo para hacer las pruebas más rápidas.
    current_user = "Acer_"
    current_user_id = UsuarioModel.find_by_nombre(nombre = current_user).id

    # Buscar una forma para confirmar si está o no denunciado el lugar.
    if DenunciarModel.find_by_lugar_persona(lugar_id,current_user_id):
      return {'message':'Ya está denunciado'}


    Lugar.denuncias += 1
    denuncia = DenunciarModel (
      id_lugar = lugar_id,
      id_persona = current_user_id
    )

    try:
      Lugar.commit()
      denuncia.save()
      return {'message': 'Reportaste el lugar {} con éxito'.format(lugar_id)}
    except Exception as e:
      print(e)
      return {'message': "Algo fue mal"}, 500


class MeGusta(Resource):
  #@jwt_required
  def get(self,lugar_id):
    Lugar = LugarModel.query.get(lugar_id)
    if not Lugar:
      return {'message':'No existe ese lugar'}

    # Solo para hacer las pruebas más rápidas.
    current_user = "Acer_"
    current_user_id = UsuarioModel.find_by_nombre(nombre = current_user).id

    if LeGustaModel.find_by_lugar_nombre(lugar_id,current_user_id):
      return {'message':'Ya te gusta este lugar'}

    '''
      So fucking easy with SQLAlchemy, rofl.
    '''
    Lugar.total_likes += 1

    nuevomegusta = LeGustaModel (
      id_lugar = lugar_id,
      id_persona = current_user_id
    )

    try:
      Lugar.commit()
      nuevomegusta.save()
      return {'message': 'Ahora te gusta el lugar {}'.format(lugar_id)}
    except Exception as e:
      print(e)
      return {'message': "Algo fue mal"}, 500


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


'''
    Retornar las direcciones de la tabla.
'''
class LugarDescripcion(Resource):
  # TODO: Buscar por nombre
  def get(self,lugar_id):
    current_place = LugarModel.query.get(lugar_id)
    if not current_place:
      return {'message':'{} no existente'.format(lugar_id)}

    '''
      Debería también recuperar todos los horarios, 
      los me gusta, las denuncias, etc.
    '''

    def to_json_lugar(x):
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
        'vacaciones':x.vacaciones,
        'denuncias':x.denuncias,
        'total_likes':x.total_likes
      }
    def to_json_horario(x):
      return { 
        'lugar_id': x.id_lugar,
        'diadelasemana': x.diadelasemana,
        'horadeapertura_dia': x.horadeapertura_dia,
        'horadecierre_dia':x.horadecierre_dia,
        'horadeapertura_tarde':x.horadeapertura_tarde,
        'horadecierre_tarde':x.horadecierre_tarde,
      }
    return {
      'General': to_json_lugar(LugarModel.query.get(lugar_id)),
      'Horario': to_json_horario(HorarioModel.find_by_lugar(lugar_id)),
    }

class SecretResource(Resource):
    @jwt_required      
    def get(self):
        return {
            'answer': 42
        }





class AddCancha(Resource):
  #@jwt_required
  def post(self,lugar_id):
    parser = reqparse.RequestParser()
    parser.add_argument('tipo_de_pasto',
        help='Este campo no puede estar vacio',
        required=True)
    parser.add_argument('tipo_de_piso',
        help='Este campo no puede estar vacio',
        required=True)
    parser.add_argument('techado', type=int,
        help='Este campo no puede estar vacio',
        required=True)
    parser.add_argument('iluminacion', type=int,
        help='Este campo no puede estar vacio',
        required=True)
    parser.add_argument('fotodecancha',
        help='Este campo no puede estar vacio',
        required=True)

    data = parser.parse_args()

    if not LugarModel.query.get(lugar_id):
      return {'message':'No existe ese lugar'}

    nuevacancha = CanchaModel (
      id_lugar = lugar_id,
      tipo_de_pasto = data['tipo_de_pasto'],
      tipo_de_piso = data['tipo_de_piso'],
      techado = data['techado'],
      iluminacion = data['iluminacion'],
      fotodecancha = data['fotodecancha']
    )

    try:
      nuevacancha.save()
      return {'message': 'La cancha se ha agregado'}
    except Exception as e:
      print(e)
      return {'message': "Algo fue mal"}, 500




class AddHorario(Resource):
  #@jwt_required
  def post(self):
    parser = reqparse.RequestParser()
    parser.add_argument('lugar_id', type=int,
        help='Este campo no puede estar vacio',
        required=True)
    parser.add_argument('diadelasemana', type=int,
        help='Este campo no puede estar vacio',
        required=True)
    parser.add_argument('horadeapertura_dia', type=int,
        help='Este campo no puede estar vacio',
        required=True)
    parser.add_argument('horadecierre_dia', type=int,
        help='Este campo no puede estar vacio',
        required=True)
    parser.add_argument('horadeapertura_tarde', type=int,
        help='Este campo no puede estar vacio',
        required=True)
    parser.add_argument('horadecierre_tarde', type=int,
        help='Este campo no puede estar vacio',
        required=True)
    parser.add_argument('vacaciones', type=int,
        help='Este campo no puede estar vacio',
        required=True)

    data = parser.parse_args()

    if not LugarModel.query.get(lugar_id):
      return {'message':'No existe ese lugar'}

    if HorarioModel.find_by_lugar(lugar_id):
      return {'message':'Ya posee un horario'}

    nuevo_horario = Model (
      id_lugar = lugar_id,
      diadelasemana = data['diadelasemana'],
      horadeapertura_dia = data['horadeapertura_dia'],
      horadecierre_dia = data['horadecierre_dia'],
      horadeapertura_tarde = data['horadeapertura_tarde'],
      horadecierre_tarde = data['horadecierre_tarde'],
    )

    try:
      nuevo_horario.save_to_db()
      return {'message': 'El horario se ha agregado'}
    except Exception as e:
      print(e)
      return {'message': "Algo fue mal"}, 500



class AddAddress(Resource):
  #@jwt_required
  def post(self):
    parser = reqparse.RequestParser()
    parser.add_argument('lugar_id',
        help='Este campo no puede estar vacio',
        required=True)
    parser.add_argument('Address1',
        help='Este campo no puede estar vacio',
        required=True)
    parser.add_argument('Address2', 
        help='Este campo no puede estar vacio',
        required=True)
    parser.add_argument('Address3',
        help='Este campo no puede estar vacio',
        required=True)
    parser.add_argument('City',
        help='Este campo no puede estar vacio',
        required=True)
    parser.add_argument('State', 
        help='Este campo no puede estar vacio',
        required=True)
    parser.add_argument('Country', 
        help='Este campo no puede estar vacio',
        required=True)
    parser.add_argument('PostalCode', type=int,
        help='Este campo no puede estar vacio',
        required=True)

    data = parser.parse_args()
    lugar_id = data['lugar_id']

    if not LugarModel.query.get(lugar_id):
      return {'message':'No existe ese lugar'}

    if DireccionModel.find_by_ID(lugar_id):
      return {'message':'Ya posee un horario'}

    nuevadireccion = Model (
      id_lugar = lugar_id,
      Address1 = data['Address1'],
      Address2 = data['Address2'],
      Address3 = data['Address3'],
      City = data['City'],
      State = data['State'],
      Country = data['Country'],
      PostalCode = data['PostalCode'],
    )

    try:
      nuevadireccion.save_to_db()
      return {'message': 'El horario se ha agregado'}
    except Exception as e:
      print(e)
      return {'message': "Algo fue mal"}, 500

class AddSport(Resource):
  #@jwt_required
  def post(self):
    parser = reqparse.RequestParser()
    parser.add_argument('lugar_id', type=int,
        help='Este campo no puede estar vacio',
        required=True)
    parser.add_argument('tipo_deporte',
        help='Este campo no puede estar vacio',
        required=True)

    data = parser.parse_args()
    lugar_id = data['lugar_id']

    if not LugarModel.query.get(lugar_id):
      return {'message':'No existe ese lugar'}

    row = DeporteModel.find_by_lugar(lugar_id)

    invalido = 0
    for i in range(0,len(row)):
      if row[i].tipo_deporte == data['tipo_deporte']:
        invalido = 1

    if invalido:
      return {'message':'Ese deporte ya existe'}

    nuevo_deporte = DeporteModel (
      id_lugar = lugar_id,
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
    parser.add_argument('lugar_id',
          type=int,
          help='Este campo no puede estar vacio',
          required=True)
    parser.add_argument('diadelasemana',
          type=int,
          help='Este campo no puede estar vacio',
          required=True)
    parser.add_argument('fechaalquiler',
          help='Este campo no puede estar vacio',
          required=True)
    # type=datetime significa que va a ejecutar datetime(horacomienzo) al argumento
    parser.add_argument('horacomienzo',
          type=int,help='Este campo no puede estar vacio',
          required=True)
    parser.add_argument('senado',
          type=int,
          help='Este campo no puede estar vacio',
          required=True)
    # Tiempo en horas.
    parser.add_argument('tiempo',
          type=int,
          help='Este campo no puede estar vacio',
          required=True)

    data = parser.parse_args()
    id_lugar = data['lugar_id']

    if not LugarModel.query.get(id_lugar):
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
    if (
        data['horacomienzo'] >= DataHorario.horadeapertura_dia and 
        data['horacomienzo'] <= DataHorario.horadeapertura_dia
       ):
      horario_invalido = 1
    if (
    data['horacomienzo'] >= DataHorario.hora_apertura_tarde and
    data['horacomienzo'] <= DataHorario.horadeapertura_tarde
       ):
      horario_invalido = 1

    if horario_invalido:
      return {'message':'Horario invalido'},500

    # Verifico si ya está alquilado, probablemente estén mal los tipos después los corrijo.
    if AlquilaLugarModel.verificar_alquiler(id_lugar,data['fechaalquilar'],data['horacomienzo']):
      return {'message':'Horario no disponible'},500

    nuevo_alquiler = AlquilaLugarModel (
      id_lugar = id_lugar,
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
      return {'message': 'El lugar {} se ha alquilado a las {} horas hasta las {} horas, espera la confirmacion.'.format(
      id_lugar,hora_from_int_to_string(data['horacomienzo']),str(hora_from_int_to_string(data['horacomienzo'])+timedelta(hours=data['tiempo'])))}

    except Exception as e:
      print(e)
      return {'message': "Algo exploto"}, 500

class Reservas(Resource):
  # Versión prueba
  #@jwt_required
  def get(self):
    # Nombre cliente.
    #current_user = get_jwt_identity()
    current_user = "Acer_"
    current_user_id = UsuarioModel.find_by_nombre(nombre = current_user).id

    if AlquilaLugarModel.query.get(current_user_id) == None:
      return {'message':'No posee ninguna reserva hecha.'}

    def to_json(x):
      return {
        'id_lugar': x.id_lugar,
        'fecha_alquilado': x.fechaalquiler,
        'diadelasemana': x.diadelasemana,
        'senado':x.senado,
        'tiempo':x.tiempo,
        'confirmado':x.confirmado,
      }
    return {'alquiler': list(map(lambda x: to_json(x), AlquilaLugarModel.query.get(current_user_id)))}

'''
class AddVacaciones(Resource):
  def post(self):
    parser = reqparse.RequestParser()
'''

class AddHorario(Resource):
  def post(self):
    parser = reqparse.RequestParser()
    parser.add_argument('lugar_id', 
            type=int,
            help='Este campo no puede estar vacio',
            required=True)
    parser.add_argument('diadelasemana', 
            type=int,
            help='Este campo no puede estar vacio',
            required=True)
    parser.add_argument('horadeapertura_dia',
            type=int,
            help='Este campo no puede estar vacio',
            required=True)
    parser.add_argument('horadecierre_dia',
            type=int,
            help='Este campo no puede estar vacio',
            required=True)
    parser.add_argument('horadeapertura_tarde',
            type=int,
            help='Este campo no puede estar vacio',
            required=True)
    parser.add_argument('horadecierre_tarde',
            type=int,
            help='Este campo no puede estar vacio',
            required=True)

    data = parser.parse_args()   
    id_lugar = data['lugar_id']

    lugar_horario = HorarioModel (
      id_lugar = data['lugar_id'],
      diadelasemana = data['diadelasemana'],
      horadeapertura_dia = data['horadeapertura_dia'],
      horadecierre_dia = data['horadecierre_dia'],
      horadeapertura_tarde = data['horadeapertura_tarde'],
      horadecierre_tarde = data['horadecierre_tarde'],
    )

    if HorarioModel.query.get(id_lugar):
      print(HorarioModel.query.get(id_lugar))
      return {'message': 'Ese lugar ya posee un horario definido, si desea cambiarlo use /cambiar(no definido)'}

    try:
      lugar_horario.save_to_db()
      return {
        'message': 'El horario al lugar {} se ha guardado'.format(id_lugar)
      }
    except Exception as e:
      print(e)
      return {'message':'Algo falló al agregar el lugar'},500



class InfoUsuario(Resource):
  def get(self,nombre):
    def to_json(x):
      return {
        'nombre': x.nombre,
        'correo': x.correo
      }   
    return {'nombre': to_json(UsuarioModel.find_by_nombre(nombre))}



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
      total_likes = 0,
      vacaciones = 0,
      denuncias = 0
    )

    try:
      nuevo_lugar.save_to_db()
      return {
        'message': 'El lugar {} se ha guardado'.format(data['lugar_nombre'])
      }
    except Exception as e:
      print(e)
      return {'message':'Algo falló al agregar el lugar'},500
