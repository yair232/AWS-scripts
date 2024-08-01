import boto3
from datetime import date, datetime

#check if the name start with yair
def get_instance_name_tag(instance):
    tags = instance.get('Tags', [])
    for tag in tags:
        if tag['Key'] == 'Name' and tag['Value'].startswith('yair'):
            return True
        
#return the date tag
def get_instance_date_tag(instance):
    tags = instance.get('Tags', []) 
    for tag in tags:
        if tag['Key'] == 'Date' :
            return tag['Value']




def main(): 
    client = boto3.client('ec2')
    resp = client.describe_instances()
    id_list = []
    for reservation in resp['Reservations']:
        for instance in reservation['Instances']:
            if get_instance_name_tag(instance) == True:
                instance_date= get_instance_date_tag(instance)
                date_object = datetime.strptime(instance_date, '%Y-%m-%d').date() #change the date from string to date format
            # if the instance up more than 7 days add it to the list
                if((date.today() - date_object).days > 7):
                    id_list.append(instance['InstanceId']) 
    #check if the list is empty
    if(len(id_list) != 0):
#terminate all the instance that in the list
        client.terminate_instances(InstanceIds=(id_list))
        print("i terminate the instance that 7 days and more old")
    else:#the list is empty:)
        print("no instance to terminate :)")
main()
