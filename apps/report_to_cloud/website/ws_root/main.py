import logging
import os
import sys

# Remove the standard version of Django 
for k in [k for k in sys.modules if k.startswith('django')]: 
    del sys.modules[k] 

# Must set this env var before importing any part of Django
# 'project' is the name of the project created with django-admin.py
os.environ['DJANGO_SETTINGS_MODULE'] = 'ws_django.settings'

import django.core.handlers.wsgi
import django.core.signals
import django.db
import django.dispatch.dispatcher

# Google App Engine imports.
from google.appengine.ext.webapp import util

# Force Django to reload its settings.
from django.conf import settings
settings._target = None

def log_exception(*args, **kwds):
    logging.exception('Exception in request:')

# Log errors.
django.dispatch.Signal.connect(
   django.core.signals.got_request_exception, log_exception)

# Unregister the rollback event handler.
django.dispatch.Signal.disconnect(
django.core.signals.got_request_exception,
django.db._rollback_on_exception)

def main():
    # Create a Django application for WSGI.
    application = django.core.handlers.wsgi.WSGIHandler()

    # Run the WSGI CGI handler with that application.
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
