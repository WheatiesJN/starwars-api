# HOW TO USE (slow + simple):
# 1. cd c:\xampp\htdocs\projects\starwars_project
# 2. py -m venv .venv              # create env (space before .venv)
# 3. .\.venv\Scripts\Activate.ps1  # EXACT: one dot + backslash; NOT '..venv'
#    If blocked: Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
# 4. pip install SQLAlchemy PyMySQL fastapi uvicorn
# 5. Ensure MySQL schema 'starwarsDB' exists
# 6. python populate.py
# 7. uvicorn api:app --reload  (optional API)
# 8. If activation fails, run: Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
# 9. If you see Already populated; abort, drop tables or delete rows before rerun.

from sqlalchemy import (
    Column, Integer, String, ForeignKey, CheckConstraint,
    UniqueConstraint, Index
)
from sqlalchemy.orm import relationship
from database import Base

# ----------------------------------------------------------
# FRANCHISE
# ----------------------------------------------------------
class Franchise(Base):
    __tablename__ = "franchise"

    franchise_id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255))
    start_year = Column(Integer)

    films = relationship("Film", back_populates="franchise")
    tv_series = relationship("TVSeries", back_populates="franchise")
    books = relationship("Book", back_populates="franchise")
    games = relationship("Game", back_populates="franchise")

# ----------------------------------------------------------
# FILMS
# ----------------------------------------------------------
class Film(Base):
    __tablename__ = "films"

    film_id = Column(Integer, primary_key=True)
    franchise_id = Column(Integer, ForeignKey("franchise.franchise_id"))
    rating = Column(String(10))
    box_office = Column(Integer)

    franchise = relationship("Franchise", back_populates="films")

    __table_args__ = (
        Index("idx_films_franchise", "franchise_id"),
        CheckConstraint('box_office >= 0', name='check_box_office_positive')
    )

# ----------------------------------------------------------
# TV SERIES
# ----------------------------------------------------------
class TVSeries(Base):
    __tablename__ = "tv_series"

    series_id = Column(Integer, primary_key=True)
    franchise_id = Column(Integer, ForeignKey("franchise.franchise_id"))
    title = Column(String(100))
    start_year = Column(Integer)
    end_year = Column(Integer)
    num_seasons = Column(Integer)

    franchise = relationship("Franchise", back_populates="tv_series")

# ----------------------------------------------------------
# BOOKS
# ----------------------------------------------------------
class Book(Base):
    __tablename__ = "books"

    book_id = Column(Integer, primary_key=True)
    franchise_id = Column(Integer, ForeignKey("franchise.franchise_id"))
    title = Column(String(100))
    publication_year = Column(Integer)
    author = Column(String(100))

    franchise = relationship("Franchise", back_populates="books")

# ----------------------------------------------------------
# SPECIES
# ----------------------------------------------------------
class Species(Base):
    __tablename__ = "species"

    species_id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    classification = Column(String(100))

    characters = relationship("Character", back_populates="species")

# ----------------------------------------------------------
# AFFILIATIONS
# ----------------------------------------------------------
class Affiliation(Base):
    __tablename__ = "affiliations"

    affiliation_id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    description = Column(String(255))

    characters = relationship("Character", back_populates="affiliation")

# ----------------------------------------------------------
# PEOPLE
# ----------------------------------------------------------
class Person(Base):
    __tablename__ = "people"

    person_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    birth_year = Column(String(20))
    role_type = Column(String(50))

    characters = relationship("Character", back_populates="person")

# ----------------------------------------------------------
# CHARACTERS
# ----------------------------------------------------------
class Character(Base):
    __tablename__ = "characters"

    character_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    person_id = Column(Integer, ForeignKey("people.person_id"))
    species_id = Column(Integer, ForeignKey("species.species_id"))
    affiliation_id = Column(Integer, ForeignKey("affiliations.affiliation_id"))

    person = relationship("Person", back_populates="characters")
    species = relationship("Species", back_populates="characters")
    affiliation = relationship("Affiliation", back_populates="characters")

    __table_args__ = (UniqueConstraint("name", "species_id", name="uix_character_species"),)

# ----------------------------------------------------------
# PLANETS
# ----------------------------------------------------------
class Planet(Base):
    __tablename__ = "planets"

    planet_id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    region = Column(String(100))
    climate = Column(String(100))

# ----------------------------------------------------------
# GAMES
# ----------------------------------------------------------
class Game(Base):
    __tablename__ = "games"

    game_id = Column(Integer, primary_key=True)
    franchise_id = Column(Integer, ForeignKey("franchise.franchise_id"))
    title = Column(String(100))
    release_year = Column(Integer)
    developer = Column(String(100))

    franchise = relationship("Franchise", back_populates="games")
