# AWS Snippets

A collection of handy snippets for various AWS tasks

## [deploy_keypair_worldwide.py](deploy_keypair_worldwide.py)

When you create a key pair in Amazon EC2, it is only imported into the region where it was created. This snippet will push that key pair to all AWS regions

## [get_instances_for_ansible.py](get_instances_for_ansible.py)

Get an Ansible compatible list of connections for the instances in the specified region(s)

## [search_for_ami.py](search_for_ami.py)

AMI IDs are specific to a region. That makes is a bit of a hassle to find the same AWS maintained AMI across the AWS Cloud. This snippet allows you to quickly search any specified region for an AMI maintained by AWS matching on the name or description

## [start_instances.py](start_instances.py)

Start a number of demo instances