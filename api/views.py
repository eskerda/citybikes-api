from pymongo import Connection
import json

from api import app
from flask import jsonify, request, render_template
from models import Network as Network_Model

import models

connection = Connection(app.config['MONGO_HOST'], app.config['MONGO_PORT'])
db = getattr(connection, app.config['MONGO_DB'])
Network = Network_Model(db, connection)

@app.before_request
def get_fields():
    app.fields = request.args.get('fields', None)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/networks/', methods = ['GET'])
@app.route('/networks', methods = ['GET'])
def list_networks():
    networks = Network.find()
    response = {
        'networks': map(lambda network: network.map_data(app.fields), networks)
    }
    return jsonify(response)

@app.route('/networks/<network_id>', methods = ['GET'])
def get_network(network_id):
    network = Network.find({'_id': network_id})[0]
    network.Stations()
    return jsonify(network.map_data(app.fields))


