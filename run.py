#!/usr/bin/env python3
from dom import app, socketio, IFACE, PORT
import eventlet

eventlet.monkey_patch()

if __name__ == "__main__":
    socketio.run(app, host=IFACE, port=PORT)
