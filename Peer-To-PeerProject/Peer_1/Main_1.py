#Server peer 1
from socket import *
import time
import threading
#Directory of target file 
file_dir = "File_1.txt" 
#Initialize dict of target files and their corresponding ports 
peer_table = {}

#number of peers
peerCount = 2
#Socket initialization
server_port = 3001
l_addr = '127.0.0.1'
cn_sock = socket(AF_INET, SOCK_STREAM)
cn_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
cn_sock.bind((l_addr, server_port))

c_sock = socket (AF_INET, SOCK_STREAM)
#Server Hander (multithreaded)
class ServerHandler(threading.Thread):
    def __init__(self, connection_socket, _id):        
        threading.Thread.__init__(self)
        self.connection_socket = connection_socket
        self._id = _id
        

    def run(self):
        #Add file to dict 
        peer_table ["File_1.txt"] = '3001' 
        def format_peer_table():
            k = []
            for key, value in peer_table.items():
                k.append(key)
                k.append(value)
            return ','.join(k)
        def set_peer_table(self):
                #Assuming the client socket is already connected parse recieved data into dict pair
                rcvd_port, rcvd_filename = self.client_socket.recv(48).decode().split(',')
                peer_table[rcvd_filename] = rcvd_port
                print (peer_table)
        def give_peer_table(self):
                if(len(peer_table) == peerCount):
                    self.client_socket.send("REQ ACPT".encode())
                    print ("Thread {} accepted REQ DICT request".format(self._id))
                    self.client_socket.send(format_peer_table().encode())
                else:
                    self.client_socket.send("REQ DENY".encode())
                    print ("Thread {} denied REQ DICT request".format(self._id))
        def send_file(self, _file):
                with open (_file) as f:
                    otpt_f = f.read()
                    self.client_socket.send(otpt_f.encode())
                    print ("Thread {} sent {}".format(self._id, file_dir))
        while True:
            print ("Thread " + str(self._id) + ' ' + "initialized and listening" )
            self.connection_socket.listen(1)
            self.client_socket, self.addr = self.connection_socket.accept()
            print ("Thread {} connected to ".format(self._id) + str(self.addr))
            self.ctrl = self.client_socket.recv(8).decode()
            
            #Control messages
            if self.ctrl == 'ADD FILE':
                print ("Thread {} accepted ADD FILE request".format(self._id))
                set_peer_table(self)
            elif self.ctrl == 'REQ DICT':
                give_peer_table(self)
            elif self.ctrl == 'REQ FILE':
                send_file(self, file_dir)
            time.sleep(1)
            print ("Thread {} resetting socket".format(self._id))
            self.client_socket.close()
class ClientHandler ():
    def __init__(self, client_socket, addr):
        #initialize socket 
        self.client_socket = client_socket
        self.addr = addr
    def obtain_file_data (self, filename, port ):
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect ((self.addr, port))
        self.client_socket.send("REQ FILE".encode())
        print ("retrieving " + filename + " from server")
        with open (filename, 'x') as f:
            f.write(self.client_socket.recv(512).decode())
            f.close()
    def begin_all_file_req(self, table):
        print ("waiting ")
        while len(peer_table) < peerCount: 
           pass
        for key, value in table.items():
            print ("initiating contact")
            if key != file_dir:
                self.obtain_file_data(key, int(value))
        
#main body 

for i in range (peerCount * 3):
    server_thread = ServerHandler(cn_sock, i +1)
    server_thread.start()

client_main = ClientHandler(c_sock, l_addr)
time.sleep(4)
print (peer_table)
client_main.begin_all_file_req(peer_table)