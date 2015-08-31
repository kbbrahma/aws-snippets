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

def main(options=None):
	"""
	"""
	args = utils.args.get([
		{ 'short': '-s', 'long': '--search-for', 'help': "String of partial of the AMI to search for. Will use the latest version if at all possible", 'required': True },
		{ 'short': '-r', 'long': '--region', 'help': "Which region(s) to search in. 'all' is a valid selection", 'required': False, 'default': [], 'action': 'append', 'required': True },
		], options)
	AKEY, SKEY = utils.credentials.get(args.credentials)

	#amis = search_for_ami.main('-c {} -s "amzn-ami-hvm*ebs" -r {}'.format(args.credentials))

if __name__ == '__main__': main()