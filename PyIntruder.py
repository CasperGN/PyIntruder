#!/usr/bin/python3

import os, sys, requests, argparse, re
from random import choice
from time import sleep
from OpenSSL import SSL
from datetime import datetime
from socket import gaierror

class PyIntruder():

	def __init__(self, redir, save, out, url, payload):
		pwd = os.path.dirname(os.path.realpath(__file__))

		self.redir = redir
		self.save_responses = save
		if out:
			self.output_dir = out
		else:
			self.output_dir = os.getcwd()
		if self.output_dir.endswith('/'):
			self.output_dir = output_dir[:-1]
		self.baseurl = url
		self.payloaddata = payload
		targetUrl = re.compile(r'://([\w\.-]+)/')
		self.target = targetUrl.findall(self.baseurl)[0]

		self.useragents = []
		with open(f'{pwd}/user-agents.txt', 'r') as agents:
			for useragent in agents:
				self.useragents.append(useragent.rstrip())
		
		
	def run(self):

		### Attempt connection to each URL and print stats
		result = []

		for payload in self.payloaddata:
			user_agent = choice(self.useragents)
			headers = {'User-Agent': user_agent}
			payload = payload.strip('\n')
			url = self.baseurl.replace('$', payload)
			try:
				r = requests.get(url, headers=headers, allow_redirects=self.redir)
				# Here we attempt to circumvent rate limit and/or temporary blocks on our IP
				# Often when 403 og 429 is returned because of a block a small html document
				# is returned with that is len =~ 200
				if r.status_code == 403 and len(r.content) < 200 or r.status_code == 429 and len(r.content) < 200:
					# Testing has shown that at least blocks from Akamai last around 2 minutes
					print(f"{str(datetime.now())} - Request was possibly blocked by WAF: Sleeping thread for 140 seconds for {self.target}")
					sleep(140)
					r = requests.get(url, headers=headers, allow_redirects=self.redir)
					if r.status_code == 403 and len(r.content) < 200 or r.status_code == 429 and len(r.content) < 200:
						# At this point we just continue
						continue
			except (SSL.SysCallError, gaierror):
				continue
			result.append([r.status_code, len(r.content), str(r.elapsed.total_seconds()*1000)[:7], url])
			if r.status_code == 404:
				# The url/endpoint is not working, lets just break out
				return result
			if self.save_responses and len(r.content) != 0:
				try:
					with open(f'{self.output_dir}/{str(datetime.now()).replace(" ", "T").replace(":", "-").split(".")[0]}-{self.payloaddata.index(payload)}', 'w') as f:
						f.write(f'{url}\n\n{r.status_code}\n\n{r.content}')
				except:
					print(f'Error: could not write file {self.output_dir}/{str(datetime.now()).replace(" ", "T").replace(":", "-").split(".")[0]}-{self.payloaddata.index(payload)}')
			sleep(0.5)
		return result

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
	#output = intruder.run()
	#print("Status\tLength\tTime\t  Host")
	#print("---------------------------------")
	#for result in output:
	#	print(f'{result[0]}\t{result[1]}\t{result[2]}\t{result[3]}')