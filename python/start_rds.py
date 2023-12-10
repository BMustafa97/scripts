import json
import boto3

def lambda_handler(event, context):
    start = False  # Set start to True or False based on your condition
    stop = False  # Set stop to True or False based on your condition

    if start:
        start_rds()
    elif stop:
        stop_rds()
    else:
        print("No action specified, set start or stop to True")


def start_rds():
    rds = boto3.client('rds', region_name='eu-west-1')
    instances = rds.describe_db_instances()
    
    for instance in instances['DBInstances']:
        if instance['DBInstanceIdentifier'].endswith('database-1'):
            rds.start_db_instance(DBInstanceIdentifier=instance['DBInstanceIdentifier'])
            print("RDS instance started: " + instance['DBInstanceIdentifier'])
        else:
            print("No RDS instances found")

def stop_rds():
    rds = boto3.client('rds', region_name='eu-west-1')
    instances = rds.describe_db_instances()
    
    for instance in instances['DBInstances']:
        if instance['DBInstanceIdentifier'].endswith('database-1'):
            rds.stop_db_instance(DBInstanceIdentifier=instance['DBInstanceIdentifier'])
            print("RDS instance stopped: " + instance['DBInstanceIdentifier'])
        else:
            print("No RDS instances found")
