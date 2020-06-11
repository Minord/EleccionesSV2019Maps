import 'ol/ol.css';
import {Map, View} from 'ol';
import TileLayer from 'ol/layer/Tile';
import OSM from 'ol/source/OSM';
import Source from 'ol/source/Source';
import Vector from 'ol/layer/Vector'

import {Fill, Circle, Style, Stroke} from 'ol/style';
import TileGrid from 'ol/tilegrid/TileGrid';
import { toStringHDMS } from 'ol/coordinate';


//This is a builder for create a Map

class MapBuilder{

    constructor(target_name){
        this.map = new Map({
            target : target_name
        });
    }

    buildCoastLine(){
        //index 0
        coastLineLayer = new Vector({
            
        });
        this.map.addLayer();
    }

    buildBorderLine(){
        //index 1
    }
    buildCountyBackGround(){
        //index 2
    }

    addCantonLayer(){  
        //index 6
    }
    addMunicLayer(){   // Transparent  -- RuledColored
        //Index 5
    }
    addDepLayer(){ // Transparent  -- RuledColored
        //Index 4
    }

    addSymbolizeRule(type, style){ // Add a Fill Rule
        //change Munic or Layer Style
    }
    addHoverControl(type, style){  // Add Hover Control
        //register an event on map
    }

    addDepNames(){
        //index 10
    }
    addMunicNames(){
        //index 11
    }

    addImportantCities(){
        //index 12 and 13 for labels
    }
    addNormalCities(){
        //index 14 and 15 for labels
    }
}