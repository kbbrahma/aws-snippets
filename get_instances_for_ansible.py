#! /usr/bin/env python

# standard libraries
import sys

# 3rd party libraries
import boto
import boto.ec2

# project libraries
import utils.args
import utils.credentials
import search_for_ami

def get_ami_user_name(ami_id, connection):
	user_name = 'ec2-user'
	images = connection.get_all_images(filters={ 'image-id': ami_id })
	for image in images:
		if 'ubuntu' in image.name.lower():
			user_name = 'ubuntu'
			break

	return user_name

def main(options=None):
	"""
	Create a list of hosts to connect to via Ansible for the specified region(s)
	"""
	args = utils.args.get([
		{ 'short': '-r', 'long': '--region', 'help': "Which region(s) to search in. 'all' is a valid selection", 'required': False, 'default': [], 'action': 'append', 'required': True },
		], options)
	AKEY, SKEY = utils.credentials.get(args.credentials)
	
	for region in boto.ec2.regions():
		# make sure we're supposed to scan this region
		if not region.name in args.region and not 'all' in args.region: continue

		ami_user_names = {}

		connection = None
		try:
			connection = boto.ec2.connect_to_region(region.name, aws_access_key_id=AKEY, aws_secret_access_key=SKEY)
		except Exception, err:
			print err

		if connection:
			try:
				for reservation in connection.get_all_instances():
					for instance in reservation.instances:
						if not ami_user_names.has_key(instance.image_id): ami_user_names[instance.image_id] = get_ami_user_name(instance.image_id, connection)
						print "{}\tansible_connection=ssh\tansible_ssh_user={}".format(instance.ip_address, ami_user_names[instance.image_id])
			except Exception, err:
				if "401 Unauthorized" in "{}".format(err):
					print "Not authorized to query the [{}] region".format(region.name)
				else:
					print err

if __name__ == '__main__': main()