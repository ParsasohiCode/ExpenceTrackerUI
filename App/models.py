from .db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from datetime import datetime

class Users(Base):
  __tablename__ = 'users' 
  id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  username = Column(String, unique=True, nullable=False)
  email = Column(String, unique=True, nullable=False)
  hashed_password = Column(String, nullable=False)
  is_active = Column(Boolean, default=True)
  role = Column(String, default="user")
  
class Expenses(Base):
  __tablename__ = 'expenses'
  id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  title = Column(String, nullable=False)
  description = Column(String, nullable=False)
  amount = Column(Integer, nullable=False)
  date = Column(DateTime, nullable=False , default=datetime.now())
  category = Column(String, nullable=False)
  owner_id = Column(Integer, ForeignKey("users.id"))