import logging
import os
import boto3

logging.basicConfig(level=os.environ.get('LOG_LEVEL', 'INFO'))

### SETTING UP BOTO3 CLIENT
ec2 = boto3.client('ec2')
logger = logging.getLogger(__name__)

### SETTING UP VARIABLES
start = False
stop = False

### FUNCTION TO CHECK BOX IS UP AND RUNNING
def lambda_handler(event, context):

    filters = [{  
    'Name': 'tag:Name',
    'Values': ['NAME OF YOUR EC2 INSTANCE']
    }]

    instance_id = ec2.describe_instances(Filters=filters)['Reservations'][0]['Instances'][0]['InstanceId']
    print(f'Instance-id =', instance_id)
    
    if start:
        start_instances(instance_id)
        logger.info('Instance is starting')
    elif stop:
        stop_instances(instance_id)
        logger.info('Instance is stopping')
    else:
        logger.info('No action specified, set start or stop to True')
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
### FUNCTION TO START INSTANCE
def start_instances(instance_id):
    print('starting instance now')
    ec2.start_instances(
        InstanceIds=[
            instance_id,
        ],
        # if DryRun=True, then no instances are started -- good for testing
        DryRun=False
    )

### ERROR FUNCTION
def error():
    print('error occured, Instance was stopping whilst code was called')
