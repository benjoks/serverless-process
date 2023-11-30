import logging
import boto3
import json
import os
import time
from utils.aws_resources.dynamo_get_data import get_cantidad_sqs

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ARN_STATE = os.getenv('ARN_STATE')
URL_QUEUE = os.getenv('URL_QUEUE')


def handler(event,context):
    """ Se llama a SQS y se manda payload a stateMachine, ejecutandose segun cantidad de la tabla """

    x = 0
    cantidad =  get_cantidad_sqs()
    tiempo = 60 // cantidad
    while x < cantidad:
        sqs = boto3.client('sqs')
        response = sqs.receive_message(
            QueueUrl=URL_QUEUE,
            AttributeNames=['All'],
            MaxNumberOfMessages=1,
            MessageAttributeNames=[
                'All'
            ],
            VisibilityTimeout=0,
            WaitTimeSeconds=0
        )
        logger.info("SQS procesada: %s", (x+1))
        logger.info("response %s", response)
        if "Messages" in response:
            body = json.loads(response["Messages"][0]["Body"])
            logger.info("body %s", type(body))
            logger.info("response %s", type(body["message"]))
            send_to_statemachine(json.dumps(body["message"]))
            receipt_handle = response["Messages"][0]["ReceiptHandle"]
            response_delete = sqs.delete_message(
                QueueUrl=URL_QUEUE,
                ReceiptHandle=receipt_handle
            )
            print("sleep {}".format(tiempo))
            time.sleep(tiempo)
        else:
            x = cantidad
        x = x + 1
    return "Fin"

def send_to_statemachine(body : str):
    logger.info(body)
    logger.info(ARN_STATE)
    message_body = body
    client = boto3.client('stepfunctions')
    response = client.start_execution(
        stateMachineArn= ARN_STATE,
        input=message_body
    )
    logger.info("Se ejecuta StepFunction")
    return message_body
