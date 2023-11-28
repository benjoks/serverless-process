# import os
# import logging

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)

# URL_BASE_PERSONAS =  os.getenv('URL_BASE_PERSONAS')

def handler(message, context):
    """ Se encarga de mandar el pdf mediante correo """

    try:
          

        return message
    
    except Exception as e:
        # logger.exception(str(e))
        raise Exception(500, e, "Error en el proceso")
