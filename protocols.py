import socket
import urlparse
import sys
import urllib2
import httplib

def do_GET(host, request, www):
	# socket approach not working
	try:
		html = ""
		request = b"GET / HTTP/1.1\nHost: "+www+host+"\n\n"
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((host, 80))
		print request
		s.send(request)
		result = s.recv(10000)
		while (len(result) > 0):
			html = html + result
			result = s.recv(10000)
		return html
	except:
		try:
			response = urllib2.urlopen("http://"+www+host)
			html = response.read()
			return html
		except:
			return ""

def do_POST(host, request, data):
	print 'do_POST'

def do_HEAD(host, request, data):
	print 'do_HEAD'