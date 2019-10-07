from pymongo import Connection
import json

from api import app
from flask import jsonify, request, render_template, redirect, abort
from models import Network as Network_Model
from models import Nearby as Nearby_Model

import models
import config

connection = Connection(app.config['MONGO_HOST'], app.config['MONGO_PORT'])
db = getattr(connection, app.config['MONGO_DB'])
Network = Network_Model(db, connection)
Nearby = Nearby_Model(db, connection)
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
    endpoint = config.ENDPOINT
    prefix   = config.PREFIX
    return render_template('index.html', networks = networks,
                           endpoint = endpoint, prefix = prefix)


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

@app.route('/near/', methods = ['GET'])
@app.route('/near', methods = ['GET'])
def get_near():
    longitude = request.args.get('longitude', None)
    latitude = request.args.get('latitude', None)
    distance = request.args.get('distance', 500)

    if longitude is None or latitude is None:
        return jsonify({
            'error': 'Please specify both longitude and latitude parameters'
        }), 400
    
    try:
        longitude = float(longitude)
        latitude = float(latitude)
        distance = int(distance)
    except ValueError:
        return jsonify({
            'error': 'Longitude and latitude should be float and distance should be an integer'
        }), 400

    Nearby.near(longitude, latitude, distance)
    return jsonify(Nearby.map_data(app.fields))
