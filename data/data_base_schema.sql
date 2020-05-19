/*
Esta base de datos tiene el proposito de mantener una base de datos con los datos de las elecciones 
preciedenciales 2019 esto con el proposito de analizar geograficamente haciendo uso de PostGis
limites politicos  geocoding para ver donde estan los centros de votacion. 

De estos tados se pueden sacar varios mapas interesantes
*/

CREATE DATABASE Elections2019Exploratory;

CREATE EXTENSION postgis;


-- Crear tabla de departamentos
CREATE TABLE departamentos (
	cod_dep integer PRIMARY KEY,
	nombre varchar(50),
	poblacion INTEGER,
	pos_geom geometry(POLYGON, 4326 )
);
-- crear tablas de municipios
CREATE TABLE municipios (
	cod_munic integer PRIMARY KEY,
	nombre varchar(50),
	poblacion INTEGER,
	pos_geom geometry(POLYGON, 4326 ),
	cod_dep integer REFERENCES departamentos( cod_dep )
);

CREATE TABLE cantones (
	cod_canton integer PRIMARY KEY,
	nombre varchar(50),
	poblacion INTEGER,
	pos_geom geometry( POLYGON, 4326 ),
	cod_munic integer REFERENCES municipios( cod_munic )
);

-- Crear tabla de centros de votacion
CREATE TABLE centros (
	centro_id SERIAL PRIMARY KEY,
	nombre varchar(50),
	direccion varchar(100),
	pos_geom geometry( POINT, 4326 ),
	cod_munic integer REFERENCES municipios (cod_munic)
);

-- Crear la tabla de actas
CREATE TABLE actas (
	-- identificacion y procedencia attr
	jrv_id integer PRIMARY KEY,
	cod_dep integer REFERENCES departamentos (cod_dep),
	cod_munic integer REFERENCES municipios (cod_munic),
	centro_id integer REFERENCES centros (centro_id),
	-- detalles votos
	sobrantes integer,
	inutilizadas integer,
	fmln_votos integer,
	gana_votos integer,
	vamos_votos integer,
	arena_votos integer,
	pcn_votos integer,
	pdc_votos integer,
	ds_votos integer,
	total_arena_coalision_votos integer,
	impugnados integer,
	nulos_votos integer,
	abstenciones integer,
	votos_validos integer,
	otros_votos integer,
	votos_validos_mas_otros integer,
	votos_totales integer
);

