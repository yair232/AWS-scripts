import boto3
import json
def create_s3(sure): # Creates an S3 bucket named 'yaircli' and sets its policy
    s3 = boto3.client('s3', 'us-east-1')
    bucket_name='yaircli'
    s3.create_bucket(Bucket=bucket_name) # Create the bucket
    if sure == 'yes':
        # Define and apply public read policy
        bucket_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "PublicReadGetObject",
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": f"arn:aws:s3:::{bucket_name}/*"
            }
        ]
    }
        bucket_policy_json = json.dumps(bucket_policy)
        s3 = boto3.client('s3')
        s3.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy_json)
    print("S3 bucket created successfully")
    return("S3 bucket created successfully")


    
def list_my_s3(bucket_name='yaircli'): # Lists the 'yaircli' bucket if it exists.
    s3 = boto3.client('s3', 'us-east-1')
    response = s3.list_buckets()
    bucket_list = []
    for bucket in response['Buckets']:
        if bucket['Name'] == bucket_name:
            bucket_list.append(bucket['Name'])
    
    if(len(bucket_list) != 0):
        return bucket_list
    print("there is no bucket to list")
    return "there is no bucket to list"


def upload(file,object_name): #  Uploads a file to the 'yaircli' bucket.
    s3 = boto3.client('s3', 'us-east-1')
    bucket_name = 'yaircli'
    try:
        s3.upload_file(file, bucket_name, object_name)
        print(f"File '{file}' uploaded to '{bucket_name}/{object_name}'")
        return (f"File '{file}' uploaded to '{bucket_name}/{object_name}'")
    except Exception as e:
        print(f"Error uploading file: {e}")
        return f"Error uploading file: {e}",400
