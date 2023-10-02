from sqlalchemy import Column, Integer, String, ARRAY, Tuple
from app.database import Base


class Books(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    description = Column(String)
    rating = Column(Integer)


class Audit(Base):
    __tablename__ = "audit"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    headers = Column("headers", ARRAY(String))
    method = Column(String)
    response = Column(String)
