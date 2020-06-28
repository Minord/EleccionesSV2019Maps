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
		json_build_object ('cod_munic', cod_munic,'cod_dep', cod_dep, 'nombre', nombre) as properties, -- properties prop
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
		json_build_object ('cod_canton', cod_canton, 'cod_munic', cod_munic, 'nombre', nombre) as properties, -- properties prop
		cast(ST_AsGeoJson(ST_Simplify(pos_geom, 0)) as json) as geometry -- geometry in geojson format is a muti-polygon
		FROM cantones
	) AS result_f
) AS result_s1;
{% endsql %}


--  ############## this is getting the munics or cantones in a certain deps #################

{% sql 'municipios_in_dep', note='This query return a geojson'%}

SELECT row_to_json(result_s1) FROM (
	SELECT 'FeatureCollection' as type, array_agg(row_to_json(result_f)) as features
	FROM (
		SELECT 'Feature' as type,
		json_build_object ('cod_munic', cod_munic, 'nombre', nombre) as properties,
		cast(ST_AsGeoJson(pos_geom) as json) as geometry
		FROM municipios
		WHERE cod_dep = {{ cod_dep|guards.integer }}
	) AS result_f
) as result_s1

{% endsql %}

{% sql 'cantones_in_dep', note='This query return a geojson'%}


WITH valid_cods_munic_arr AS (
	SELECT cod_munic 
	FROM municipios
	WHERE cod_dep = {{ cod_dep | guards.integer }}
)

SELECT row_to_json(result_s1) FROM (
	SELECT 'FeatureCollection' as type, array_agg(row_to_json(result_f)) as features
	FROM (
		SELECT 'Feature' as type,
		json_build_object ('cod_canton', cod_canton,'cod_munic', cantones.cod_munic, 'nombre', nombre) as properties,
		cast(ST_AsGeoJson(pos_geom) as json) as geometry
		FROM cantones
		INNER JOIN valid_cods_munic_arr ON cantones.cod_munic = valid_cods_munic_arr.cod_munic
	) AS result_f
) as result_s1

{% endsql %}

{% sql 'munic_resultado_in_dep', note = 'This query return a geojson'%}

SELECT row_to_json(result_s1) FROM (
	SELECT 'FeatureCollection' as type, array_agg(row_to_json(result_f)) as features
	FROM (
		SELECT 'Feature' as type,
		json_build_object('cod_munic', cod_munic,
		                  'nombre', nombre,
			          'votos_arena_coalicion', cast((SELECT sum(total_arena_coalision_votos) FROM actas WHERE actas.cod_munic = cod_munic) as integer),
			          'votos_fmln', CAST((SELECT sum(fmln_votos) FROM actas WHERE actas.cod_munic = cod_munic) as integer),
			          'votos_gana', CAST((SELECT sum(gana_votos) FORM actas WHERE actas.cod_munic = cod_munic) AS integer),
			          'votos_vamos', CAST((SELECT sum(vamos_votos) FROM actas WHERE actas.cod_munic = cod_munic) AS integer)) as properties,
		cast(ST_asGeoJson(pos_geom as json)) as geometry
		FROM muncipios
		WHERE cod_dep = {{ cod_dep | guards.integer }}  -- cod_dep is the parameter that we pass here.
	) AS result_f
)as result_s1
{% endsql%}
