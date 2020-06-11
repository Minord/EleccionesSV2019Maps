#this is a script to load data into DB

import os
import json 
import csv
import configparser

import psycopg2 
import psycopg2.extras

from snaql.factory import Snaql

#get the actual file dir
dir_path = os.path.dirname(os.path.realpath(__file__))

#load a json file
def load_json_here(file_name):
    with open(dir_path + "/{}".format(file_name), 'r', encoding='utf-8') as f:
        json_f = json.load(f)
    return json_f

def getConnection():
    password = input("Please enter the pass:")
    return psycopg2.connect("dbname = elections2019SV user = postgres password = {}".format(password))

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

#this is over complicated
def put_actas_data():

    conn = getConnection()
    cur = conn.cursor()

    actas = None

    with  open('actas.csv') as csvfile:
        actas =  csv.DictReader(csvfile)

        row_counter = 0
        for acta_row in actas:
            if row_counter > 0:
                insert_command = "INSERT INTO actas VALUES (" + \
                                "{},".format(acta_row["JRV_ID"]) + \
                                "ARRAY(SELECT cod_dep FROM departamentos WHERE TRANSLATE(nombre, 'áéíóúÁÉÍÓÚ', 'aeiouAEIOU') ILIKE '{}'),".format(acta_row["DEPARTAMENTO"]) + \
                                "ARRAY(SELECT cod_munic FROM municipios WHERE TRANSLATE(nombre, 'áéíóúÁÉÍÓÚ', 'aeiouAEIOU') ILIKE '{}'),".format(acta_row["MUNICIPIO"]) + \
                                "NULL," + \
                                "{},".format(acta_row["SOBRANTES"]) + \
                                "{},".format(acta_row["INUTILIZADAS"])  + \
                                "{},".format(acta_row["FMLN"])  + \
                                "{},".format(acta_row["GANA"])  + \
                                "{},".format(acta_row["VAMOS"])  + \
                                "{},".format(acta_row["ARENA"])  + \
                                "{},".format(acta_row["PCN"])  + \
                                "{},".format(acta_row["PDC"])  + \
                                "{},".format(acta_row["DS"])  + \
                                "{},".format(acta_row["TOTAL_ARENA_PCN_PDC_DS"])  + \
                                "{},".format(acta_row["IMPUGNADOS"])  + \
                                "{},".format(acta_row["NULOS"]) + \
                                "{},".format(acta_row["ABSTENCIONES"])  + \
                                "{},".format(acta_row["VOTOS_VALIDOS"])  + \
                                "{},".format(acta_row["OTROS_VOTOS"])  + \
                                "{},".format(acta_row["VV_MAS_OTROS"])  + \
                                "{},".format(acta_row["VV_MAS_OTROS"])  + \
                                "{},".format(acta_row["ARENA_PCN_PDC_DS"])  + \
                                "{});".format(acta_row["FALTANTES"])
                cur.execute(insert_command)
            else:
                pass
            row_counter += 1

    #commit changes in data base
    conn.commit()
    print("close conexion")
    cur.close()
    conn.close()

#quiza los comandos embebidos en python no son lo mas ideal. Tengo que buscar otra forna de hacer esto de forma mas
#eficiente talvez si automatizo la insercion de datos y hago que la conexion sea automatica me haorro mas tiempo
def get_db_conf(path = None):
    config = configparser.ConfigParser()
    if path is None:
        config.read('db.conf')
    else:
        config.read(path)
    if len(config) <= 0:
        print("No se encontro archivo de configuracion")
        return None

    return config

class DataBase:

    def __init__(self, db_name = None, db_user = None, db_pass = None, conf_path = None):
        #get credentials

        if db_user is None or db_pass is None:
            if conf_path is not None:
                db_conf = get_db_conf(conf_path)

                if db_conf is not None:
                    db_name = db_conf['DEFAULT']['DB_NAME']
                    db_user = db_conf['DEFAULT']['DB_USER']
                    db_pass = db_conf['DEFAULT']['DB_PASSWORD']
                else:
                    db_name = input('database name: ')
                    db_user = input('user name: ')
                    db_pass = input('password name: ')
            else:
                db_conf = get_db_conf()
                if db_conf is not None:
                    db_name = db_conf['DEFAULT']['DB_NAME']
                    db_user = db_conf['DEFAULT']['DB_USER']
                    db_pass = db_conf['DEFAULT']['DB_PASSWORD']
                else:
                    db_name = input('database name: ')
                    db_user = input('user name: ')
                    db_pass = input('password name: ')

        self.db_name = db_name
        self.db_user = db_user
        self.db_pass = db_pass

        self.db_conn = None
    
    def connect(self):
        if self.db_conn is None:
            self.db_conn = psycopg2.connect("dbname = {} user = {} password = {}".format(self.db_name, self.db_user, self.db_pass))
            print("SUCCESS CONNECTION")
        return self.db_conn
    def close(self):
        self.db_conn.close()
        self.db_conn = None
        print("CLOSE CONNECTION")

    def commit(self):
        self.db_conn.commit()
        print("SECCESS CONNECTION")


#This is for get a easy way for get the sql in my cases.
class SnaqlConn:

    def __init__(self):
        self.root_location = os.path.abspath(os.path.dirname(__file__))
        self.snaql_factory = Snaql(self.root_location, 'queries')

    def get_queries(self, file_name):
        return self.snaql_factory.load_queries(file_name)


def push_actas_to_db():  #this should work
    db = DataBase(conf_path = '../db.conf')
    cur = db.connect().cursor()

    snaql_c = SnaqlConn()
    actas_queries = snaql_c.get_queries('insert_actas.sql')

    with  open('actas.csv') as csvfile:
        actas =  csv.DictReader(csvfile)

        for acta_row in actas:
    
            acta_row["JRV_ID"] = int(acta_row["JRV_ID"].replace(',',''))
            cur.execute(actas_queries.insert_actas(**acta_row))

    db.commit()
    cur.close()
    db.close()

push_actas_to_db()

#TODO: later add the center id to actas table