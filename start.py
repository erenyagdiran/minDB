#!/usr/bin/python 

from __future__ import with_statement 
import web
import re
import os
import shelve
import uuid
import json

VALID_KEY = re.compile('[a-zA-Z0-9_-]{1,255}')

urls = (
        '/(.*)', 'MemoryDB',
        )

def is_valid_key(key):
    if VALID_KEY.match(key) is not None:
        return True
    return False
    
def validate_key(fn):
    def new(*args):
        if not is_valid_key(args[1]):
            web.badrequest()
        return fn(*args)
    return new

class AbstractDB(object):
    def GET(self, name):
        if len(name) <= 0:
           keys = {}
           keysToJson = []
           for key in self.keys():
              keysToJson.append(key)     
           keys['keys'] = keysToJson
           return json.dumps(keys)
        else:
            return self.get_resource(name)
           
    @validate_key
    def POST(self, name):
        data = web.data()
        self.put_key(str(name), data)
        return json.dumps(str(name))

    @validate_key
    def DELETE(self, name):
        self.delete_key(str(name))
        
    def PUT(self, name=None):
        key = str(uuid.uuid4())
        self.POST(key)
        print key
        return json.dumps(key)

    @validate_key
    def get_resource(self, name):
        result = self.get_key(str(name))
        if result is not None: 
            print result
            return json.dumps(result)
        
class MemoryDB(AbstractDB):
    database = {}
    def get_key(self, key):
        try:
            return self.database[key]
        except KeyError:
            web.notfound()
            
    def put_key(self, key, data):
        self.database[key] = data
    
    def delete_key(self, key):
        try:
            del(self.database[key])
        except KeyError:
            web.notfound()
    
    def keys(self):
        return self.database.iterkeys()


import asyncore, socket
class Replicator(asyncore.dispatcher):

    def __init__(self, host,port, path):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect( (host, port) )
        self.buffer = 'GET %s HTTP/1.0\r\n\r\n' % path

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()

    def handle_read(self):
        print self.recv(8192)

    def writable(self):
        return (len(self.buffer) > 0)

    def handle_write(self):
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]
  
    def rest_get(self):
    def rest_post(self):
    def rest_delete(self):
    def rest_put(self):


def print_banner():
   banner='\033[94m' + '''                   (           
                   )\ )    (   
    )    (        (()/(  ( )\  
   (     )\   (    /(_)) )((_) 
   )\  '((_)  )\ )(_))_ ((_)_  
 _((_))  (_) _(_/( |   \ | _ ) 
| '  \() | || ' \))| |) || _ \ 
|_|_|_|  |_||_||_| |___/ |___/ 
''' + '\033[0m'
   print banner                            

def async_task():
   print "Async job starts"
   client = Replicator('www.python.org',80,'/')
   client2 = Replicator('www.python.org',80,'/')
   asyncore.loop()

if __name__ == "__main__":
    print_banner() 
    app = web.application(urls, globals())
    print "Min-db is now listening"
    import threading
    threads=[]
    t = threading.Thread(target=async_task)
    threads.append(t)
    t.start()
    app.run()
