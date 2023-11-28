module.exports = () => (
    {
    "Type": "AWS::S3::Bucket",
    "DeletionPolicy":"Retain",
    "Properties":
        {
            "BucketName": "${self:custom.S3_BUCKET}",
            "VersioningConfiguration": {
                "Status": "Enabled"
            }
        }
    }
);
