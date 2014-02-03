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

    var map = L.map('map').setView([30, 0], 2)
    L.mapbox.tileLayer('eskerda.map-btpzyfuk', {
        attribution: '<a href="http://mapbox.com">'
                   + 'MapBox</a> contributors'
    }).addTo(map)

    function getNetworks() {
        return $.get('/networks').pipe(function(data){
            return data
        })
    }

    $.when(getNetworks()).done(function(networks){
        var net_layer = L.layerGroup([])

        _.each(networks.networks, function(net) {
            var popup = "<ul>" +
                        "<li class='city'>"+net.location.city+"</li>" +
                        "<li class='network'>"+net.name+"</li>" +
                        "</ul>"
            L.marker([net.location.latitude,
                      net.location.longitude],
                      {icon: purpleIcon}).addTo(net_layer)
                    .bindPopup(popup, {className: 'dark-popup network-popup'})
        })

        net_layer.addTo(map)
    })
})
