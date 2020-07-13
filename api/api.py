from flask import Blueprint

api = Blueprint('api', __name__, url_prefix='/api/geoserver')


# ============ Departamentos end-points =================
@api.route('/departamentos')
def departamentos():
    return 'departamentos'

@api.route('/departamento/<cod_dep>')
def departameto(cod_dep):
    return 'departemento ' + cod_dep

@api.route('/departamentos/dict')
def departamentos_dict():
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
