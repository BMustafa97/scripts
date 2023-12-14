#!/usr/bin/env python

import boto3
from dateutil import parser

region = 'eu-west-2'

def newest_image(list_of_images):
    latest = None

    for image in list_of_images:
        if not latest:
            latest = image
            continue

        if parser.parse(image['CreationDate']) > parser.parse(latest['CreationDate']):
            latest = image

    return latest

client = boto3.client('ec2', region_name=region)

filters = [ {
        'Name': 'name',
        'Values': ['Windows_Server-2022-English-Full-EKS_Optimized-1.27-*']
    }
    ]
 
response = client.describe_images(Owners=['amazon'], Filters=filters)
 
source_image = newest_image(response['Images'])
print("\033[34mLatest Version Windows_Server-2022-English-Full-EKS_Optimized:", source_image['ImageId'], "\033[0m")
