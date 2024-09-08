import boto3
import uuid

def create_zone(name , private):
    client = boto3.client('route53')
    # Default to 'yaircli.com' if no name is provided
    if name == None:
        name = 'yaircli.com'
    # Create the hosted zone
    response = client.create_hosted_zone(
        Name= name,
        VPC={
            'VPCRegion': 'us-east-1',
            'VPCId': 'vpc-08c04cf2cf7964afd'
        },
        CallerReference=str(uuid.uuid4()), # Unique reference for the request
        HostedZoneConfig={
            'Comment': 'Created by cli',
            'PrivateZone': private
        }
    ) 
    # Extract the hosted zone ID from the response
    hosted_zone_id = response['HostedZone']['Id'].split('/')[-1]
    # Add a tag to the hosted zone
    tag_response = client.change_tags_for_resource(
        ResourceType='hostedzone',
        ResourceId=hosted_zone_id,
        AddTags=[
            {
                'Key': 'name',
                'Value': 'yaircli'
            }
        ]
    )


def get_hosted_zone_id():
    client = boto3.client('route53')
    zone_name= 'yaircli.com'
    # List all hosted zones
    response = client.list_hosted_zones()
    
    # Iterate through the hosted zones
    for zone in response['HostedZones']:
        if zone['Name'].rstrip('.') == zone_name:
            return zone['Id'].split('/')[-1]  # Extract the hosted zone ID from the ARN

def create_dns_record(record_name, record_type, record_values,function,ttl=300):
    client = boto3.client('route53')
    
    # Retrieve the hosted zone ID
    hosted_zone_id = get_hosted_zone_id()
    if not hosted_zone_id:
        print("Hosted zone not found.")
        return
    
    if isinstance(record_values, str):
        record_values = [value.strip() for value in record_values.split(',')]
    
    # Prepare the record set change request
    if function == 'create':
        change_batch = {
            'Changes': [
                {
                    'Action': 'CREATE',
                    'ResourceRecordSet': {
                        'Name': record_name,
                        'Type': record_type,
                        'TTL': ttl,
                        'ResourceRecords': [{'Value': value} for value in record_values],
                    }
                }
            ]
        }
    else:
        change_batch = {
            'Changes': [
                {
                    'Action': 'DELETE',
                    'ResourceRecordSet': {
                        'Name': record_name,
                        'Type': record_type,
                        'TTL': ttl,
                        'ResourceRecords': [{'Value': value} for value in record_values],
                    }
                }
            ]
        }
    
    # Create or delete the DNS record
    response = client.change_resource_record_sets(
        HostedZoneId=hosted_zone_id,
        ChangeBatch=change_batch
    )
    
    print("Record",function, "successful")
