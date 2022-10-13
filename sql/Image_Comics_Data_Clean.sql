CREATE DATABASE image_comics;
USE image_comics;

-- Explore Data
DESC characters;

SELECT DISTINCT `Gender`
FROM characters;

-- Look for possible duplicates
SELECT Name, COUNT(*)
FROM Characters
GROUP BY Name
HAVING COUNT(*) > 1
ORDER by Name;

SELECT a.*
FROM characters a
JOIN (SELECT Name, `Real Name`, COUNT(*)
	FROM characters
    GROUP BY Name, `Real Name`
    HAVING COUNT(*) > 1) b
ON a.Name = b.Name AND a.`Real Name` = b.`Real Name`
ORDER by a.Name;

SELECT a.*
FROM characters a
JOIN (SELECT Name, `Current Alias`, COUNT(*)
	FROM characters
    GROUP BY Name, `Current Alias`
    HAVING COUNT(*) > 1) b
ON a.Name = b.Name AND a.`Current Alias` = b.`Current Alias`
ORDER by a.Name;

--  Looks like some duplicates come from TV series
SELECT *
FROM characters
WHERE `First appearance` LIKE '%TV series%';

SELECT * 
FROM characters
WHERE `First appearance` LIKE '%Season%';

-- Delete those duplicates
DELETE FROM characters 
WHERE `First appearance` LIKE '%TV series%';

-- Make temp table to delete from same table that is being selected from (mySQL workaround)
DELETE FROM characters 
WHERE Name IN
(
	SELECT * FROM
    (
		SELECT Name
		FROM characters
		GROUP BY Name
		HAVING COUNT(Name) > 1
		AND `First appearance` LIKE '%Season%'
    )tmp_table
);

-- Parse Year into its own column
ALTER TABLE characters
Add Year YEAR;

UPDATE characters
SET Year = REGEXP_SUBSTR(`First appearance`, '199[0-9]|20[0-9]{2}');
