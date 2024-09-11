from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

URL_DATABASE = 'postgresql://postgres:Alekappa1@localhost:5432/next'
engine = create_engine(URL_DATABASE)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
