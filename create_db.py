from database import engine, Base
import orm_models  # ensure models are imported so metadata is populated

def main():
    Base.metadata.create_all(bind=engine)
    print("DB tables created.")

if __name__ == "__main__":
    main()
