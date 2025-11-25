from fastapi import FastAPI
from database import SessionLocal, engine
from orm_models import Base, Franchise, Film, TVSeries, Book, Species, Affiliation, Person, Character, Planet, Game

Base.metadata.create_all(bind=engine)
app = FastAPI()

# After populate.py: uvicorn api:app --reload

# ------------ helper ------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------------------------------------------
# BASIC ENDPOINT GENERATOR
# (super simple CRUD for every table)
# ---------------------------------------------------------
def build_crud_routes(model, name: str):
    @app.get(f"/{name}")
    def list_items(db=next(get_db())):
        return db.query(model).all()

    @app.get(f"/{name}/{{item_id}}")
    def get_item(item_id: int, db=next(get_db())):
        return db.query(model).filter_by(**{model.__table__.primary_key.columns.values()[0].name: item_id}).first()

    @app.delete(f"/{name}/{{item_id}}")
    def delete_item(item_id: int, db=next(get_db())):
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
build_crud_routes(Species, "species")
build_crud_routes(Affiliation, "affiliations")
build_crud_routes(Person, "people")
build_crud_routes(Character, "characters")
build_crud_routes(Planet, "planets")
build_crud_routes(Game, "games")
