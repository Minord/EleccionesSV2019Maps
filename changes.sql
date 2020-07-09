--I need solve this problem.
UPDATE cantones
SET can.cod_munic = mun.cod_munic
FROM cantones AS can
INNER JOIN municipios AS mun
ON ST_Contains(mun.pos_geom, ST_PointOnSurface(can.pos_geom));
