module.exports = () => ({
    "Type": "AWS::Events::EventBus",
    "Properties": {
            "Name": "${self:custom.busEventName}"
        }
});
