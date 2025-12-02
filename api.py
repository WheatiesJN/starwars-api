from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import SessionLocal, engine
from orm_models import Base, Franchise, Film, TVSeries, Book, Species, Affiliation, Person, Character, Planet, Game
from pydantic import BaseModel
from typing import Optional

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Star Wars Database API")

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

# =============================================================
# 1. PEOPLE - Foundation table (no dependencies)
# =============================================================
@app.get("/people")
def get_all_people(db: Session = Depends(get_db)):
    """READ - Get all people"""
    return db.query(Person).all()

@app.post("/people")
def create_person(person: PersonCreate, db: Session = Depends(get_db)):
    """CREATE - Add new person (do this FIRST before creating characters)"""
    new_person = Person(**person.dict())
    db.add(new_person)
    db.commit()
    db.refresh(new_person)
    return new_person

# =============================================================
# 2. SPECIES - Foundation table (no dependencies)
# =============================================================
@app.get("/species")
def get_all_species(db: Session = Depends(get_db)):
    """READ - Get all species"""
    return db.query(Species).all()

@app.post("/species")
def create_species(species: SpeciesCreate, db: Session = Depends(get_db)):
    """CREATE - Add new species"""
    new_species = Species(**species.dict())
    db.add(new_species)
    db.commit()
    db.refresh(new_species)
    return new_species

# =============================================================
# 3. AFFILIATIONS - Foundation table (no dependencies)
# =============================================================
@app.get("/affiliations")
def get_all_affiliations(db: Session = Depends(get_db)):
    """READ - Get all affiliations"""
    return db.query(Affiliation).all()

@app.post("/affiliations")
def create_affiliation(affiliation: AffiliationCreate, db: Session = Depends(get_db)):
    """CREATE - Add new affiliation"""
    new_affiliation = Affiliation(**affiliation.dict())
    db.add(new_affiliation)
    db.commit()
    db.refresh(new_affiliation)
    return new_affiliation

# =============================================================
# 4. CHARACTERS - Requires person_id, species_id, affiliation_id
# =============================================================
@app.get("/characters")
def get_all_characters(db: Session = Depends(get_db)):
    """READ - Get all characters"""
    return db.query(Character).all()

@app.get("/characters/{character_id}")
def get_character(character_id: int, db: Session = Depends(get_db)):
    """READ - Get specific character"""
    character = db.query(Character).filter_by(character_id=character_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    return character

@app.post("/characters")
def create_character(character: CharacterCreate, db: Session = Depends(get_db)):
    """CREATE - Add new character (create person/species/affiliation first!)"""
    new_char = Character(**character.dict())
    db.add(new_char)
    db.commit()
    db.refresh(new_char)
    return new_char

@app.put("/characters/{character_id}")
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

@app.delete("/characters/{character_id}")
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
@app.get("/characters/detailed/all")
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
    ).all()
    
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

@app.get("/view/character_overview")
def get_character_overview_view(db: Session = Depends(get_db)):
    """VIEW ACCESS - character_overview (run setup_view.sql first)"""
    try:
        result = db.execute(text("SELECT * FROM character_overview"))
        columns = result.keys()
        rows = result.fetchall()
        return [{col: val for col, val in zip(columns, row)} for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"View not found. Run setup_view.sql first. Error: {str(e)}")

@app.get("/procedure/characters_by_affiliation/{affiliation_name}")
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

def build_crud_routes(model, name: str):
    @app.get(f"/{name}")
    def list_items(db = Depends(get_db)):
        return db.query(model).all()

    @app.get(f"/{name}/{{item_id}}")
    def get_item(item_id: int, db = Depends(get_db)):
        return db.query(model).filter_by(**{model.__table__.primary_key.columns.values()[0].name: item_id}).first()

    @app.delete(f"/{name}/{{item_id}}")
    def delete_item(item_id: int, db = Depends(get_db)):
        obj = db.query(model).filter_by(**{model.__table__.primary_key.columns.values()[0].name: item_id}).first()
        if obj:
            db.delete(obj)
            db.commit()
            return {"status": "deleted"}
        return {"error": "not found"}

# attach endpoints
build_crud_routes(Franchise, "franchise")
build_crud_routes(Film, "films")
build_crud_routes(TVSeries, "tvseries")
build_crud_routes(Book, "books")
build_crud_routes(Planet, "planets")
build_crud_routes(Game, "games")
