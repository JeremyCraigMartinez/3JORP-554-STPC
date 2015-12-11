import socket
import urlparse
import sys
import urllib2
import httplib

def do_CALL(host, data):
	# socket approach not working
	try:
		html = ""
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((host, 80))
		s.send(data)
		result = s.recv(4096)
		while (len(result) > 0):
			html = html + result
			result = s.recv(4096)
		return html
	except:
		try:
			response = urllib2.urlopen("http://"+host)
			html = response.read()
			return html
		except:
			print "http://"+host
			return ""