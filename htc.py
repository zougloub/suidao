#!/usr/bin/env python
# -*- coding: utf-8 vi:noet

__license__ = "GPL v3 - https://www.gnu.org/licenses/gpl.html"

import sys, io, os, fcntl, socket, time, argparse
import requests

if __name__ == "__main__":
	parser = argparse.ArgumentParser(
	 description="HTTP tunnel",
	)

	parser.add_argument("url",
	 help="location where hts.py will answer",
	)

	try:
		import argcomplete
		argcomplete.autocomplete(parser)
	except:
		pass

	args = parser.parse_args()

	url = args.url

	fd_i = sys.stdin.fileno()
	def r():
		try:
			return os.read(fd_i, 1024)
		except OSError:
			return b""

	flag = fcntl.fcntl(fd_i, fcntl.F_GETFL)
	fcntl.fcntl(fd_i, fcntl.F_SETFL, flag | os.O_NONBLOCK)
	flag = fcntl.fcntl(fd_i, fcntl.F_GETFL)
	if flag & os.O_NONBLOCK == 0:
		raise Exception("pouet")

	s = requests.Session()

	res = s.put(url, data={})
	if res.status_code != 201:
		raise Exception(res)

	t = time.time()
	while True:

		now = time.time()
		if now > t + 1e-3:
			data = r()
			if data != b"":
				res = s.post(url, files={"file": data})
				if res.status_code != 201:
					raise Exception(res)
		t = now

		res = s.get(url)
		if res.status_code != 201:
			raise Exception(res)
		sys.stdout.buffer.write(res.content)
		sys.stdout.flush()

