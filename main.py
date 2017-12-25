from g import app
from views import *

import argparse
import os

# pass args
parser = argparse.ArgumentParser("Monica Test System")
parser.add_argument("--addr", help="IP address of this server",
                    type=str, default="0.0.0.0")
parser.add_argument("--port", help="port number used for this server",
                    type=int, default=5001)
args = parser.parse_args()

# start Flask
debug = False 
threaded = True
app.run(host=args.addr, port=args.port, debug=debug, threaded=threaded)

