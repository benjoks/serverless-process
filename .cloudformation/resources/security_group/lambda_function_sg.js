module.exports = () => (

    {
        "Type": "AWS::EC2::SecurityGroup",
        "Properties":
            {
                "GroupName": "${self:service}-lambda-security-group-process",
                "GroupDescription": "Acceso para SOAP Oracle Report",
                "VpcId": "${file(${self:provider.stage}.yml):vpc-id}"
            }
    
    }
    );
    