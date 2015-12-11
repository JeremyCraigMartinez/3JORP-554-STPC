#!/usr/bin/python

'''
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                 

s.connect(("cnn.com" , 80))
s.sendall("GET / HTTP/1.1\r\n\r\n")
print "hello"
print s.recv(10000)
s.close
'''

import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("z.cdn.turner.com" , 80))
s.sendall("GET /cnn/tmpl_asset/static/www_homepage/2990/css/hplib-min.css HTTP/1.1\r\n\r\n")
result = s.recv(10000)
while (len(result) > 0):
	print(result)
	result = s.recv(10000)
s.close()