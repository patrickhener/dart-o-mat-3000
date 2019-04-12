# Import flask and template operators, as well socketio
from flask import Flask, render_template
from flask_socketio import SocketIO

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Babel for translations
from flask_babel import Babel

# Import a module / component using its blueprint handler variable (mod_game)
from app.mod_game.controllers import mod_game as game_module

# Define the WSGI application object
app = Flask(__name__)

# Grab Configuration from config.py
app.config.from_object('config')
IPADDR = app.config["IPADDR"]
IFACE = app.config["IFACE"]
PORT = app.config["PORT"]
RECOGNITION = app.config["RECOGNITION"]
SOUND = app.config["SOUND"]

# Define SocketIO
socketio = SocketIO(app)

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Babel for translation
babel = Babel(app)

# HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


# Register blueprint(s)
app.register_blueprint(game_module)

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()
