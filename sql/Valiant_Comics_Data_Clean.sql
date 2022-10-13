CREATE DATABASE valiant_comics;
USE valiant_comics;

DESC characters;

SELECT Gender, COUNT(*)
FROM characters
GROUP BY Gender;

-- Parse Year and remove entries that were prior to valiant entertainment era in 2012 (e.g. valiant comics, acclaim comics)

ALTER TABLE characters
Add Year YEAR;

UPDATE characters
SET Year = REGEXP_SUBSTR(`First appearance`, '20[1-2][0-9]');

-- Removing entries where the year is unverified
DELETE
FROM characters
WHERE Year is NULL;

-- Finding and removing duplicates
SELECT a.*
FROM characters a
JOIN (SELECT Name, COUNT(*)
	FROM characters
    GROUP BY Name
    HAVING COUNT(*) > 1) b
ON a.Name = b.Name 
ORDER by a.Name;

DELETE a
FROM characters a
JOIN (SELECT Name, COUNT(*)
	FROM characters
    GROUP BY Name
    HAVING COUNT(*) > 1) b
ON a.Name = b.Name
WHERE a.Universe NOT LIKE "%Valiant Entertainment%";

-- Fixing text that did not convert correctly
UPDATE characters
SET Aliases = "The Øracle"
WHERE `Full name` = "Octavio Gonzalez";

UPDATE characters
SET Family = REPLACE( Family, '\u2020', '');

-- Normalizing Unknown Gender
UPDATE characters
SET Gender = REPLACE(Gender, "???", "");

UPDATE characters
SET Gender = REPLACE(Gender, "?", "");

UPDATE characters
SET Gender = REPLACE(Gender, "Unknown", "");