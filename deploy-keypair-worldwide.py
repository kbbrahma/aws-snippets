#! /usr/bin/env python

# standard libraries
import sys

# 3rd party libraries
import boto
import boto.ec2

# project libraries
import utils.args
import utils.credentials

# setup
args = utils.args.get({
	'key_name': { 'short': '-n', 'long': '--keypair-name', 'help': "The name of the key pair to import", 'required': True },
	'key_path': { 'short': '-p', 'long': '--keypair-path', 'help': "The path of the file containing the public key of the key pair you want to distribute"},
	'key_string': { 'short': '-s', 'long': '--keypair-string', 'help': "The string for the public key of the key pair your want to distribute. This is handy if you're 'cat'-ing the output of ~/.ssh/authorized_keys"}
	})
AKEY, SKEY = utils.credentials.get(args.credentials)

def main():
	"""
	Deploy the passed key pair to all regions the credentials have access to
	"""
	keypairs = []
	if args.keypair_path:
		try:
			with open(args.keypair_path, 'r') as fh:
				for line in fh:
					if line.startswith('ssh-rsa'):
						keypairs.append(line.strip())
		except Exception, err:
			print "Could not open the file [{}]. Threw exception:\n\t{}".format(args.keypair_path, err)

	if args.keypair_string:
		keypairs.append(args.keypair_string)

	for region in boto.ec2.regions():
		connection = None
		try:
			connection = boto.ec2.connect_to_region(region.name, aws_access_key_id=AKEY, aws_secret_access_key=SKEY)
		except Exception, err:
			print err

		if connection:
			for keypair in keypairs:
				try:
					print connection.import_key_pair(key_name=args.keypair_name, public_key_material=keypair)
				except Exception, err:
					print "Could not import the key pair to region [{}]. Threw exception:\n\t{}".format(region, err)

if __name__ == '__main__': main()