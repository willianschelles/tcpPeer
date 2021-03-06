import socket
import sys

print(sys.argv)

peerId = int(sys.argv[1])
N = int(sys.argv[2])

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

strPeerId = str(peerId)
logFile = "log%s.txt" % strPeerId

# open file, write and close
def printOnFile( stringToPrint ):
    stringToPrint = 'SERVER: %s' % stringToPrint
    logFileTxT = open(logFile, "a")
    print >>sys.stderr, 'Log file: ', stringToPrint

    logFileTxT.write(stringToPrint)
    logFileTxT.close()

    
# current peer ID
strlog = 'Inicia server de peerId %s\n' % sys.argv[1]
print >>sys.stderr, 'Inicia server de peerId %s\n ' % sys.argv[1]
printOnFile(strlog) 

# number of peers
strlog = 'Numero de peers %s\n' % sys.argv[2]
print >>sys.stderr, strlog
printOnFile(strlog)
leader = 0


#initializing datas
port = peerId + 5000
sock = socket
sock = initializeSocket( sock )
peerIdList = []
initializePeerIdList( peerIdList )
countConnection = 0


#f.write(N)

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
                countConnection += 1
                if countConnection == N:
                    leader = electFirstLeader()
                    
                peerIdConcate = ''.join(str(e) for e in peerIdList) #concatenate "string" to list which peer is running
                print >>sys.stderr, 'Enviando peers ativos para o cliente: "%s\n"' % peerIdConcate   
                strlog = 'Enviando peers ativos para o cliente: "%s"\n' % peerIdConcate
                printOnFile(strlog)
                connection.sendall(peerIdConcate)                   #send active peers to client
            else:
                #print >>sys.stderr, '-no data-', client_address
                break
        # verify if this peer is the new leader
        if leader == 0:
            for j in range(N) :
                if j == peerId:
                    leader = 1
                    strlog = 'Eu sou o novo lider, meu peer Id eh: %s\n' % sys.argv[1]
                    print >>sys.stderr, strlog
                    printOnFile(strlog)
                    break
                elif int(peerIdList[j]) == 1:
                    strlog = 'O lider e o peerId: %s\n' % str(j)
                    print >>sys.sterr, strlog
                    printOnFile(strlog)
                    
                    # leader is peerIdList[j]
                    break
    except socket.error, exc:
        strlog = "exception: %s\n" % exc
        print >>sys.stderr, strlog
        printOnFile(strlog)


    finally:
        # Clean up the connection
        connection.close()
        #logFileTxT.close()
