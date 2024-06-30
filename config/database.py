from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "mysql+mysqlconnector://root:maurop10133@localhost:3306/TPIViajes"

engine = create_engine(DATABASE_URL)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get the session
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()