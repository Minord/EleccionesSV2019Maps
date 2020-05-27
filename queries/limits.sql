{% sql 'departamentos_geojson', note='This query return a geojson' %}
-- Make a row of the top level geo json
SELECT row_to_json(result_s1) FROM
(
     -- features is an array of departamentos features geojson
	SELECT 'FeatureCollection' as type, (array_agg(row_to_json(result_f))) as features
	FROM (
        --  create a featues as json
		SELECT 'Feature' as type, -- type prop
		json_build_object ('cod_dep', cod_dep, 'nombre', nombre) as properties, -- properties prop
		cast(ST_AsGeoJson(ST_Simplify(pos_geom, 0)) as json) as geometry -- geometry in geojson format is a muti-polygon
		FROM departamentos
	) AS result_f
) AS result_s1;
{% endsql %}

{% sql 'municipios_geojson', note='This query return a geojson' %}
-- Make a row of the top level geo json
SELECT row_to_json(result_s1) FROM
(
     -- features is an array of departamentos features geojson
	SELECT 'FeatureCollection' as type, (array_agg(row_to_json(result_f))) as features
	FROM (
        --  create a featues as json
		SELECT 'Feature' as type, -- type prop
		json_build_object ('cod_munic', cod_munic, 'nombre', nombre) as properties, -- properties prop
		cast(ST_AsGeoJson(ST_Simplify(pos_geom, 0)) as json) as geometry -- geometry in geojson format is a muti-polygon
		FROM municipios
	) AS result_f
) AS result_s1;
{% endsql %}

{% sql 'cantones_geojson', note='This query return a geojson' %}
-- Make a row of the top level geo json
SELECT row_to_json(result_s1) FROM
(
     -- features is an array of departamentos features geojson
	SELECT 'FeatureCollection' as type, (array_agg(row_to_json(result_f))) as features
	FROM (
        --  create a featues as json
		SELECT 'Feature' as type, -- type prop
		json_build_object ('cod_munic', cod_canton, 'nombre', nombre) as properties, -- properties prop
		cast(ST_AsGeoJson(ST_Simplify(pos_geom, 0)) as json) as geometry -- geometry in geojson format is a muti-polygon
		FROM cantones
	) AS result_f
) AS result_s1;
{% endsql %}