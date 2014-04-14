import json

DEBUG = True
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DB = 'citybikes'
PORT = 5051
REDIRECT = json.loads(open('redirects.json', 'r').read())
PREFIX = '' # ie: /v2 for http://api.citybik.es/v2/networks
ENDPOINT = 'http://api.citybik.es'
