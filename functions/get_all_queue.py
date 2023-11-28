from utils.aws_resources.dynamo_get_data import get_sqs_false
from lib.api_responses import response_bad_request,response_not_found,response_success_data
from utils.constants import MESSAGE_RES_200, DESCRIPTION_RES_200, MESSAGE_RES_400, MESSAGE_RES_404, DESCRIPTION_RES_SQS_404, DESCRIPTION_RES_400_DATE,DESCRIPTION_RES_400_RUT,DESCRIPTION_RES_404_DB
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def handler(message, context):
    """ Se encarga de obtener los elementos que pasaron por SQS pero que no han sido procesados """

    try:
        res_db = get_sqs_false()
        logger.info(res_db)
        if res_db["Count"]<1 :
            return response_not_found(MESSAGE_RES_404,DESCRIPTION_RES_SQS_404)
        data = parse_response(res_db["Items"])
        json_data = {
            "message": "Elementos no procesados aun",
            "items":data
        }
        return response_success_data(MESSAGE_RES_200, DESCRIPTION_RES_200,json_data)
    
    except Exception as e:
        logger.exception(str(e))
        raise Exception(500, e, "Error en el proceso")

def parse_response(res):
    lista_item = []
    item_ob = {}
    for item in res:
        item_ob["id_compra"] = item["id"]
        item_ob["rut_comprador"] = item["rut_comprador"]
        item_ob["fecha_compra"] = item["fecha_compra"]
        item_ob["estado"] = "A la espera para procesar"

        lista_item.append(item_ob)
    return lista_item
