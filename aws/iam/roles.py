import boto3
import json

iamr = boto3.resource('iam')
iamc = boto3.client('iam')



def createRole(name,policy_arns):
    #aws iam attach-role-policy --role-name Test-UserAccess-Role --policy-arn arn:aws:iam::123456789012:role/PolicyForRole4

    #https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html#ec2-instance-profile

    assume_role_policy_document = json.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
            "Effect": "Allow",
            "Principal": {
                "Service": "ec2.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
            }
        ]
    })

    role = iamr.create_role( Path= "/",
                            RoleName=name,
                            AssumeRolePolicyDocument = assume_role_policy_document,
                            MaxSessionDuration=43200,
                            )
    for policy_arn in policy_arns:
        #create role
        response = role.attach_policy(
            PolicyArn=policy_+"_instance_pofile"arn,
        )

        #create instance profile
        responsecip =iamc.create_instance_profile(InstanceProfileName=name+"_instance_pofile",
                                    Path="/");

        #print(responsecip)

        #add role to instance profile
        responseatrc = iamc.add_role_to_instance_profile(
            InstanceProfileName=name,
            RoleName=name)
        #print(responseatrc)

