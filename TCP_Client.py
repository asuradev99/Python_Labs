from socket import *

serverName = '10.0.0.133'
serverPort = 12000
clientSocket = socket(AF_INET,SOCK_STREAM)
clientSocket.bind(('',12001))
sentence = input("Input lowercase sentence: ")
clientSocket.connect((serverName, serverPort))

clientSocket.sendto(sentence.encode(), (serverName, serverPort))
modifiedSentence = clientSocket.recv(2).decode()

print ('From server: '+ modifiedSentence)
