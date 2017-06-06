import socket
import sys
import time

port = 5000;

peerId = int(sys.argv[1])
print peerId

# number of peers
N = int(sys.argv[2])

# create list of active peers
peerIdList = []
for i in range(N) :
	peerIdList.append(0)


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
			sock.connect(("localhost", port + i))
			# Send data
			message = '%d' % peerId
			#message += leader
			print >>sys.stderr, 'Eviando msg: "%s" to port: %d' % (message, port+i)
			sock.sendall(message)

			#read and update peerIdList of active peers
			data = sock.recv(64)
			for (key, val) in enumerate(list(data)):
				peerIdList[key] = val
		except socket.error, exc:
			down_port = port + i
			print "caiu a porta: %d" % down_port
			print "except error: %s" % str(exc)
			down_peerId = down_port - 5000
			peerIdList[down_peerId] = 0
			print 'peerId caido: %d' % down_peerId
			peerIdConcate = ''.join(str(e) for e in peerIdList) #whom
			print '=> peerIdList depois de cair: [%s]' % peerIdConcate
			for j in range(N):
				try:
					if (j + port) != down_port:
						sock.connect(("localhost", port + j))
						sock.sendall(peerIdConcate)
				except socket.error, exc:
					print "deu temer pro j = %d" % j


		#  if leader == port:

		#  sock.sendall(errorMessage)

		finally:
		#port += 1
			print >>sys.stderr, 'finallyClient----------'
			sock.close()
