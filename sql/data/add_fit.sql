INSERT INTO fit (sourceid, name)
SELECT id, 'Standard' FROM source where name = 'admin';
INSERT INTO fit (sourceid, name)
SELECT id, 'Asian' FROM source where name = 'admin';

