-- Assuming the table is named `bands` and has columns: `band_name`, `main_style`, `formed`, `split`

-- Step 1: Calculate lifespan
-- Step 2: Filter for Glam rock style
-- Step 3: Order by lifespan

SELECT band_name, (IFNULL(split, '2020') - formed) AS lifespan
    FROM metal_bands
    WHERE FIND_IN_SET('Glam rock', IFNULL(style, "")) > 0
    ORDER BY lifespan DESC;