import json

import psycopg2
import shapely.wkt
import shapely.geometry

import db

def description_to_dict(description):
    """This take description format of psycopg2 cursor.description
    and convert to a simple dict with name and col_pos values"""
    description_dict = {}
    for col_num in range(0, len(description)):
        description_dict[ description[col_num].name ] = col_num
    return description_dict


def check_limit_type(description):
    """Check the limit type of a table result"""
    limit_type =  "limit"
    if "cod_canton" in description:
        limit_type = "cantones"
    elif "cod_munic" in description:
        limit_type = "municipios"
    elif "cod_dep" in description:
        limit_type = "departamentos"
    return limit_type

def extract_props(row, description):
    """Collect the props that exist of a table row and convert in a dict this is
    use in normal json case and geo+json case"""
    props = {}
    #if limit is canton
    if "cod_canton" in description:
        props["cod_canton"] = row[description["cod_canton"]]
        props["nombre"] = row[description["nombre"]]
        #add superior limits classes if their exist
        if "cod_munic" in description:
            props["cod_munic"] = row[description["cod_munic"]]

            if "nombre_munic" in description:
                props["nombre_munic"] = row[description["nombre_munic"]]

        if "cod_dep" in description:
            props["cod_dep"] = row[description["cod_dep"]]
    #if limit is municipio
    elif "cod_munic" in description:
        props["cod_munic"] = row[description["cod_munic"]]
        props["nombre"] = row[description["nombre"]]
        #add superior limit class if exist
        if "cod_dep" in description:
            props["cod_dep"] = row[description["cod_dep"]]

            if "nombre_dep" in description:
                props["nombre_dep"] = row[description["nombre_dep"]]
    #if the limis is departamento
    elif "cod_dep" in description:
        props["cod_dep"] = row[description["cod_dep"]]
        props["nombre"] = row[description["nombre"]]
    #normal properties of limit
    if "poblacion" in description:
        props["poblacion"] = row[description["poblacion"]]
    #parties classes votes consolidates
    if "arena_coalision_votos" in description:
        props["arena_coalision_votos"] = row[description["arena_coalision_votos"]]

    if "fmln_votos" in description:
        props["fmln_votos"] = row[description["fmln_votos"]]

    if "gana_votos" in description:
        props["gana_votos"] = row[description["gana_votos"]]

    if "vamos_votos" in description:
        props["vamos_votos"] = row[description["vamos_votos"]]

    return props

def db_to_json(db_result, description):
    """Convert the fetchall() result of db query and convert
    to json format"""
    limits = []
    type_limit = check_limit_type(description)
    #Populate limits.
    for row in db_result:
        limit = extract_props(row, description)

        if "geometry" in description:
            limit["geometry"] = row[description["geometry"]]
        limits.append(limit)

    #put the list in a dict for make {}
    limitsCollection = {type_limit + "Collection":limits}
    #Convert to json
    return json.dumps(limitsCollection)

def db_to_geojson(db_result, description):
    """Convert the fetchall() result of db query and convert it 
    to geo+json format"""
    features = []
    for row in db_result:
        props = extract_props(row, description)
        geom = None
        if "geometry" in description:
            g = shapely.wkt.loads(row[description["geometry"]])
            geom = shapely.geometry.mapping(g)
        feature = {"type": "Feature",
                   "properties": props,
                   "geometry": geom}
        features.append(feature)
    featureCollection = {"type":"featureCollection", "features": features}
    return json.dumps(featureCollection)


#make query to db
def execute_query(query): #TODO: this should be move to limits
    """Execute a query in db and return it the result tuple list and
    a tuple with a description in a dictionary format"""
    conn = db.get_db()
    cur = conn.cursor()
    cur.execute(query)
    db_result = cur.fetchall()
    description = cur.description()
    description = description_to_dict(description)
    cur.close()
    conn.close()
    return db_result, description



def build_query(fields_dict, filters_dict, limit_type): # TODO
    if limit_type == 'departamentos':
        pass
    if limit_type == 'municipios':
        pass
    if limit_type == 'cantones':
        pass

#format result.
def format_result(result, format = 'geojson'):
    formated_r = None
    if 'geojson':
        formated_r = db_to_geo_json(result)
    elif 'json':
        formated_r = db_to_json(result)
    else:
        return 'Error not valid_format'
    return formated_r

#look for props that will be returned
def look_for_father_munic(args):
    father_munic = {}
    if args.get("father-munic") == 'true':
        father_munic["cod_munic"] = True
        father_munic["nombre_munic"] = True
    return father_munic


def look_for_father_dep(args):
    father_dep = {}
    if args.get("father-dep") == 'true':
        father_dep["cod_dep"] = True
        father_dep["nombre_dep"] = True
    return father_dep


def look_for_political_classes(args):
    political_classes = {}

    if args.get("arena-coalision") == 'true':
        political_classes["arena_coalision_votos"] = True

    if args.get("fmln") == 'true':
        political_classes["fmln_votos"] = True

    if args.get("gana") == 'true':
        political_classes["gana_votos"] = True

    if args.get("vamos") == 'true':
        political_classes["vamos_votos"] = True
    
    return political_classes

def look_for_population(args):
    poblacion = {}
    if args.get("poblacion") == 'true':
        poblacion["poblacion"] = True
    return poblacion

def look_for_geometry(args):
    geometry = {}
    if args.get("geometry") == 'true':
        geometry["geometry"] = True
    return geometry

#look for query condition
def filter_per_ids(args,  cod = None):
    ids = {}
    if args.get("ids"):
        #the ids args is a string that looks like '1,2,3'
        #we need to split by ',' and convert to int
        ids_arg = args.get("ids")
        ids_arg = ids_arg.split(',')
        ids["ids"] = list(map(int, ids_arg))
    if cod is not None:
        ids["ids"] = [int(cod)]
    return ids

def filter_per_deps_ids(args):
    deps = {}
    if args.get("deps"):
        deps_arg = args.get("deps").split(',')
        deps_arg = list(map(int, deps_arg))
        deps["deps"] = deps_arg
    return deps
