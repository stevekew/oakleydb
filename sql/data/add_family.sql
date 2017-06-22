INSERT INTO family (sourceid, name, inserttime, validfrom)
SELECT id, 'Special Edition', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP FROM source where name = 'admin';
