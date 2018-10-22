#!/usr/bin/env python

import bottle
import os
import sys

# Change working directory so relative paths (and template lookup) work again
os.chdir(os.path.dirname(__file__))

sys.path.insert(0, "/var/local/www/python/keeping-data-alive/fedora/bottle-webapp")
from fedora import app

app.run(debug=True, host="localhost", port=3000, reloader=True)
