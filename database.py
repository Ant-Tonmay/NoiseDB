from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import urllib.parse

password = urllib.parse.quote("Root@003")  # URL-encode the password
URL_DATABASE = f"mysql+pymysql://home:{password}@localhost:3306/NoiseApp"
engine = create_engine(URL_DATABASE)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()