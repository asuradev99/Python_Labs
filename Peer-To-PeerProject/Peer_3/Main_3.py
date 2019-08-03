#Peer 3
from socket import *
import time
import threading

#Directory of target file 
file_dir = "File_3.txt"

#local peer table
l_peer_table = {}

#Socket initalization
server_port = 3003
l_addr = '127.0.0.1'  
cn_sock = socket(AF_INET, SOCK_STREAM)

#Server socket initialization
s_sock = socket(AF_INET, SOCK_STREAM)
s_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s_sock.bind((l_addr, server_port))

#Server Handler (multithreaded)
class ServerHandler(threading.Thread):
    #initialize server handler 
    def __init__(self, connection_socket, _id):
        threading.Thread.__init__(self)
        self.connection_socket = connection_socket
        self._id = _id

    #server body code
    def run(self):
        #when local file requested, send it to client 
        def send_file(self, _file):
            #open local file
            with open (_file) as f:
                #copy file to string and send string 
                otpt_f = f.read()
                self.client_socket.send(otpt_f.encode())
                print ("Thread {} sent {}".format(self._id, file_dir))
        #main loop: listening for connection, accept connection, take action, close connection repeat
        while True:
            #begin listening for connections 
            self.connection_socket.listen(1)
            print ("Thread " + str(self._id) + ' ' + "initialized and listening" )
            #accept connection 
            self.client_socket, self.addr = self.connection_socket.accept()
            print ("Thread {} connected to ".format(self._id) + str(self.addr))
            #recieve an 8-byte control message to take specific actions
            self.ctrl = self.client_socket.recv(8).decode()
            #Request file message 
            if self.ctrl == 'REQ FILE':
                send_file(self, file_dir)
            
            time.sleep(0.01)
            print ("Thread {} resetting socket".format(self._id))
            self.client_socket.close()

class ClientHandler ():
    def __init__(self, client_socket, addr):
        #initialize socket 
        self.client_socket = client_socket
        self.addr = addr
    def inform_server(self):
        print ("Connecting to server to add file to server peer table...")
        #connect to server socket 
        self.client_socket.connect ((self.addr, 3001))
        self.client_socket.send("ADD FILE".encode())
        #send file name and port to server 
        self.client_socket.sendall((str(server_port) + "," + file_dir).encode())
        print ("Peer 3 has delivered it's file to the server")
        #close socket 
        self.client_socket.shutdown(SHUT_RDWR)
        self.client_socket.close()

    def obtain_peer_table(self, delay):
        self.rcvd_ctrl = ""
        #loop to repeat requesting peer table until it is complete 
        while self.rcvd_ctrl != "REQ ACPT":
            #initialize client socket 
            self.client_socket = socket(AF_INET, SOCK_STREAM)
            self.client_socket.connect ((self.addr, 3001))
            #send request peer table control message 
            self.client_socket.send ("REQ DICT".encode())
            #recieve 8-byte control message response 
            self.rcvd_ctrl = self.client_socket.recv(8).decode()
            #break if recieved request accepted message 
            if self.rcvd_ctrl == "REQ ACPT": break
            #close connection 
            self.client_socket.shutdown(SHUT_RDWR)
            self.client_socket.close()
            print ("REQ DICT denied, waiting {} seconds: {}".format(delay, self.rcvd_ctrl))
            #wait a delay period until retrying
            time.sleep(delay)
            delay *= 2 
        print ("REQ DICT accepted, recieving peer dict")
        #parse recieved string and format it into dict 
        table = self.client_socket.recv(256).decode().split(',')
        table = dict(zip(*[iter(table)]*2))
        #close socket 
        self.client_socket.shutdown(SHUT_RDWR)
        self.client_socket.close()
        #return formatted dict 
        return table
    def obtain_file_data (self, filename, port ):
        #initialize socket 
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect ((self.addr, port))
        #send a request for file control message 
        self.client_socket.send("REQ FILE".encode())
        print ("retrieving " + filename + " from server")
        #open file and write contents of recieved file data to it 
        with open (filename, 'x') as f:
            f.write(self.client_socket.recv(512).decode())
            #close connection
            f.close()

    def begin_all_file_req(self, table):
        print ("Client waiting for peers to finish sending their files and download the peer table...")
        #wait for peer table to be complete
        for key, value in table.items():
            #make sure the file reference isn't to the local file 
            if key != file_dir:
                print ("Requesting " + key + " from port " + value)
                #run obtain_file_data with key, the name of the file, and value, the port 
                self.obtain_file_data(key, int(value))

#create server threads             
for i in range (3):
    server_thread = ServerHandler(s_sock, i+1)
    server_thread.start()

#create client handler
client_main = ClientHandler(cn_sock, l_addr)
client_main.inform_server()
l_peer_table = client_main.obtain_peer_table(0.1)
client_main.begin_all_file_req(l_peer_table)
print ("Done")