import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def prepare_payload_sqs_dynamo(detail):
    logger.info(detail)
    retorno =  {}
    retorno["id"] = detail["id_compra"]
    retorno["estado"] = 0
    retorno["fecha_compra"] = detail["fecha_compra"]
    retorno["valor_total"] =detail["valor_total"]
    retorno["moneda"] = detail["moneda"]
    rut = str(detail["comprador"]["rut"])+"-"+detail["comprador"]["dv"]
    retorno["rut_comprador"] = rut
    retorno["payload"] = detail
    logger.info(retorno)
    return retorno