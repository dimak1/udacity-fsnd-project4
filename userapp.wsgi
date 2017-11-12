#!/usr/bin/python
import sys 
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/") 
from userapp import app as application

print('Starting app...')
application.secret_key = 'secretkey'
