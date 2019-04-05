# Custom IP and Port Config, needed for example in QR Code generation
IPADDR = '0.0.0.0'
PORT = 5000

# Statement for enabling the development environment
DEBUG = True
TESTING = True

# Define the application directory
import os
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
CSRF_SESSION_KEY = b'\xb2\xbf\x94\xbc\xc4\xacr\xbcH\xb6\xc2s^im\xa4\xbb\x7f\xaa\xdax\xbbG'

# Cookie setup
SESSION_COOKIE_NAME = "darts_session"
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'Lax'

# Security Setup
CSRF_ENABLED = True
