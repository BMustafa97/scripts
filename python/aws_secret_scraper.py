import boto3
import logging
import re

# set up logging
logging.basicConfig(filename='scrape_aws_secrets.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# set up the region
region = 'eu-west-2'
# set up the string to search for
string = 'your_string_here'

# function which updates the secret value for a given secret name
def update_secret_value(secret_name, string):
    # set up the boto3 client
    client = boto3.client('secretsmanager', region_name=region)
    # get the secret value
    response = client.get_secret_value(SecretId=secret_name)
    # get the secret value
    secret_value = response['SecretString']
    new_secret_value = re.sub(string, '', secret_value)

    ######################################################################################
    # UNCOMMENT THE BELOW TO UPDATE THE SECRET VALUE, BE CAREFUL!
    # CHECK THE LOG FILE TO ENSURE THE CORRECT SECRETS ARE BEING UPDATED!
    # response = client.update_secret(SecretId=secret_name, SecretString=new_secret_value)
    # print("Secret value updated successfully.")
    # logging.info("Secret value updated successfully.")
    ######################################################################################


# function which lists all the secrets in a given region
def list_secrets(region):
    # set up the boto3 client
    client = boto3.client('secretsmanager', region_name=region)
    # get the list of secrets
    response = client.list_secrets(
        MaxResults=100,
    )
    # get the list of secret names
    secret_list = response['SecretList']
    # return the list of secret names
    return secret_list

# function which gets the secret value for a given secret name
def get_secret_value(region, secret_name):
    # set up the boto3 client
    client = boto3.client('secretsmanager', region_name=region)
    # get the secret value
    response = client.get_secret_value(SecretId=secret_name)
    # get the secret value
    secret_value = response['SecretString']
    # return the secret value
    return secret_value

# function which searches for a given string in a given secret value with string being 'encypt=false'
def search_for_string(secret_value, string):
    # if the string is in the secret value
    if string in secret_value:
        return True
    else:
        return False
    
# call the functions
try:
    list_secrets=list_secrets(region)
    for secret in list_secrets:
        # print (secret['Name'])
        secret_name = secret['Name']
        secret_value = get_secret_value(region, secret_name)
        # print(secret_value)
        if search_for_string(secret_value, string):
            print("Secret Name: " + secret_name)
            logging.info("Secret Name: " + secret_name)
            # call a function to update the secret value with the new string value
            update_secret_value(secret_name, string)
        else:
            pass
except:
    print("Error getting secret value.")
    logging.info("Error getting secret value.")
    pass
