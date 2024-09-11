import boto3
import uuid

def create_zone(name, private):
    client = boto3.client('route53')
    if name is None:
        name = 'yaircli.com'  # Default to 'yaircli.com'
    response = client.create_hosted_zone(
        Name=name,
        VPC={
            'VPCRegion': 'us-east-1',
            'VPCId': 'vpc-08c04cf2cf7964afd'
        },
        CallerReference=str(uuid.uuid4()),
        HostedZoneConfig={
            'Comment': 'Created by yair CLI',
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
                        'Type': record_type,  # Use provided type
                        'TTL': ttl,
                        'ResourceRecords': [{'Value': value} for value in record_values],
                    }
                }
            ]
        }

    elif function == 'update':
        # Fetch the record list and update based on matching name
        record_list = client.list_resource_record_sets(HostedZoneId=hosted_zone_id)
        for record_set in record_list['ResourceRecordSets']:
            if record_name == record_set['Name']:
                # Use existing values for type, ttl, and values if not provided
                if record_type is None:
                    record_type = record_set['Type']
                if ttl is None:
                    ttl = record_set.get('TTL', 'No TTL')
                if not record_values:
                    record_values = [record['Value'] for record in record_set.get('ResourceRecords', [])]

                change_batch = {
                    'Changes': [
                        {
                            'Action': 'UPSERT',
                            'ResourceRecordSet': {
                                'Name': record_name,
                                'Type': record_type,
                                'TTL': ttl,
                                'ResourceRecords': [{'Value': value} for value in record_values]
                            }
                        }
                    ]
                }
                break
        else:
            print(f"Error: Record with name '{record_name}' not found in zone '{zone_name}'.")
            return

    elif function == 'delete':
        # Fetch the record list and delete based on matching name
        record_list = client.list_resource_record_sets(HostedZoneId=hosted_zone_id)
        for record_set in record_list['ResourceRecordSets']:
            if record_name == record_set['Name']:
                change_batch = {
                    'Changes': [
                        {
                            'Action': 'DELETE',
                            'ResourceRecordSet': {
                                'Name': record_set['Name'],
                                'Type': record_set['Type'],
                                'TTL': record_set.get('TTL'),
                                'ResourceRecords': record_set.get('ResourceRecords', [])
                            }
                        }
                    ]
                }
                break
        else:
            print(f"Error: Record with name '{record_name}' not found in zone '{zone_name}'.")
            return
    
    try:
        response = client.change_resource_record_sets(
            HostedZoneId=hosted_zone_id,
            ChangeBatch=change_batch
        )
        print(f"Record {function} successful")
    
    except client.exceptions.InvalidChangeBatch as e:
        print(f"Failed to {function} record: {e}")

def get_existing_record_by_name(record_name, hosted_zone_id):
    client = boto3.client('route53')
    response = client.list_resource_record_sets(HostedZoneId=hosted_zone_id)
    
    for record in response['ResourceRecordSets']:
        if record['Name'] == record_name:
            return record
    
    print(f"Error: Record with name '{record_name}' not found.")
    return None

def list_hosted_zones_with_comment():
    target_key = 'name'
    target_value = 'yaircli'
    client = boto3.client('route53')

    # List all hosted zones
    response = client.list_hosted_zones()
    tagged_zones = []

    for zone in response['HostedZones']:
        hosted_zone_id = zone['Id'].split('/')[-1]

        # Retrieve tags for each hosted zone
        try:
            tags_response = client.list_tags_for_resource(
                ResourceType='hostedzone',
                ResourceId=hosted_zone_id
            )
            
            # Check for the specific tag
            resource_tags = tags_response.get('ResourceTagSet', {}).get('Tags', [])
            for tag in resource_tags:
                if tag['Key'] == target_key and tag['Value'] == target_value:
                    tagged_zones.append({
                        'Name': zone['Name'],
                        'Id': hosted_zone_id,
                        'Tag': tag['Value']
                    })
                    break

        except client.exceptions.ClientError as e:
            print(f"Error fetching tags for hosted zone {hosted_zone_id}: {e}")

    return tagged_zones