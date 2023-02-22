import boto3
import paramiko

# Set up boto3 client for EC2 and S3
ec2 = boto3.client('ec2')
s3 = boto3.client('s3')

# Create VPC and subnet for EC2 instance
vpc = ec2.create_vpc(CidrBlock='10.0.0.0/16')
subnet = ec2.create_subnet(VpcId=vpc['Vpc']['VpcId'], CidrBlock='10.0.0.0/24')

# Create security group for EC2 instance
sg = ec2.create_security_group(GroupName='web-server', Description='Web server security group', VpcId=vpc['Vpc']['VpcId'])
ec2.authorize_security_group_ingress(GroupId=sg['GroupId'], IpPermissions=[
    {
        'IpProtocol': 'tcp',
        'FromPort': 22,
        'ToPort': 22,
        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
    },
    {
        'IpProtocol': 'tcp',
        'FromPort': 80,
        'ToPort': 80,
        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
    }
])

# Launch EC2 instance
instance = ec2.run_instances(ImageId='ami-0c94855ba95c71c99', InstanceType='t2.micro', KeyName='my-key-pair', MinCount=1, MaxCount=1, NetworkInterfaces=[
    {
        'DeviceIndex': 0,
        'SubnetId': subnet['Subnet']['SubnetId'],
        'Groups': [sg['GroupId']],
        'AssociatePublicIpAddress': True
    }
])['Instances'][0]
ec2.create_tags(Resources=[instance['InstanceId']], Tags=[{'Key': 'Name', 'Value': 'web-server'}])

# Deploy static website to S3
bucket_name = 'my-static-website'
s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': 'us-west-2'})
s3.put_object(Bucket=bucket_name, Key='index.html', Body='<html><body><h1>Hello world</h1></body></html>', ContentType='text/html')

# Install Nginx on EC2 instance
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=instance['PublicIpAddress'], username='ubuntu', key_filename='my-key-pair.pem')
stdin, stdout, stderr = ssh.exec_command('sudo apt-get update && sudo apt-get install -y nginx')
print(stdout.read().decode())
print(stderr.read().decode())
ssh.close()
