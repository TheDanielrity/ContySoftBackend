from flask import Blueprint, jsonify, request, render_template
import time

import traceback

# Logger
from src.database.db_sqlserver import check_database
from src.utils.Logger import Logger

main = Blueprint('index_blueprint', __name__, template_folder='../../templates')


@main.route('/')
def index():
    try:
        Logger.add_to_log("info", "{} {}".format(request.method, request.path))
        start_time = time.time()
        # Verificar el estado de la base de datos
        db_status = check_database()
        health_status = {
            "status": "Saludable" if db_status else "Mal",
            "db_status": "Oka" if db_status else "Falló",
            "uptime": f"{int(time.time() - start_time)} segundos",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()),
        }
        return render_template('health.html', health_status=health_status)
    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())

        response = jsonify({'message': "Internal Server Error", 'success': False})
        return response, 500