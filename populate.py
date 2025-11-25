# RUN THESE (one per line):
# cd c:\xampp\htdocs\projects\starwars_project
# py -m venv .venv
# .\.venv\Scripts\Activate.ps1
# pip install SQLAlchemy PyMySQL
# python populate.py

from database import Base, engine, SessionLocal
from orm_models import *

Base.metadata.create_all(engine)

session = SessionLocal()

# Abort if already populated
if session.query(Franchise).filter_by(name="Star Wars").first():
    print("Already populated; abort.")
    session.close()
    raise SystemExit()

# ---------------- FRANCHISE ----------------
f1 = Franchise(name="Star Wars", description="Main Timeline", start_year=1977)
session.add(f1)
session.flush()  # get f1.franchise_id

# ---------------- FILMS --------------------
session.add_all([
    Film(franchise=f1, rating="PG", box_office=300000000),
    Film(franchise=f1, rating="PG-13", box_office=500000000),
    Film(franchise=f1, rating="PG", box_office=600000000),
])

# ---------------- TV SERIES ----------------
session.add_all([
    TVSeries(franchise=f1, title="Clone Wars", start_year=2008, end_year=2020, num_seasons=7),
    TVSeries(franchise=f1, title="Rebels", start_year=2014, end_year=2018, num_seasons=4),
])

# ---------------- BOOKS --------------------
session.add_all([
    Book(franchise=f1, title="Thrawn", publication_year=2017, author="Timothy Zahn"),
    Book(franchise=f1, title="Heir to the Empire", publication_year=1991, author="Timothy Zahn"),
])

# ---------------- SPECIES ------------------
human = Species(name="Human", classification="Mammal")
twi = Species(name="Twi'lek", classification="Humanoid")
session.add_all([human, twi])

# ---------------- AFFILIATIONS -------------
rebel = Affiliation(name="Rebel Alliance", description="Resistance group")
empire = Affiliation(name="Galactic Empire", description="Authoritarian regime")
session.add_all([rebel, empire])

# ---------------- PEOPLE -------------------
luke = Person(name="Luke Skywalker", birth_year="19BBY", role_type="Jedi")
vader = Person(name="Darth Vader", birth_year="41BBY", role_type="Sith")
session.add_all([luke, vader])
session.flush()  # ensure IDs assigned

# ---------------- CHARACTERS ---------------
session.add_all([
    Character(name="Luke", person=luke, species=human, affiliation=rebel),
    Character(name="Vader", person=vader, species=human, affiliation=empire),
])

# ---------------- PLANETS -----------------
session.add_all([
    Planet(name="Tatooine", region="Outer Rim", climate="Arid"),
    Planet(name="Coruscant", region="Core Worlds", climate="Urban"),
    Planet(name="Naboo", region="Mid Rim", climate="Temperate"),
])

# ---------------- GAMES -------------------
session.add_all([
    Game(franchise=f1, title="KOTOR", release_year=2003, developer="Bioware"),
    Game(franchise=f1, title="Battlefront II", release_year=2005, developer="Pandemic"),
])

session.commit()
session.close()

print("Database populated.")
