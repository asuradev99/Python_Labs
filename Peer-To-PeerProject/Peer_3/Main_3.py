from socket import *
import threading

#Directory of target file 
file_dir = "/Peer-To-PeerProject/Peer_3/File_3.txt"
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

class ServerHandler(threading.Thread):
    def __init__(self, client_socket, addr):
        self.client_socket = client_socket
        self.addr = addr
    def run(self):
        pass

class ClientHandler ():
    def __init__(self, client_socket, addr):
        #initialize socket 
        self.client_socket = client_socket
        self.addr = addr
    def inform_server(self):
        #process to give file name and port to server so other peers can access it
        #connect to server socket 
        self.client_socket.connect ((self.addr, 3001))
        #send file name and port to server 
        self.client_socket.sendall((str(server_port) + "," + file_dir).encode())
        print ("Peer 3 has delivered it's file to the server")
        #close socket
       
        

client_main = ClientHandler(cn_sock, l_addr)
client_main.inform_server()