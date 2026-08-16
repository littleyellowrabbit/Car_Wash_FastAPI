from sqlalchemy import Column,String,Integer
from sqlalchemy.orm import DeclarativeBase

class SQLBase(DeclarativeBase):
    pass

class User(SQLBase):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(15),nullable=False)
    password = Column(String(15),nullable=False)
    permission = Column(String(15),nullable=False)