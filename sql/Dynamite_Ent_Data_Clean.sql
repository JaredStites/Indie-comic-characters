CREATE DATABASE dynamite_ent;
USE dynamite_ent;

DESC characters;

Select Name, COUNT(*)
FROM characters
GROUP BY Name
HAVING COUNT(*) > 1
ORDER BY Name;

-- Remove duplicates that are not from the respective main universe
DELETE a
FROM characters a
JOIN(SELECT *
	FROM characters
    WHERE Universe LIKE '%818793%') b
ON a.Name = b.Name
WHERE a.Universe NOT LIKE '%818793%';

-- Ashley is a variation of Ash from the Army of Darkness
DELETE FROM characters
WHERE Name LIKE '%Ashley%';

DELETE FROM characters
WHERE Name = 'Andar' AND Universe NOT LIKE '%616%';

DELETE FROM characters
WHERE Name = 'Batman' AND Universe NOT LIKE 'Prime Earth';

DELETE FROM characters
WHERE Name = 'Bettie Page' AND Universe NOT LIKE '%UU019%';

DELETE FROM characters
WHERE Name = 'Captain Victory' AND Universe NOT LIKE '%Kirby Genesis%';

DELETE FROM characters
WHERE Name = 'Robocop' AND Universe NOT LIKE '%UU035%';

-- Parse Year into its own column
ALTER TABLE characters
Add Year YEAR;

UPDATE characters
SET Year = REGEXP_SUBSTR(`First appearance`, '199[0-9]|20[0-9]{2}');

-- Remove characters that have a year prior to the creation of Dynamite in 2004
DELETE FROM Characters
WHERE Year < 2004;

