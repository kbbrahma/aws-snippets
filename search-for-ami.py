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
	Find the AMI ID for each region for the specified AWS maintained AMI
	"""
	args = utils.args.get([
		{ 'short': '-s', 'long': '--search-for', 'help': "String of partial of the AMI to search for", 'required': True },
		{ 'short': '-r', 'long': '--region', 'help': "Which region(s) to search in. 'all' is a valid selection", 'required': False, 'default': [], 'action': 'append', 'required': True },
		], options)
	AKEY, SKEY = utils.credentials.get(args.credentials)

	results = []

	for region in boto.ec2.regions():
		# make sure we're supposed to scan this region
		if not region.name in args.region and not 'all' in args.region: continue

		connection = None
		try:
			connection = boto.ec2.connect_to_region(region.name, aws_access_key_id=AKEY, aws_secret_access_key=SKEY)
		except Exception, err:
			print err

		is_searchable = True
		if connection:
			for filters in [
		 		{ 'name': '{}*'.format(args.search_for) },
				{ 'description': '{}*'.format(args.search_for) },
				]:
				if not is_searchable: break
				try:
					for i in connection.get_all_images(owners='amazon', filters=filters):
						print '{}\t{}\t{}\t'.format(region.name, i.id, i.name)
						results.append({ 'region': region.name, 'ami_id': i.id, 'ami_name': i.name })
				except Exception, err:
					if "401 Unauthorized" in "{}".format(err):
						print "Not authorized to search in the [{}] region".format(region.name)
						is_searchable = False
					else:
						print err

if __name__ == '__main__': main()