from socket import *
serverPort = 12000
serverSocket = socket(AF_INET,SOCK_DGRAM)

#binds socket to port 12000 explicitly
serverSocket.bind(('', serverPort))

print ("server initialized and ready")

#main while loop
while 1:   
    message, clientAddress = serverSocket.recvfrom(2048)
    modifiedMessage = message.upper()
    print ("recieved message: " + message)
    serverSocket.sendto(modifiedMessage,clientAddress)