import json
import math

import requests

OLD_API_LIST = 'http://api.citybik.es/networks.json'
NEW_API_LIST = 'http://staging.citybik.es/networks'

def dist(lat1, long1, lat2, long2):
    # Convert latitude and longitude to 
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
        
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
        
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
        
    # Compute spherical distance from spherical coordinates.
        
    # For two locations in spherical coordinates 
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) = 
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
    
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )

    # Remember to multiply arc by the radius of the earth 
    # in your favorite set of units to get length.
    return arc

old_nets = json.loads(requests.get(OLD_API_LIST).text)
new_nets = json.loads(requests.get(NEW_API_LIST).text)
redirects = {}
missing   = []
for net in old_nets:
    if net['name'] not in [n['network']['id'] for n in new_nets['networks']]:
        # Try to find a network in new_nets with a similar lat/lng
        t_lat = net['lat'] / 1E6
        t_lng = net['lng'] / 1E6
        current = None
        for nnet in new_nets['networks']:
            lat = float(nnet['network']['location']['latitude'])
            lng = float(nnet['network']['location']['longitude'])
            if current is None or dist(
                   float(current['location']['latitude']),
                   float(current['location']['longitude']),
                   t_lat, t_lng) > dist(lat,lng,t_lat, t_lng):
                current = nnet['network']
        if current is not None:
            redirects[net['name']] = current['id']
        else:
            missing.append(net['name'])

print json.dumps(redirects, sort_keys = False, indent = 2)
