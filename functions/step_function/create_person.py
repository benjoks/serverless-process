import requests
import os
import json
import logging
from utils.authorize import get_token

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

URL_BASE_PERSONAS =  os.getenv('URL_BASE_PERSONAS')

def handler(message, context):
    """ Se encarga de crear a la persona en la api personas """

    try:
        payload = json.dumps(message["comprador"])
        logger.info("Payload = %s", payload)
        url = URL_BASE_PERSONAS
        #url = "https://api.bvmdev.com/v1/personas"
        token = get_token()
        logger.info(token)
        headers = {"Content-type":"application/json", "Accept":"application/json", "Authorization": token }
        response = requests.post(url,data = payload, headers=headers)
        logger.info("Response %s", response)
        if response.status_code==200:    
            message["message"] = "Se ha ingresado al cliente  a la Base de Datos"        
            return message
        raise "Error al utilizar servicio de crear persona"
    except Exception as e:
        logger.exception(str(e))
        raise Exception(500, e, "Error en el proceso")
