-- This SQL statement selects the 'origin' column and the count of distinct 'fans' from the 'metal_bands' table.
-- The 'COUNT(DISTINCT fans)' function counts the number of distinct 'fans' for each 'origin'.
-- The 'GROUP BY origin' clause groups the results by 'origin'.
-- The 'ORDER BY fans DESC' clause orders the results by the count of 'fans' in descending order.
-- The result will be a table with two columns: 'origin' and 'fans', where 'fans' is the count of distinct 'fans' for each 'origin'.
 SELECT origin, COUNT(DISTINCT fans) AS 'fans' FROM metal_bands
    GROUP BY origin
    ORDER BYfans DESC;
