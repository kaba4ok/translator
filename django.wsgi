# encoding: utf-8

import os, sys

virtual_env = os.path.expanduser('~/venv/translator')
activate_this = os.path.join(virtual_env, 'bin/activate_this.py')
execfile(activate_this, dict(__file__=activate_this))

sys.path.insert(0, os.path.join(os.path.expanduser('~'), 'django/translator'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'translator.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
