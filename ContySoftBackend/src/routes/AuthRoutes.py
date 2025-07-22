import traceback, requests, json
from flask import Blueprint, jsonify, request

from src.models.seguridad.UsuarioModel import Usuario
from src.models.CustomResponseModel import CustomResponseModel
from src.models.seguridad.UsuarioRegistroRequestModel import UsuarioRegistroRequest
from src.utils.Seguridad import Seguridad
from decouple import config


#services
from src.services.AuthService import AuthService
from src.utils.Logger import Logger

main = Blueprint('auth_blueprint', __name__)
api_ruc = config('API_RUC')
token_ruc = config('TOKEN_RUC')


@main.route('/validar-email/<email>', methods=['GET'])
def validar_email(email: str):
    try:
        usuario_autenticado = AuthService.login_usuario(email)
        email_valido = True
        mensaje = 'El email es válido.'
        if usuario_autenticado != None:
            email_valido = False
            mensaje = 'El email ya está siendo usado, por favor, recupere su cuenta o contáctese con el administrador del sistema.'
        print(email)
        return jsonify({
                'message': mensaje,
                'data': email_valido })
    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return CustomResponseModel('Sucedió un error interno.', None).InternalServerError()
    
@main.route('', methods=['POST', 'OPTIONS'])
def login():
    try:
        usuario = request.json['usuario']
        password = request.json['password']

        usuario_autenticado = AuthService.login_usuario(usuario)
        if usuario_autenticado != None and Seguridad.verify_password(password, usuario_autenticado.password):
            token_codificado = Seguridad.generar_token(usuario_autenticado)
            return jsonify({
                'usuario': usuario_autenticado.usuario,
                'fullname': usuario_autenticado.fullname,
                'token': token_codificado
                })
        else:
            return CustomResponseModel('Usuario y/o contraseña incorrecta.', None).Unauthorized()
    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return CustomResponseModel('Sucedió un error interno.', None).InternalServerError()
@main.route('/registro', methods=['POST'])
def registro():
    try:
        data = request.json
        registro = None
        if data == None:
            return CustomResponseModel('No se recibió la información correcta.', None).BadRequest()
        else:
            registro = UsuarioRegistroRequest(data.get('ruc'),
                                              data.get('razon_social'),
                                              data.get('tipo_persona'),
                                              data.get('usuario_sol'),
                                              data.get('password_sol'),
                                              data.get('usuario'),
                                              Seguridad.hash_text(data.get('password')),
                                              data.get('id_plan'))
        print(registro)   
        usuario_autenticado = AuthService.registrar_usuario(registro)
        token_codificado = Seguridad.generar_token(usuario_autenticado)
        return jsonify({
            'usuario': usuario_autenticado.usuario,
            'fullname': usuario_autenticado.fullname,
            'token': token_codificado
            })
    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return CustomResponseModel(str(ex), None).InternalServerError()


@main.route('/info-sunat', methods=['POST'])
def info_sunat():
    ruc = request.json['ruc']
    
    ruc_en_uso = AuthService.existe_ruc(ruc)
    if ruc_en_uso:
        return CustomResponseModel('El RUC  ya se encuentra en uso en nuestro sistema, si esto no es correcto, contáctese con el adminsitrador.', None, False).Ok()


    url = f'{api_ruc}?numero={ruc}'
    # url = f'https://ww1.sunat.gob.pe/ol-ti-itfisdenreg/itfisdenreg.htm?accion=obtenerDatosRuc&nroRuc={ruc}&fbclid=IwZXh0bgNhZW0CMTAAAR1zXeu3NjGzcQGdbz89T0cRR_8QpOFFssXhVUV7uiSq_oMqopMYRQwIRTM_aem_APAPMQ9bIq6ACihQgIpWfw'
    headers = {
        'Authorization': f'Bearer {token_ruc}'
        }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return CustomResponseModel('El RUC no esta en uso en nuestro sistema, puede continuar. :)', response.json(), True).Ok()
    else:
        response = json.loads(response.text)
        return CustomResponseModel(response['message'], None).BadRequest()