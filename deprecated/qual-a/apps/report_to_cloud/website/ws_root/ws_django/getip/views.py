
import json
import time

from django.http import HttpResponse

def getip(request):
    
    if request.method == 'GET':
        
        ip = request.META['REMOTE_ADDR']
        return HttpResponse( '<h2>ip=|%s|</h2>' % ip )
    
    elif request.method == 'POST':
        return HttpResponse( 'Please do not post here, post at your local post office.' )
        
    
