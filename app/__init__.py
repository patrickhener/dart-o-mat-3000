# Import flask and template operators, as well socketio
from flask import Flask, render_template
from flask_socketio import SocketIO

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Import Minify
from flask_minify import minify

# Define the WSGI application object
app = Flask(__name__)

# Grab Configuration from config.py
app.config.from_object('config')
IPADDR = app.config["IPADDR"]
PORT = app.config["PORT"]

# Define SocketIO
socketio = SocketIO(app)

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Minify Things
minify(app=app, html=True, js=True, cssless=True, cache=True, fail_safe=True)

# HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_game)
from app.mod_game.controllers import mod_game as game_module

# Register blueprint(s)
app.register_blueprint(game_module)

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()
