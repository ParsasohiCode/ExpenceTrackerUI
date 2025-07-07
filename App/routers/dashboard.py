from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, Form, Request, Depends, Cookie, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from ..db import SessionLocal
from ..models import Expenses
import jwt
from ..routers.auth import SECRET_KEY, ALGORYTHM

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

router = APIRouter(
  prefix="/dashboard",
  tags=["dashboard"],
)

templates = Jinja2Templates(directory="App/templates")

db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/", response_class=HTMLResponse)
def dashboard_page(request: Request, db: db_dependency, access_token: str = Cookie(None), category: str = None, date: str = None):
    user_id = None
    if access_token:
        try:
            token = access_token.replace("Bearer ", "")
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORYTHM])
            user_id = payload.get("id")
        except Exception:
            pass
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    query = db.query(Expenses).filter(Expenses.owner_id == user_id)
    if category:
        query = query.filter(Expenses.category == category)
    if date:
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            query = query.filter(Expenses.date >= date_obj, Expenses.date < date_obj.replace(hour=23, minute=59, second=59))
        except Exception:
            pass
    expenses = query.order_by(Expenses.date.desc()).all()
    total = sum(e.amount for e in expenses)
    categories = db.query(Expenses.category).filter(Expenses.owner_id == user_id).distinct().all()
    return templates.TemplateResponse("dashboard.html", {"request": request, "expenses": expenses, "total": total, "categories": [c[0] for c in categories], "selected_category": category or '', "selected_date": date or ''})

@router.post("/add_expense")
def add_expense(request: Request, db: db_dependency, access_token: str = Cookie(None),
                title: str = Form(...), description: str = Form(...), amount: int = Form(...),
                category: str = Form(...), date: str = Form(None)):
    user_id = None
    if access_token:
        try:
            token = access_token.replace("Bearer ", "")
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORYTHM])
            user_id = payload.get("id")
        except Exception:
            pass
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    expense_date = datetime.strptime(date, "%Y-%m-%d") if date else datetime.now()
    expense = Expenses(
        title=title,
        description=description,
        amount=amount,
        date=expense_date,
        category=category,
        owner_id=user_id
    )
    db.add(expense)
    db.commit()
    return RedirectResponse(url="/dashboard/", status_code=303)

@router.post("/delete_expense/{expense_id}")
def delete_expense(expense_id: int, db: db_dependency, access_token: str = Cookie(None)):
  user_id = None
  if access_token:
      try:
          token = access_token.replace("Bearer ", "")
          payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORYTHM])
          user_id = payload.get("id")
      except Exception:
          pass
  if not user_id:
      raise HTTPException(status_code=401, detail="Not authenticated")
  expense = db.query(Expenses).filter(Expenses.id == expense_id, Expenses.owner_id == user_id).first()
  if not expense:
      raise HTTPException(status_code=404, detail="Expense not found")
  db.delete(expense)
  db.commit()
  return RedirectResponse(url="/dashboard/", status_code=303)

@router.post("/update_expense/{expense_id}")
def update_expense(expense_id: int, request: Request, db: db_dependency, access_token: str = Cookie(None),
                   title: str = Form(...), description: str = Form(...), amount: int = Form(...), category: str = Form(...), date: str = Form(None)):
    user_id = None
    if access_token:
        try:
            token = access_token.replace("Bearer ", "")
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORYTHM])
            user_id = payload.get("id")
        except Exception:
            pass
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    expense = db.query(Expenses).filter(Expenses.id == expense_id, Expenses.owner_id == user_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    from datetime import datetime
    expense.title = title
    expense.description = description
    expense.amount = amount
    expense.category = category
    if date:
        expense.date = datetime.strptime(date, "%Y-%m-%d")
    db.commit()
    return RedirectResponse(url="/dashboard/", status_code=303)