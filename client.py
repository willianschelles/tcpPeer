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
	peerIdList.append(int(1))


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
		if int(peerIdList[i]) == 1:
			try:
				#print >>sys.stderr, '##########CLIENT'
				# Connect the socket to the port where the server is listening
				sock.connect(("localhost", port + i))
				# Send data
				peerIdConcate = ''.join(str(e) for e in peerIdList) #whom
				#message += leader
				print >>sys.stderr, 'Eviando msg: "%s" to port: %d' % (peerIdConcate, port+i)
				sock.sendall(peerIdConcate)

				#read and update peerIdList of active peers
				data = sock.recv(64)
				for (key, val) in enumerate(list(data)):
					peerIdList[key] = val
			except socket.error, exc:
				down_port = port + i
				down_peerId = down_port - 5000
				peerIdList[down_peerId] = 0
				print "caiu a porta %d referente ao peer de id %d" % (down_port, down_peerId)
				#print "except error: %s" % str(exc)
				peerIdConcate = ''.join(str(e) for e in peerIdList) #whom
				#print '=> peerIdList depois de cair: [%s]' % peerIdConcate

				#send message to active peers about the connection failure
				for (key, val) in enumerate(list(peerIdList)):
					#garantee that the message will be sent only to active peers
					if int(val) == 1:
						try:
							port_to_connect = key + port
							if (port_to_connect) != down_port:
								#print 'conectando a porta %d' % port_to_connect
								sock.connect(("localhost", port_to_connect))
								sock.sendall(peerIdConcate)
						except socket.error, exc:
							print "deu temer pro key = %d" % key


			#  if leader == port:

			#  sock.sendall(errorMessage)

			finally:
			#port += 1
				#print >>sys.stderr, 'finallyClient----------'
				sock.close()
