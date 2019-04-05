#!/usr/bin/env python3
from app import app, socketio, IPADDR, PORT
from flask_socketio import SocketIO
import eventlet

eventlet.monkey_patch()

socketio.run(app, host=IPADDR, port=PORT)
