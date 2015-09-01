#! /usr/bin/env python

# standard libraries
import sys

# 3rd party libraries
import boto
import boto.ec2

# project libraries
import utils.args
import utils.credentials

def main(options=None):
	"""
	Deploy the passed key pair to all regions the credentials have access to
	"""
	args = utils.args.get([
		{ 'short': '-r', 'long': '--region', 'help': "Which region(s) to search in. 'all' is a valid selection", 'required': False, 'default': [], 'action': 'append', },
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
			num_of_instances = 0
			could_not_query_region = False
			try:
				for reservation in connection.get_all_instances():
					for instance in reservation.instances:
						print "{}\t{}\t{}".format(region.name, instance.id, instance.instance_type)
						num_of_instances +=  1
			except Exception, err:
				if "401 Unauthorized" in "{}".format(err):
					print "Not authorized to query the [{}] region".format(region.name)
					could_not_query_region = True
				else:
					print err

			if num_of_instances == 0 and could_not_query_region == False:
				print "{}\t0\t0".format(region.name)

if __name__ == '__main__': main()