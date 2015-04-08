__author__ = 'orak'

import web
import shelve

from GlobalVariables import *



class DB:
    # database = {}
    database = shelve.open("MyDatabase")
    global testq

    def get_key(self, key):
        try:
            return self.database[key]
        except KeyError:
            web.notfound()

    def put_key(self, key, value):
        item = {}
        item['cmd'] = "PUT"
        item['key'] = key
        item['value'] = value
        # testq.put(item)
        # print testq
        self.sendToServers(item)
        self.database[key] = value

    def delete_key(self, key):
        try:
            item = {}
            item['cmd'] = "DELETE"
            item['key'] = key
            testq.put(item)

            # del(self.database[key])
            del self.database[key]
        except KeyError:
            web.notfound()

    def keys(self):
        # return self.database.iterkeys()
        return self.database.iterkeys()

    def sendToServers(self, data):
        print data
        # global GlobalVariablesClass
        # print GlobalVariablesClass.replicationServerConnections
        gv = GlobalVariables()
        k = gv.retreiveAllKeys()
        print k
'''
import shelve

d = shelve.open(filename) # open -- file may get suffix added by low-level
# library

d[key] = data   # store data at key (overwrites old data if
# using an existing key)
data = d[key]   # retrieve a COPY of data at key (raise KeyError if no
# such key)
del d[key]      # delete data stored at key (raises KeyError
# if no such key)
flag = d.has_key(key)   # true if the key exists
klist = d.keys() # a list of all existing keys (slow!)

# as d was opened WITHOUT writeback=True, beware:
d['xx'] = range(4)  # this works as expected, but...
d['xx'].append(5)   # *this doesn't!* -- d['xx'] is STILL range(4)!

# having opened d without writeback=True, you need to code carefully:
temp = d['xx']      # extracts the copy
temp.append(5)      # mutates the copy
d['xx'] = temp      # stores the copy right back, to persist it

# or, d=shelve.open(filename,writeback=True) would let you just code
# d['xx'].append(5) and have it work as expected, BUT it would also
# consume more memory and make the d.close() operation slower.

d.close()       # close it
'''