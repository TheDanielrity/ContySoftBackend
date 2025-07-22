import traceback
import json
from flask import Blueprint, jsonify, request
from src.models.CustomResponseModel import CustomResponseModel
from src.utils.ApiSunat import ApiSunat
#services
from src.services.VentasService import VentasService
from src.utils.Logger import Logger
from src.utils.Seguridad import Seguridad

main = Blueprint('ventas_blueprint', __name__)


@main.route('/periodos', methods = ['POST'])
def obtenerPeriodos():
    try:
        print('inicio')
        token = request.json['token']
        data_verified = Seguridad.validar_token(token)
        if data_verified:
            Id = data_verified.get('id')
        else:
            return CustomResponseModel('Ha ocurrido un error, inténtelo nuevamente.', None).Unauthorized()
        response = VentasService.get_period(Id)
        print(response)
        return response

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return CustomResponseModel('Ha ocurrido un error interno, inténtelo nuevamente', None).InternalServerError()

@main.route('/obtener', methods = ['POST'])
def obtenerVentas():
    try:
        periodo = request.json['periodo']
        token = request.json['token']
        data_verified = Seguridad.validar_token(token)
        if data_verified:
            Id = data_verified.get('id')
        else:
            return CustomResponseModel('Ha ocurrido un error, inténtelo nuevamente.', None).Unauthorized()
        
        response = VentasService.get_ventas(Id, periodo)
        return jsonify(response)

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return CustomResponseModel('Ocurrió un error al cargar las ventas, inténtelo nuevamente', None).InternalServerError()



@main.route('/importar', methods = ['POST'])
async def importarVentas():
    try:
        periodo = request.json['periodo']
        token = request.json['token']
        data_verified = Seguridad.validar_token(token)
        if data_verified:
            Id = data_verified.get('id')
        else:
            return CustomResponseModel('Ha ocurrido un error, inténtelo nuevamente.', None).Unauthorized()


        response = await VentasService.save_data_ventas(Id, periodo)
        
        return response

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return CustomResponseModel('Ocurrió un error al importar las ventas, inténtelo nuevamente', None).InternalServerError()
    

@main.route('/productos/<ruc>-<numSerie>-<numDocumento>' ,methods = ['GET'])
def obtenerProductos(ruc, numSerie, numDocumento):
    try:
        response = VentasService.get_products(ruc, numSerie, numDocumento)
        return response
    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return CustomResponseModel('Ha ocurrido un error interno, inténtelo nuevamente', None).InternalServerError()