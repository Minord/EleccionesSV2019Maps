import 'ol/ol.css';
import {Map, View} from 'ol';
import TileLayer from 'ol/layer/Tile';
import OSM from 'ol/source/OSM';
import Source from 'ol/source/Source';

import {Fill, Circle, Style, Stroke} from 'ol/style';
import TileGrid from 'ol/tilegrid/TileGrid';
import { toStringHDMS } from 'ol/coordinate';



//Direccion del servidor
var server_name = "http://127.0.0.1:5000"


//Fuentes
class SourcesIndex{
  
  costructor(){
    this.departamentos = null;
    this.municipios = null;
    this.cantones = null;
  }
  //auxiliary methods

  //index methods
  getCoastLine() {
    //TODO: still not exist in server
  }

  getBorderLine() {
    //TODO: still not exist in server
  }

  getCountryShape(){
    //TODO: still not exist in server
  }

  //departamentos limits source for direct use in our maps
  getDepartamentosLimits(){
    if (this.departamentos == null){
      this.departamentos = new ol.source.Vector({
          projection : 'EPSG:4326',
          url: server_name + '/geoserver/departementos.geojson',
          format: new ol.format.GeoJSON()
      });
    }
    return this.departamentos;
  }
  //municipios limits source for direct use in our maps
  getMunicipiosLimits(){
    if (this.municipios == null){
      this.municipios = new ol.source.Vector({
          projection : 'EPSG:4326',
          url: server_name + '/geoserver/municipios.geojson',
          format: new ol.format.GeoJSON()
      });
    }
    return this.municipios;
  }
  //cantones limits source for direct use in our maps
  getCantonesLimites(){
    if (this.cantones == null){
      this.cantones = new ol.source.Vector({
          projection : 'EPSG:4326',
          url: server_name + '/geoserver/cantones.geojson',
          format: new ol.format.GeoJSON()
      });
    }
    return this.cantones;
  }

  getImportantCities(){
    //TODO: still not exist in server
  }

  getNormalCities(){
    //TODO: still not exist in server
  }

  getJRVs(){
    //TODO: still not exist in server
  }

  getDepartamentoBorder(cod_dep){
      //TODO: still not exits in server is decorative
  }

  getDepartamentoCoastLine(cod_dep){
    //TODO: still not exits in server is decorative
  }

  getDepartamento(cod_dep){
    //TODO: still not exits in server is important
  }

  getMunicipiosInDepartamento(cod_dep){
    //TODO: still nor exist in server is important
  }
  


}

class MapsStyleFactory{
  constructor(){ 
    this.mainFillColor = "#ffffff";

    this.textMapColor = "#2c264c";

    this.darkStrokeColor = "#6358a5";
    this.normStrokeColor = "#9188cc";
    this.ligthStrokeColor = 'rgba(206, 200, 244, 0.2)';

    this.GanaColor = "#2faff1";
    this.FmlnColor = "#d83026";
    this.ArenaCoalisionColor = "#5444ba";
    this.VamosColor = "#e639de";

    this.GanaRamp = ["#cdebfb", "#9ad8f8", "#6ec7f5", "#2faff1"];
    this.FmlnRamp = ["#f3c4c1", "#eda5a1", "#e57770", "#d83026"];
    this.ArenaCoalisionRamp = ["#ccc7ea", "#b3abe0c", "#8d82d1", "#5444ba"];

    this.boldLineWidth = 1.5;
    this.normLineWidth = 1;
    this.thinLineWidth = 0.4;

  }

  whiteFillStyle(){
    return new Style({
      fill: new Fill({
        color: this.mainFillColor
      })
    });
  }

  cantonesStyle(){
    return new Style({
      stroke: new Stroke({
        color: this.ligthStrokeColor,
        width: this.thinLineWidth
      })
    });
  }

  departamentosBordersStyle(){
    return new Style({
      stroke: new Stroke({
        color: this.darkStrokeColor,
        width: this.boldLineWidth
      })
    });
  }

  municipiosBordersStyle(){
    return new Style({
      stroke: new Stroke({
        color: this.normStrokeColor,
        width: this.normLineWidth
      })
    });
  }

  municipiosCategoricalWinner(){
    return new Style({
      stroke : this.municipiosBordersStyle().getStroke(),
      fill : new Fill({
        //I'm here for continue here
      })
    });
  }




}