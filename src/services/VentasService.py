from io import BytesIO
from src.database.db_sqlserver import get_conexion
from src.models.contabilidad.DatosVentasModel import DatosVentas
from src.models.contabilidad.DatosVentasRequestModel import DatosVentasRequest
from src.models.CustomResponseModel import CustomResponseModel
from src.utils.Logger import Logger
from src.utils.ApiSunat import ApiSunat
from translate import Translator
from src.utils.Seguridad import Seguridad
from src.utils.tablas_sunat import TIPO_CP, ESTADO_CP, TIPO_DOCUMENTO
import re, requests, aiohttp, asyncio, pyodbc, traceback, zipfile
from flask import jsonify
from decouple import config
from datetime import datetime

traductor = Translator(to_lang='es')
url_sunat_cpe = config('API_SUNAT_CPE')
url_sunat = config('API_SUNAT')
url_sunat_sire = config('API_SIRE')

# header_txt = [
#             "Ruc", "Razon Social", "Periodo", "CAR SUNAT", "Fecha de emisión", "Fecha Vcto/Pago", 
#             "Tipo CP/Doc.", "Serie del CDP", "Nro CP o Doc. Nro Inicial (Rango)", 
#             "Nro Final (Rango)", "Tipo Doc Identidad", "Nro Doc Identidad", 
#             "Apellidos Nombres/ Razón Social", "Valor Facturado Exportación", "BI Gravada", 
#             "Dscto BI", "IGV / IPM", "Dscto IGV / IPM", "Mto Exonerado", "Mto Inafecto", 
#             "ISC", "BI Grav IVAP", "IVAP", "ICBPER", "Otros Tributos", "Total CP", 
#             "Moneda", "Tipo Cambio", "Fecha Emisión Doc Modificado", "Tipo CP Modificado", 
#             "Serie CP Modificado", "Nro CP Modificado", "ID Proyecto Operadores Atribución", 
#             "Tipo de Nota", "Est. Comp", "Valor FOB Embarcado", "Valor OP Gratuitas", 
#             "Tipo Operación", "DAM / CP", "CLU"
#             ]

meses = {
    '01': 'ENERO',
    '02': 'FEBRERO',
    '03': 'MARZO',
    '04': 'ABRIL',
    '05': 'MAYO',
    '06': 'JUNIO',
    '07': 'JULIO',
    '08': 'AGOSTO',
    '09': 'SEPTIEMBRE',
    '10': 'OCTUBRE',
    '11': 'NOVIEMBRE',
    '12': 'DICIEMBRE'
}

header_txt = [
    "RUC",
    "ID",
    "Periodo",
    "CAR SUNAT",
    "Fecha de Emisión",
    "Fecha Vcto/Pago",
    "Tipo CP/Doc",
    "Serie del CDP",
    "Nro CP o Doc Nro Inicial (Rango)",
    "Nro Final (Rango)",
    "Tipo Doc Identidad",
    "Nro Doc Identidad",
    "Apellidos Nombres / Razón Social",
    "Valor Facturado Exportación",
    "BI Gravada",
    "Dscto BI",
    "IGV/IPM",
    "Dscto IGV/IPM",
    "Mto Exonerado",
    "Mto Inafecto",
    "ISC",
    "BI Grav IVAP",
    "IVAP",
    "ICBPER",
    "Otros Tributos",
    "Total CP",
    "Moneda",
    "Tipo Cambio",
    "Fecha Emisión Doc Modificado",
    "Tipo CP Modificado",
    "Serie CP Modificado",
    "Nro CP Modificado",
    "ID Proyecto Operadores Atribución",
    "CLU 1",
    "CLU 2",
    "CLU 3",
    "CLU 4",
    "CLU 5",
    "CLU 6",
    "CLU 7",
    "CLU 8",
    "CLU 9",
    "CLU 10",
    "CLU 11",
    "CLU 12",
    "CLU 13",
    "CLU 14",
    "CLU 15",
    "CLU 16",
    "CLU 17"
]


