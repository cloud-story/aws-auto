from aws.ec2.instance import ec2_insnstances_bp
from flask import Flask


app = Flask(__name__)

app.register_blueprint(ec2_insnstances_bp, url_prefix='/ec2')

app.run(debug=True, port=5001, host='0.0.0.0')

#run a simple instance
#ec2Intance.runSimpleInstance({})


#Create instance with role
#ec2Intance.runInstancesWithRole({});


#terminate instances 
#ec2Intance.terminateInstance(['i-0dd1fc31f592d6fd2']);