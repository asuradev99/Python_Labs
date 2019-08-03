#Peer 2 
from socket import *
import time
import threading

#Directory of target file 
file_dir = "File_2.txt"

#local peer table
l_peer_table = {}

#Socket initalization
server_port = 3002 
l_addr = '127.0.0.1'  
cn_sock = socket(AF_INET, SOCK_STREAM)
#Server socket initialization
s_sock = socket(AF_INET, SOCK_STREAM)
s_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s_sock.bind((l_addr, server_port))

class ServerHandler(threading.Thread):
    def __init__(self, connection_socket, _id):
        threading.Thread.__init__(self)
        self.connection_socket = connection_socket
        self._id = _id
    def run(self):
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
            if self.ctrl == 'REQ FILE':
                send_file(self, file_dir)
            time.sleep(1)
            print ("Thread {} resetting socket".format(self._id))
            self.client_socket.close()

class ClientHandler ():
    def __init__(self, client_socket, addr):
        #initialize socket 
        self.client_socket = client_socket
        self.addr = addr
    def inform_server(self):
        #process to give file name and port to server so other peers can access it
        #connect to server socket 
        self.client_socket.connect ((self.addr, 3001))
        self.client_socket.send("ADD FILE".encode())
        #send file name and port to server 
        self.client_socket.sendall((str(server_port) + "," + "File_2.txt").encode())
        print ("Peer 2 has delivered it's file to the server")
        self.client_socket.shutdown(SHUT_RDWR)
        self.client_socket.close()

    def obtain_peer_table(self, delay):
        self.rcvd_ctrl = ""
        while self.rcvd_ctrl != "REQ ACPT":
            self.client_socket = socket(AF_INET, SOCK_STREAM)
            self.client_socket.connect ((self.addr, 3001))
            self.client_socket.send ("REQ DICT".encode())
            self.rcvd_ctrl = self.client_socket.recv(8).decode()
            if self.rcvd_ctrl == "REQ ACPT": break
            self.client_socket.shutdown(SHUT_RDWR)
            self.client_socket.close()
            print ("REQ DICT denied, waiting {} seconds: {}".format(delay, self.rcvd_ctrl))
            time.sleep(delay)
            delay *= 2 
        print ("REQ DICT accepted, recieving peer dict")
        table = self.client_socket.recv(256).decode().split(',')
        table = dict(zip(*[iter(table)]*2))
        self.client_socket.shutdown(SHUT_RDWR)
        self.client_socket.close()
        return table
    def obtain_file_data (self, filename, port ):
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect ((self.addr, port))
        self.client_socket.send("REQ FILE".encode())
        print ("retrieving " + filename + " from server")
        with open (filename, 'x') as f:
            f.write(self.client_socket.recv(512).decode())
            f.close()
    def begin_all_file_req(self, table):
        for key, value in table.items():
            if key != file_dir:
                self.obtain_file_data(key, int(value))
for i in range (3):
    server_thread = ServerHandler(s_sock, i+1)
    server_thread.start()

client_main = ClientHandler(cn_sock, l_addr)
client_main.inform_server()
l_peer_table = client_main.obtain_peer_table(1)

client_main.begin_all_file_req(l_peer_table)
print ("done")