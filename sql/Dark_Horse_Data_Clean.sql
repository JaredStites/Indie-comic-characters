CREATE DATABASE dark_horse_comics;
USE dark_horse_comics;

DESC characters;

-- Exploring gender data then cleaning
SELECT Gender, COUNT(*)
FROM characters
GROUP BY Gender;

SELECT *
FROM characters
WHERE Gender = '' and Creators = '' and `First appearance` = '' and `Current Alias` = '';

UPDATE characters
SET Gender = ""
WHERE Name = 'Blue Back';

UPDATE characters
SET Gender = "Female"
WHERE Name = 'Morrigan Corde';

-- Removing characters that do not have useable info
DELETE FROM characters
WHERE Gender = '' and Creators = '' and `First appearance` = '' and `Current Alias` = '';

-- Checking for duplicates
SELECT a.*
FROM characters a
JOIN (SELECT Name, COUNT(Name)
	FROM characters
    GROUP BY Name
    HAVING COUNT(Name) > 1) b
ON a.Name = b.Name
ORDER by a.Name;

-- Parse Year into its own column
ALTER TABLE characters
Add Year YEAR;

UPDATE characters
SET Year = REGEXP_SUBSTR(`First appearance`, '199[0-9]|20[0-9]{2}');




