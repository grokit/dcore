
import json
import time

import models

from django.http import HttpResponse

def renderJsonNode(lJson, sb):
    reportTime = lJson['time'] 
    name = lJson['name']
    timezoneAdjust = -60*60*7

    olStatus = '<font color="#CC0000">OFFLINE</font>'

    if abs(time.time() - reportTime) < 240:
        olStatus = '<font color="#FF9900">ONLINE?</font>'
    if abs(time.time() - reportTime) < 120:
        olStatus = '<font color="#33CC33">ONLINE</font>'
    
    sb.append("<li><b>%s:</b> %s <b>(%s)</b>\n" % (name, time.strftime('%Y-%m-%d %H:%M %Ss', time.localtime(timezoneAdjust + reportTime)), olStatus))
    sb.append("<ul>\n")

    for (k, v) in lJson.items():
        sb.append("<li>%s: %s</li>\n" % (k, v))
    
    sb.append("</ul>\n")
    sb.append('</br>\n')

    return sb

def display_in_html(request, param = ''):
    
    
    rP2P = models.getRecentP2P()
    
    sb = []
    sb.append('<html><body>\n')
    sb.append('<ul>\n')

    for lJson in rP2P:

        lJson['client_ip'] = request.META['REMOTE_ADDR']

        try:
            renderJsonNode(lJson, sb)
        except Exception as e:
            sb.append('Error: could not html-render: %s. Exception: %s.</br>' % (lJson, e))

    sb.append('</ul>\n')
    sb.append('</body></html>\n')
    
    html = "".join(sb)

    return HttpResponse( html )

def clear_db(request):
    models.cleanSlate()
    return HttpResponse( '<h1>Cleared DB</h1>' )
  
def share_ip(request):
    
    if request.method == 'GET':
        
        rP2P = models.getRecentP2P()
        return HttpResponse( json.dumps(rP2P) )
    
    elif request.method == 'POST':
        
        jsp = json.loads(request.POST.keys()[0])
        models.save( jsp['name'], jsp )

        return HttpResponse( 'POST OK' )
        
    
