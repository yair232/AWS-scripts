from flask import Flask, request, jsonify
import subprocess
import sys
from platform_engineering import *

app = Flask(__name__)
@app.route('/ec2', methods=['POST'])

def ec2(): # Handles POST requests for EC2 actions.

    response = action_ec2(request) ## Process EC2 action
    if isinstance(response, list):
        return response[0], response[1] # Return response with status code
    return response


@app.route('/s3', methods=['POST'])

def s3(): # Handles POST requests for S3 actions.

    response = action_s3(request) # Process S3 action
    if isinstance(response, list):
        return response[0], response[1] # Return response with status code
    return response


@app.route('/route53', methods=['POST']) 

def route53(): # Handles POST requests for Route 53 actions.

    response = action_route53(request) # Process Route 53 action
    if isinstance(response,list):
        return response[0], response[1] # Return response with status code
    return response


if __name__ == '__main__':
    app.run(port=2310,host="127.0.0.1",debug=True)