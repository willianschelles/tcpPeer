import socket
import sys

print(sys.argv)

# current peer ID
peerId = int(sys.argv[1])
print >>sys.stderr, 'Eu sou o server %d ' % peerId

# number of peers
N = int(sys.argv[2])
print >>sys.stderr, 'Numero de peers %d ' % N


# elect first leader
def electFirstLeader( ):
    return 1 if peerId == 0 else 0

# create, bind and putting socket on listen
def initializeSocket( sock ):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to the port
    server_address = ('localhost', port)
    #print >>sys.stderr, 'starting up on %s port %s' % server_address
    sock.bind(server_address)
    # Listen for incoming connections
    sock.listen(1)
    return sock

# create list of active peers
def initializePeerIdList( peerIdList ):
    for i in range(N) :
        peerIdList.append(1)


#initializing datas
leader = electFirstLeader()
port = peerId + 5000
sock = socket
sock = initializeSocket( sock )
peerIdList = []
initializePeerIdList( peerIdList )

while True:

    # Wait for a connection
    connection, client_address = sock.accept()
    try:
        print >>sys.stderr, 'Connection from: ', client_address
        # Receive the data in small chunks and retransmit it
        while True:

            dataRcvd = connection.recv(32)  #data is peerId
            if dataRcvd:
                for (key, val) in enumerate(list(dataRcvd)):
                    peerIdList[key] = val

                peerIdConcate = ''.join(str(e) for e in peerIdList) #concatenate "string" to list which peer is running
                print >>sys.stderr, 'Enviando peers ativos para o cliente: "%s"' % peerIdConcate   
                connection.sendall(peerIdConcate)                   #send active peers to client
            else:
                #print >>sys.stderr, '-no data-', client_address
                break
        # verify if this peer is the new leader
        if leader == 0:
            for j in range(N) :
                if j == peerId:
                    leader = 1
                    print >>sys.stderr, 'Eu sou o novo lider, meu peer Id eh: %d' % peerId
                    break
                elif int(peerIdList[j]) == 1:
                    print 'Nao sou o lider, o lider eh o: %d' % j
                    # leader is peerIdList[j]
                    break
    except socket.error, exc:
        print "exception: %s" % exc


    finally:
        # Clean up the connection
        connection.close()
