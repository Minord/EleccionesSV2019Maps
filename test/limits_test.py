#How i import the db here.
import unittest


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

    def test_convert_to_dict():
        pass

    def test_is
