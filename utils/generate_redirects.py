import json

import requests

OLD_API_LIST = 'http://api.citybik.es/networks.json'
NEW_API_LIST = 'http://staging.citybik.es/networks'
LAT_DIF = 0.25
LNG_DIF = 0.25

old_nets = json.loads(requests.get(OLD_API_LIST).text)
new_nets = json.loads(requests.get(NEW_API_LIST).text)
redirects = {}
missing   = []
for net in old_nets:
    if net['name'] not in [n['network']['id'] for n in new_nets['networks']]:
        # Try to find a network in new_nets with a similar lat/lng
        t_lat = net['lat'] / 1E6
        t_lng = net['lng'] / 1E6
        for nnet in new_nets['networks']:
            lat = nnet['network']['location']['latitude']
            lng = nnet['network']['location']['longitude']
            found = ((lat >= t_lat - LAT_DIF and lat <= t_lat + LAT_DIF) and (lng >= t_lng - LNG_DIF and lng <= t_lng + LAT_DIF))
            if found:
                redirects[net['name']] = nnet['network']['id']
                break
        if not found:
            missing.append(net)

print json.dumps(redirects)
