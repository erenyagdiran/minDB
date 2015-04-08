__author__ = 'orak'

import  shelve

class GlobalVariables():
    replicationServerConnections = []

    # addressDatabase = shelve.open("MyClientsAddressDatabase")

    def saveIdAddr(self, name, addr,port):
        addressDatabase = open('workfile', 'w')
        addressDatabase.write(str(name) + ',' + str(addr) + '\n')
        # self.addressDatabase[name] = addr
        # self.addressDatabase.sync()

    def retreiveAllKeys(self):
        # return self.addressDatabase.readlin
        addressDatabase = open('workfile', 'r')
        k = addressDatabase.readline()
        return k