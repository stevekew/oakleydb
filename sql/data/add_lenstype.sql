INSERT INTO lenstype (sourceid, name, validfrom) 
SELECT id, 'Uncategorised', CURRENT_TIMESTAMP FROM source WHERE name = 'admin'
