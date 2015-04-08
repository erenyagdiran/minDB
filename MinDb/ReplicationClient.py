
__author__ = 'orak'

#

# Echo client program

import random
import socket


def listenForDataOnPort(port):
    HOST = ''                 # Symbolic name meaning all available interfaces
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, port))
    while 1:
        s.listen(1)
        print "listening...on " + str(port)
        conn, addr = s.accept()
        print 'Connected by', addr
        while 1:
            data = conn.recv(1024)
            if not data: break
            # conn.sendall(data)
        conn.close()
        print 'got this data...' + data

HOST = '127.0.0.1'    # The remote host
PORT = 50007              # The same port as used by the server
DATALISTENINGPORT = random.randint(1024, 50000) # The port on which client is listening
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall('Hello, world im listening on port ' + str(DATALISTENINGPORT) + ', 1')
data = s.recv(1024)
s.close()
print 'Received data from master', repr(data)
listenForDataOnPort(DATALISTENINGPORT)

