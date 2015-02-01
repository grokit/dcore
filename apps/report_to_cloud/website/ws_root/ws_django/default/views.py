
from django.http import HttpResponse

def index(request):
  
  html = '<html><body><h1>Hello and welcome to a fun fun fun place!</h1><p>If you are not having fun yet, try to put a broad smile on your face. Feeling better? I knew it!</p></body></html>'
  
  return HttpResponse(html)
  