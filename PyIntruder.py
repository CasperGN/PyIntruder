#!/usr/bin/python3

import os
import sys
import requests
import argparse

class PyIntruder():

	def __init__(self, redir, save, out, url, payload):
		self.redir = redir
		self.save_responses = save
		if out:
			self.output_dir = os.getcwd()
			if self.output_dir.endswith('/'):
				self.output_dir = output_dir[:-1]
		self.baseurl = url
		self.payloaddata = payload

		self.run()
		
	def run(self):

		### Attempt connection to each URL and print stats
		print("Status\tLength\tTime\t  Host")
		print("---------------------------------")

		for payload in self.payloaddata:
			payload = payload.strip('\n')
			url = self.baseurl.replace('$', payload)
			r = requests.get(url, allow_redirects=self.redir)
			print(f'{r.status_code}\t{len(r.content)}\t{str(r.elapsed.total_seconds()*1000)[:5]}\t{url}')
			if self.save_responses and len(r.content) != 0:
				try:
					with open('%s/%s' % (output_dir, payload), 'wb') as f:
						f.write(r.content)
				except:
					print("Error: could not write file '%s/%s'" % (output_dir, payload))

if __name__ == '__main__':
	parser = argparse.ArgumentParser(prog='PyIntruder')
	parser.add_argument('url', type=str, help='Url with $ to replace')
	parser.add_argument('payload', type=str, help='payload to replace $ with')
	parser.add_argument('-r', '--redir', help='Allow HTTP redirects', action="store_true")
	parser.add_argument('-s', '--save', help='Save HTTP response content to files', action="store_true")
	parser.add_argument('-o', '--out', type=str, help='Directory to save HTTP responses')


	if len(sys.argv) == 1:
		parser.print_help(sys.stderr)
		sys.exit(1)

	args = parser.parse_args()

	redir = args.redir if args.output else None
	save = args.save if args.callback else None
	output = args.out if args.target else None

	intruder = PyIntruder(redir, save, output)

