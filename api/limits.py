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
    #TODO: here we have to chek if geom json.dumps works good.
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


class Limit():

    limit_queries = None

    def __init__(self):
        if limit_queries is None:
            #TODO: load_queries files
            pass

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
        """This will execute the queries in db and will fetch and format the
        resutls

        PARAMETERS
        --------
            query - a string that is the SQL that we going to execute in db.
            result_format - a string that indicate the format should return the
            functions valid content ['json', 'geojson']

        RETURNS
        --------
            results - a string that is the result formated in the indicate form """
        #TODO: implement
        pass


class Departamentos(Limit):

    def get(self, ids, props, geometry, political_classes, result_format):
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

    def get(self, ids, dep, props, geometry, political_classes,
            result_format):
        pass 

class Cantones(Limit):

    def get(self, ids, munic, dep, props, geometry, result_format):
        pass

