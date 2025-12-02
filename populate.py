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
f1 = Franchise(name="Star Wars", description="Main Skywalker Saga Timeline", start_year=1977)
f2 = Franchise(name="Star Wars Legends", description="Expanded Universe Stories", start_year=1991)
f3 = Franchise(name="Star Wars Disney+", description="Streaming Original Series", start_year=2019)
session.add_all([f1, f2, f3])
session.flush()  # get franchise IDs

# ---------------- FILMS --------------------
session.add_all([
    Film(franchise=f1, rating="PG", box_office=775398007),     # A New Hope
    Film(franchise=f1, rating="PG", box_office=538375067),     # Empire Strikes Back
    Film(franchise=f1, rating="PG", box_office=475106177),     # Return of the Jedi
    Film(franchise=f1, rating="PG", box_office=1027044677),    # The Phantom Menace
    Film(franchise=f1, rating="PG", box_office=653779970),     # Attack of the Clones
    Film(franchise=f1, rating="PG-13", box_office=868390560),  # Revenge of the Sith
    Film(franchise=f1, rating="PG-13", box_office=2068223624), # The Force Awakens
    Film(franchise=f1, rating="PG-13", box_office=1332539889), # The Last Jedi
    Film(franchise=f1, rating="PG-13", box_office=1074144248), # The Rise of Skywalker
    Film(franchise=f1, rating="PG-13", box_office=1056057273), # Rogue One
])

# ---------------- TV SERIES ----------------
session.add_all([
    TVSeries(franchise=f1, title="The Clone Wars", start_year=2008, end_year=2020, num_seasons=7),
    TVSeries(franchise=f1, title="Star Wars Rebels", start_year=2014, end_year=2018, num_seasons=4),
    TVSeries(franchise=f3, title="The Mandalorian", start_year=2019, end_year=2023, num_seasons=3),
    TVSeries(franchise=f3, title="The Book of Boba Fett", start_year=2021, end_year=2022, num_seasons=1),
    TVSeries(franchise=f3, title="Obi-Wan Kenobi", start_year=2022, end_year=2022, num_seasons=1),
    TVSeries(franchise=f3, title="Ahsoka", start_year=2023, end_year=2023, num_seasons=1),
    TVSeries(franchise=f1, title="Star Wars Resistance", start_year=2018, end_year=2020, num_seasons=2),
])

# ---------------- BOOKS --------------------
session.add_all([
    Book(franchise=f2, title="Heir to the Empire", publication_year=1991, author="Timothy Zahn"),
    Book(franchise=f2, title="Dark Force Rising", publication_year=1992, author="Timothy Zahn"),
    Book(franchise=f2, title="The Last Command", publication_year=1993, author="Timothy Zahn"),
    Book(franchise=f1, title="Thrawn", publication_year=2017, author="Timothy Zahn"),
    Book(franchise=f1, title="Ahsoka", publication_year=2016, author="E.K. Johnston"),
    Book(franchise=f1, title="Lost Stars", publication_year=2015, author="Claudia Gray"),
    Book(franchise=f1, title="Bloodline", publication_year=2016, author="Claudia Gray"),
    Book(franchise=f2, title="Shadows of the Empire", publication_year=1996, author="Steve Perry"),
])

# ---------------- SPECIES ------------------
human = Species(name="Human", classification="Mammal")
twi = Species(name="Twi'lek", classification="Humanoid")
wookiee = Species(name="Wookiee", classification="Mammal")
droid = Species(name="Droid", classification="Artificial")
togruta = Species(name="Togruta", classification="Humanoid")
yoda_species = Species(name="Yoda's Species", classification="Unknown")
gungan = Species(name="Gungan", classification="Amphibian")
session.add_all([human, twi, wookiee, droid, togruta, yoda_species, gungan])

# ---------------- AFFILIATIONS -------------
rebel = Affiliation(name="Rebel Alliance", description="Resistance against the Empire")
empire = Affiliation(name="Galactic Empire", description="Authoritarian galactic government")
jedi = Affiliation(name="Jedi Order", description="Ancient order of Force users")
sith = Affiliation(name="Sith", description="Dark side Force users")
republic = Affiliation(name="Galactic Republic", description="Democratic galactic government")
resistance = Affiliation(name="Resistance", description="Opposition to the First Order")
first_order = Affiliation(name="First Order", description="Successor to the Galactic Empire")
session.add_all([rebel, empire, jedi, sith, republic, resistance, first_order])

