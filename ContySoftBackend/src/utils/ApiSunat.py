from decouple import config
import requests

class ApiSunat:
    url_token_cpe = config('URL_SUNAT_TOKEN')
    client_id_cpe = config('CLIENT_ID')
    client_secret_cpe = config('CLIENT_SECRET')
    
    url_token_sire= config('URL_TOKEN_SIRE')
    client_id_sire = config('CLIENT_ID_SIRE')
    client_secret_sire = config('CLIENT_SECRET_SIRE')
    


    @classmethod
    def generate_token_cpe(cls):
        url = 'https://api.sunat.gob.pe/v1/contribuyente/contribuyentes'
        payload = f'grant_type=client_credentials&scope={url}&client_id={cls.client_id_cpe}&client_secret={cls.client_secret_cpe}'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
            }
        response = requests.post(url=cls.url_token_cpe, headers=headers, data=payload)
        if response.status_code == 200:
            token = dict(response.json())
            token = token.get('access_token')
            return token
        else:
            return None
        

    @classmethod
    def generate_token_sire(cls, ruc, username, password):
        url = 'https://api-sire.sunat.gob.pe'

        payload = f'grant_type=password&scope={url}&client_id={cls.client_id_sire}&client_secret={cls.client_secret_sire}&username={ruc}{username}&password={password}'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.post(url=cls.url_token_sire, headers=headers, data=payload)
        if response.status_code == 200:
            token = dict(response.json())
            token = token.get('access_token')
            return token
        else:
            return None