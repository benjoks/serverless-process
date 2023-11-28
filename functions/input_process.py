import logging
import json
import os
import boto3
from utils.gen import validate_date_in, validar_rut,validar_email
from utils.aws_resources.sqs import enviar_to_sqs
from utils.aws_resources.dynamo_write_data import write_in_dynamo_sqs_payload

from lib.api_responses import response_bad_request,response_success,response_server_error
from utils.constants import MESSAGE_RES_200, DESCRIPTION_RES_201, MESSAGE_RES_400, DESCRIPTION_RES_400_DATE,DESCRIPTION_RES_400_VARIABLE,DESCRIPTION_RES_400_RUT,MESSAGE_RES_500,DESCRIPTION_RES_500,DESCRIPTION_RES_400_EMAIL

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def handler(message, context):
    """ Recive input, guarda en dynamo y envia a SQS  """
    try:
        logger.info("Input %s",message)
        body_i = (message["body"])
        body = json.loads(body_i)
        logger.info("Input %s",body)
        body_comprador = body["comprador"]
        validate = validate_input(body_comprador)
        if (validate != True):
            return validate
        
        db_response = write_in_dynamo_sqs_payload(body)
        if(db_response["ResponseMetadata"]["HTTPStatusCode"] == 200 or 201):
            payload = { "isfile":1,
                "message":message["body"]
            }
            response = enviar_to_sqs(payload)
            logger.info(json.dumps(response))
            return response_success(MESSAGE_RES_200, DESCRIPTION_RES_201)
        
        return response_server_error(MESSAGE_RES_500,DESCRIPTION_RES_500)
    except Exception as e:
        logger.exception(str(e))
        raise Exception(500, e, "Error en el proceso")
    
def validate_input(body):
    if validate_date_in(body["fecha_nacimiento"])==False:
        return response_bad_request(MESSAGE_RES_400, DESCRIPTION_RES_400_DATE % body["fecha_nacimiento"])
    if (len(body["paterno"])>15):
        return response_bad_request(MESSAGE_RES_400, DESCRIPTION_RES_400_VARIABLE % (body["paterno"],"15"))
    if (len(body["nombres"])>15):
        return response_bad_request(MESSAGE_RES_400, DESCRIPTION_RES_400_VARIABLE % (body["nombres"],"15"))
    if (len(body["nacionalidad"])>15):
        return response_bad_request(MESSAGE_RES_400, DESCRIPTION_RES_400_VARIABLE % (body["nacionalidad"],"10"))
    if (len(body["materno"])>15):
        return response_bad_request(MESSAGE_RES_400, DESCRIPTION_RES_400_VARIABLE % (body["materno"],"15"))
    if (validar_email(body["email"])==False):
        return response_bad_request(MESSAGE_RES_400, DESCRIPTION_RES_400_EMAIL % body["email"])
    sexo = ['masculino','m','femenino','f','otro','o']
    if ((body["sexo"].lower() in sexo) == False):
        return response_bad_request(MESSAGE_RES_400, "Variable Sexo no es valida")
    if validar_rut(str(body["rut"]),body["dv"])!=True:
        rut = str(body["rut"])+"-"+body["dv"]
        return response_bad_request(MESSAGE_RES_400, DESCRIPTION_RES_400_RUT % rut)
    return True