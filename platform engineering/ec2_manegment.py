import boto3
def EC2(type, ami):
    if ami == 'amazon':
        ami = 'ami-0182f373e66f89c85'
    else:
        ami = 'ami-0e86e20dae9224db8'
    instances = []
    ec2 = boto3.resource('ec2')
    response = ec2.create_instances(
        ImageId= ami,
        InstanceType= type,
        MinCount=1,
        MaxCount=1,
        KeyName= "yairg",
        SecurityGroupIds= ['sg-0cb8272bc259f528d'],
        SubnetId='subnet-05aef944f475b371d',
        TagSpecifications=[{'ResourceType': 'instance', 'Tags': [{'Key': 'Name','Value': 'yair-CLI'}]}],
    )[0]
    #wait for the instance upload and print when finish
    response.wait_until_running()
    response.reload()
    print("Instance ID:", response.id)
    instances.append(response)
    
    return instances
#check if the name start with yair
def get_instance_name_tag(instance):
    tags = instance.get('Tags', [])
    for tag in tags:
        if tag['Key'] == 'Name' and tag['Value'].startswith('yair-CLI'):
            return True

def stop_ec2_instance(all):
    client = boto3.client('ec2')
    id_list = list_my_ec2()
    if all == 'all':
        instance_ids = list(id_list.keys())
        if(len(instance_ids) != 0):
            client.stop_instances(InstanceIds=(instance_ids))
            print("I stop the instance that you create")
        else:
            print("no instance to stop")
    else:
        if all not in id_list:
            print("eror the id of the instance is not yours")
        else:
            client.stop_instances(InstanceIds=(all))
            print("I stop the instance", all)

def list_my_ec2():
    client = boto3.client('ec2')
    resp = client.describe_instances()
    id_list = {}
    for reservation in resp['Reservations']:
        for instance in reservation['Instances']:
            if get_instance_name_tag(instance) == True:
                id_list[instance['InstanceId']] = instance['State']['Name']  

    return id_list

def start_ec2_instance(all):
    client = boto3.client('ec2')
    id_list = list_my_ec2()
    if all == 'all':
        instance_ids = list(id_list.keys())
        if(len(instance_ids) != 0):
            client.start_instances(InstanceIds=(instance_ids))
            print("I start the instance that you create")
        else:
            print("no instance to start")
    else:
        if all not in id_list:
            print("eror the id of the instance is not yours")
        else:
            client.start_instances(InstanceIds=(all))
            print("I start the instance", all)


def get_instance_name_tag(instance):
    tags = instance.get('Tags', [])
    for tag in tags:
        if tag['Key'] == 'Name' and tag['Value'].startswith('yair-CLI'):
            return True