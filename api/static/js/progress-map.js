$(function() {
    var netIcon = L.icon({
    iconUrl: '/static/img/purple-pin.png',
        iconSize:     [10, 20], // size of the icon
        iconAnchor:   [6, 20], // point of the icon which will correspond to marker's location
        popupAnchor:  [0, -24] // point from which the popup should open relative to the iconAnchor
    })
    var map = L.map('progress-map').setView([30, 0], 2)
    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">'
                   + 'OpenStreetMap</a> contributors'
    }).addTo(map)
    $.get('/networks', function(data){
        _.each(data.networks, function(net) {
            var popup = "<ul>" +
                        "<li class='city'>"+net.network.location.city+"</li>" +
                        "<li class='network'>"+net.network.name+"</li>" +
                        "</ul>"
            L.marker([net.network.location.latitude,
                      net.network.location.longitude],
                      {icon: netIcon}).addTo(map)
                    .bindPopup(popup, {className: 'dark-popup network-popup'})
        })
    })
})