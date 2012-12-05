# -*- coding: utf-8 -*-
# Copyright (C) 2010-2012, eskerda <eskerda@gmail.com>
# Distributed under the AGPL license, see LICENSE.txt

import json
from datetime import datetime
from bson.objectid import ObjectId

class Document(object):
    
    __collection__ = None
    data = {}

    def __init__(self, db, connection, data = {}):
        self.collection = getattr(db, self.__collection__)
        self.connection = connection
        self.db = db
        self.data = data

    def __getattr__(self, attr):
        if attr in self.data:
            return self.data[attr]
        else:
            err = '\'%s\' object has no attribute \'%s\'' % (self.__class__.__name__, attr)
            raise AttributeError(err)

    def save(self, safe=True, *args, **kwargs):
        return self.collection.save(self.data, safe, *args, **kwargs)

    def find(self, *args, **kwargs):
        results = self.collection.find(*args, **kwargs)
        return map(lambda data: self.__class__(self.db, self.connection, data), results)

    def map_data(self):
        return self.data

    def read(self, id):
        self.data = self.collection.find_one({'_id': id})

class Stat(Document):
    __collection__ = 'station_stats'
    __public_name__ = 'stat'

class Station(Document):
    __collection__ = 'stations'
    __public_name__ = 'station'

    def map_data(self, fields = None):
        result = {
            'id': self._id,
            'name': self.name,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'bikes': self.last_stat['bikes'],
            'slots': self.last_stat['free'],
            'timestamp': self.last_stat['timestamp'].isoformat()
        }
        return { self.__public_name__: result }

class Network(Document):
    __collection__ = 'systems'
    __public_name__ = 'network'
    stations = None

    def Stations(self):
        sModel = Station(self.db, self.collection)
        self.stations = sModel.find({'network_id': self._id})

    def map_data(self, fields = None):
        result = {
            'id': self._id,
            'name': self.name,
            'location': {
                'city': self.city,
                'country': self.country,
                'latitude': self.latitude,
                'longitude': self.longitude
            },
            'company': self.data['company'],
            'href': '/networks/{0}'.format(self._id)
        }
        if self.stations is not None:
            result['stations'] = map(lambda station: station.map_data(), self.stations)

        return {self.__public_name__: {
                        key: value for (key, value) in result.iteritems() 
                            if fields is None or key in fields
                    }}


class GeneralPurposeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, ObjectId):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


class ModelEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Document):
            return json.dumps({obj.__public_name__: obj.map_data(['name'])}, cls = GeneralPurposeEncoder)
        return json.JSONEncoder.default(self, obj)