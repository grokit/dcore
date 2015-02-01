
from google.appengine.ext import db

from django import forms

import time
import json 

class P2PInfo(db.Model):
    
    # https://developers.google.com/appengine/docs/python/datastore/typesandpropertyclasses
    # name and date are required for server-side processing (ordering and selecting)    
    name = db.StringProperty(required=False, multiline=False)
    date = db.FloatProperty(required=False)
    # All user data here.    
    data = db.StringProperty(required=False, multiline=False)

def getRecentP2P():
    
    # https://developers.google.com/appengine/docs/python/datastore/queryclass
    query = P2PInfo.all()
    query.order('-date')
    it = query.run()

    ul = []
    
    for u in it:
        try:
            data = json.loads( u.data )
            ul.append( data )
        except:
            pass
    
    return ul

def save(name, jsonD):
    
    q = P2PInfo.all()
    q.filter("name ==", name)
    
    person = []
    for p in q.run():
        db.delete(p)
    
    # Add
    jsonD['time'] = time.time()
    ljson = json.dumps(jsonD)
    e = P2PInfo(name = name, date = jsonD['time'], data = ljson)
    e.put()
  
def cleanSlate():
    
    query = P2PInfo.all()
    it = query.run()
    
    for u in it:
        db.delete(u)

