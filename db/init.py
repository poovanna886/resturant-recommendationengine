from sqlalchemy import Column, ForeignKey, Integer, String, Float, PickleType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()
class Restaurant(Base):
    __tablename__ = 'restaurant'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=True)
    type = Column(String(250), nullable=True) #Cuisine
    popularity = Column(Float, nullable=True)
    recommendation = Column(Float, nullable=True) #dict {user_id : float}

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=True)
    session_preferences = Column(PickleType, nullable=True) #filters




engine = create_engine('sqlite:///plated.db')
Base.metadata.create_all(engine)