class VentasService:


    @classmethod
    def get_period(cls, Id):
        # start_time = datetime.now()

        data = {'data': [[], []]
            }
        try:
            with get_conexion() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("EXEC Contabilidad.Usp_ObtenerDatosContables @Id = ?;", Id)
                    row = cursor.fetchone()
                    if not row:
                        return CustomResponseModel('Ocurrió un error interno.', None).InternalServerError()
                    
                    ruc, username, password = row
            print(username)
            print(password)
            # username = Seguridad.desencriptar_data(username, 'username')
            # password = Seguridad.desencriptar_data(password, 'password')
            print(username)
            print(password)
            url = f'{url_sunat_sire}/rvierce/padron/web/omisos/140000/periodos'
            start_time = datetime.now()
            token = ApiSunat.generate_token_sire(ruc, username, password)
            if not token:
                return CustomResponseModel("Verifique que su CLAVE SOL sea correcta.", None).BadRequest()
            
            headers = {'Authorization': f'Bearer {token}'}
            response = requests.get(url, headers=headers)
            end_time = datetime.now()
            print(end_time-start_time)
            if response.status_code != 200:
                response = dict(response.json())
                return CustomResponseModel(response.get('msg'), None).BadRequest(code=response.get('cod'))
            
            response = list(response.json())
            for anio in response:
                if anio.get('desEstado').lower() == 'presentado':
                    data['data'][0].append({
                        'year': f"{anio.get('numEjercicio')}-{anio.get('desEstado')}",
                        'value': anio.get('numEjercicio'),
                        })
                    for period in anio.get('lisPeriodos'):
                        if period.get('desEstado').lower() == 'presentado':
                            data['data'][1].append({
                                'periodo': f"{meses.get(period.get('perTributario')[-2:])[:3]}-{period.get('desEstado')}",
                                'value': period.get('perTributario'),
                                })

            print(data)
            
            return jsonify(data)
            
                

        except pyodbc.Error as e:
            Logger.add_to_log("error", str(e))
            match = re.findall(r'(?:\]|\)|^)([^()\[\]]+)(?:\(|\[|$)', e.args[1])
            message = "Ups, sucedió un error interno."
            if match:
                message = ' '.join(match).strip()

            raise Exception(message)
    # @classmethod
    # def get_period(cls, Id):
    #     # start_time = datetime.now()
    #     ruc = None
    #     username = None
    #     password = None
    #     data = {'data':[ [],{}]
    #         }
    #     try:
    #         with get_conexion() as conn:
    #             with conn.cursor() as cursor:
    #                 cursor.execute("EXEC Contabilidad.Usp_ObtenerDatosContables @Id = ?;", Id)
    #                 row= cursor.fetchone()
    #                 if row:
    #                     ruc, username, password = row
    #                 else:
    #                     return CustomResponseModel('Ocurrió un error interno.', None).InternalServerError()

    #         url = f'{url_sunat_sire}/rvierce/padron/web/omisos/140000/periodos'
    #         start_time = datetime.now()
    #         token = ApiSunat.generate_token_sire(ruc, username, password)
    #         if not token:
    #             return CustomResponseModel("Verifique que su CLAVE SOL sea correcta.", None).BadRequest()
            
    #         headers = {'Authorization': f'Bearer {token}'}
    #         response = requests.get(url, headers=headers)
    #         end_time = datetime.now()
    #         print(end_time-start_time)
    #         if response.status_code == 200:
    #             response = list(response.json())
    #             for anio in response:
    #                 if anio.get('desEstado').lower() == 'presentado':
    #                     data['data'][0].append({
    #                         'label': f'{anio.get("numEjercicio")}-{anio.get("desEstado")}',
    #                         'value': anio.get("numEjercicio")
    #                         })
    #                     data['data'][1][anio.get("numEjercicio")] = []
    #                     for period in anio.get('lisPeriodos'):
    #                         if period.get('desEstado').lower() == 'presentado':
    #                             date = datetime.strptime(period.get('perTributario'), "%Y%m")
    #                             mes = date.strftime("%B")
    #                             print(mes)
    #                             data['data'][1][anio.get("numEjercicio")].append({
    #                                 'label': f'{mes[:3].upper()}-{period.get("desEstado")}',
    #                                 'value': period.get("perTributario")
    #                                 })
    #             print(data)
                
    #             return jsonify(data)
    #         else:
    #             response = dict(response.json())
    #             return CustomResponseModel(response.get('msg'), None).BadRequest(code=response.get('cod'))

    #     except pyodbc.Error as e:
    #         Logger.add_to_log("error", str(e))
    #         match = re.findall(r'(?:\]|\)|^)([^()\[\]]+)(?:\(|\[|$)', e.args[1])
    #         message = "Ups, sucedió un error interno."
    #         if match:
    #             message = ' '.join(match).strip()

    #         raise Exception(message)
    @classmethod
    def get_products(cls, ruc, numSerie, numDoc):
        try:
            if numSerie.upper().startswith('F'):
                tipo_CP = 'factura'
            elif numSerie.upper().startswith('B'):
                tipo_CP = 'boleta'
            else:
                return CustomResponseModel('Tipo de documento no admitido, solo boleta o factura.', None).BadRequest()
            data = {}
            headers = {'Authorization': f'Bearer {config("TOKEN_API_SUNAT")}'}
            response = requests.get(f'{url_sunat_cpe}/{tipo_CP}/{ruc}-{numSerie}-{numDoc}', headers=headers)
            response = dict(response.json())

            if response.get('status') != 200:
                return CustomResponseModel(response.get('message'), None).BadRequest(code=response.get('status'))
            
            records = response.get('data').get('detalleComprobanteBean') or []
            for record in records:
                record['cantidad'] = float(record.get('cantidad'))
                record['precioUnitario'] = float(record.get('precioUnitario'))
                record['valorVtaUnitario'] = float(record.get('valorVtaUnitario'))
                record['subtotal'] = record.get('precioUnitario') * record.get('cantidad')

            data['data'] = records
            
            
            return jsonify(data)
         
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
            raise Exception(ex)
    @classmethod
    def get_ventas(cls, Id, periodo):
        
        try:
            connection = get_conexion()
            with connection.cursor() as cursor:
                cursor.execute("EXEC Contabilidad.Usp_ObtenerDatosVentas @Id = ?, @periodo = ?;", Id, periodo)
                data = {'data': []}
                datos_ventas = cursor.fetchall()
                datos_ventas = [DatosVentasRequest(*record) for record in datos_ventas]
                # for venta in datos_ventas:
                data['data'].extend([{
                        'ruc': venta.ruc,
                        'serieCP': venta.serie_CP,
                        'numCP': venta.num_CP,
                        'fechaEmision': venta.fecha_emision,
                        'cliente': venta.cliente,
                        'periodo': venta.periodo,
                        'razonSocial': venta.razon_social,
                        'BI_Gravada': f'{venta.bi_gravada:.2f}',
                        'monto_inafecto': f'{venta.monto_inafecto:.2f}',
                        'IGV_IPM': f'{venta.igv_ipm:.2f}',
                        'total': f'{venta.total:.2f}',
                        'estadoCP': venta.estado_CP,
                        'idEstadoCP': venta.id_estado_CP,
                        'idTipoCP': venta.id_tipo_CP,
                        'tipoCP': venta.tipo_CP
                    } for venta in datos_ventas])
            connection.close()

            return data
        except pyodbc.Error as e:
            Logger.add_to_log("error", str(e))
            match = re.findall(r'(?:\]|\)|^)([^()\[\]]+)(?:\(|\[|$)', e.args[1])
            message = "Ups, sucedió un error interno."
            if match:
                message = ' '.join(match).strip()

            raise Exception(message)
    

    @classmethod
    async def __validate_data(cls, record, ruc, session, token):
        json_data = {
                    "numRuc": f"{ruc}",
                    "codComp": f"{record.id_tipo_CP}",
                    "numeroSerie": f"{record.serie_CP}",
                    "numero": f"{record.num_CP}",
                    "fechaEmision": f"{record.fecha_emision}",
                    "monto": f"{record.total:.2f}"
                        }
        
        
        header = {'Authorization': f'Bearer {token}'}
        async with session.post(f'{url_sunat}', headers=header, json=json_data) as response:
            response_data = dict(await response.json())
            
            if response.status != 200:
                return CustomResponseModel(response_data.get('message'), None).InternalServerError(response.status)
            
            print(response_data.get('data').get('estadoCp'))
            if response_data.get('data').get('estadoCp') == None:
                print('entra')
                # session = requests.Session()
                await cls.__validate_data(record, ruc, session, token)
            else:
                record.id_estado_CP = response_data.get('data').get('estadoCp')
            print('sale')
            
        
        return record
    # @classmethod
    # def _validate_data(cls, record, ruc, session, token):
    #     json_data = {
    #                 "numRuc": f"{ruc}",
    #                 "codComp": f"{record.id_tipo_CP}",
    #                 "numeroSerie": f"{record.serie_CP}",
    #                 "numero": f"{record.num_CP}",
    #                 "fechaEmision": f"{record.fecha_emision}",
    #                 "monto": f"{record.total:.2f}"
    #                     }
        
    #     if not token:
    #         return CustomResponseModel('Ocurrió un error interno. Inténtelo nuevamente.', None).InternalServerError()
    #     header = {'Authorization': f'Bearer {token}'}
    #     with session.post(f'{url_sunat}', headers=header, json=json_data) as response:
    #         response_data = dict(response.json())
    #         if response.status_code == 200:
    #             print('not none')
    #             print(response_data.get('data').get('estadoCp'))
    #             record.id_estado_CP = response_data.get('data').get('estadoCp')
    #         else:
    #             return CustomResponseModel(response_data.get('message'), None).InternalServerError(response.status)
        
    #     return record

    @classmethod
    async def save_data_ventas(cls, Id, periodo):
        start_time = datetime.now()
        try:
            with get_conexion() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("EXEC Contabilidad.Usp_ExistePeriodo @Id = ?, @periodo = ?;", Id, periodo)
                    if cursor.fetchone():
                        return CustomResponseModel('La información se guardó exitosamente.', None).Ok()
                    
                    cursor.execute("EXEC Contabilidad.Usp_ObtenerDatosContables @Id = ?;", Id)
                    row = cursor.fetchone()
                    
                    if not row:
                        return CustomResponseModel('Ocurrió un error interno.', None).InternalServerError()
                    
                    ruc, username, password = row
            # username = Seguridad.desencriptar_data(username)
            # password = Seguridad.desencriptar_data(password)

            url = f'{url_sunat_sire}/rvierce/gestionprocesosmasivos/web/masivo/consultaestadotickets'
            params = {
                'perIni': periodo, 
                'perFin': periodo, 
                'page': 1, 
                'perPage': 100
                }
            headers = {'Authorization': f'Bearer {ApiSunat.generate_token_sire(ruc, username, password)}'}
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()

            codTipoAchivoReporte = None
            nomArchivoReporte = None
            if response.status_code == 200:
                for record in response.json().get('registros', []):
                    if record.get('desProceso') == 'Generación de Registros':
                        for archivo_txt in record.get('archivoReporte', []):
                            if archivo_txt.get('nomArchivoReporte').endswith(f'LE{ruc}{periodo}00140400011112.zip'):
                                codTipoAchivoReporte = archivo_txt.get('codTipoAchivoReporte')
                                nomArchivoReporte = archivo_txt.get('nomArchivoReporte')
                                break
                    if codTipoAchivoReporte:
                        break
            else:
                return CustomResponseModel(response.json().get('msg'), None).BadRequest(code=response.json().get('cod'))

            url = f'{url_sunat_sire}/rvierce/gestionprocesosmasivos/web/masivo/archivoreporte'
            params = {
                'nomArchivoReporte': nomArchivoReporte,
                'codTipoArchivoReporte': codTipoAchivoReporte,
                'codLibro': '140000'
            }
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            
            lines = []
            ruc_txt = ''

            if response.status_code != 200:
                return CustomResponseModel(response.json().get('msg'), None).BadRequest(code=response.json().get('cod'))

            with zipfile.ZipFile(BytesIO(response.content), 'r') as archivo_zip:
                with archivo_zip.open(archivo_zip.namelist()[0]) as archivo_txt:
                    for  line in archivo_txt:
                        line = line.decode('utf-8-sig').strip().split('|')
                        lines.append(line)
                    ruc_txt = line[0]


            # validamos que no haya más de un ruc en todas las  líneas y que la linea de la cabecera del txt sea igual al del a lista header
            # if len(set(ruc_txt[1:])) > 1 or lines[0] != header_txt:
            #     return CustomResponseModel('No se recibió la información correcta.', None).BadRequest()
            
            if ruc_txt != ruc:
                return CustomResponseModel('No se recibió la información correcta.', None).BadRequest()
            
            
            into_data = [DatosVentas(*line[:28]) for line in lines[1:]]
            
            data = []


            
            token = ApiSunat.generate_token_cpe()
            if not token:
                return CustomResponseModel('Ocurrió un error interno. Inténtelo nuevamente.', None).InternalServerError()
            
            async with aiohttp.ClientSession() as session:
                tasks = [
                    cls.__validate_data(record, ruc, session, token)
                    for record in into_data
                ]
                results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # with requests.Session() as session:
            #     results = [
            #         cls.__validate_data(record, ruc_final, session, token)
            #         for record in into_data
            #     ]

            data.extend([(record.ruc, 
                          record.num_doc_CP, 
                          record.razon_social_CP, 
                          record.id_tipo_doc_CP, 
                          record.id_tipo_CP, 
                          record.serie_CP, 
                          record.car_sunat,
                          record.num_CP, 
                          record.fecha_emision, 
                          record.periodo,
                          record.bi_gravada,
                          record.dscto_BI, 
                          record.igv_ipm, 
                          record.dscto_IGV_IPM, 
                          record.monto_exonerado,
                          record.monto_inafecto, 
                          record.isc, 
                          record.bi_Grav_IVAP, 
                          record.ivap, 
                          record.icbper, 
                          record.otros_Tributos,
                          record.id_estado_CP,
                          record.total,
                          record.moneda,
                          record.tipo_cambio) for record in results])

           
            with get_conexion() as conn:

                with conn.cursor() as cursor:
                    
                    cursor.execute("EXEC Contabilidad.Usp_ValidarRuc @Id = ?, @ruc = ?;", Id, ruc)
                    row= cursor.fetchone()
                    if row:
                        cursor.executemany("EXEC Contabilidad.Usp_InsertarDatosVentas @ruc = ?, @num_doc_cliente_CP = ?, @razon_social_cliente_CP = ?,\
                                            @id_tipo_doc_cliente_CP = ?, @id_tipo_CP = ?, @serie_CP = ?, @CAR_sunat_ventas = ?, @num_CP_ventas = ?, \
                                       @fecha_emision_ventas = ?, @periodo_ventas = ?, @BI_Gravada = ?, @dscto_BI = ?, @IGV_IPM = ?, @dscto_IGV_IPM = ?, \
                                       @monto_exonerado = ?, @monto_inafecto = ?, @ISC = ?, @BI_Grav_IVAP = ?, @IVAP = ?,  @ICBPER = ?,  @otros_Tributos = ?,\
                                        @id_estado_CP = ?, @total = ?, @moneda = ?, @tipo_cambio = ?;", data)
                
            # connection.close()
            end_time = datetime.now()
            print(end_time-start_time)
            return CustomResponseModel('La información se guardó exitosamente.', None).Ok()
        except pyodbc.Error as e:
            Logger.add_to_log("error", str(e))
            match = re.findall(r'(?:\]|\)|^)([^()\[\]]+)(?:\(|\[|$)', e.args[1])
            message = "Ups, sucedió un error interno."
            if match:
                message = ' '.join(match).strip()
            print(e)
            raise Exception(message)