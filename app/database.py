from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DATABASE = 'postgresql'
USER = 'danniel'
PASSWORD = 'danniel'
HOST = 'localhost'
PORT = '5432'
DB_NAME = 'postgres'

SQLALCHEMY_DATABASE_URL = f'postgresql://{USER}:{PASSWORD}@{HOST}/{DB_NAME}'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL)

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


