from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from .auth import get_current_user_from_cookie
from ..db import SessionLocal
from ..models import Expenses

expenses_router = APIRouter(
  prefix="/expenses",
  tags=["expenses"],
)

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

class Expense(BaseModel):
  title: str = Field(min_length=3)
  amount: int = Field(gt=0)
  description: str = Field(min_length=3)
  date: datetime = Field(default=datetime.now().date())
  category: str = Field(min_length=3)


db_dependency = Annotated[Session, Depends(get_db)]

current_user = Annotated[dict, Depends(get_current_user_from_cookie)]

@expenses_router.get("/read_all_expenses")
async def read_all_expenses(db: db_dependency , current_user: current_user):
  if current_user is None:
    raise HTTPException(status_code=401, detail="Unauthorized")
  return db.query(Expenses).filter(Expenses.owner_id == current_user.get("id")).all()

@expenses_router.get("/read_expense/{expense_id}")
async def read_expense(expense_id: int, db: db_dependency , current_user: current_user):
  if current_user is None:
    raise HTTPException(status_code=401, detail="Unauthorized")
  expense = db.query(Expenses).filter(Expenses.id == expense_id).first()
  if not expense:
    raise HTTPException(status_code=404, detail="Expense not found")
  return expense

@expenses_router.post("/create_expense")
async def create_expense(expense: Expense, db: db_dependency , current_user: current_user):
  if current_user is None:
    raise HTTPException(status_code=401, detail="Unauthorized")
  db_expense = Expenses(**expense.model_dump() , owner_id = current_user.get("id"))
  db.add(db_expense)
  db.commit()
  return {"message": "Expense created successfully"}

@expenses_router.put("/update_expense/{expense_id}")
async def update_expense(expense_id: int, expense: Expense, db: db_dependency , current_user: current_user):
  if current_user is None:
    raise HTTPException(status_code=401, detail="Unauthorized")
  expense_to_update = db.query(Expenses).filter(Expenses.id == expense_id).first()
  if not expense_to_update:
    raise HTTPException(status_code=404, detail="Expense not found")

@expenses_router.delete("/delete_expense/{expense_id}")
async def delete_expense(expense_id: int, db: db_dependency , current_user: current_user):
  if current_user.get("role") != "admin":
    raise HTTPException(status_code=403, detail="Forbidden")
  expense = db.query(Expenses).filter(Expenses.id == expense_id).first()
  if not expense:
    raise HTTPException(status_code=404, detail="Expense not found")
