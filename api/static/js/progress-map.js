$(function() {
    var purpleIcon = L.icon({
    iconUrl: '/static/img/purple-pin.png',
        iconSize:     [10, 20], // size of the icon
        iconAnchor:   [6, 20], // point of the icon which will correspond to marker's location
        popupAnchor:  [0, -24] // point from which the popup should open relative to the iconAnchor
    })

    var greenIcon = L.icon({
    iconUrl: '/static/img/green-pin.png',
        iconSize:     [10, 20], // size of the icon
        iconAnchor:   [6, 20], // point of the icon which will correspond to marker's location
        popupAnchor:  [0, -24] // point from which the popup should open relative to the iconAnchor
    })

    var redIcon = L.icon({
    iconUrl: '/static/img/yellow-pin.png',
        iconSize:     [10, 20], // size of the icon
        iconAnchor:   [6, 20], // point of the icon which will correspond to marker's location
        popupAnchor:  [0, -24] // point from which the popup should open relative to the iconAnchor
    })

    var map = L.map('progress-map').setView([30, 0], 2)
    L.mapbox.tileLayer('eskerda.map-btpzyfuk', {
        attribution: '<a href="http://mapbox.com">'
                   + 'MapBox</a> contributors'
    }).addTo(map)

    function getOldNetworks() {
        return $.ajax(
            'http://api.citybik.es/networks.json',
            { dataType: 'jsonp' }
        ).pipe(function(data){
            return data
        })
    }

    function getNewNetworks() {
        return $.get('/networks').pipe(function(data){
            return data
        })
    }

    $.when(
        getOldNetworks(),
        getNewNetworks()
    ).done(function(oldData, newData){
        // Compare both data feeds
        var done  = []
        var todo  = []
        var latDif = 0.25
        var lngDif = 0.25
        _.each(oldData, function(network) {
            var lat = network.lat / 1E6
            var lng = network.lng / 1E6
            var found = false
            for (var i = 0; i < newData.networks.length && !found; i++) {
                var newnet = newData.networks[i]
                var newlat = newnet.network.location.latitude
                var newlng = newnet.network.location.longitude

                found = (
                    (newlat >= lat-latDif && newlat <= lat+latDif)
                    &&
                    (newlng >= lng-lngDif && newlng <= lng+lngDif)
                )
            }
            if (!found) {
                todo.push(network)
            } else {
                done.push(newData.networks[i-1])
                newData.networks.splice(i-1, 1)
            }
        })

        var todo_layer = L.layerGroup([])
        var done_layer = L.layerGroup([])
        var new_layer = L.layerGroup([])

        _.each(todo, function(net) {
            var popup = "<ul>" +
                        "<li class='network'>"+net.name+"</li>" +
                        "</ul>"
            L.marker([net.lat/1E6,
                      net.lng/1E6],
                      {icon: redIcon}).addTo(todo_layer)
                    .bindPopup(popup, {className: 'dark-popup network-popup'})
        })

        _.each(done, function(net) {
            var popup = "<ul>" +
                        "<li class='city'>"+net.network.location.city+"</li>" +
                        "<li class='network'>"+net.network.name+"</li>" +
                        "</ul>"
            L.marker([net.network.location.latitude,
                      net.network.location.longitude],
                      {icon: purpleIcon}).addTo(done_layer)
                    .bindPopup(popup, {className: 'dark-popup network-popup'})
        })

        _.each(newData.networks, function(net) {
            var popup = "<ul>" +
                        "<li class='city'>"+net.network.location.city+"</li>" +
                        "<li class='network'>"+net.network.name+"</li>" +
                        "</ul>"
            L.marker([net.network.location.latitude,
                      net.network.location.longitude],
                      {icon: greenIcon}).addTo(new_layer)
                    .bindPopup(popup, {className: 'dark-popup network-popup'})
        })

        todo_layer.addTo(map)
        done_layer.addTo(map)
        new_layer.addTo(map)

        L.control.layers({},{
            'New': new_layer,
            'Ported': done_layer,
            'Not Ported (yet)': todo_layer
        }).addTo(map)
    })
})
