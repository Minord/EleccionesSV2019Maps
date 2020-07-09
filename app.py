import os
import json


from flask import Flask, jsonify
from flask import render_template, url_for
from flask import request
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









#WORKING AREA
#-----------------------------------------------------------------------------------------------------
#TODO: Recontruct the  pertartamentos end point for made it more like a rest API
#try to make acomplish it more like a standar in OGC. well it has to be more
#
#STYLE-------
#   /geoserver/departamentos             - fro get all DEPs
#   /geoserver/departamentos/<dep_id>    - for get a certain DEP
#   /geoserver/departamentos/dict        - json with dep dictionary into IDs
#
#Queries Aceptable --------
#   votos_arena_coalision = false
#   votos_fmln=false
#   votos_gana=false
#   votos_vamos=false
#   ganador=false
#   geometry=true
#   deps={list of deps is}
#
#But how i get it

class Departamentos():
    """Handle the getting information of departamentos limits"""

    dep_q = None

    def __init__(self, db, request, cod_dep = None):
        self.db = db
        self.request = request
        self.cod_dep = None
        if(Departamentos.department_queries is None):
            #create queries_factor
            dep_q = snaql_factory.load_queries('departamentos.sql')

    def get(self):
        """Handle any GET request to departamentos"""
        
        v_arena_coalision = False
        v_fmln = False
        v_vamos = False
        v_gana = False
        ids = self.cod_dep
        geometry = True

        if self.request.args.get("arena_coalision") == 'true':
            v_arena_coalision = True
        elif self.request.args.get("fmln") == 'true':
            v_fmln = True
        elif self.request.args.get("vamos") == 'true':
            v_vamos = True
        elif self.request.args.get("gana") == 'true':
            v_gana = True

        if self.cod_dep is None:
            if self.request.args.get("deps") is not None:
                #parse to int list.
                ids = self.request.args.get("deps")
        
        if self.request.args.get("geometry") == 'false':
            geometry = False

        #check the vality of ids
        if ids is not None:
            #transform ids form int to list for generalize
            if not isinstance(ids, list):
                ids = [ids]
            
            for id in ids:
                try:
                    #check if is a int
                    id = int(id)
                    if not self.check_dep_code(id):
                        #error is not valid
                        return 'bad_request! cod_dep not in db', 400
                except:
                    #error not valid id
                    return 'bad_request! cod_dep has to be number', 400

        query = dep_q.select_departamentos(ids, geometry, votos_arena_coalison,
                                          votos_fmln, votos_vamos, votos_gana)
    
        conn = db.get_db()
        cur = conn.cursor()

        cur.execute(query)

        results = cur.fetchall()
        
        #packing as geojson
        #packing as json
        format = request.args.get('format')
        if format == 'geojson' or format == '' or format is None:
            #return a geojson
            pass
        elif format == 'json':
            #return a json
            pass


    #COMPLETE check
    def select_departamentos(ids = None, 
                             geometry = True, 
                             votos_arena_coalision = False,
                             votos_fmln = False,
                             votos_vamos = False,
                             votos_gana = False):
        """This build the query for make to db the parameters
        ids [ids is int: 1 dep | ids is list: in deps | ids is None: all deps]
        the other parameter if it is true it will contain it field in the result"""
        query_args = {}

        if geometry is True:
            query_args['geometry'] = geometry

        if votos_arena_coalision is True:
            query_args['votos_arena_coalision'] = votos_arena_coalision

        if votos_fmln is True:
            query_args['votos_fmln'] = votos_fmln

        if votos_vamos is True:
            query_args['votos_vamos'] = votos_vamos

        if votos_gana is True:
            query_args['votos_gana'] = votos_gana

        if ids is not None:
            if isinstance(ids, list):
                query_args['cods_list'] = ids
            else:
                query_args['cod_dep'] = ids

        return departamentos_queries.select_departamentos(**query_args)


    def get_dict(self):
        pass

    def check_dep_code(self, cod_dep):
        """Check if a dep_cod exits in DB"""
        exist = False
        db = self.db.get_db()
        cur = db.cursor()

        query_args = {"cod_dep": cod_dep}

        cur.execute(departementos_queries.check_cod(**query_args))

        result = cur.fetchone()
        if result[0][0] == cod_dep:
            exist = True

        return exist

#The end points for departamento API
@app.route('/geoserver/departamentos')
def departamentos():
    pass
@app.route('/geoserver/departamentos/<cod_dep>')
def departamento(cod_dep):
    pass
@app.route('/geoserver/departamentos/dict')
def departamentos_dict():
    deps = Departamentos(db, request)
    return deps.get_dict()
#-------------------------------------------------------------------------------------------------------
#END WORKING AREA






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
