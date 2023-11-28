module.exports = () => ({
    "Type": "AWS::DynamoDB::Table",
    "DeletionPolicy":"Retain",
    "Properties": {
        "TableName": "${file(${self:provider.stage}.yml):TABLA_NUMSQS_PROCESS}",
        "AttributeDefinitions": [
            {
                "AttributeName": "idNumSqs",
                "AttributeType": "N"
            }
        ],
        "KeySchema": [
            {
                "AttributeName": "idNumSqs",
                "KeyType": "HASH"
            }
        ],
        "ProvisionedThroughput": {
            "ReadCapacityUnits": 2,
            "WriteCapacityUnits": 2
        }
    }
});
