from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import SessionLocal, engine
from orm_models import Base, Franchise, Film, TVSeries, Book, Species, Affiliation, Person, Character, Planet, Game
from pydantic import BaseModel
from typing import Optional

Base.metadata.create_all(bind=engine)

description_text = """
## Star Wars Database API

"""

app = FastAPI(
    title="Star Wars Database API",
    description=description_text,
    version="1.0.0",
    openapi_tags=[
        {"name": "People", "description": "Manage people - START HERE to create characters"},
        {"name": "Species", "description": "Manage species (Human, Twi'lek, etc.)"},
        {"name": "Affiliations", "description": "Manage affiliations (Rebel Alliance, Empire, etc.)"},
        {"name": "Characters", "description": "Manage characters (requires Person, Species, Affiliation IDs)"},
        {"name": "Advanced Queries", "description": "Complex queries with multiple joins, views, and procedures"},
        {"name": "Franchise", "description": "Manage Star Wars franchises"},
        {"name": "Films", "description": "Manage films with ratings and box office"},
        {"name": "Planets", "description": "Manage planets and locations"},
        {"name": "TV Series", "description": "Manage TV series"},
        {"name": "Books", "description": "Manage books"},
        {"name": "Games", "description": "Manage video games"},
    ]
)

# After populate.py: uvicorn api:app --reload

# ------------ helper ------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------ Pydantic Models for POST/PUT ------------
class CharacterCreate(BaseModel):
    name: str
    person_id: int
    species_id: int
    affiliation_id: int

class CharacterUpdate(BaseModel):
    name: Optional[str] = None
    species_id: Optional[int] = None
    affiliation_id: Optional[int] = None

class PersonCreate(BaseModel):
    name: str
    birth_year: Optional[str] = None
    role_type: Optional[str] = None

class SpeciesCreate(BaseModel):
    name: str
    classification: str

class AffiliationCreate(BaseModel):
    name: str
    description: Optional[str] = None

class FranchiseCreate(BaseModel):
    name: str
    description: Optional[str] = None
    start_year: Optional[int] = None

class FilmCreate(BaseModel):
    franchise_id: int
    rating: str
    box_office: int

class PlanetCreate(BaseModel):
    name: str
    region: Optional[str] = None
    climate: Optional[str] = None

# =============================================================
# PEOPLE - Foundation table (no dependencies)
# =============================================================
@app.get("/people", tags=["People"], summary="List all people")
def get_all_people(db: Session = Depends(get_db)):
    """**READ** - Get all people in the database"""
    return db.query(Person).order_by(Person.person_id).all()

