-- ranks country origins of bands, ordered by the number of (non-unique) fans
COPY metal_bands(origin, fans) FROM 'metal_bands.csv' DELIMITER ',' CSV HEADER;

-- Rank country origins of bands, ordered by the number of (non-unique) fans
SELECT origin, SUM(fans) AS nb_fans 
   FROM metal_bands
   GROUP BY origin
   ORDER BY nb_fans DESC;
