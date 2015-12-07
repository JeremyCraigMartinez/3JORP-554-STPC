#How to run

1. run proxy on command line: `python proxy`
2. open browser
3. search browser leading with `localhost:8080`. (e.g. `http://localhost:8080/www.cnn.com`)

#How it works
- creates socket for proxy server
- calls main loop
	- uses `select` to listen for incoming traffic
	- recieves request from browser. Starts new thread in function Forward()
		- forward parses the header. extracts the data and calls client
		- client determines whether to do a GET, POST, or HEAD function call
		- enqueues data from destination
	- dequeues data from destination and returns it to browser
- browser displays data from destination