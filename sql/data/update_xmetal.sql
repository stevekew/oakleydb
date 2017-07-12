-- fix the penny TiO2 Emerald image path
UPDATE model SET image='http://www.aquaria.za.net/oakleydb/images/X-Metal/Penny_TiO2_Emerald.jpg', imagesmall='http://www.aquaria.za.net/oakleydb/images/X-Metal/small/Penny_TiO2_Emerald.jpg' WHERE sku='04-133'

-- Set up the bse curves
UPDATE style SET basecurveid = (SELECT id FROM basecurve WHERE name='8.75') WHERE name='Juliet'
UPDATE style SET basecurveid = (SELECT id FROM basecurve WHERE name='8.75') WHERE name='X-Squared'
UPDATE style SET basecurveid = (SELECT id FROM basecurve WHERE name='8.75') WHERE name='X Metal XX'
UPDATE style SET basecurveid = (SELECT id FROM basecurve WHERE name='8.75') WHERE name='Romeo 2.0'
UPDATE style SET basecurveid = (SELECT id FROM basecurve WHERE name='8.75') WHERE name='Romeo'
UPDATE style SET basecurveid = (SELECT id FROM basecurve WHERE name='8.75') WHERE name='Penny'
UPDATE style SET basecurveid = (SELECT id FROM basecurve WHERE name='8.75') WHERE name='Mars'
UPDATE style SET basecurveid = (SELECT id FROM basecurve WHERE name='8.75') WHERE name='Half-X'