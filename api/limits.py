import json

import psycopg2
import shapely.wkt
import shapely.geometry

def description_to_dict(description):
    """This take description format of psycopg2 cursor.description
    and convert to a simple dict with name and col_pos values"""
    description_dict = {}
    for col_num in range(0, len(description)):
        description_dict[ description[col_num].name ] = col_num
    return description_dict


def check_limit_type(row, description):
    """Check the limit type of a table result"""
    limit_type =  "limit"
    if description["cod_canton"]:
        limit_type = "cantones"
    elif description["cod_munic"]:
        limit_type = "municipios"
    elif description["cod_dep"]:
        limit_type = "departamentos"
    return limit_type

def extract_props(row, description):
    """Collect the props that exist of a table row and convert in a dict this is
    use in normal json case and geo+json case"""
    props = {}
    #if limit is canton
    if description["cod_canton"]:
        props["cod_canton"] = row["cod_canton"]
        props["nombre"] = row["nombre"]
        #add superior limits classes if their exist
        if description["cod_munic"]:
            props["cod_munic"] = row["cod_munic"]

            if description["nombre_munic"]:
                props["nombre_munic"] = row["nombre_munic"]

        if description["cod_dep"]:
            props["cod_dep"] = row["cod_dep"]
    #if limit is municipio
    elif description["cod_munic"]:
        props["cod_munic"] = row["cod_munic"]
        props["nombre"] = row["nombre"]
        #add superior limit class if exist
        if description["cod_dep"]:
            props["cod_dep"] = rew["cod_dep"]

            if description["nombre_dep"] 
                props["nombre_dep"] = row["nombre_dep"]
    #if the limis is departamento
    elif description["cod_dep"]:
        props["cod_dep"] = row["cod_dep"]
        props["nombre"] = row["nombre"]
    #normal properties of limit
    if description["poblacion"]:
        props["poblacion"] = row["poblacion"]
    #parties classes votes consolidates
    if description["arena_coalision_votos"]:
        props["arena_coalision_votos"] = row["arena_coalision_votos"]

    if description["fmln_votos"]:
        props["fmln_votos"] = row["fmln_votos"]

    if description["gana_votos"]:
        props["gana_votos"] = row["gana_votos"]

    if description["vamos_votos"]:
        props["vamos_votos"] = row["vamos_votos"]

    return props

def db_to_json(db_result, description):
    """Convert the fetchall() result of db query and convert
    to json format"""
    limits = []
    type_limit = check_limit_type(db_result[0], description)
    #Populate limits.
    for row in db_result:
        limit = extract_props(row, description)

        if description["geometry"]:
            limit["geometry"] = row["geometry"]

    #put the list in a dict for make {}
    limitsCollection = {type_limit + "Collection":limits}
    #Convert to json
    return json.dumps(limitsCollection)

def db_to_geojson(db_result, description):
    """Convert the fetchall() result of db query and convert it 
    to geo+json format"""
    #TODO: here we have to chek if geom json.dumps works good.
    features = []
    for row in db_result:
        props = extract_props(row, description)
        geom = None
        if description["geometry"]:
            g = shapely.wkt(row[row["geometry"]])
            geom = shapely.geometry.mapping(g)
        feature = {"type": "feature",
                   "properties": props,
                   "geometry": geom}
        features.append(feature)
    featureCollection = {"featureCollection": features}
    return json.dumps(featureCollection)


class Limit():

    limit_queries = None

    def __init__(self):
        if limit_queries is None:
            #TODO: load_queries files

    def check_ids_vality(self ,ids, limit_type):
        """This return true if ids content is valid and has ids that exits in db
        
        PARAMETERS
        ----------
            ids - this can be a void list that will return true ever or has a
            list of ids.
            limit_type - this is the limit type that is the id for search in the
            correct table valid content ["departamentos", "municipios",
            "cantones"]

        RETURNS
        ---------
            is_valid - a boolean true if ids are valid
        """
        #TODO: implement
        pass

    def execute_query(self, query, result_format):
        """"This will execute the queries in db and will fetch and format the
        resutls

        PARAMETERS
        --------
            query - a string that is the SQL that we going to execute in db.
            result_format - a string that indicate the format should return the
            functions valid content ["json", "geojson"]

        RETURNS
        --------
            results - a string that is the result formated in the indicate form
        """"
        #TODO: implement
        pass


class Departamentos(Limit):

    def get(self, ids, props, geometry, political_classes, result_format)
        #check ids validity
        #add props
        #add geometry
        #add political_casses

        #send to query builder
        #execute query
        #get results
        #TODO: implement
        pass


class Municipios(Limit):

    def get(self, ids, dep, props, geometry, political_classes, result_format)
        pass 

class Cantones(Limit):

    def get(self, ids, munic, dep, props, geometry, result_format):
        pass

