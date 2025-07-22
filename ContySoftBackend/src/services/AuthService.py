import traceback
from src.database.db_sqlserver import get_conexion
from src.models.seguridad.UsuarioRegistroRequestModel import UsuarioRegistroRequest
from src.models.seguridad.UsuarioAutenticadoModel import UsuarioAutenticado
from src.utils.Logger import Logger
import pyodbc
import re

class AuthService:
    @classmethod
    def login_usuario(self, usuario: str):
        try:
            connection = get_conexion()
            usuario_autenticado = None
            with connection.cursor() as cursor:
                cursor.execute('exec Seguridad.Usp_Usuario_Obtener @usuario=?', (usuario))
                row=cursor.fetchone()
                if row != None:
                    usuario_autenticado = UsuarioAutenticado(int(row[0]), usuario, row[1], row[2])
            connection.close()
            return usuario_autenticado
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())

    @classmethod
    def existe_ruc(self, ruc: str):
        try:
            connection = get_conexion()
            ruc_en_uso = False

            with connection.cursor() as cursor:
                cursor.execute('SELECT 1 FROM Seguridad.UsuarioContable WHERE ruc = ?', (ruc))
                row=cursor.fetchone()
                if row != None:
                    ruc_en_uso = True
            connection.close()
            return ruc_en_uso
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())

    @classmethod
    def registrar_usuario(self, usuarioRequest: UsuarioRegistroRequest):
        try:
            connection = get_conexion()
            usuario_autenticado = None
            with connection.cursor() as cursor:
                cursor.execute('exec Seguridad.Usp_Usuario_Registrar @ruc=?, @razon_social=?, @tipo_persona=?, @usuario_sol=?, @password_sol=?, @usuario=?, @password=?, @id_plan=?', (
                        usuarioRequest.ruc,
                        usuarioRequest.razon_social,
                        usuarioRequest.tipo_persona,
                        usuarioRequest.usuario_sol,
                        usuarioRequest.password_sol,
                        usuarioRequest.usuario,
                        usuarioRequest.password,
                        usuarioRequest.id_plan
                    ))
                row=cursor.fetchone()
                if row is not None:
                    usuario_autenticado = UsuarioAutenticado(int(row[0]), usuarioRequest.usuario, row[1], row[2])
            connection.close()
            return usuario_autenticado
        except pyodbc.Error as e:
            Logger.add_to_log("error", str(e))
            # Buscar el mensaje específico dentro del error
            match = re.search(r'\|(.*?)\|', e.args[1])
            message = "Ups, sucedió un error interno."
            if match:
                message = match.group(1)  # Extrae el mensaje capturado

            raise Exception(message)  # Lanza una nueva excepción con el mensaje deseado