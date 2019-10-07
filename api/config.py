import json
from os import environ

DEBUG = environ.get('DEBUG', 'False') == 'True'
MONGO_HOST = environ.get('MONGODB_HOST', 'localhost')
MONGO_USER = environ.get('MONGODB_USER', None)
MONGO_PASSWORD = environ.get('MONGODB_PASSWORD', None)
MONGO_PORT = int(environ.get('MONGODB_PORT', 27017))
MONGO_DB = environ.get('MONGODB_DATABASE', 'citybikes')
PORT = int(environ.get('PORT', 5051))
REDIRECT = json.loads(open('redirects.json', 'r').read())
PREFIX = ''  # ie: /v2 for http://api.citybik.es/v2/networks
ENDPOINT = environ.get('ENDPOINT', 'http://api.citybik.es')
