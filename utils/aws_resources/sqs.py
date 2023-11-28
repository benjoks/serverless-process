import logging
import boto3
import os
import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

URL_QUEUE = os.getenv('URL_QUEUE')


def enviar_to_sqs(payload):
    sqs = boto3.client('sqs')
    url=URL_QUEUE
    print(url)
    response = sqs.send_message(
        QueueUrl=url,
        MessageBody=json.dumps(payload)
    )
    logger.info("SE ENVÍA A SQS")
    return(response)
