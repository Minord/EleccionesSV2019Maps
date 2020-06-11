import os
import json

from flask import Flask, jsonify
from flask import render_template, url_for
from . import db

import psycopg2.extras
from snaql.factory import Snaql

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
    return render_template('index.html')


@app.route('/simple-map')
def simple_map():
    return render_template('simple_map.html')

@app.route('/sandbox')
def sandbox():
    return render_template('sandbox.html')
##################### GEO DATA PROVIDERS ###################
@app.route('/geoserver')
def geo_directory():
    return "This Go to be the map service directory"

@app.route('/geoserver/departementos.geojson')
def geo_departamentos():
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
    db_conn = db.get_db()
    #queries
    cur = db_conn.cursor()
    cur.execute(limits_queries.cantones_geojson())
    result = cur.fetchone()
    db_conn.commit()
    cur.close()
    return str(result[0]).replace("'", '"')

@app.route('/geoserver/minicipios-in-dep/<dep>.geojson')
def geo_cantones():
    db_conn = db.get_db()
    #queries
    cur = db_conn.cursor()
    cur.execute(limits_queries.cantones_geojson())
    result = cur.fetchone()
    db_conn.commit()
    cur.close()
    return str(result[0]).replace("'", '"')


@app.route('/dbtest')
def database_test():
    db_conn = db.get_db()
    #handle with data base
    cur = db_conn.cursor()
    cur.execute("SELECT nombre FROM cantones;")
    result = cur.fetchall()
    db_conn.commit()
    cur.close()
    return (str(result))

    #.encode('latin-1').decode("utf-8")
#test end points delete this.

