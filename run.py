#!/usr/bin/env python3
from app import app, socketio, IFACE, PORT
from flask_socketio import SocketIO
import eventlet

eventlet.monkey_patch()

socketio.run(app, host=IFACE, port=PORT)
