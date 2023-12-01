from sqlalchemy  import create_engine
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker
pass_db='1501'
SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:{pass_db}@localhost:5432/tarea"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False,autoflush=False)
Base = declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()