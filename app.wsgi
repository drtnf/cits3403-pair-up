#! /usr/bin/python3.6

import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/home/tim/CITS3403/cits3403-pair-up/')
from app import app
app.secret_key = 'sshh!'
