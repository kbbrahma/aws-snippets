# AWS Snippets

A collection of handy snippets for various AWS tasks

## deploy-keypair-worldwide.py

When you create a key pair in Amazon EC2, it is only imported into the region where it was created. This snippet will push that key pair to all AWS regions

## search-for-ami.py

AMI IDs are specific to a region. That makes is a bit of a hassle to find the same AWS maintained AMI across the AWS Cloud. This snippet allows you to quickly search any specified region for an AMI maintained by AWS matching on the name or description