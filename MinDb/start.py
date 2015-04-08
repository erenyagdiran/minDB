#!/usr/bin/python 

from __future__ import with_statement 
import re
import uuid
import json
from DB import *
from MinDb.ServerListener import ServerListener

VALID_KEY = re.compile('[a-zA-Z0-9_-]{1,255}')

urls = ('/(.*)', 'RequestHandler')

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


class RequestHandler:

    def GET(self, name):
        if len(name) <= 0:
           keys = {}
           keysToJson = []
           # for key in self.keys():
           db = DB()
           for key in db.keys():
                keysToJson.append(key)
           keys['keys'] = keysToJson
           return json.dumps(keys)
        else:
            return self.get_resource(name)
           
    @validate_key
    def POST(self, name):
        # print "my data is:"
        # print web.ctx.globals.counter.replicationServerConnections
        data = web.data()
        db = DB()
        db.put_key(str(name), data)
        return json.dumps(str(name))

    @validate_key
    def DELETE(self, name):
        db = DB()
        db.delete_key(str(name))
        
    def PUT(self, name=None):
        key = str(uuid.uuid4())
        db = DB()
        db.POST(key)
        print key
        return json.dumps(key)

    @validate_key
    def get_resource(self, name):
        db = DB()
        result = db.get_key(str(name))
        if result is not None: 
            print result
            return json.dumps(result)

# def add_global_hook():
#     global GlobalVariables
#     g = web.storage({"counter": GlobalVariables})
#     def _wrapper(handler):
#         web.ctx.globals = g
#         return handler()
#     return _wrapper


if __name__ == "__main__":
    # global GlobalVariablesClass
    # print globals()['shared'] = GlobalVariablesClass
    app = web.application(urls, globals())
    # app.add_processor(add_global_hook())

    print "Min-db is now listening"

    listenerThread = ServerListener()
    listenerThread.start()

    print "server exiting"

    app.run()
