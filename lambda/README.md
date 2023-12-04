# Info

If you would like to add a lambda layer to your account, use the following command once you have configured the AWS CLI.


aws lambda publish-layer-version --layer-name requests-layer --zip-file fileb://requests-layer.zip --compatible-runtimes python3.9 --profile default --region eu-west-2

## Relevant Links
https://aws.amazon.com/blogs/compute/upcoming-changes-to-the-python-sdk-in-aws-lambda/

https://medium.com/@koppulaanil1786/aws-lambda-layers-3f371e51bbaf

