# standard library
import json
import os
import sys

def get(fn):
	"""
	Get the credentials from the specified .json file
	and return them in the format:

	(akey, skey)
	"""
	results = None

	if os.path.exists(fn):
		credentials = None
		try:
			with open(fn, 'rb') as fh:
				credentials = json.load(fh)
		except Exception, err: print err

		if credentials and credentials.has_key('access_key') and credentials.has_key('secret_key'):
			results = (credentials['access_key'], credentials['secret_key'])

	return results

if __name__ == '__main__': print get(sys.argv[-1])