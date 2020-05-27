import 'ol/ol.css';
import Map from 'ol/Map';
import View from 'ol/View';
import GeoJSON from 'ol/format/GeoJSON';


var map = new Map({
    target: 'map',
    layers: [
      new ol.layer.Tile({
        source: new ol.source.OSM()
      })
    ],
    view: new View({
      center: ol.proj.fromLonLat([-88.85, 13.75]),
      zoom: 8.5
    })
});