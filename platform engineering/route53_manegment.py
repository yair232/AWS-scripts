import boto3
import uuid

def create_zone(name, private):
    client = boto3.client('route53')
    if name is None:
        name = 'yaircli.com'
    response = client.create_hosted_zone(
        Name=name,
        VPC={
            'VPCRegion': 'us-east-1',
            'VPCId': 'vpc-08c04cf2cf7964afd'
        },
        CallerReference=str(uuid.uuid4()),
        HostedZoneConfig={
            'Comment': 'Created by cli',
            'PrivateZone': private
        }
    )
    hosted_zone_id = response['HostedZone']['Id'].split('/')[-1]
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

def get_hosted_zone_id(zone_name):
    client = boto3.client('route53')
    response = client.list_hosted_zones()
    
    for zone in response['HostedZones']:
        if zone['Name'].rstrip('.') == zone_name:
            return zone['Id'].split('/')[-1]
    print(f"Error: Hosted zone '{zone_name}' not found.")
    return None

def create_dns_record(record_name, record_type, record_values, function, zone_name, ttl=300):
    client = boto3.client('route53')
    hosted_zone_id = get_hosted_zone_id(zone_name)
    if not hosted_zone_id:
        print("Hosted zone not found.")
        return

    if isinstance(record_values, str):
        record_values = [value.strip() for value in record_values.split(',')]

    # Ensure record_name has a trailing dot
    if not record_name.endswith('.'):
        record_name += '.'


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
    elif function == 'update':
        existing_record = get_existing_record(record_name, record_type, hosted_zone_id)
        if not existing_record:
            print(f"Error: Record with name '{record_name}' and type '{record_type}' not found in zone '{zone_name}'.")
            return
        
        if ttl is None:
            ttl = existing_record['TTL']
        record_values = record_values if record_values else [r['Value'] for r in existing_record['ResourceRecords']]
        
        change_batch = {
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': record_name,
                        'Type': record_type,
                        'TTL': ttl,
                        'ResourceRecords': [{'Value': value} for value in record_values],
                    }
                }
            ]
        }

    elif function == 'delete':
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
    
    try:
        response = client.change_resource_record_sets(
            HostedZoneId=hosted_zone_id,
            ChangeBatch=change_batch
        )
        print(f"Record {function} successful")
    
    except client.exceptions.InvalidChangeBatch as e:
        print(f"Failed to {function} record: {e}")

def get_existing_record(record_name, record_type, hosted_zone_id):
    client = boto3.client('route53')
    response = client.list_resource_record_sets(HostedZoneId=hosted_zone_id)
    
    for record in response['ResourceRecordSets']:
        if record['Name'] == record_name and record['Type'] == record_type:
            return record
    
    print(f"Error: Record with name '{record_name}' and type '{record_type}' not found.")
    return None
