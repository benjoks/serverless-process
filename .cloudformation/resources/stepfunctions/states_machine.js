module.exports = () => ({
    "CatchAllFallback": {
      "Type": "Task",
      "Resource": {"Fn::Sub": "${self:custom.ARN_PREFIX_LAMBDAS}-catchFallback"},
      "End": true
    },
    "createPerson": {
      "Type": "Task",
      "Resource": {"Fn::Sub": "${self:custom.ARN_PREFIX_LAMBDAS}-createPerson"},
      "Next": "uploadPdf",
      "Catch": [{
        "ErrorEquals": ["States.ALL"],
        "Next": "CatchAllFallback"
      }]
    },
    "uploadPdf": {
      "Type": "Task",
      "Resource": {"Fn::Sub": "${self:custom.ARN_PREFIX_LAMBDAS}-uploadPdf"},
      "Next": "sendEmail",
      "Catch": [
        {
          "ErrorEquals": ["States.ALL"],
          "Next": "CatchAllFallback"
        },
      ]
    },
    "sendEmail": {
      "Type": "Task",
      "Resource": {"Fn::Sub": "${self:custom.ARN_PREFIX_LAMBDAS}-sendEmail"},
      "Next": "Fin",
      "Catch": [
        {
          "ErrorEquals": ["States.ALL"],
          "Next": "CatchAllFallback"
        },
      ]
    },
    "Fin": {
      "Type": "Pass",
      "End": true
      }
  })