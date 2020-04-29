#!/usr/bin/python3

import os
import sys
import requests
import optparse

def main():
	# Get Options
	parser = optparse.OptionParser()

	parser.add_option('-r', '--redir',
		              dest="redir",
		              default=False,
		              action="store_true",
		              help='Allow HTTP redirects',
		             )
	parser.add_option('-s', '--save',
		              dest="save",
		              default=False,
		              action="store_true",
		              help='Save HTTP response content to files',
		             )
	parser.add_option('-o', '--out',
		              dest="out",
		              default=os.getcwd(),
		              help='Directory to save HTTP responses',
		             )
	parser.set_usage("""Usage: ./PyIntruder.py [options] <base url> <payload list>
	(Use '$' as variable in url that will be swapped out with each payload)

	Example:  PyIntruder.py http://www.example.com/file/$.pdf payloads.txt
		""")
	options, remainder = parser.parse_args()

	redir = options.redir
	save_responses = options.save
	output_dir = options.out
	if output_dir.endswith('/'):
		output_dir = output_dir[:-1]


	### Assign arguments to variables
	if len(remainder) == 2:
		baseurl = remainder[0]
		if '$' not in baseurl:
			print("Error: Please include variable character ('$') in URL")
			sys.exit()
		payloadfile = remainder[1]
	else:
		print("Invalid number of arguments: use -h option for usage")
		sys.exit()

	### Try reading payloads into variable
	try:
		with open(payloadfile) as f:
			payloaddata = f.readlines()
	except:
		print("Error: cannot read file '%s'" % payloadfile)
		sys.exit()

	### Attempt connection to each URL and print stats
	print("Status\tLength\tTime\t  Host")
	print("---------------------------------")

	for payload in payloaddata:
		payload = payload.strip('\n')
		url = baseurl.replace('$', payload)
		r = requests.get(url, allow_redirects=redir)
		print("%s\t%s\t%s\t  %s" % (r.status_code, len(r.content), r.elapsed.total_seconds()*1000, url))
		if save_responses and len(r.content) != 0:
			try:
				with open('%s/%s' % (output_dir, payload), 'wb') as f:
					f.write(r.content)
			except:
				print("Error: could not write file '%s/%s'" % (output_dir, payload))

if __name__ == '__main__':
	main()

