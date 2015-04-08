
__author__ = 'orak'
import threading
import socket
from GlobalVariables import *



class ServerListener (threading.Thread):

    def run(self):
        print "Starting " + self.name
        listenForClients()
        print "Exiting " + self.name

def listenForClients():
    HOST = ''                 # Symbolic name meaning all available interfaces
    PORT = 50007              # Arbitrary non-privileged port
    global replicationServerConnections
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    while 1:
        data2 = ''
        s.listen(1)
        print "listening...on 50007"
        conn, addr = s.accept()
        print 'Connected by', addr
        while 1:
            data = conn.recv(1024)
            if not data: break
            data2 += data
            conn.sendall(data)
        conn.close()
        print 'going to save data in global list... ' + data2
        # print globals()
        gv = GlobalVariables()
        gv.saveIdAddr("1", addr(0),data2)
        GlobalVariables.replicationServerConnections.append({addr,data2})
