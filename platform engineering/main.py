import argparse
from ec2_manegment import *
from s3_manegment import *
from route53_manegment import *

def main():
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
    parser.add_argument('--Function', '--function', choices=['create','delete'], help=('the --function is required for create or delete records'))
    args = parser.parse_args()
    if args.resource == 'ec2':
        if args.action == 'create':
            if not args.type or not args.image:
                parser.error("--type and --image are required for creating EC2 instance")
            EC2(args.type, args.image)
        elif args.action == 'manage':
            if not args.status or not args.instance:
                parser.error("--status and --instance are requierd for the manage EC2 instance")
            if args.status == 'stop':
                stop_ec2_instance(args.instance)
            elif args.status == 'start':
                start_ec2_instance(args.instance)
        elif args.action == 'list':
            list_id = list_my_ec2()
            print(list_id)


    if args.resource == 's3':
        if args.action == 'create':
            if not args.choice:
                parser.error("--choice is required for creating s3 bucket")
            if args.choice == 'public':
                sure = input("are you sure?")
                if sure == 'yes':
                    create_s3(sure)
            else:
                create_s3(sure='no')
        elif args.action == 'manage':
            if args.file == '' or not args.name:
                parser.error("The --file argument cannot be an empty string and --name are required.")
            upload(args.file,args.name)
        elif args.action == 'list':
            s3_list = list_my_s3()
            if not s3_list:
                print("Their is no list that asosiaet for you")
            else:
                print(s3_list)

    if args.resource == 'route53':
        if args.action == 'create':
            if not args.choice:
                parser.error("--choice is required for creating route53")
            if args.choice == 'public':
                create_zone(args.name,private=False,)
            else:
                create_zone(private=True)
        if args.action == 'manage':
            if (not args.name) or (not args.type) or (not args.values) or (not args.ttl) or (not args.Function):
                parser.error("The --name --type --values --ttl cannot be empty while create record.")
            create_dns_record(args.name,args.type,args.values,args.ttl,args.function)

main()