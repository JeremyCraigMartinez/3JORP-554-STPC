#!/usr/bin/python

import socket
import select
import time
import sys
import threading
from copy import deepcopy

from protocols import do_GET, do_POST, do_HEAD

import urllib2

def client(host, request, data, protocol, www):
	if protocol == 'GET':
		return do_GET(host, request, www)
	elif protocol == 'POST':
		return do_POST(host, request, data)
	elif protocol == 'HEAD':
		return do_HEAD(host, request)
	else:
		raise ValueError('wrong protocol')

def forward(data):
	request,options = parseHeader(deepcopy(data[:data.find('\r\n\r\n')]))
	if request['url'] == 'favicon.ico':
		return

	body = ""
	if "Content-Length" in options:
		body = data[data.find('\r\n\r\n')+4:data.find('\r\n\r\n')+4+int(options['Content-Length'])]

	if request['url'] == "":
		return "<html><body><h1>Enter a URL</h1><h3>example: localhost:8080/http://www.cnn.com/</h3></body></html>"
	
	try:
		return client(request['url'],request['request'],body,request['protocol'],request['www'])
	except ValueError as e:
		print e
		return "<html><body><p>Error: " + str(e) + "</p></body></html>"

	return "<html><body><h1>Good job: " + request['url'] + "</h1></body></html>"

def parseHeader(data):
	fields = data.split('\r\n')

	url = fields[0][fields[0].find(' ')+1:fields[0].find('HTTP/1.1')-1]
	url = url[url.find('http')+7:]
	www = ""
	if url.startswith('www.'):
		www = "www."
		url = url[4:]
	if url.endswith('/'):
		url = url[:len(url)-1]

	request = {
		"request": fields[0],
		"url": url,
		"www": www,
		"protocol": fields[0][:fields[0].find(' ')]
	}
	options = []
	for op in fields[1:]:
		key, field = op[:op.find(':')], op[op.find(':')+2:]
		if key != '' and field != '':
			if key == "Connection":
				options.append(("Connection","close"))
			elif key != "Proxy-Connection":
				options.append((key,field))

	return request,options

def listen(server):
	inputs = [server]
	outputs = []
	queue = []
	while True:
		readable, writable, exceptional = select.select(inputs, outputs, [])

		for s in readable:
			if s is server:
				connection, client_address = s.accept()
				connection.setblocking(0)
				inputs.append(connection)

			else:
				# recv data up to 1024 bytes
				data = s.recv(10000)
				#t = threading.Thread(target=forward, args=(data,))
				#t.daemon = True
				#t.start()
				html = forward(data)
				
				if html:
					s.send(html)

				# remove inputs so next select call does not read it again
				inputs.remove(s)
				# close socket that select intercepted and that we were reading from
				s.close()

# set socket for the server to listen on
def set_sockets(host, port):
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server.setblocking(0)

	server_address = (host, port)
	print >>sys.stderr, 'starting up on %s port %s' % server_address
	server.bind(server_address)

	server.listen(5)

	return server

if __name__ == '__main__':
	try:
		server = set_sockets('localhost', 8080)

		listen(server)
	except KeyboardInterrupt:
		print('ctrl-c exit')
		sys.exit(0)