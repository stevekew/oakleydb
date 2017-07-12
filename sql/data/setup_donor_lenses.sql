INSERT INTO lensdonor (sourceid, styleid, donorstyleid, inserttime, validfrom)
SELECT s.id, st1.id, d.id, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP FROM source s, style st1, style d
WHERE s.name = 'admin'
AND st1.name = 'Juliet'
AND d.name in ('Big Taco', 'Commit SQ/AV', 'Crosshair', 'Dispatch', 'Fast Jacket', 'Fast Jacket XL', 'Flak Jacket', 'Flak Jacket XLJ', 'Gascan', 'Gascan S', 'Half Jacket', 'Half Jacket XLJ', 'Half Jacket 2.0', 'Holbrook', 'Jawbone', 'Jawbone V', 'Monster Dog', 'Monster Doggle', 'Pit Boss', 'Pit Bull', 'Plaintiff', 'Racing Jacket', 'Racing Jacket V', 'Romeo', 'Romeo 2.0', 'Scalpel', 'Split Jacket', 'Straight Jacket 2', 'Ten X', 'X Metal XX', 'X Squared');
