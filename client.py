import socket
import sys
import time

port = 5000;

peerId = int(sys.argv[1])
print peerId

# number of peers
N = int(sys.argv[2])

if peerId == 0:
    leader = 1
else:
    leader = 0

while True:
	time.sleep(3)
	i = 1
	for i in range(N):
	#    try:
	    # Create a TCP/IP socket
	    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	    try:
	        #print >>sys.stderr, '##########CLIENT'
	        # Connect the socket to the port where the server is listening
	        sock.connect(("localhost", port))
	        port += 1
	        # Send data
	        message = '%d' % peerId
	        #message += leader
	        print >>sys.stderr, 'Eviando msg: "%s" to port: %d' % (message, port)
	        sock.sendall(message)

	        # while amount_received < amount_expected:
	        data = sock.recv(64)
	        # amount_received += len(data)
	        #print >>sys.stderr, 'received "%s"' % data
	    except socket.error, exc:
	        print "except error: %s" % str(exc)
	        print "caiu porta: %d" % str(port)
	        print "except error: %s" % errorMessage
	        
	     #   if leader == port:

	      #  sock.sendall(errorMessage)

	    finally:
	            print >>sys.stderr, 'finallyClient----------'
	            #sock.close()

