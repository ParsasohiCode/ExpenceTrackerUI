from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .auth import get_current_user
from ..db import SessionLocal
from ..models import Users

admin_router = APIRouter(
  prefix="/admin",
  tags=["admin"],
)

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

db_dependency = Annotated[Session, Depends(get_db)]

current_user = Annotated[dict, Depends(get_current_user)]

@admin_router.get("/read_all_users")
async def read_all_users(db: db_dependency):
  users = db.query(Users).all()
  return users

@admin_router.get("/read_user/{user_id}")
async def read_user(user_id: int, db: db_dependency):
  user = db.query(Users).filter(Users.id == user_id).first()
  if not user:
    raise HTTPException(status_code=404, detail="User not found")
  return user

@admin_router.delete("/delete_user/{user_id}", status_code=204)
async def delete_user(user_id: int, db: db_dependency , current_user: current_user):
  if current_user.get("role") != "admin":
    raise HTTPException(status_code=403, detail="Forbidden")
  user = db.query(Users).filter(Users.id == user_id).first()
  if not user:
    raise HTTPException(status_code=404, detail="User not found")
  db.delete(user)
  db.commit()
  return {"message": "User deleted successfully"}