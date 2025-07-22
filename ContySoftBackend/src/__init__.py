from flask import Flask, jsonify
from flask_cors import CORS

# Routes
from src.routes import AuthRoutes, IndexRoutes, VentasRoutes

app = Flask(__name__)

def init_app(config):
    app.config.from_object(config)

    # Configurar CORS
    CORS(app)

    # Blueprints
    app.register_blueprint(IndexRoutes.main, url_prefix='/')
    app.register_blueprint(AuthRoutes.main, url_prefix='/api/auth')
    app.register_blueprint(VentasRoutes.main, url_prefix='/api/ventas')

    return app