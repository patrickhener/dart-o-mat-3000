import os
# Custom IP and Port Config, needed for example in QR Code generation
IPADDR = '192.168.1.160'  # QRCode IP
IFACE = '0.0.0.0'  # Server Interface IP
PORT = 5000
RECOGNITION = False  # Use Recognition or not. If not you will have buttons to insert Score in gameController
SOUND = False  # Sound output if you want
# Babel default settings
BABEL_DEFAULT_LOCALE = "de"
BABEL_DEFAULT_TIMEZONE = "UTC"

# Statement for enabling the development environment
DEBUG = True
TESTING = True

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database - we are working with
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app/mod_game/database.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Secret Keys
SECRET_KEY = b'J\xd1\xd0:Y\xb3\xce\x04\xc7\xc0\x1f\xa2p\x88\xd9\x04'
