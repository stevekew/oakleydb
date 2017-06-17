INSERT INTO gender (sourceid, name)
SELECT id, 'Mens' FROM source where name = 'admin';
INSERT INTO gender (sourceid, name)
SELECT id, 'Womens' FROM source where name = 'admin';
INSERT INTO gender (sourceid, name)
SELECT id, 'Unisex' FROM source where name = 'admin';

