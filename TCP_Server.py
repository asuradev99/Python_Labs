from socket import *
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)

print ('Server ready')

connectionSocket, addr = serverSocket.accept()
print ("accepted connection")
sentence = connectionSocket.recv(1024).decode()
print ("Received message from " + str(addr[0]) +  ": " + sentence)
capitalizedSentence = sentence.upper()
connectionSocket.sendto(capitalizedSentence.encode(), addr)
connectionSocket.close()
    





