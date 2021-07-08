from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json
postgres = open("postgres.json")
POSTGRES_URI = json.load(postgres)["POSTGRES_URI"]
postgres.close()
engine = create_engine(
    POSTGRES_URI)
Session = sessionmaker(bind=engine)
Base = declarative_base()
