from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE = 'sqlite:///pdf-qa.db'
# Create a connection to the database
engine = create_engine(URL_DATABASE, connect_args={"check_same_thread": False})

# Create a session
SessionLocal = sessionmaker(autoflush=False,autocommit=False, bind=engine)

# Create a base class
Base = declarative_base()