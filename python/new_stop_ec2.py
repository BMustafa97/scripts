import logging
import os
import boto3

logging.basicConfig(level=os.environ.get('LOG_LEVEL', 'INFO'))

### SETTING UP BOTO3 CLIENT
ec2 = boto3.client('ec2')
logger = logging.getLogger(__name__)

### FUNCTION TO CHECK BOX IS UP AND RUNNING
def lambda_handler(event, context):

    filters = [{  
    'Name': 'tag:Name',
    'Values': ['NAME OF YOUR EC2 INSTANCE']
    }]

    response = ec2.describe_instances(Filters=filters)
    # logger.info(response)
    instance_id = ec2.describe_instances(Filters=filters)['Reservations'][0]['Instances'][0]['InstanceId']
    print(f'Instance-id =', instance_id)
    
    if response['Reservations'][0]['Instances'][0]['State']['Name'] == 'running':
        logger.info('Instance is running')
        stop_instances(instance_id)
    elif response['Reservations'][0]['Instances'][0]['State']['Name'] == 'stopped':
        logger.info('Instance is stopped, exiting lambda')
        print('Instance is stopped, exiting lambda')
    else:
        logger.info('Instance is stopping')
        error()

### FUNCTION TO STOP INSTANCE
def stop_instances(instance_id):
    print('stopping instance now')
    ec2.stop_instances(
    InstanceIds=[
        instance_id,
    ],
    # if DryRun=True, then no instances are stopped -- good for testing
    Hibernate=False,
    DryRun=False,
    Force=False
)

### ERROR FUNCTION
def error():
    print('error occured, Instance was stopping whilst code was called')
