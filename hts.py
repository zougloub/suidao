#!/usr/bin/env python
# -*- coding: utf-8 vi:noet

__license__ = "GNU AFFERO GENERAL PUBLIC LICENSE v3 - https://www.gnu.org/licenses/agpl-3.0.en.html"


import sys, io, os, time, fcntl, socket
import flask

app = flask.Flask(__name__)

app.config["JSON_AS_ASCII"] = False

sessions = dict()

@app.route("/<path:url>", methods=("PUT",))
def put(url):
	if 0:
		fd_o = sys.stdout.fileno()
		fd_i = sys.stdin.fileno()
		def r():
			try:
				return os.read(fd_i, 1024)
			except OSError:
				return b""

		w = lambda x: os.write(fd_o, x)
	else:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect(("127.0.0.1", 22))
		fd_i = fd_o = s.fileno()
		def r():
			try:
				return s.recv(1024)
			except IOError:
				return b""
		def w(data):
			while data:
				n = s.send(data)
				data = data[n:]

	flag = fcntl.fcntl(fd_i, fcntl.F_GETFL)
	fcntl.fcntl(fd_i, fcntl.F_SETFL, flag | os.O_NONBLOCK)
	flag = fcntl.fcntl(fd_i, fcntl.F_GETFL)
	if flag & os.O_NONBLOCK == 0:
		raise Exception("pouet")

	sessions[url] = (fd_i, fd_o, r, w)

	return flask.jsonify(
	 response='success',
	), 201


@app.route("/<path:url>", methods=("GET",))
def get(url):
	if url not in sessions:
		return b"", 404
	fd_i, fd_o, r, w = sessions[url]
	res = r()
	return res, 201

@app.route("/<path:url>", methods=("POST",))
def post(url):
	if url not in sessions:
		return b"", 404
	fd_i, fd_o, r, w = sessions[url]
	b = io.BytesIO()
	flask.request.files["file"].save(b)
	w(b.getvalue())
	return flask.jsonify(
	 response='success',
	), 201


if __name__ == '__main__':
	app.run(
	 debug=True,
	)

