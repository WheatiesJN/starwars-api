-- =====================================================
-- CREATE STORED PROCEDURE: GetCharactersByAffiliation
-- =====================================================
-- This procedure retrieves all characters for a given affiliation
-- Example: CALL GetCharactersByAffiliation('Rebel Alliance');
-- =====================================================

USE starwarsDB;

-- Drop if exists
DROP PROCEDURE IF EXISTS GetCharactersByAffiliation;

DELIMITER //

CREATE PROCEDURE GetCharactersByAffiliation(
    IN aff_name VARCHAR(100)
)
BEGIN
    SELECT 
        c.character_id,
        c.name AS character_name,
        p.name AS person_name,
        p.birth_year,
        p.role_type,
        s.name AS species_name,
        s.classification,
        a.name AS affiliation_name,
        a.description
    FROM 
        characters c
        INNER JOIN people p ON c.person_id = p.person_id
        INNER JOIN species s ON c.species_id = s.species_id
        INNER JOIN affiliations a ON c.affiliation_id = a.affiliation_id
    WHERE 
        a.name = aff_name
    ORDER BY 
        c.character_id;
END //

DELIMITER ;

-- Test the procedure
CALL GetCharactersByAffiliation('Rebel Alliance');
CALL GetCharactersByAffiliation('Galactic Empire');
