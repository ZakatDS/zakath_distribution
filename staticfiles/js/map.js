var southWest = L.latLng(-180, -180);
var northEast = L.latLng(180, 180); 

var maxBoundArea = L.latLngBounds(southWest, northEast);

var map = L.map(
    'map', {
        zoomControl:true, 
        maxNativeZoom:28, 
        minZoom:3, 
        maxBounds: maxBoundArea
    }
).setView([20.5937, 78.9629], 4);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);



var markers = []


class Point{
    constructor(lat, lng){
        this.lat = lat;
        this.lng = lng;
        this.marker = L.marker([this.lat, this.lng]);
    }


    mark(){
        this.marker.addTo(map)
        return this.marker;
    }

    markOne(){

        if (markers.length >= 1){
            markers.forEach(marker => {
                marker.remove()
            })
            markers = []
        }
        this.mark()

        markers.push(this.marker)

    }

    remove(){
        this.marker.remove()
    }

    bindPopup(text, point){
        point.bindPopup(text).addTo(map)
    }
}

var currentLocation = {
    'lat': 0,
    'lng': 0
}

map.on('dblclick', (e) => {
    var point = new Point(e.latlng.lat, e.latlng.lng);
    point.markOne()

    currentLocation['lat'] = e.latlng.lat
    currentLocation['lng'] = e.latlng.lng
})



function markCurrentLocation(){
    let location = null;
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;
            location = {
            'lat': latitude,
            'lng': longitude,
            }
            currentLocation = location;
            map.setView([location['lat'], location['lng']], 13)
            let point = new Point(location['lat'], location['lng'])
            point.markOne()
        });
        
        } else {
        alert("Geolocation is not supported by this browser.");
        }
}


let getMyLocation = document.getElementById('getMyLocation')
let submitMyLocation = document.getElementById('submitMyLocation')

getMyLocation.onclick = markCurrentLocation

submitMyLocation.onclick = function(e) {
    e.preventDefault()
    let form = document.getElementById('locationForm')
    let inputLat = document.getElementById('lat')
    let inputLng = document.getElementById('lng')
    inputLat.value = currentLocation['lat']
    inputLng.value = currentLocation['lng']
    form.submit()
}