# ---------------- PEOPLE -------------------
luke = Person(name="Luke Skywalker", birth_year="19BBY", role_type="Jedi Knight")
vader = Person(name="Darth Vader", birth_year="41BBY", role_type="Sith Lord")
leia = Person(name="Leia Organa", birth_year="19BBY", role_type="Princess")
han = Person(name="Han Solo", birth_year="29BBY", role_type="Smuggler")
obi_wan = Person(name="Obi-Wan Kenobi", birth_year="57BBY", role_type="Jedi Master")
yoda = Person(name="Yoda", birth_year="896BBY", role_type="Jedi Grand Master")
anakin = Person(name="Anakin Skywalker", birth_year="41BBY", role_type="Jedi Knight")
padme = Person(name="Padmé Amidala", birth_year="46BBY", role_type="Queen")
ahsoka = Person(name="Ahsoka Tano", birth_year="36BBY", role_type="Former Jedi")
chewbacca = Person(name="Chewbacca", birth_year="200BBY", role_type="Co-pilot")
r2d2 = Person(name="R2-D2", birth_year="33BBY", role_type="Astromech Droid")
c3po = Person(name="C-3PO", birth_year="112BBY", role_type="Protocol Droid")
rey = Person(name="Rey", birth_year="15ABY", role_type="Jedi")
kylo = Person(name="Ben Solo", birth_year="5ABY", role_type="Dark Side User")
palpatine = Person(name="Sheev Palpatine", birth_year="84BBY", role_type="Sith Lord")
session.add_all([luke, vader, leia, han, obi_wan, yoda, anakin, padme, ahsoka, chewbacca, r2d2, c3po, rey, kylo, palpatine])
session.flush()  # ensure IDs assigned

# ---------------- CHARACTERS ---------------
session.add_all([
    Character(name="Luke Skywalker", person=luke, species=human, affiliation=rebel),
    Character(name="Darth Vader", person=vader, species=human, affiliation=empire),
    Character(name="Princess Leia", person=leia, species=human, affiliation=rebel),
    Character(name="Han Solo", person=han, species=human, affiliation=rebel),
    Character(name="Obi-Wan Kenobi", person=obi_wan, species=human, affiliation=jedi),
    Character(name="Yoda", person=yoda, species=yoda_species, affiliation=jedi),
    Character(name="Anakin Skywalker", person=anakin, species=human, affiliation=jedi),
    Character(name="Padmé Amidala", person=padme, species=human, affiliation=republic),
    Character(name="Ahsoka Tano", person=ahsoka, species=togruta, affiliation=jedi),
    Character(name="Chewbacca", person=chewbacca, species=wookiee, affiliation=rebel),
    Character(name="R2-D2", person=r2d2, species=droid, affiliation=rebel),
    Character(name="C-3PO", person=c3po, species=droid, affiliation=rebel),
    Character(name="Rey", person=rey, species=human, affiliation=resistance),
    Character(name="Kylo Ren", person=kylo, species=human, affiliation=first_order),
    Character(name="Emperor Palpatine", person=palpatine, species=human, affiliation=sith),
])

# ---------------- PLANETS -----------------
session.add_all([
    Planet(name="Tatooine", region="Outer Rim", climate="Arid desert"),
    Planet(name="Coruscant", region="Core Worlds", climate="Urban cityscape"),
    Planet(name="Naboo", region="Mid Rim", climate="Temperate grasslands"),
    Planet(name="Hoth", region="Outer Rim", climate="Frozen tundra"),
    Planet(name="Dagobah", region="Outer Rim", climate="Murky swamp"),
    Planet(name="Endor", region="Outer Rim", climate="Temperate forest"),
    Planet(name="Kamino", region="Wild Space", climate="Stormy ocean"),
    Planet(name="Geonosis", region="Outer Rim", climate="Rocky desert"),
    Planet(name="Mustafar", region="Outer Rim", climate="Volcanic lava"),
    Planet(name="Alderaan", region="Core Worlds", climate="Temperate plains"),
    Planet(name="Jakku", region="Western Reaches", climate="Desert wasteland"),
    Planet(name="Mandalore", region="Outer Rim", climate="Desert and forest"),
])

# ---------------- GAMES -------------------
session.add_all([
    Game(franchise=f1, title="Knights of the Old Republic", release_year=2003, developer="BioWare"),
    Game(franchise=f1, title="Star Wars Battlefront II", release_year=2005, developer="Pandemic Studios"),
    Game(franchise=f1, title="Jedi: Fallen Order", release_year=2019, developer="Respawn Entertainment"),
    Game(franchise=f1, title="Jedi: Survivor", release_year=2023, developer="Respawn Entertainment"),
    Game(franchise=f1, title="Republic Commando", release_year=2005, developer="LucasArts"),
    Game(franchise=f2, title="The Force Unleashed", release_year=2008, developer="LucasArts"),
    Game(franchise=f1, title="Star Wars Squadrons", release_year=2020, developer="Motive Studios"),
])

session.commit()
session.close()

print("Database populated.")
