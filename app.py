import aws.ec2.instance as ec2Intance

#run a simple instance
#ec2Intance.runSimpleInstance({})


#Create instance with role
ec2Intance.runInstancesWithRole({});


#terminate instances 
#ec2Intance.terminateInstance(['i-0dd1fc31f592d6fd2']);