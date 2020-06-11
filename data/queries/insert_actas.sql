{% sql 'insert_actas', note = 'this search in the dep and munic tablas by name for a correct id' %}

INSERT INTO actas VALUES(
    {{ JRV_ID | guards.integer}},
    CAST((SELECT cod_dep FROM departamentos WHERE TRANSLATE(nombre, 'áéíóúÁÉÍÓÚ', 'aeiouAEIOU') ILIKE {{ DEPARTAMENTO | guards.string }} LIMIT 1) AS integer),
    CAST((SELECT cod_munic FROM municipios WHERE TRANSLATE(nombre, 'áéíóúÁÉÍÓÚ', 'aeiouAEIOU') ILIKE {{ MUNICIPIO | guards.string }} LIMIT 1) AS integer),
    NULL, 
    {{ SOBRANTES | guards.integer}},
    {{ INUTILIZADAS | guards.integer}},
    {{ FMLN | guards.integer}},
    {{ GANA | guards.integer}},
    {{ VAMOS | guards.integer}},
    {{ ARENA | guards.integer}},
    {{ PCN | guards.integer}},
    {{ PDC | guards.integer}},
    {{ DS| guards.integer}},
    {{ TOTAL_ARENA_PCN_PDC_DS | guards.integer}},
    {{ IMPUGNADOS | guards.integer}},
    {{ NULOS | guards.integer}},
    {{ ABSTENCIONES | guards.integer}},
    {{ VOTOS_VALIDOS | guards.integer}},
    {{ OTROS_VOTOS | guards.integer}},
    {{ VV_MAS_OTROS | guards.integer}},
    {{ TOTALES| guards.integer}},
    {{ ARENA_PCN_PDC_DS| guards.integer}},
    {{ FALTANTES| guards.integer}}
);
{% endsql %}