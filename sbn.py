#!/bin/env python

"""
SBN - Search AWS EC2 with various parameters
"""
import getopt
import sys
import boto3


class TextColors:
    """Change printed text color"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


INSTANCE = ''
REGIONS = ''
NAME = ''
try:
    OPTS, ARGS = getopt.getopt(sys.argv[1:], "hn:d:r:",
                               ["name=", "dns=", "region="])
except getopt.GetoptError as get_error:
    print(str(get_error))
    print("%s -n <name> -d <PrivateDnsName> -r <regions>" % sys.argv[0])
    sys.exit(2)

for OPT, ARG in OPTS:
    if OPT in ("-h", "--help"):
        print("%s -n <name> -d <PrivateDnsName> -r <regions>" % sys.argv[0])
        sys.exit()
    elif OPT in ("-n", "--name"):
        NAME = ARG
    elif OPT in ("-d", "--dns"):
        INSTANCE = ARG
    elif OPT in ("-r", "--region"):
        REGIONS = ARG

if REGIONS and INSTANCE:
    print("You cannot specify -d and -r at the same time.")
    sys.exit(2)

if REGIONS:
    REGION_LIST = REGIONS.split(',')
    for region in REGION_LIST:
        EC2 = boto3.client('ec2', region_name=region)
        fname = [{'Name': 'tag:Name', 'Values': [NAME]}]
        response = EC2.describe_instances(Filters=fname)
        for ec2instance in response['Reservations']:
            print(ec2instance['Instances'][0]['PrivateDnsName'])

elif INSTANCE:
    if 'ec2.internal' in INSTANCE:
        I_REGION = 'us-east-1'
    elif 'us-east-2' in INSTANCE:
        I_REGION = 'us-east-2'
    elif 'us-west-1' in INSTANCE:
        I_REGION = 'us-west-1'
    elif 'us-west-2' in INSTANCE:
        I_REGION = 'us-west-2'

    ec2 = boto3.client('ec2', region_name=I_REGION)
    filters = [{'Name': 'private-dns-name', 'Values': [INSTANCE]}]
    response = ec2.describe_instances(Filters=filters)
    print("{0}\n\t{1}".format(TextColors.HEADER
                              + 'Region:' + TextColors.ENDC, I_REGION))
    print("{0}\n\t{1}".format(TextColors.HEADER
                              + 'ImageId:'
                              + TextColors.ENDC,
                              response['Reservations'][0]['Instances']
                              [0]['ImageId']))
    print("{0}\n\t{1}".format(TextColors.HEADER
                              + 'InstanceId:'
                              + TextColors.ENDC,
                              response['Reservations'][0]['Instances']
                              [0]['InstanceId']))
    print("{0}\n\t{1}".format(TextColors.HEADER
                              + 'InstanceType:'
                              + TextColors.ENDC,
                              response['Reservations'][0]['Instances']
                              [0]['InstanceType']))
    print("{0}\n\t{1}".format(TextColors.HEADER
                              + 'State:'
                              + TextColors.ENDC,
                              response['Reservations'][0]['Instances']
                              [0]['State']['Name']))
    print("{0}\n\t{1}".format(TextColors.HEADER
                              + 'SubnetId:'
                              + TextColors.ENDC,
                              response['Reservations'][0]['Instances']
                              [0]['ImageId']))
    print("{0}\n\t{1}".format(TextColors.HEADER
                              + 'VpcId:'
                              + TextColors.ENDC,
                              response['Reservations'][0]['Instances']
                              [0]['VpcId']))
    print("{0}\n\t{1}".format(TextColors.HEADER
                              + 'IamInstanceProfile:'
                              + TextColors.ENDC,
                              response['Reservations'][0]['Instances']
                              [0]['IamInstanceProfile']['Arn']))
    print("{0}".format(TextColors.HEADER
                       + 'SecurityGroups:'
                       + TextColors.ENDC))
    for s_grp in response['Reservations'][0]['Instances'][0]['SecurityGroups']:
        print("\t{0}: {1}".format(TextColors.BOLD
                                  + s_grp['GroupId']
                                  + TextColors.ENDC, s_grp["GroupName"]))
    print("{0}".format(TextColors.HEADER + 'Tags:' + TextColors.ENDC))
    for tag in response['Reservations'][0]['Instances'][0]['Tags']:
        print("\t{0}: {1}".format(TextColors.BOLD
                                  + tag['Key']
                                  + TextColors.ENDC, tag['Value']))
