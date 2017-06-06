import socket
import sys


print(sys.argv)

# first argument is port to listen
#port = int(sys.argv[1])
#print port

# current peer ID
peerId = int(sys.argv[1])
#print peerId

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
#print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

# create list of active peers
peerIdList = []
for i in range(N) :
    peerIdList.append(1)

while True:

    # Wait for a connection
    #print >>sys.stderr, '##########SERVAR: waiting for a connection'
    connection, client_address = sock.accept()
    try:
        print >>sys.stderr, 'connection from', client_address

        # Receive the data in small chunks and retransmit it
        while True:
            dataRcvd = connection.recv(32) #data is peerId
            #print >>sys.stderr, 'peerIdRcvd "%s"' % peerIdRcvd
            if dataRcvd:
                
                
                #print "Recebi um vetor de peerIds aqui no serva"
                for (key, val) in enumerate(list(dataRcvd)):
                    peerIdList[key] = val

                peerIdConcate = ''.join(str(e) for e in peerIdList) #whom


                #send active peers to client
                print >>sys.stderr, 'Enviando para o cliente a msg: "%s"' % peerIdConcate
                #print >>sys.stderr, '%s' % peerIdConcate
                connection.sendall(peerIdConcate)
                
            else:
                #print >>sys.stderr, '-no data-', client_address
                break

        # verify if this peer is the new leader
        if leader == 0:
            for j in range(N) :
                if j == peerId:
                    leader = 1
                    print >>sys.stderr, 'EU SOU o novo lider [peerId]: %d' % peerId
                    break
                elif int(peerIdList[j]) == 1:
                    print 'Novo lider nao sou eu, eh o [peerId]: %d' % j
                    # leader is peerIdList[j]
                    break


    finally:
        # Clean up the connection
        connection.close()
