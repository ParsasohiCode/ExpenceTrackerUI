from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from passlib.hash import pbkdf2_sha256
from .auth import get_current_user
from ..db import SessionLocal
from ..models import Users

user_router = APIRouter(
  prefix="/user",
  tags=["user"],
)

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

class User(BaseModel):
  username: str = Field(min_length=3)
  email: str = Field(min_length=3)
  password: str = Field(min_length=3)

db_dependency = Annotated[Session, Depends(get_db)]

current_user = Annotated[dict, Depends(get_current_user)]

@user_router.get("/get_current_user_info")
async def get_current_user_info(db: db_dependency , current_user: current_user):
  if current_user is None:
    raise HTTPException(status_code=401, detail="Unauthorized")
  user = db.query(Users).filter(Users.id == current_user.get("id")).first()
  return user

@user_router.put("/change_password")
async def change_password(password: str,new_password: str, db: db_dependency , current_user: current_user):
  if current_user is None:
    raise HTTPException(status_code=401, detail="Unauthorized")
  user = db.query(Users).filter(Users.id == current_user.get("id")).first()
  if not user:
    raise HTTPException(status_code=404, detail="User not found")
  if not pbkdf2_sha256.verify(password, user.hashed_password):
    raise HTTPException(status_code=401, detail="Wrong password")
  user.hashed_password = pbkdf2_sha256.hash(new_password)
  db.commit()
  return {"message": "Password changed successfully"}