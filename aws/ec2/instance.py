import boto3
import aws.iam.roles as iamrole
import time 

client = boto3.client('ec2')


def runSimpleInstance(instanceProperties):
    """
        aws ec2 run-instances --image-id ami-0915bcb5fa77e4892 --count 1 --instance-type t2.micro --key-name ec-new-2021 --security-group-ids sg-0af1fa8b64bdfdb5b \
    --subnet-id subnet-663b5a48
    """
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
        MinCount=1,
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


def runInstancesWithRole(instanceProperties):
    """ 
    aws ec2 run-instances --image-id ami-0915bcb5fa77e4892 --count 2 --instance-type t2.micro --key-name ec-new-2021 --security-group-ids sg-0af1fa8b64bdfdb5b \
    subnet-id subnet-663b5a48 --iam-instance-profile arn:aws:iam::764319766871:role/AMZ_EC2_Role_FOR_SSM \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=env,Value=dev}]'
    """

    #Create Role
    print("Creating role:")
    roleName="EC2_SSM_"+str(round(time.time() * 1000))
    #roleName = 'EC2_SSM_1614362392395'
    iamrole.createRole(roleName,['arn:aws:iam::aws:policy/service-role/AmazonEC2RoleforSSM'])

    #wait 30 sec
    print("Waiting 30 Sec-----")
    time.sleep(30)

    print("Creating EC2 Instances")
    response = client.run_instances(
        ImageId=instanceProperties.get('imageId','ami-0915bcb5fa77e4892'),
        InstanceType= instanceProperties.get('instanceType','t2.micro'),
        InstanceInitiatedShutdownBehavior='stop',
        SecurityGroupIds=[
            'sg-0af1fa8b64bdfdb5b',
        ],
        KeyName=instanceProperties.get('keyName','ec-new-2021'),
        SubnetId = instanceProperties.get('subnetId','subnet-663b5a48'),
        MaxCount=3,
        MinCount=3,
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Env',
                        'Value': 'Dev'
                    },
                ]
            },
        ],
        IamInstanceProfile={
            'Name': roleName+"_instance_pofile"
        }
    )
    print(response)