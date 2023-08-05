import os, errno
BASE_DIR=os.path.dirname(os.path.abspath(__file__))
LOGGER_CONFIG = os.path.join(os.path.dirname(BASE_DIR), 'logger.conf')
try:
    os.makedirs('~/.network-analyzer/logs')
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

import logging
import logging.config
print "Logger config location", LOGGER_CONFIG
logging.config.fileConfig(LOGGER_CONFIG)
logger = logging.getLogger(__name__)
logger.info("Loaded " + __name__)

from rpc_apiserver import app, methods
from flask_socketio import SocketIO
# from jsonrpcserver.response import NotificationResponse
socketio = SocketIO(app)

import socketio_server.server