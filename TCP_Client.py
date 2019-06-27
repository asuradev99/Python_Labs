from socket import *
serverName = '10.0.0.134'
serverPort = 12000
clientSocket = socket(AF_INET,SOCK_STREAM)
sentence = input("Input lowercase sentence: ")
clientSocket.connect((serverName, serverPort))
clientSocket.sendto(sentence.encode(), (serverName, serverPort))
modifiedSentence = clientSocket.recv(1024).decode()

print ('From server: '+ modifiedSentence)
