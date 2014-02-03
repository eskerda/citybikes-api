from pymongo import Connection
import json

from api import app
from flask import jsonify, request, render_template, redirect, abort
from models import Network as Network_Model

import models

connection = Connection(app.config['MONGO_HOST'], app.config['MONGO_PORT'])
db = getattr(connection, app.config['MONGO_DB'])
Network = Network_Model(db, connection)
redirects = app.config['REDIRECT']

def handle_redirect_or_notfound(network_id):
    if network_id in redirects:
        return redirect('/networks/%s' % redirects[network_id], 301)
    else:
        abort(404)

@app.before_request
def get_fields():
    app.fields = request.args.get('fields', None)

@app.route('/')
def index():
    networks = Network.find()
    networks = map(lambda network: network.map_data(None), networks)
    return render_template('index.html', networks = networks)

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
    network = Network.find({'_id': network_id})
    if len(network) == 0:
        return handle_redirect_or_notfound(network_id)
    else:
        network = network[0]
    network.Stations()
    response = {
        'network': network.map_data(app.fields)
    }
    return jsonify(response)


