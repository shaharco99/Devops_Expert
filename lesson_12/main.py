import boto3
#
# client = boto3.client('ec2')
# response = client.describe_instances()
# print(response)
#
# for instance in response['Reservations'][0]['Instances']:
#     print(instance['InstanceId'])
#
# ec2 = boto3.resource('ec2')
# response = ec2.create_instances(
#     InstanceType='t2.micro',
#     ImageId='ami-0c4e4b4eb2e11d1d4',
#     MaxCount=1,
#     MinCount=1)

client = boto3.client('ec2')


def create_instance():
    ec2 = boto3.resource('ec2')
    ec2.create_instances(
        InstanceType='t2.micro',
        ImageId='ami-0c4e4b4eb2e11d1d4',
        MaxCount=1,
        MinCount=1)


def terminate_instances(instance_ids):
    client.terminate_instances(InstanceIds=instance_ids)


def get_instances_ids():
    ids = []
    response = client.describe_instances()

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            ids.append(instance['InstanceId'])
    return ids


ids = get_instances_ids()
# create_instance()
stop_instance(ids)