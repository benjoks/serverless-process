import os
import boto3
from boto3 import resource
from boto3.dynamodb.conditions import Key

REGION_NAME_BY_STAGE = os.getenv('REGION_NAME_BY_STAGE')
dynamo_resource = boto3.resource('dynamodb', region_name=REGION_NAME_BY_STAGE)

TABLA_SQS_PAYLOAD = os.getenv("TABLA_SQS_PAYLOAD")
TABLA_NUMSQS_PROCESS = os.getenv('TABLA_NUMSQS_PROCESS')

dynamo_resource = boto3.resource('dynamodb', region_name=REGION_NAME_BY_STAGE)

dynamo_sqs_payload = resource('dynamodb', use_ssl=True).Table(TABLA_SQS_PAYLOAD)
dynamo_sqs = resource('dynamodb', use_ssl=True).Table(TABLA_NUMSQS_PROCESS)


def get_sqs_false():
    try:
        reproceso_db = dynamo_resource.Table(TABLA_SQS_PAYLOAD)
        response = reproceso_db.query(
            IndexName="estadoIndex",
            KeyConditionExpression=
               'estado = :estado',
            ExpressionAttributeValues={
                ':estado': 0
             }
        )
        return response
    except Exception as e:
        raise Exception(500, e,"Error en get_sqs_false")

def get_cantidad_sqs():
    try:
        response = dynamo_sqs.query(
            ConsistentRead = True,
            KeyConditionExpression=
                Key('idNumSqs').eq(1)
        )
        response = response["Items"][0]["valor"]
        return response
    except Exception as e:
        raise Exception(500, e, 'get_cantidad_sqs')