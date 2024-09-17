import boto3
from datetime import date
def make_instance(value , num, user_data):
# create a new EC2 client based on the configure.txt
    instances = []
    ec2 = boto3.resource('ec2')
    for i in range(num):
        response = ec2.create_instances(
            ImageId= value[2],
            InstanceType= value[0],
            MinCount=1,
            MaxCount=1,
            KeyName= value[1],
            SecurityGroupIds= [value[3]],
            SubnetId='subnet-0f035c2fcf9e885c7',
            TagSpecifications=[{'ResourceType': 'instance', 'Tags': [{'Key': 'Name','Value': 'yair-Wb'+str(i+1)},\
                                                                      {'Key': 'Date','Value': str(date.today())}]}],
            UserData= user_data

        )[0]
        #wait for the instance upload and print when finish
        response.wait_until_running()
        response.reload()
        print("Instance ID:", response.id)
        print("public IP:", response.public_ip_address)
        instances.append(response)
    
    return instances


 
#read the content of the file 
def read_file_content(path):
    file = open(path, 'r')
    content = file.read()
    file.close()

    return content
#convert the content to string
def convert_string_to_value(file):
    SEPERATES_BY_CHAR = ":"
    value = []
    lines = file.split('\n')
    for line in lines:
        none, made_in_year = line.split(SEPERATES_BY_CHAR)
        value.append(made_in_year)
    return value

def main():
    path=r"C:\Users\Yair\Desktop\nitzanim\python_final\confirgure.txt" 
    path_user_data = r"C:\Users\Yair\Desktop\nitzanim\python_final\user_data.sh"
    file = read_file_content(path)
    user_data = read_file_content(path_user_data)
    value = convert_string_to_value(file)
    num = int(input("how many instance u want to make"))
    make_instance(value, num, user_data)
    print("i made ", num, "instance secssfuly" )
main()