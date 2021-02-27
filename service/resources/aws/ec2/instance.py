import boto3
import service.resources.aws.iam.roles as iamrole
import time 
from flask import Blueprint, request, json, Response
from flask import json, jsonify, make_response, request
from flask_restplus import Namespace, Resource
from service.utils.aws_logger import AWSLogger
from service.utils.date_util import  DateUtil
from service.utils.exceptions import BadRequestException, MissingRequestBodyException
from service.utils.constants import GENERIC_ERROR_RESPONSE_TEMPLATE
import copy


client = boto3.client('ec2')
ns = Namespace("Enrollment")
logger = AWSLogger(__name__)

@ns.route("/instance/create/simple")
class SimpleInstance(Resource):

    @ns.doc(id="post", description="Create simple ec2 t2.micro instance")
    @ns.response(200, "Successfull")
    @ns.response(400, "Bad Request")
    @ns.response(401, "Unauthorized")
    @ns.response(500, "Internal Server Error")
    def post(self):
        #TODO read from Requests
        instanceProperties={};
        """
        aws ec2 run-instances --image-id ami-0915bcb5fa77e4892 --count 1 --instance-type t2.micro --key-name ec-new-2021 --security-group-ids sg-0af1fa8b64bdfdb5b \
        --subnet-id subnet-663b5a48
        """

        response = None
        start_time = DateUtil.current_milli_time()
        logger.log_info("Start of Create Simple Instance API.")
        try:
            run_instance_res = client.run_instances(
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

            response = make_response(jsonify(run_instance_res), 200)
        except BadRequestException as e:
            raise e
        except Exception as e:
            # Internal server error
            logger.log_error("Internal server error while getting the active courses. Error: {}".format(str(e)))
            response = copy.deepcopy(GENERIC_ERROR_RESPONSE_TEMPLATE)
            response["status"]["code"] = 500
            response["status"]["message"] = str(e)
            response = make_response(jsonify(response), 500)

        response.headers["Content-Type"] = "application/json"
        logger.log_info("Completed get active courses API.", start_time=start_time)
        return response


@ns.route("/instance/create/simple/<string:instanceIds>")
class TerminateInstance(Resource):

    @ns.doc(id="delete", description="Terminate an Instance")
    @ns.response(200, "Successfull")
    @ns.response(400, "Bad Request")
    @ns.response(401, "Unauthorized")
    @ns.response(500, "Internal Server Error")
    def delete(self,instanceIds):    
        #aws ec2 terminate-instances --instance-ids i-0da7b1b2a4a7a8d51

        response = None
        start_time = DateUtil.current_milli_time()
        logger.log_info("Start of Terminate Instance API.")
        try:
            if not instanceIds:
                return "Please provide instance id's to be terminated"
            terminate_instance_res = client.terminate_instances(
                InstanceIds=instanceIds
            )

            response = make_response(jsonify(terminate_instance_res), 200)
        except BadRequestException as e:
            raise e
        except Exception as e:
            # Internal server error
            logger.log_error("Internal server error while getting the active courses. Error: {}".format(str(e)))
            response = copy.deepcopy(GENERIC_ERROR_RESPONSE_TEMPLATE)
            response["status"]["code"] = 500
            response["status"]["message"] = str(e)
            response = make_response(jsonify(response), 500)

        response.headers["Content-Type"] = "application/json"
        logger.log_info("Completed get active courses API.", start_time=start_time)
        return response

@ns.route("/instance/create/withrole")
class InstanceWithRole(Resource):

    @ns.doc(id="post", description="Create an Instance with Role")
    @ns.response(200, "Successfull")
    @ns.response(400, "Bad Request")
    @ns.response(401, "Unauthorized")
    @ns.response(500, "Internal Server Error")
    def delete(self):  
    
        """ 
        aws ec2 run-instances --image-id ami-0915bcb5fa77e4892 --count 2 --instance-type t2.micro --key-name ec-new-2021 --security-group-ids sg-0af1fa8b64bdfdb5b \
        subnet-id subnet-663b5a48 --iam-instance-profile arn:aws:iam::764319766871:role/AMZ_EC2_Role_FOR_SSM \
        --tag-specifications 'ResourceType=instance,Tags=[{Key=env,Value=dev}]'
        """

        #TODO read from Requests
        instanceProperties={};
        start_time = DateUtil.current_milli_time()
        logger.log_info("Start of Create Instance with Role API.")
        try:
            #Create Role
            print("Creating role:")
            roleName="EC2_SSM_"+str(round(time.time() * 1000))
            #roleName = 'EC2_SSM_1614362392395'
            iamrole.createRole(roleName,['arn:aws:iam::aws:policy/service-role/AmazonEC2RoleforSSM'])

            #wait 30 sec
            print("Waiting 30 Sec-----")
            time.sleep(30)

            print("Creating EC2 Instances")
            instance_with_role_res = client.run_instances(
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

            response = make_response(jsonify(instance_with_role_res), 200)
        except BadRequestException as e:
            raise e
        except Exception as e:
            # Internal server error
            logger.log_error("Internal server error while getting the active courses. Error: {}".format(str(e)))
            response = copy.deepcopy(GENERIC_ERROR_RESPONSE_TEMPLATE)
            response["status"]["code"] = 500
            response["status"]["message"] = str(e)
            response = make_response(jsonify(response), 500)

        response.headers["Content-Type"] = "application/json"
        logger.log_info("Completed get active courses API.", start_time=start_time)
        return response