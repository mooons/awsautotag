#!/usr/bin/env python

"""
Auto Tagging utility for AWS
Coded by moomons

Use with caution
"""

import boto3
import time

# Credentials
aws_access_key_id = "XXXXXXXXXXXXXXXXXXXX"
aws_secret_access_key = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# Interval between two checks
interval = 10

# So far this script can only check and tag 'Project' key
ProjectTag = [{'Key': 'Project', 'Value': '619:Phase3'}]

# Prompt
print('Will tag all EC2 instances / spot instances with the tag below, press any key to continue:')
print(ProjectTag)

# Wait for user input
raw_input()

"""
# You can remove the region_name, aws_access_key_id and aws_secret_access_key just like below
# to use default credential configured using "aws configure" (Recommended)

ec2 = boto3.resource('ec2')
client_ec2 = boto3.client('ec2')
"""

ec2 = boto3.resource(
    'ec2',
    region_name="us-east-1",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

client_ec2 = boto3.client(
    'ec2',
    region_name="us-east-1",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)


# Main loop to check and tag

while True:

    print('Checking ...')

    for i in ec2.instances.all():
        needtagging = 1

        if i.tags is not None:
            for tags in i.tags:
                if tags['Key'] == 'Project':
                    # print 'Tag Project detected: ' + i.id
                    if tags['Value'] == ProjectTag[0]['Value']:
                        print '[ OK ] EC2 tagged: ' + i.id
                        needtagging = 0
                    else:
                        print '[ WARNING ] EC2 With WRONG TAG: ' + i.id

                        exit(0)
                    break

        if needtagging == 1:
            print '[ NO TAG ] Tagging EC2: ' + i.id
            ec2.create_tags(Resources=[i.id], Tags=ProjectTag)

    tags = client_ec2.describe_tags()['Tags']

    for i in client_ec2.describe_spot_instance_requests()['SpotInstanceRequests']:
        # print i['SpotInstanceRequestId']
        needtagging = 1
        for tag in tags:
            if i['SpotInstanceRequestId'] == tag['ResourceId']:
                if tag['Key'] == 'Project':
                    if tag['Value'] == ProjectTag[0]['Value']:
                        needtagging = 0
                        print '[ OK ] Spot tagged: ' + i['SpotInstanceRequestId']
                    else:
                        print '[ WARNING ] Spot with WRONG TAG: ' + i['SpotInstanceRequestId'] + ' ' + tag['Value']
                    break
        if needtagging == 1:
            print '[ NO TAG ] Tagging Spot: ' + i['SpotInstanceRequestId']
            ec2.create_tags(Resources=[i['SpotInstanceRequestId']], Tags=ProjectTag)

    time.sleep(interval)


