#this is a script to load data into DB

import os
import json 
import psycopg2 

#get the actual file dir
dir_path = os.path.dirname(os.path.realpath(__file__))

#load a json file
def load_json_here(file_name):
    with open(dir_path + "/{}".format(file_name), 'r', encoding='utf-8') as f:
        json_f = json.load(f)
    return json_f

def getConnection():
    password = input("Please enter the pass:")
    return psycopg2.connect("dbname = elections2019exploratory user = postgres password = {}".format(password))

def put_departamentos_basic_data():
    conn = getConnection()
    cur = conn.cursor()

    departamentos = load_json_here("departamentos.geojson")

    for dep in departamentos["features"]:
        insert_command = "INSERT INTO departamentos (cod_dep, nombre, pos_geom) VALUES  " + \
                         "( '{}' , '{}', ST_GeomFromGeoJSON('{}'));".format(dep['properties']['cod_dep'], 
                                                                            dep['properties']['nombre'], 
                                                                            str(dep['geometry']).replace("'",'"'))
        cur.execute(insert_command)
    conn.commit()

    print("close conexion")
    cur.close()
    conn.close()

def put_municipios_basic_data():
    conn = getConnection()
    cur = conn.cursor()

    municipios = load_json_here("municipios.geojson")

    for munic in municipios["features"]:
        insert_command = "INSERT INTO municipios (cod_munic, cod_dep, nombre, pos_geom) VALUES  " + \
                         "( '{}' ,'{}' ,'{}', ST_GeomFromGeoJSON('{}'));".format(munic['properties']['cod_munic'],
                                                                                 munic['properties']['cod_dep'], 
                                                                                 munic['properties']['nombre'], 
                                                                                 str(munic['geometry']).replace("'",'"'))
        cur.execute(insert_command)
    conn.commit()

    print("close conexion")
    cur.close()
    conn.close()


#put_municipios_basic_data() - alredy done.



#mandar informacion de los cantones.

def put_cantones_basic_data():
    conn = getConnection()
    cur = conn.cursor()

    cantones = load_json_here("cantones.geojson")

    for canton in cantones["features"]:
        insert_command = "INSERT INTO cantones (cod_canton, nombre, cod_munic,pos_geom) VALUES (" + \
                         "'{}', '{}', ".format(canton['properties']['cod_canton'], canton['properties']['nombre']) + \
                            "(SELECT munic.cod_munic FROM municipios as munic WHERE munic.nombre ILIKE '{}' AND munic.cod_dep = '{}'),".format(canton['properties']['nombre_munic'], canton['properties']['cod_dep']) + \
                            "ST_GeomFromGeoJSON('{}'));".format(str(canton['geometry']).replace("'",'"'))
        cur.execute(insert_command)
    conn.commit()
    print("close conexion")
    cur.close()
    conn.close()

#load cantones data
#put_cantones_basic_data() - DONE


#id duplecados en cantones
# los mageyes
# rest area rural antiguo cuscacltan
# El Chilamate
# El Riel