import socket
import sys

print(sys.argv)

# first argument is port to listen
#port = int(sys.argv[1])
#print port

# current peer ID
peerId = int(sys.argv[1])
print peerId

# number of peers
N = int(sys.argv[2])

# first leader
if peerId == 0:
    leader = 1
else:
    leader = 0
port = peerId + 5000

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Bind the socket to the port
server_address = ('localhost', port)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

# create list of active peers
peerIdList = []

while True:

    for i in range(N) :
        peerIdList.append(0)
    # Wait for a connection
    print >>sys.stderr, '##########SERVAR: waiting for a connection'
    connection, client_address = sock.accept()
    try:
        print >>sys.stderr, 'connection from', client_address

        # Receive the data in small chunks and retransmit it
        while True:
            peerIdRcvd = connection.recv(32) #data is peerId
            print >>sys.stderr, 'peerIdRcvd "%s"' % peerIdRcvd
            if peerIdRcvd:
                teste = int(peerIdRcvd)
                print >>sys.stderr, 'teste peer Id RCVD %d' % teste
                peerIdList[teste] = 1 # confirm that the peer is

                print peerIdList


                peerIdConcate = ''.join(str(e) for e in peerIdList)

                # j = 0
                # for j in range(N):
                #     peerIdConcate += str(peerIdList[i])
                    

                print >>sys.stderr, 'PeerIdCocate = ', peerIdConcate

                #send active peers to client
                print >>sys.stderr, 'sending data back to the client'
                print >>sys.stderr, '%s' % peerIdConcate 
                connection.sendall(peerIdConcate)
                #connection.sendal
            else:
                print >>sys.stderr, '########## no more data from', client_address
                break

        # verify if this peer is the new leader
        for j in range(N) :
            if j == peerId:
                lider = 1
                print >>sys.stderr, 'eu ', client_address
            if peerIdList[j] == 1:
                # leader is peerIdList[j]
                break

                
            
    finally:
        # Clean up the connection
        connection.close()