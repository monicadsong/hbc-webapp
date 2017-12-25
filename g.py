"""
Global variables with initialization and configuration
"""
from flask import Flask
#from flask_autoindex import AutoIndex

import os

# flask application object
app = Flask(__name__)
app.config.from_object('config')
