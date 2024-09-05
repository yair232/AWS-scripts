import argparse
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

def stop_ec2_instance():
    client = boto3.client('ec2')
    id_list = list_my_ec2()
    instance_ids = list(id_list.keys())
    if(len(instance_ids) != 0):
        client.stop_instances(InstanceIds=(instance_ids))
        print("I stop the instance that you create")
    else:
        print("no instance to stop")




def list_my_ec2():
    client = boto3.client('ec2')
    resp = client.describe_instances()
    id_list = {}
    for reservation in resp['Reservations']:
        for instance in reservation['Instances']:
            if get_instance_name_tag(instance) == True:
                id_list[instance['InstanceId']] = instance['State']['Name']  

    return id_list

def start_ec2_instance():
    client = boto3.client('ec2')
    id_list = list_my_ec2()
    instance_ids = list(id_list.keys())
    if(len(instance_ids) != 0):
        client.start_instances(InstanceIds=(instance_ids))
        print("I start the instance that you create")
    else:
        print("no instance to start")


def main():
    parser = argparse.ArgumentParser(description='Manage AWS resources.')
    parser.add_argument('-r', '--resource', required=True, choices=['ec2', 's3', 'route53'],
                        help='Type of AWS resource to manage.')
    parser.add_argument('-a', '--action', required=True, choices=['create', 'manage', 'list'],
                        help='Action to perform on the specified resource.')
    parser.add_argument('-t', '--type', choices=['t2.nano', 't4g.nano'],
                        help='Type of EC2 instance (required for EC2 create action).')
    parser.add_argument('-i', '--image', '--ami', choices=['ubuntu', 'amazon'],
                        help='Image for EC2 instance (required for EC2 create action).')
    parser.add_argument( '--status', choices=['start', 'stop'],
                        help='Specify whether to start or stop the EC2 instance.')
    args = parser.parse_args()
    if args.resource == 'ec2':
        if args.action == 'create':
            if not args.type or not args.image:
                parser.error("--type and --image are required for creating EC2 instance")
            EC2(args.type, args.image)
        elif args.action == 'manage':
            if not args.status:
                parser.error("--status are requierd for the manage EC2 instance")
            if args.status == 'stop':
                stop_ec2_instance()
            elif args.status == 'start':
                start_ec2_instance()
        else:
            list_id = list_my_ec2()
            print(list_id)
            


main()