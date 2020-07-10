import unittest #Unit testing module
import json

#import testing funcs
from api.limits import (description_to_dict,
                    check_limit_type,
                    extract_props,
                    db_to_json, db_to_geojson)



class TestColumn():
    """This class of for simulate the
    Column class of psycopg2"""
    def __init__(self, name):
        self.name = name

#Variables for use in tests
row_example = (1, "ahuachapan", 1039, "Point(100 100)", 23,43,32,43)

row_description = {"cod_dep":0,
                   "nombre": 1,
                   "poblacion":2,
                   "geometry": 3,
                   "arena_coalision_votos": 4,
                   "fmln_votos": 5,
                   "gana_votos": 6,
                   "vamos_votos": 7}


class TestLimitsMethods(unittest.TestCase):

    def test_description_to_dict(self):
        #create a description usual object.
        description = (TestColumn("cod_dep"),
                       TestColumn("nombre"),
                       TestColumn("poblacion"))
        #Expected result for test
        expected_result = {"cod_dep": 0,
                           "nombre": 1,
                           "poblacion": 2}

        self.assertEqual(description_to_dict(description),
                          expected_result, "do not match")

    
    def test_check_limit_type(self):
        #des means description
        des_dep = {"cod_dep":0, "nombre":1, "poblacion":2}

        des_munic = {"cod_munic":0, "cod_dep": 1,
                     "nombre":2, "poblacion":3}

        des_canton = {"cod_canton": 0, "cod_munic": 1, 
                      "cod_dep" : 2, "nombre": 3, "poblacion": 4}

        self.assertEqual("departamentos", check_limit_type(des_dep))
        self.assertEqual("municipios", check_limit_type(des_munic))
        self.assertEqual("cantones", check_limit_type(des_canton))

    def test_extract_props(self):
        #des means description
        input_des = {
            "cod_munic": 0,
            "nombre": 1,
            "cod_dep": 2,
            "nombre_dep": 3,
            "poblacion": 4,
            "fmln_votos": 5,
            "geometry": 6
        }

        input_row = (5, "victoria", 9, "cabañas", 23123, 21)

        expected_result = {
            "cod_munic": 5,
            "nombre": "victoria",
            "cod_dep": 9,
            "nombre_dep": "cabañas",
            "poblacion": 23123,
            "fmln_votos": 21
        }

        result = extract_props(input_row, input_des)
        self.assertEqual(result, expected_result, "do not match")

    def test_db_to_json(self):
        description = {"cod_dep": 0, "nombre": 1, "geometry": 2}
        db_result = [(1, "ahuachapan", "POINT( 1 1 )"),
                     (9, "cabañas", "POINT( 2 2 )")]
        
        expected_json = """{
            "departamentosCollection": [
                {
                    "cod_dep": 1,
                    "nombre": "ahuachapan",
                    "geometry": "POINT( 1 1 )"
                },
                {
                    "cod_dep": 9,
                    "nombre": "cabañas",
                    "geometry": "POINT( 2 2 )"
                }
            ]}"""

        expected_result = json.dumps(json.loads(expected_json))
        result = db_to_json(db_result, description)
        

        self.assertEqual(expected_result, result, 'do not match')

    def test_db_to_geojson(self):
        description = {"cod_dep": 0, "nombre": 1, "geometry": 2}
        db_result = [(1, "ahuachapan", "POINT( 1 1 )"),
                     (9, "cabañas", "POINT( 2 2 )")]

        expected_geojson = """
        { "type": "featureCollection",
          "features": [
            {"type": "Feature",
             "properties": {
                "cod_dep": 1,
                "nombre": "ahuachapan"
             },
             "geometry": {
                "type": "Point",
                "coordinates": [1.0, 1.0]
             }
            },
            {
            "type": "Feature",
            "properties": {
                "cod_dep": 9,
                "nombre": "cabañas"
            },
            "geometry": {
                "type": "Point",
                "coordinates": [2.0, 2.0]
            }
            }
          ]}
        """
        expected_result = json.dumps(json.loads(expected_geojson))
        result = db_to_geojson(db_result, description)
        self.assertEqual(result, expected_result, "do not match")
