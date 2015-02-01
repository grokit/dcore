from django.conf.urls import *

import settings

urlpatterns = patterns('',
  (r'^share_ip$', 'ws_django.p2p.views.share_ip'),
  (r'^getip$', 'ws_django.getip.views.getip'),
  (r'^share_ip/html$', 'ws_django.p2p.views.display_in_html'),
  (r'^share_ip/clear$', 'ws_django.p2p.views.clear_db'),
  (r'^$', 'ws_django.default.views.index'),
  (r'^jsonp.*$', 'ws_django.p2p.views.share_ip'),
)

# Mirror what would happen with google app engine on local mode
if settings.DEBUG:
  urlpatterns += patterns('',
      (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '../static'}),
  )
