-- =====================================================
-- CREATE VIEW: character_overview
-- =====================================================
-- This view provides detailed character information
-- by joining characters with people, species, and affiliations
-- =====================================================

USE starwarsDB;

-- Drop if exists
DROP VIEW IF EXISTS character_overview;

-- Create the view
CREATE VIEW character_overview AS
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
ORDER BY 
    c.character_id;

-- Test the view
SELECT * FROM character_overview;
