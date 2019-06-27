from socket import *
serverName = '10.0.0.134'
serverPort = 12000

#sets up client socket interface.
clientSocket = socket(AF_INET, SOCK_DGRAM)

#message to send to server:
#message = raw_input('Input Lower case sentence: ')

#socket to send mesage
clientSocket.sendto(message, (serverName, serverPort))

#receives message from server
modifiedMessage, serverAdress = clientSocket.recvfrom(2048)

#prints the message
print("Server replied: " +  modifiedMessage)

#close the socket interface
clientSocket.close()
