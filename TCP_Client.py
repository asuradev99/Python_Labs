from socket import socket, AF_INET, SOCK_STREAM
serverName = '127.0.0.1'
serverPort = 12000
clientSocket = socket(AF_INET,SOCK_STREAM)
clientSocket.bind(('',12001))
sentence = input("Input lowercase sentence: ")
clientSocket.connect((serverName, serverPort))

clientSocket.sendto(sentence.encode(), (serverName, serverPort))
modifiedSentence = clientSocket.recv(1024).decode()

print ('From server: '+ modifiedSentence)
