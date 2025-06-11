from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    games_played = Column(Integer, default=0)
    games_won = Column(Integer, default=0)

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

class Password(Base):
    __tablename__ = "passwords"
    id = Column(Integer, primary_key=True)
    word = Column(String)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship("Category")

class GameResult(Base):
    __tablename__ = "results"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    points = Column(Integer, nullable=False)
