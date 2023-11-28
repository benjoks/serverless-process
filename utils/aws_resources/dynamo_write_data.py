import logging
import os
import boto3
from boto3 import resource
from boto3.dynamodb.conditions import Key
from utils.aws_resources.dynamo_prepare_payload import prepare_payload_sqs_dynamo

REGION_NAME_BY_STAGE = os.getenv('REGION_NAME_BY_STAGE')
TABLA_SQS_PAYLOAD = os.getenv("TABLA_SQS_PAYLOAD")

dynamo_resource = boto3.resource('dynamodb', region_name=REGION_NAME_BY_STAGE)
dynamo_sqs_payload = resource('dynamodb', use_ssl=True).Table(TABLA_SQS_PAYLOAD)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def write_in_dynamo_sqs_payload(detail):
    try:
        response = dynamo_sqs_payload.put_item(
            Item = prepare_payload_sqs_dynamo(detail)
        )
        logger.info("Carga en Dynamo")
        return response
    except Exception as e:
        raise Exception(500, e, 'write_in_dynamo_process')
