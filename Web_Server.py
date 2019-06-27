#import socket module
from socket import *

#prepare server socket  
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', 4000))
serverSocket.listen(1)

#commit test 

#main loop
while True:
    #Establish the connection
    print ('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    print ("Accepted connection from:  " + addr[0] + "\n")

    try:
        #main body for connection
        message = connectionSocket.recv(2048).decode()
        filename = message.split()[1]

        #open and change requested file
        f = open(filename[1:], "w+")
        
        print ("Message from " + addr[0] + ": " + str(message.split()))
        f.seek(0)
        f.write("Your Ip address is " + addr[0] )
        f.write("\n The operating system you are using is " + str(message.split()[13:16]))
        f.write("\n The browser you are using is " + str(message.split() [21]))
        f.seek(0)
        outputdata = f.read()
        #Send one HTTP header line 
        hdr = "HTTP/1.1 200 OK\r\n"
        connectionSocket.send(hdr.encode())
        connectionSocket.send("\r\n".encode())
        print ("File found and will be sent")

    
        connectionSocket.send(outputdata.encode())
        print ("File send to client")
        break
    #Send 404 message if file not in server directory
    except IOError:
        print ("file not found.")
        e_hdr = "HTTP/1.1 404 Not Found\r\n"
        connectionSocket.send(e_hdr.encode())
        connectionSocket.send("\r\n".encode())

connectionSocket.close()
  
    