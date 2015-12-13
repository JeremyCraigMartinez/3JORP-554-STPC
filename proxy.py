#!/usr/bin/python

import socket
import select
import time
import sys
import threading
from copy import deepcopy

from protocols import do_CALL

#import urllib2

DEBUG = 0

class myThread (threading.Thread):
    def __init__(self, s):
        threading.Thread.__init__(self)
        self.s = s
    def run(self):
        #print "Starting "		
        if DEBUG: print "myThread: Running"             
        process_data(self.s)
        if DEBUG: print "myThread: complete"             

def process_data(s):     
	# recv data up to 10240 bytes
    if DEBUG: print "process_data: Processing Data\n"            
    data = s.recv(10240)
    if DEBUG: print "process_data: inbound data -- ",data
    html = forward(data)
    if html:
        if DEBUG: print "process_data: forward data -- ", html
        s.send(html)
    # close socket that select intercepted and that we were reading from
    s.close()
    if DEBUG: print "process_data: complete", html

def client(host, data):
	return do_CALL(host, data)

def forward(data):
	#parse headers into the url, headers options (in tuple)
	url,options = parseHeader(deepcopy(data[:data.find('\r\n\r\n')]))
	if url == 'favicon.ico':
		return

	#find body and set individual variable for data
	body = ""
	if "Content-Length" in options:
		body = data[data.find('\r\n\r\n')+4:data.find('\r\n\r\n')+4+int(options['Content-Length'])]

	if url == "":
		return "<html><body><h1>Enter a URL</h1><h3>example: localhost:8080/http://www.cnn.com/</h3></body></html>"
	
	try:
		return client(url,data)
        
	except ValueError as e:
		#poor url request
		print e
		return "<html><body><p>Error: " + str(e) + "</p></body></html>"

	return "<html><body><h1>Good job: " + url + "</h1></body></html>"

def parseHeader(data):
	#for easier parsing
	fields = data.split('\r\n')

	#parse out url
	url = fields[0][fields[0].find(' ')+1:fields[0].find('HTTP/1.1')-1]
	url = url[url.find('http')+7:]
	#if it starts with www, put in sep
	if url.startswith('www.'):
		url = url[4:]
	if url.endswith('/'):
		url = url[:len(url)-1]
		
	options = []
	for op in fields[1:]:
		key, field = op[:op.find(':')], op[op.find(':')+2:]
		if key != '' and field != '':
			options.append((key,field))

	return url,options

def listen(server):
	inputs = [server]
	outputs = []
	if DEBUG: print "listen"
 	while True:
		
		connection, client_address = server.accept()
		if DEBUG: print "accept", connection
		connection.setblocking(1)
		inputs.append(connection)
		thread = myThread(connection)
		thread.start()

# set socket for the server to listen on
def set_sockets(host, port):
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server.setblocking(1)

	server_address = (host, port)
	if DEBUG: print >>sys.stderr, 'starting up on %s port %s' % server_address
	server.bind(server_address)

	server.listen(5)

	return server

#when run from command line
if __name__ == '__main__':
	try:
		server = set_sockets('localhost', 8080)

		#main program
		listen(server)

	#catch the end of the program and spit this out	
	except KeyboardInterrupt:
		print('ctrl-c exit')
		sys.exit(0)