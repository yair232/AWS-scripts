import argparse
from ec2_manegment import *
from s3_manegment import *
from route53_manegment import *


def main():
    # Define required and optional arguments for the script
    parser = argparse.ArgumentParser(description='Manage AWS resources.')
    parser.add_argument('-r', '--resource', required=True, choices=['ec2', 's3', 'route53'],
                        help='Type of AWS resource to manage.')
    parser.add_argument('-a', '--action', required=True, choices=['create', 'manage', 'list'],
                        help='Action to perform on the specified resource.')
    parser.add_argument('-t', '--type', choices=['t2.nano', 't4g.nano','A', 'CNAME', 'MX', 'TXT'],
                        help='Type of EC2 instance (required for EC2 create action)/Type of DNS record.')
    parser.add_argument('-i', '--image', '--ami', choices=['ubuntu', 'amazon'],
                        help='Image for EC2 instance (required for EC2 create action).')
    parser.add_argument( '--status', choices=['start', 'stop'],
                        help='Specify whether to start or stop the EC2 instance.')
    parser.add_argument('--instance', help='which instance you whant to start or stop(id)/if you whant all type all.')
    parser.add_argument('--choice', choices=['public', 'private'],
                        help='choice between public and private access.')
    parser.add_argument('--file', '--upload', help='Path to the file you want to upload')
    parser.add_argument('--name', help='give a name for the file/dns record name')
    parser.add_argument('--values', help='Comma-separated values for the DNS record')
    parser.add_argument('--ttl', type=int, default=300, help='Time-to-live for the DNS record')
    parser.add_argument('--Function', '--function', choices=['create','delete','update'], help=('the --function is required for create or delete records'))
    parser.add_argument('--zone_name', help=('Specify the name of the DNS zone where you want to create or delete records'))
    args = parser.parse_args()
    # EC2 resource management
    if args.resource == 'ec2':
        if args.action == 'create':
            # Validate presence of all necessary parameters for EC2 instance creation
            if not args.type or not args.image:
                parser.error("--type and --image are required for creating EC2 instance")
            EC2(args.type, args.image)
        elif args.action == 'manage':
            # Ensure all necessary parameters for managing EC2 instances are provided
            if not args.status or not args.instance:
                parser.error("--status and --instance are requierd for the manage EC2 instance")
            if args.status == 'stop':
                stop_ec2_instance(args.instance)
            elif args.status == 'start':
                start_ec2_instance(args.instance)
        elif args.action == 'list':
            # List all EC2 instances
            list_id = list_my_ec2()
            print(list_id)

# S3 resource management
    if args.resource == 's3':
        if args.action == 'create':
            if not args.choice:
                # Validate presence of all necessary parameters for s3 bucket creation
                parser.error("--choice is required for creating s3 bucket")
            if args.choice == 'public':
            # Confirm with the user before creating a public S3 bucket
                sure = input("are you sure?") 
                if sure == 'yes':
                    create_s3(sure)
            else:
                create_s3(sure='no')
        elif args.action == 'manage':
        # Validate presence of file path and name for managing S3
            if args.file == '' or not args.name:
                parser.error("The --file argument cannot be an empty string and --name are required.")
            upload(args.file,args.name)
        elif args.action == 'list':
            # List all S3 buckets
            s3_list = list_my_s3()
            if not s3_list:
                print("Their is no list that asosiaet for you")
            else:
                print(s3_list)
# Route53 resource management
    if args.resource == 'route53':
        if args.action == 'create':
            # Validate presence of choice parameter for creating Route53 zone
            if not args.choice:
                parser.error("--choice is required for creating route53")
            if args.choice == 'public':
                create_zone(args.name,private=False,)
            else:
                create_zone(args.name,private=True)
            # Ensure all necessary parameters for managing Route53 records are provided
        if args.action == 'manage':
            if args.Function == 'update' or args.Function == 'delete':
                if (not args.name) and (not args.zone_name):
                    parser.error("the --name and --zone_name are required for update the record")
                if  (not args.values) and (not args.ttl):
                    parser.error(" --values or --ttl are required to update")
                create_dns_record(args.name,args.type,args.values,args.Function,args.zone_name,args.ttl)
                    
            else:
                if (not args.name) or (not args.type) or (not args.values) or (not args.ttl) or (not args.Function) or (not args.zone_name):
                    parser.error("The --name --type --values --ttl --zone_name cannot be empty while create/delete record.")
                create_dns_record(args.name,args.type,args.values,args.Function,args.zone_name,args.ttl)
        if args.action == 'list':
            zone_list = list_hosted_zones_with_comment()
            print(zone_list)
            

main()