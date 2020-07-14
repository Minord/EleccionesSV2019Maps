from flask import Blueprint

from flask import request

api = Blueprint('api', __name__, url_prefix='/api/geoserver')

import pdb

# ============ Departamentos end-points =================

@api.route('/departamentos')
def departamentos():
    pdb.set_trace()
    return 'departamentos'

@api.route('/departamento/<cod_dep>')
def departameto(cod_dep):
    fields_dict = dep_id
    return 'departemento ' + cod_dep

@api.route('/departamentos/dict')
def departamentos_dict():
    fields_dict = dep_id
    return 'departamentos-dict'


# ============ Municipios end-points ===================
@api.route('/municipios')
def municipios():
    return 'municipios'

@api.route('/municipio/<cod_munic>')
def municipio(cod_munic):
    return 'municipio ' + cod_munic

@api.route('/municipios/dict')
def municipios_dict():
    return 'municipios-dict'


# ============ Cantones end-points ===================
@api.route('/cantones')
def cantones():
    return 'cantones'

@api.route('/canton/<cod_canton>')
def canton(cod_canton):
    return 'canton ' + cod_canton

@api.route('/cantones/dict')
def canton_dict():
    return 'cantones-dict'
