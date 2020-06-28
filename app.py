import os
import json


from flask import Flask, jsonify
from flask import render_template, url_for
from . import db

#add snaql for handle the sql in separate files
import psycopg2.extras
from snaql.factory import Snaql

#create the classes and instances for make use of the queries to DB
root_location = os.path.abspath(os.path.dirname(__file__))
snaql_factory = Snaql(root_location, 'queries')
limits_queries = snaql_factory.load_queries('limits.sql')

#creating the app
app = Flask(__name__)
db.init_app(app)

#Comands to execute the app for windows
#venv/Scripts/activate
# $env:FLASK_ENV = "development"
#set FLASK_APP= app.py
#flask run



#################### NAVEGABLE PAGES ###########################
@app.route('/')
def hello_world():
    """root end point it render the index page of the app"""
    return render_template('index.html')


@app.route('/simple-map')
def simple_map():
    """this end point show a basic version of the map in a page"""
    return render_template('simple_map.html')

@app.route('/sandbox')
def sandbox():
    """this is a experimental end point for test experimental pages"""
    return render_template('sandbox.html')





##################### GEO DATA PROVIDERS ###################
@app.route('/geoserver')
def geo_directory():
    return "This Go to be the map service directory"

@app.route('/geoserver/departementos.geojson')
def geo_departamentos():
    """this return a geo json that has the el salvador departamentos"""
    db_conn = db.get_db()
    #queries
    cur = db_conn.cursor()
    cur.execute(limits_queries.departamentos_geojson())
    result = cur.fetchone()
    db_conn.commit()
    cur.close()
    return str(result[0]).replace("'", '"')

@app.route('/geoserver/municipios.geojson')
def geo_municipios():
    """this is a GET that return a geojson that has all the country municipios"""
    db_conn = db.get_db()
    #queries
    cur = db_conn.cursor()
    cur.execute(limits_queries.municipios_geojson())
    result = cur.fetchone()
    db_conn.commit()
    cur.close()
    return str(result[0]).replace("'", '"')

@app.route('/geoserver/cantones.geojson')
def geo_cantones():
    """this is a GET that return a geojson that has all the cantones in the country"""
    db_conn = db.get_db()
    #queries
    cur = db_conn.cursor()
    cur.execute(limits_queries.cantones_geojson())
    result = cur.fetchone()
    db_conn.commit()
    cur.close()
    return str(result[0]).replace("'", '"')

@app.route('/geoserver/municipios-dep-<cod_dep>.geojson')
def geo_municipios_in_dep(cod_dep):
    """this is a GET that return a geojson that has all the municipios in a dep"""
    #in this case can be a good idea check if the dep_code exits.
    arguments = {'cod_dep': int(cod_dep) }
    #get the data base connection
    db_conn = db.get_db()
    #queries
    cur = db_conn.cursor()
    cur.execute(limits_queries.municipios_in_dep(**arguments))

    #get results from queries
    result = cur.fetchone()
    
    #cerrar la base de datos
    db_conn.commit()
    cur.close()

    return str(result[0]).replace("'", '"')

@app.route('/geoserver/cantones-dep-<cod_dep>.geojson')
def geo_cantones_in_dep(cod_dep):
    """this is a GET that return a geojson that has all the cantones in a departamento"""
    #maybe do dep_code validation
    arguments = {'cod_dep' : cod_dep}
    #get db connection
    db_conn = db.get_db()
    #queries
    cur = db_conn.cursor()
    cur.execute(limits_queries.cantones_in_dep(**arguments))
    #get result from query
    result = cur.fetchone()
    #close the db
    db_conn.commit()
    cur.close()
    return str(result[0]).replace("'", '"')

@app.route('/dbtest')
def database_test():
    """It this end point is for develop experimental features"""
    db_conn = db.get_db()
    #handle with data base
    cur = db_conn.cursor()
    cur.execute("SELECT nombre FROM cantones;")
    result = cur.fetchall()
    db_conn.commit()
    cur.close()
    return (str(result))
