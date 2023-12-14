import boto3
from dateutil import parser
import requests

region = 'eu-west-2'
list_of_amis = []
ami_name = 'Windows_Server-2022-English-Full-EKS_Optimized-1.27-*' # Change the AMI name here to what you want the latest version to be

def get_current_kube_ami():
    ec2 = boto3.resource(
        'ec2',
        region_name=region
    )

    for instance in ec2.instances.all():
        if instance.tags is not None:
            for tag in instance.tags:
                if tag['Key'] == 'Name' and tag['Value'] == 'INSTANCE_NAME':
                    if instance.platform == 'windows':
                        # append to a list
                        list_of_amis.append(instance.image_id)

                    else:
                        pass
                else:
                    pass
        else:
            pass

def get_latest_kube_ami(list_of_images):
    latest = None

    for image in list_of_images:
        if not latest:
            latest = image
            continue

        if parser.parse(image['CreationDate']) > parser.parse(latest['CreationDate']):
            latest = image

    return latest

def output_to_teams(new_ami, old_ami):
    # url = '' # Test URL
    url = '' # Kube URL
    headers = {'Content-Type': 'application/json'}
    payload = {
        "title": "AMI Update Notification! " + new_ami,
        "text": "Old AMI running in Prod EKS Cluster: " + str(old_ami) + "New AMI to be updated: " + new_ami + "\n" + " Count of AMIs to be updated: " + str(len(old_ami))
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print("Notification sent successfully!")
    else:
        print("Failed to send notification.")

# Main Script
def main():
        
    try: 
        client = boto3.client('ec2', region_name=region)
        filters = [ {
                'Name': 'name',
                'Values': [ami_name] # Change the AMI name here to what you want the latest version to be
            }
            ]
        response_images = client.describe_images(Owners=['amazon'], Filters=filters)
    except Exception as e:
        print(e)
        exit()

    get_current_kube_ami()
    print('\033[92mCurrent Running Windows AMIs in EKS Cluster: ' + str(list_of_amis), '\033[0m')

    source_image = get_latest_kube_ami(response_images['Images'])
    print("\033[92mLatest Version: ", source_image['ImageId'],  '\033[0m')
    count = 0
    old_ami = []
    instance_id= []
    for image in list_of_amis:
        if image == source_image['ImageId']:
            print('\033[92mLatest AMI is already running in EKS Cluster\033[0m')
        else:
            print('\033[91mLatest AMI is not running in EKS Cluster\033[0m' + '\n' + 'Please update the AMI: ' + source_image['ImageId'] + ' in EKS Cluster')
            count += 1
            old_ami.append(image)
            instance_id.append
    print('\033[92mCount: ' + str(count), '\033[0m')
    if count > 0:
        output_to_teams(source_image['ImageId'], old_ami)
    else:
        pass

def lambda_handler(event, context):
    main()

