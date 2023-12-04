'use strict';

const map = L.map('map').setView([60.31, 24.94], 13);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 16,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

const marker = L.marker([60.31, 24.94]).addTo(map);

const popup = L.popup();

function onMapClick(event) {
    popup
        .setLatLng(event.latlng)
        .setContent('Coordinates: ' + event.latlng)
        .openOn(map);
}

map.on('click', onMapClick);

L.Control.geocoder().addTo(map);

const geocoder = {
  defaultMarkGeocode: false
}
  .on('markgeocode', function(event) {
    const searched = event.geocode.searched;
    const marker = L.marker
  .addTo(map);
  });



