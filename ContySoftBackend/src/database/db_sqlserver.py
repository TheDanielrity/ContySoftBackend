import traceback
from decouple import config
import pyodbc

from src.utils.Logger import Logger

def get_conexion():
    try:
        connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={config("SQLSERVER_HOST")};DATABASE={config("SQLSERVER_DB")};UID={config("SQLSERVER_USER")};PWD={config("SQLSERVER_PASSWORD")}'
        #connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER=.;DATABASE=dbContySoft;UID={config("SQLSERVER_USER")};PWD=123456'

        return pyodbc.connect(connectionString)
    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())

def check_database():
    try:
        conn = get_conexion()
        cursor = conn.cursor()
        cursor.execute('SELECT 1') 
        cursor.close()
        conn.close()
        return True 
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return False  