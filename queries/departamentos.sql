-- This is the declaration and the code of the departamentos queries to DB.

{%sql 'select_departamentos', note="This make a query to departamentos table"%}
    
    
SELECT  cod_dep, 
        nombre,

        {{ if geometry }}
        CAST((ST_ASGeoJson(pos_geom)) as json) AS geometry, -- Probability not only geojson
        {{ endif }}
        -- Add the votes consolidate here for department in the future.
        {{ if votos_arena_coalision }}
        SUM(a.total_arena_coalision_votos),
        {{ endif }}

        {{ if votos_fmln }}
        SUM(a.fmln_votos),
        {{ endif }}

        {{ if votos_vamos }}
        SUM(a.vamos_votos),
        {{ endif }}

        {{ if votos_gana }}
        SUM(a.gana_votos)
        {{ endif }} 

        FROM departamentos as d
        INNER JOIN actas as a ON d.cod_dep = cod_dep

        {{ if cod_dep }}
        AND cod_dep = {{ cod_dep | guards.integer }} {{ endif }} 
        {{ endif }}

        {{ if cods_list }}
        AND cod_dep IN ({{ cod_list | join(', ') }})
        {{ endif }}

        GROUP BY cod_dep;

{% endsql %}

-- Query for check if a cod_dep exist.
{% sql 'check_cod'%}
    SELECT cod_dep
    FROM departamentos
    WHERE cod_dep = {{ cod_dep | guards.integer }}
{% sqlend%}
