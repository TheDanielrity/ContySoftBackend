from decouple import config
import datetime
import jwt
import pytz
import bcrypt
from cryptography.fernet import Fernet
from src.models.seguridad.UsuarioAutenticadoModel import UsuarioAutenticado
from src.utils.Logger import Logger

class Seguridad:
    secret = config('JWT_KEY')
    encryption_key_username = config('ENCRYPTION_KEY_USERNAME')
    encryption_key_password = config('ENCRYPTION_KEY_PASSWORD')
    tz = pytz.timezone('America/Lima')
    
    @classmethod
    def generar_token(self, usuario_atenticado: UsuarioAutenticado):
        payload = {
            'iat': datetime.datetime.now(tz=self.tz),
            'exp': datetime.datetime.now(tz=self.tz) + datetime.timedelta(minutes=11),
            'username': usuario_atenticado.usuario,
            'fullname': usuario_atenticado.fullname,
            'id': usuario_atenticado.id,
            'roles': ['User']
        }
        return jwt.encode(payload, self.secret, algorithm='HS256')
    
    
    @classmethod
    def validar_token(self, token: str):
        try:
            # Decodifica el token y verifica la firma y la expiración
            data = jwt.decode(token, self.secret, algorithms=['HS256'])
            return data
        except jwt.ExpiredSignatureError as ex:
            Logger.add_to_log("error", str(ex))
            return False
        except jwt.InvalidTokenError:
            return False
    @classmethod
    def hash_text(self, plain_password: str) -> str:
        salt = bcrypt.gensalt()  # Genera una sal segura
        hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), salt)  # Hashea la contraseña
        return hashed_password.decode('utf-8')  # Decodifica el resultado para obtener un string
    @classmethod    
    def verify_password(self, plain_password, hashed_password):
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    @classmethod
    def encriptar_data(cls, data, tipo):
        if tipo == 'username':
            cipher = Fernet(cls.encryption_key_username)
        else:
            cipher = Fernet(cls.encryption_key_password)
        return cipher.encrypt(data.encode()).decode()
    @classmethod
    def desencriptar_data(cls, encrypted_data, tipo) -> str:
        if tipo == 'username':
            cipher = Fernet(cls.encryption_key_username)
        else:
            cipher = Fernet(cls.encryption_key_password)

        return cipher.decrypt(encrypted_data.encode()).decode()
    