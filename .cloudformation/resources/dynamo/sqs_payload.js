module.exports = () => ({
    "Type": "AWS::DynamoDB::Table",
    "DeletionPolicy":"Retain",
    "Properties": {
        "TableName": "${file(${self:provider.stage}.yml):TABLA_SQS_PAYLOAD}",
        "AttributeDefinitions": [
            {
                "AttributeName": "id",
                "AttributeType": "S"
            },
            {
                "AttributeName": "estado",
                "AttributeType": "N"
            }
        ],
        "KeySchema": [
            {
                "AttributeName" : "id",
                "KeyType" : "HASH"
            },
            {
                "AttributeName": "estado",
                "KeyType": "RANGE"
            }
        ],
        "BillingMode": "PAY_PER_REQUEST",
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "estadoIndex",
                "KeySchema": [
                    {
                        "AttributeName" : "estado",
                        "KeyType" : "HASH"
                    }
                ],
                "Projection": {
                    "ProjectionType": "ALL"
                }
            }
        ]
    }
});
