import boto3

client = boto3.client('ec2')


def runSimpleInstance(instanceProperties):
    #aws ec2 run-instances --image-id ami-0915bcb5fa77e4892 --count 1 --instance-type t2.micro --key-name ec-new-2021 --security-group-ids sg-0af1fa8b64bdfdb5b \
    # --subnet-id subnet-663b5a48
    response = client.run_instances(
        ImageId=instanceProperties.get('imageId','ami-0915bcb5fa77e4892'),
        InstanceType= instanceProperties.get('instanceType','t2.micro'),
        InstanceInitiatedShutdownBehavior='stop',
        SecurityGroupIds=[
            'sg-0af1fa8b64bdfdb5b',
        ],
        KeyName=instanceProperties.get('keyName','ec-new-2021'),
        SubnetId = instanceProperties.get('subnetId','subnet-663b5a48'),
        MaxCount=1,
        MinCount=1
    )
    print(response)

def terminateInstance(instanceIds):
    #aws ec2 terminate-instances --instance-ids i-0da7b1b2a4a7a8d51
    if not instanceIds:
        return "Please provide instance id's to be terminated"
    response = client.terminate_instances(
        InstanceIds=instanceIds
    )

    print(response);
