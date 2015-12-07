import socket
import urlparse
import sys
import urllib2
import httplib

def do_GET(host, request):
	# socket approach not working
	'''# Create a TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	# Connect the socket to the port where the server is listening
	server_address = (host, 80)
	print 'connecting to %s port %s' % server_address
	sock.connect(server_address)

	try:
		sock.send(request+'\r\n\r\n')
		data = sock.recv(10000000)
		print data

	finally:
		sock.close()'''

	try:
		response = urllib2.urlopen(host)
		html = response.read()
		return html
	except:
		return ""

def do_POST(host, request, data):
	print 'do_POST'

def do_HEAD(host, request, data):
	print 'do_HEAD'