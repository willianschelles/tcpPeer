import socket
import sys
import time

port = 5000;

peerId = int(sys.argv[1])
print peerId

# number of peers
N = int(sys.argv[2])

# create list of active peers
def initializePeerIdList( peerIdList ):
    for i in range(N) :
        peerIdList.append(1)

# elect first leader
def electFirstLeader( ):
    return 1 if peerId == 0 else 0


strPeerId = str(peerId)
logFile = "log%s.txt" % strPeerId

#open file, write and close
def printOnFile( stringToPrint ):
    stringToPrint = 'CLIENT: %s' % stringToPrint
    logFileTxT = open(logFile, "a")
    print >>sys.stderr, 'Log file: ', stringToPrint

    logFileTxT.write(stringToPrint)
    logFileTxT.close()

leader = electFirstLeader()
peerIdList = []
initializePeerIdList( peerIdList )

# current peer ID
strlog = 'Inicia client de peerId %s\n' % sys.argv[1]
print >>sys.stderr, 'Inicia client de peerId %s\n ' % sys.argv[1]
printOnFile(strlog) 

# number of peers
strlog = 'Numero de peers %s\n' % sys.argv[2]
print >>sys.stderr, strlog
printOnFile(strlog)


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
				strlog = 'Eviando msg: "%s" to port: %d\n' % (peerIdConcate, port+i)
				print >>sys.stderr, strlog
				printOnFile(strlog)
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
				strlog = "caiu a porta %d referente ao peer de id %d" % (down_port, down_peerId)
				printOnFile(strlog)
				#if current peerId, equal peerId disconnected, stop application
				if peerId == down_peerId :
					sys.exit()
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
								strlog = "Conectando a porta %s" % port_to_connect
								printOnFile(strlog)
								# notify other peers about new leader
								sock.sendall(peerIdConcate)
						except socket.error, exc:
							print "exception: %s" % exc
							strlog = "exception: %s" % exc
							printOnFile(strlog)

			#  if leader == port:

			#  sock.sendall(errorMessage)

			finally:
			#port += 1
				#print >>sys.stderr, 'finallyClient----------'
				sock.close()
