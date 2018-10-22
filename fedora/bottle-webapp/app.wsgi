#!/usr/bin/env python

import os
# Change working directory so relative paths (and template lookup) work again
os.chdir(os.path.dirname(__file__))

import sys
sys.path.insert(0, "/var/local/www/python/keeping-data-alive/fedora/bottle-webapp")

import bottle
# ... build or import your bottle application here ...
# Do NOT use bottle.run() with mod_wsgi
from fedora import app
application = app
