#! /usr/bin/env python

# standard libraries
import argparse

# 3rd party libraries

# project libraries

def get(args, options=None):
	"""
	Build an argument parser with the specified arguments
	and return the results
	"""
	parser = argparse.ArgumentParser()

	required_arg_is_present = {
		'credentials': False,
	}

	for v in args:
		short_form = None
		long_form = None

		if v.has_key('short'):
			short_form = v['short']
			if short_form.strip('-') in required_arg_is_present.keys():
				required_arg_is_present[short_form.strip('-')] = True
			v.pop('short', None) # remove it from the dict

		if v.has_key('long'):
			long_form = v['long']
			if long_form.strip('-') in required_arg_is_present.keys():
				required_arg_is_present[long_form.strip('-')] = True
			v.pop('long', None) # remove it from the dict

		if short_form and long_form:
			parser.add_argument(
				short_form,
				long_form,
				**v
				)
		elif short_form:
			parser.add_argument(
				short_form,
				**v
				)
		elif long_form:
			parser.add_argument(
				long_form,
				**v
				)

	# required arguments	
	if not required_arg_is_present['credentials']:
		parser.add_argument('-c', '--credentials', help="A .json document containing at least 'access_key' and 'secret_key' of the credentials to authenticate as for the current script")

	results = None
	if options:
		results = parser.parse_args(options)
	else:
		results = parser.parse_args()

	return results