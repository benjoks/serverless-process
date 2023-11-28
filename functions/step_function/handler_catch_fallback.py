import logging
import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def handler(message, context):
    """ se encarga de manejar las excepciones que se presenten en el proceso """
    try:
        mensaje = json.loads(message['Cause'])
        mensajerr = mensaje['errorMessage']
        raise ValueError(mensajerr)
    except Exception as e:
        logger.exception(str(e))
        raise Exception(500, e, "Error en el proceso", "handler_catch_fallback.handler")