@app.get("/people/{person_id}", tags=["People"], summary="Get one person")
def get_person(person_id: int, db: Session = Depends(get_db)):
    """**READ** - Get specific person by ID"""
    person = db.query(Person).filter_by(person_id=person_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return person

@app.post("/people", tags=["People"], summary="Create new person")
def create_person(person: PersonCreate, db: Session = Depends(get_db)):
    """**CREATE** - Add new person (do this FIRST before creating characters)
    
    Example:
    ```json
    {
      "name": "Leia Organa",
      "birth_year": "19BBY",
      "role_type": "Princess"
    }
    ```
    """
    new_person = Person(**person.dict())
    db.add(new_person)
    db.commit()
    db.refresh(new_person)
    return new_person

@app.put("/people/{person_id}", tags=["People"], summary="Update person")
def update_person(person_id: int, person: PersonCreate, db: Session = Depends(get_db)):
    """**UPDATE** - Modify existing person"""
    db_person = db.query(Person).filter_by(person_id=person_id).first()
    if not db_person:
        raise HTTPException(status_code=404, detail="Person not found")
    
    if person.name:
        db_person.name = person.name
    if person.birth_year:
        db_person.birth_year = person.birth_year
    if person.role_type:
        db_person.role_type = person.role_type
    
    db.commit()
    db.refresh(db_person)
    return db_person

@app.delete("/people/{person_id}", tags=["People"], summary="Delete person")
def delete_person(person_id: int, db: Session = Depends(get_db)):
    """**DELETE** - Remove person"""
    person = db.query(Person).filter_by(person_id=person_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    db.delete(person)
    db.commit()
    return {"status": "deleted", "person_id": person_id}

# =============================================================
# 2. SPECIES - Foundation table (no dependencies)
# =============================================================
@app.get("/species", tags=["Species"])
def get_all_species(db: Session = Depends(get_db)):
    """READ - Get all species"""
    return db.query(Species).order_by(Species.species_id).all()

@app.get("/species/{species_id}", tags=["Species"])
def get_species(species_id: int, db: Session = Depends(get_db)):
    """READ - Get specific species"""
    species = db.query(Species).filter_by(species_id=species_id).first()
    if not species:
        raise HTTPException(status_code=404, detail="Species not found")
    return species

@app.post("/species", tags=["Species"])
def create_species(species: SpeciesCreate, db: Session = Depends(get_db)):
    """CREATE - Add new species"""
    new_species = Species(**species.dict())
    db.add(new_species)
    db.commit()
    db.refresh(new_species)
    return new_species

@app.put("/species/{species_id}", tags=["Species"])
def update_species(species_id: int, species: SpeciesCreate, db: Session = Depends(get_db)):
    """UPDATE - Modify existing species"""
    db_species = db.query(Species).filter_by(species_id=species_id).first()
    if not db_species:
        raise HTTPException(status_code=404, detail="Species not found")
    
    if species.name:
        db_species.name = species.name
    if species.classification:
        db_species.classification = species.classification
    
    db.commit()
    db.refresh(db_species)
    return db_species

@app.delete("/species/{species_id}", tags=["Species"])
def delete_species(species_id: int, db: Session = Depends(get_db)):
    """DELETE - Remove species"""
    species = db.query(Species).filter_by(species_id=species_id).first()
    if not species:
        raise HTTPException(status_code=404, detail="Species not found")
    db.delete(species)
    db.commit()
    return {"status": "deleted", "species_id": species_id}

# =============================================================
# 3. AFFILIATIONS - Foundation table (no dependencies)
# =============================================================
@app.get("/affiliations", tags=["Affiliations"])
def get_all_affiliations(db: Session = Depends(get_db)):
    """READ - Get all affiliations"""
    return db.query(Affiliation).order_by(Affiliation.affiliation_id).all()

@app.get("/affiliations/{affiliation_id}", tags=["Affiliations"])
def get_affiliation(affiliation_id: int, db: Session = Depends(get_db)):
    """READ - Get specific affiliation"""
    affiliation = db.query(Affiliation).filter_by(affiliation_id=affiliation_id).first()
    if not affiliation:
        raise HTTPException(status_code=404, detail="Affiliation not found")
    return affiliation

@app.post("/affiliations", tags=["Affiliations"])
def create_affiliation(affiliation: AffiliationCreate, db: Session = Depends(get_db)):
    """CREATE - Add new affiliation"""
    new_affiliation = Affiliation(**affiliation.dict())
    db.add(new_affiliation)
    db.commit()
    db.refresh(new_affiliation)
    return new_affiliation

@app.put("/affiliations/{affiliation_id}", tags=["Affiliations"])
def update_affiliation(affiliation_id: int, affiliation: AffiliationCreate, db: Session = Depends(get_db)):
    """UPDATE - Modify existing affiliation"""
    db_affiliation = db.query(Affiliation).filter_by(affiliation_id=affiliation_id).first()
    if not db_affiliation:
        raise HTTPException(status_code=404, detail="Affiliation not found")
    
    if affiliation.name:
        db_affiliation.name = affiliation.name
    if affiliation.description:
        db_affiliation.description = affiliation.description
    
    db.commit()
    db.refresh(db_affiliation)
    return db_affiliation

@app.delete("/affiliations/{affiliation_id}", tags=["Affiliations"])
def delete_affiliation(affiliation_id: int, db: Session = Depends(get_db)):
    """DELETE - Remove affiliation"""
    affiliation = db.query(Affiliation).filter_by(affiliation_id=affiliation_id).first()
    if not affiliation:
        raise HTTPException(status_code=404, detail="Affiliation not found")
    db.delete(affiliation)
    db.commit()
    return {"status": "deleted", "affiliation_id": affiliation_id}

# =============================================================
# 4. CHARACTERS - Requires person_id, species_id, affiliation_id
# =============================================================
@app.get("/characters", tags=["Characters"])
def get_all_characters(db: Session = Depends(get_db)):
    """READ - Get all characters"""
    return db.query(Character).order_by(Character.character_id).all()

@app.get("/characters/{character_id}", tags=["Characters"])
def get_character(character_id: int, db: Session = Depends(get_db)):
    """READ - Get specific character"""
    character = db.query(Character).filter_by(character_id=character_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    return character

@app.post("/characters", tags=["Characters"])
def create_character(character: CharacterCreate, db: Session = Depends(get_db)):
    """CREATE - Add new character (create person/species/affiliation first!)"""
    new_char = Character(**character.dict())
    db.add(new_char)
    db.commit()
    db.refresh(new_char)
    return new_char

@app.put("/characters/{character_id}", tags=["Characters"])
def update_character(character_id: int, character: CharacterUpdate, db: Session = Depends(get_db)):
    """UPDATE - Modify existing character"""
    db_char = db.query(Character).filter_by(character_id=character_id).first()
    if not db_char:
        raise HTTPException(status_code=404, detail="Character not found")
    
    if character.name:
        db_char.name = character.name
    if character.species_id:
        db_char.species_id = character.species_id
    if character.affiliation_id:
        db_char.affiliation_id = character.affiliation_id
    
    db.commit()
    db.refresh(db_char)
    return db_char

@app.delete("/characters/{character_id}", tags=["Characters"])
def delete_character(character_id: int, db: Session = Depends(get_db)):
    """DELETE - Remove character"""
    character = db.query(Character).filter_by(character_id=character_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    db.delete(character)
    db.commit()
    return {"status": "deleted", "character_id": character_id}

# =============================================================
# 5. ADVANCED QUERIES
# =============================================================
@app.get("/characters/detailed/all", tags=["Advanced Queries"])
def get_detailed_characters(db: Session = Depends(get_db)):
    """MULTIPLE JOINS - Character -> Person -> Species -> Affiliation"""
    results = db.query(
        Character.character_id,
        Character.name.label('character_name'),
        Person.name.label('person_name'),
        Person.birth_year,
        Person.role_type,
        Species.name.label('species_name'),
        Species.classification,
        Affiliation.name.label('affiliation_name'),
        Affiliation.description
    ).join(
        Person, Character.person_id == Person.person_id
    ).join(
        Species, Character.species_id == Species.species_id
    ).join(
        Affiliation, Character.affiliation_id == Affiliation.affiliation_id
    ).order_by(Character.character_id).all()
    
    return [{
        "character_id": r.character_id,
        "character_name": r.character_name,
        "person_name": r.person_name,
        "birth_year": r.birth_year,
        "role_type": r.role_type,
        "species_name": r.species_name,
        "classification": r.classification,
        "affiliation_name": r.affiliation_name,
        "affiliation_description": r.description
    } for r in results]

@app.get("/view/character_overview", tags=["Advanced Queries"])
def get_character_overview_view(db: Session = Depends(get_db)):
    """VIEW ACCESS - character_overview (run setup_view.sql first)"""
    try:
        result = db.execute(text("SELECT * FROM character_overview ORDER BY character_id"))
        columns = result.keys()
        rows = result.fetchall()
        return [{col: val for col, val in zip(columns, row)} for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"View not found. Run setup_view.sql first. Error: {str(e)}")

@app.get("/procedure/characters_by_affiliation/{affiliation_name}", tags=["Advanced Queries"])
def call_characters_by_affiliation(affiliation_name: str, db: Session = Depends(get_db)):
    """STORED PROCEDURE - GetCharactersByAffiliation (run setup_procedure.sql first)"""
    try:
        result = db.execute(
            text("CALL GetCharactersByAffiliation(:aff_name)"),
            {"aff_name": affiliation_name}
        )
        columns = result.keys()
        rows = result.fetchall()
        return [{col: val for col, val in zip(columns, row)} for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Procedure not found. Run setup_procedure.sql first. Error: {str(e)}")

# =============================================================
# 6. OTHER TABLES (Franchise, Films, TV, Books, Planets, Games)
# =============================================================

# ----------- FRANCHISE -----------
@app.get("/franchise", tags=["Franchise"])
def get_all_franchises(db: Session = Depends(get_db)):
    """READ - Get all franchises"""
    return db.query(Franchise).order_by(Franchise.franchise_id).all()

@app.get("/franchise/{franchise_id}", tags=["Franchise"])
def get_franchise(franchise_id: int, db: Session = Depends(get_db)):
    """READ - Get specific franchise"""
    franchise = db.query(Franchise).filter_by(franchise_id=franchise_id).first()
    if not franchise:
        raise HTTPException(status_code=404, detail="Franchise not found")
    return franchise

@app.post("/franchise", tags=["Franchise"])
def create_franchise(franchise: FranchiseCreate, db: Session = Depends(get_db)):
    """CREATE - Add new franchise"""
    new_franchise = Franchise(**franchise.dict())
    db.add(new_franchise)
    db.commit()
    db.refresh(new_franchise)
    return new_franchise

@app.put("/franchise/{franchise_id}", tags=["Franchise"])
def update_franchise(franchise_id: int, franchise: FranchiseCreate, db: Session = Depends(get_db)):
    """UPDATE - Modify franchise"""
    db_franchise = db.query(Franchise).filter_by(franchise_id=franchise_id).first()
    if not db_franchise:
        raise HTTPException(status_code=404, detail="Franchise not found")
    
    if franchise.name:
        db_franchise.name = franchise.name
    if franchise.description:
        db_franchise.description = franchise.description
    if franchise.start_year:
        db_franchise.start_year = franchise.start_year
    
    db.commit()
    db.refresh(db_franchise)
    return db_franchise

@app.delete("/franchise/{franchise_id}", tags=["Franchise"])
def delete_franchise(franchise_id: int, db: Session = Depends(get_db)):
    """DELETE - Remove franchise"""
    franchise = db.query(Franchise).filter_by(franchise_id=franchise_id).first()
    if not franchise:
        raise HTTPException(status_code=404, detail="Franchise not found")
    db.delete(franchise)
    db.commit()
    return {"status": "deleted", "franchise_id": franchise_id}

# ----------- FILMS -----------
@app.get("/films", tags=["Films"])
def get_all_films(db: Session = Depends(get_db)):
    """READ - Get all films"""
    return db.query(Film).order_by(Film.film_id).all()

@app.get("/films/{film_id}", tags=["Films"])
def get_film(film_id: int, db: Session = Depends(get_db)):
    """READ - Get specific film"""
    film = db.query(Film).filter_by(film_id=film_id).first()
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")
    return film

@app.post("/films", tags=["Films"])
def create_film(film: FilmCreate, db: Session = Depends(get_db)):
    """CREATE - Add new film"""
    new_film = Film(**film.dict())
    db.add(new_film)
    db.commit()
    db.refresh(new_film)
    return new_film

@app.put("/films/{film_id}", tags=["Films"])
def update_film(film_id: int, rating: Optional[str] = None, box_office: Optional[int] = None, db: Session = Depends(get_db)):
    """UPDATE - Modify film"""
    db_film = db.query(Film).filter_by(film_id=film_id).first()
    if not db_film:
        raise HTTPException(status_code=404, detail="Film not found")
    
    if rating:
        db_film.rating = rating
    if box_office:
        db_film.box_office = box_office
    
    db.commit()
    db.refresh(db_film)
    return db_film

@app.delete("/films/{film_id}", tags=["Films"])
def delete_film(film_id: int, db: Session = Depends(get_db)):
    """DELETE - Remove film"""
    film = db.query(Film).filter_by(film_id=film_id).first()
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")
    db.delete(film)
    db.commit()
    return {"status": "deleted", "film_id": film_id}

# ----------- PLANETS -----------
@app.get("/planets", tags=["Planets"])
def get_all_planets(db: Session = Depends(get_db)):
    """READ - Get all planets"""
    return db.query(Planet).order_by(Planet.planet_id).all()

@app.get("/planets/{planet_id}", tags=["Planets"])
def get_planet(planet_id: int, db: Session = Depends(get_db)):
    """READ - Get specific planet"""
    planet = db.query(Planet).filter_by(planet_id=planet_id).first()
    if not planet:
        raise HTTPException(status_code=404, detail="Planet not found")
    return planet

@app.post("/planets", tags=["Planets"])
def create_planet(planet: PlanetCreate, db: Session = Depends(get_db)):
    """CREATE - Add new planet"""
    new_planet = Planet(**planet.dict())
    db.add(new_planet)
    db.commit()
    db.refresh(new_planet)
    return new_planet

@app.put("/planets/{planet_id}", tags=["Planets"])
def update_planet(planet_id: int, planet: PlanetCreate, db: Session = Depends(get_db)):
    """UPDATE - Modify planet"""
    db_planet = db.query(Planet).filter_by(planet_id=planet_id).first()
    if not db_planet:
        raise HTTPException(status_code=404, detail="Planet not found")
    
    if planet.name:
        db_planet.name = planet.name
    if planet.region:
        db_planet.region = planet.region
    if planet.climate:
        db_planet.climate = planet.climate
    
    db.commit()
    db.refresh(db_planet)
    return db_planet

@app.delete("/planets/{planet_id}", tags=["Planets"])
def delete_planet(planet_id: int, db: Session = Depends(get_db)):
    """DELETE - Remove planet"""
    planet = db.query(Planet).filter_by(planet_id=planet_id).first()
    if not planet:
        raise HTTPException(status_code=404, detail="Planet not found")
    db.delete(planet)
    db.commit()
    return {"status": "deleted", "planet_id": planet_id}

# ----------- TV SERIES -----------
@app.get("/tvseries", tags=["TV Series"])
def get_all_tvseries(db: Session = Depends(get_db)):
    """READ - Get all TV series"""
    return db.query(TVSeries).order_by(TVSeries.series_id).all()

@app.get("/tvseries/{series_id}", tags=["TV Series"])
def get_tvseries(series_id: int, db: Session = Depends(get_db)):
    """READ - Get specific TV series"""
    series = db.query(TVSeries).filter_by(series_id=series_id).first()
    if not series:
        raise HTTPException(status_code=404, detail="TV Series not found")
    return series

@app.delete("/tvseries/{series_id}", tags=["TV Series"])
def delete_tvseries(series_id: int, db: Session = Depends(get_db)):
    """DELETE - Remove TV series"""
    series = db.query(TVSeries).filter_by(series_id=series_id).first()
    if not series:
        raise HTTPException(status_code=404, detail="TV Series not found")
    db.delete(series)
    db.commit()
    return {"status": "deleted", "series_id": series_id}

# ----------- BOOKS -----------
@app.get("/books", tags=["Books"])
def get_all_books(db: Session = Depends(get_db)):
    """READ - Get all books"""
    return db.query(Book).order_by(Book.book_id).all()

@app.get("/books/{book_id}", tags=["Books"])
def get_book(book_id: int, db: Session = Depends(get_db)):
    """READ - Get specific book"""
    book = db.query(Book).filter_by(book_id=book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.delete("/books/{book_id}", tags=["Books"])
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """DELETE - Remove book"""
    book = db.query(Book).filter_by(book_id=book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"status": "deleted", "book_id": book_id}

# ----------- GAMES -----------
@app.get("/games", tags=["Games"])
def get_all_games(db: Session = Depends(get_db)):
    """READ - Get all games"""
    return db.query(Game).order_by(Game.game_id).all()

@app.get("/games/{game_id}", tags=["Games"])
def get_game(game_id: int, db: Session = Depends(get_db)):
    """READ - Get specific game"""
    game = db.query(Game).filter_by(game_id=game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game

@app.delete("/games/{game_id}", tags=["Games"])
def delete_game(game_id: int, db: Session = Depends(get_db)):
    """DELETE - Remove game"""
    game = db.query(Game).filter_by(game_id=game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    db.delete(game)
    db.commit()
    return {"status": "deleted", "game_id": game_id}
