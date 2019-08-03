#Server peer 1
from socket import *
import time
import threading
#Directory of target file 
file_dir = "File_1.txt" 

#Initialize dict of target files and their corresponding ports 
peer_table = {}

#number of peers
peerCount = 3

#Socket initialization
server_port = 3001
l_addr = '127.0.0.1'
s_sock = socket(AF_INET, SOCK_STREAM)
s_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s_sock.bind((l_addr, server_port))

#Client socket initialization
cn_sock = socket (AF_INET, SOCK_STREAM)

#Server Hander (multithreaded)
class ServerHandler(threading.Thread):
    #initialize server handler 
    def __init__(self, connection_socket, _id):        
        threading.Thread.__init__(self)
        self.connection_socket = connection_socket
        self._id = _id
        
    #server body code
    def run(self):
        #Add file to dict 
        peer_table ["File_1.txt"] = '3001' 

        #format peer table into string for transportation 
        def format_peer_table():
            k = []
            for key, value in peer_table.items():
                k.append(key)
                k.append(value)
            return ','.join(k)
        
        #recieve file data from client and append it to local peer table
        def set_peer_table(self):
                print ("Thread {} accepted ADD FILE request".format(self._id))
                #recieve file data from client 
                rcvd_port, rcvd_filename = self.client_socket.recv(48).decode().split(',')
                #add to peer table
                peer_table[rcvd_filename] = rcvd_port
                print ("Updating peer table: " + str(peer_table))

        #when required send peer table over socket to client 
        def give_peer_table(self):
                #make sure peer table is complete before sending 
                if(len(peer_table) == peerCount):
                    #send request accepted message to client 
                    self.client_socket.send("REQ ACPT".encode())
                    print ("Thread {} accepted REQ DICT request".format(self._id))
                    #send formatted peer table (string) to client 
                    self.client_socket.send(format_peer_table().encode())
                else:
                    #send request denied message to client if peer table incomplete 
                    self.client_socket.send("REQ DENY".encode())
                    print ("Thread {} denied REQ DICT request: {}".format(self._id, peer_table))

        #when local file requested, send it to client 
        def send_file(self, _file):
                print ("Thread {} accepted REQ FILE request".format(self._id))
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
            print ("Thread " + str(self._id) + ' ' + "initialized and listening..." )
            #accept connection 
            self.client_socket, self.addr = self.connection_socket.accept()
            print ("Thread {} connected to ".format(self._id) + str(self.addr))
            #recieve an 8-byte control message to take specific actions
            self.ctrl = self.client_socket.recv(8).decode()

            #Control messages:

            #Client wants to update local peer table
            if self.ctrl == 'ADD FILE':
                print ("Thread {} accepted ADD FILE request".format(self._id))
                set_peer_table(self)
            #client requests local peer table
            elif self.ctrl == 'REQ DICT':
                give_peer_table(self)
            #client requests local file 
            elif self.ctrl == 'REQ FILE':
                send_file(self, file_dir)
            #wait to reset socket so client can close properly 
            time.sleep(0.01)
            print ("Thread {} resetting socket".format(self._id))
            #close connection and repeat
            self.client_socket.close()

#Client handler (to request files) 
class ClientHandler ():
    #initialize client handler 
    def __init__(self, client_socket, addr):
        #initialize socket 
        self.client_socket = client_socket
        self.addr = addr
    
    #method to obtain a file as instructed from the local peer table
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

    #loops which iterates through local peer table and obtains each file via obtain_file_data()
    def begin_all_file_req(self, table):
        print ("Client waiting for peers to finish sending their files and download the peer table...")
        #wait for peer table to be complete
        while len(peer_table) < peerCount: 
           pass
        #iterate through the local peer table and obtain each file reference in it 
        print ("Client ready to begin requesting")
        for key, value in table.items():
            #make sure the file reference isn't to the local file 
            if key != file_dir:
                print ("Requesting " + key + " from port " + value)
                #run obtain_file_data with key, the name of the file, and value, the port 
                self.obtain_file_data(key, int(value))
        
#main body 

#create server threads 
for i in range (peerCount * 3):
    server_thread = ServerHandler(s_sock, i +1)
    server_thread.start()
#create client handler
client_main = ClientHandler(cn_sock, l_addr)
#start requesting files from peers
client_main.begin_all_file_req(peer_table)
