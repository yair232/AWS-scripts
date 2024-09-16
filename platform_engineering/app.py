from flask import Flask, request, jsonify
import subprocess
import sys
from platform_engineering import *

app = Flask(__name__)
@app.route('/ec2', methods=['POST'])
def ec2():
    response = action_ec2(request)
    if isinstance(response, list):
        return response[0], response[1]
    return response

@app.route('/s3', methods=['POST'])
def s3():
    response = action_s3(request)
    if isinstance(response, list):
        return response[0], response[1]
    return response

@app.route('/route53', methods=['POST'])
def route53():
    response = action_route53(request)
    if isinstance(response,list):
        return response[0], response[1]
    return response


if __name__ == '__main__':
    app.run(port=2310,host="127.0.0.1",debug=True)