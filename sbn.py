#!/bin/env python

import boto3
import sys, getopt
import pprint

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

instance = ''
regions = ''
name = ''
try:
    opts, args = getopt.getopt(sys.argv[1:],"hn:d:r:",["name=","dns=","region="])
except getopt.GetoptError as e:
    print(str(e))
    print("%s -n <name tag> -d <instance dns> -r <region>" % sys.argv[0])
    sys.exit(2)

for opt, arg in opts:
    if opt in ("-h", "--help"):
        print("%s -n <name tag> -d <instance dns> -r <regions comma seperated no spaces>" % sys.argv[0])
        sys.exit()
    elif opt in ("-n", "--name"):
        name = arg
    elif opt in ("-d", "--dns"):
        instance = arg
    elif opt in ("-r", "--region"):
        regions = arg

if regions and instance:
    print("You cannot specify -d and -r at the same time.")
    sys.exit(2)

if regions:
    regionlist = regions.split(',')
    for region in regionlist:
        ec2 = boto3.client('ec2',region_name=region)
        fname = [{'Name':'tag:Name', 'Values':[name]}]
        response = ec2.describe_instances(Filters=fname)
        for ec2instance in response['Reservations']:
            print(ec2instance['Instances'][0]['PrivateDnsName'])

elif instance:
    if 'ec2.internal' in instance:
        iregion = 'us-east-1'
    elif 'us-east-2' in instance:
        iregion = 'us-east-2'
    elif 'us-west-1' in instance:
        iregion = 'us-west-1'
    elif 'us-west-2' in instance:
        iregion = 'us-west-2'

    ec2 = boto3.client('ec2',region_name=iregion)
    filters = [{'Name':'private-dns-name', 'Values':[instance]}]
    response = ec2.describe_instances(Filters=filters)
    print("{0}\n\t{1}".format(bcolors.HEADER + 'Region:' + bcolors.ENDC, iregion))
    print("{0}\n\t{1}".format(bcolors.HEADER + 'ImageId:' + bcolors.ENDC, response['Reservations'][0]['Instances'][0]['ImageId']))
    print("{0}\n\t{1}".format(bcolors.HEADER + 'InstanceId:' + bcolors.ENDC, response['Reservations'][0]['Instances'][0]['InstanceId']))
    print("{0}\n\t{1}".format(bcolors.HEADER + 'InstanceType:' + bcolors.ENDC, response['Reservations'][0]['Instances'][0]['InstanceType']))
    print("{0}\n\t{1}".format(bcolors.HEADER + 'State:' + bcolors.ENDC, response['Reservations'][0]['Instances'][0]['State']['Name']))
    print("{0}\n\t{1}".format(bcolors.HEADER + 'SubnetId:' + bcolors.ENDC, response['Reservations'][0]['Instances'][0]['ImageId']))
    print("{0}\n\t{1}".format(bcolors.HEADER + 'VpcId:' + bcolors.ENDC, response['Reservations'][0]['Instances'][0]['VpcId']))
    print("{0}\n\t{1}".format(bcolors.HEADER + 'IamInstanceProfile:' + bcolors.ENDC, response['Reservations'][0]['Instances'][0]['IamInstanceProfile']['Arn']))
    print("{0}".format(bcolors.HEADER + 'SecurityGroups:' + bcolors.ENDC))
    for secgroup in response['Reservations'][0]['Instances'][0]['SecurityGroups']:
        print("\t{0}: {1}".format(bcolors.BOLD + secgroup['GroupId'] + bcolors.ENDC, secgroup["GroupName"]))
    print("{0}".format(bcolors.HEADER + 'Tags:' + bcolors.ENDC))
    for tag in response['Reservations'][0]['Instances'][0]['Tags']:
        print("\t{0}: {1}".format(bcolors.BOLD + tag['Key'] + bcolors.ENDC, tag['Value']))
