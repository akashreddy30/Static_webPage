steps followed to complete the task:

---MANUAL PROCEDURE---:

1. Created the AWS account.
2.  Slected the region.
3. Selected the VPC(Virtual Private Cloud) service.
4. Created VPC with specific name and IPv4 CIDR block.
5. Created two Public Subnets with a single availability zone and unique names and IPv4 CIDR block.
6.Selected the EC2 Service.
7.Selected t2. micro freetier Ubuntu Linux.
8.Created a Bucket
9.Uploaded a HTML file.
10.Hosted the static web page.

----REMOTE EXECUTION----:

1.Writing the Python Script which uses the boto3 to connect with the AWS and do the following steps.
                --> Set up boto3 client for EC2 and S3
                --> Create VPC and subnet for EC2 instance
                --> Create security group for EC2 instance
                -->  Launch EC2 instance
                -->  Deploy static website to S3
                -->  Install Nginx on EC2 instance


STATIC WEB SITE CREATED with URL:

http://973hdshfdsj.s3-website-us-east-1.amazonaws.com



