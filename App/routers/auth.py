from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request, Form, Cookie
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from ..db import SessionLocal
from ..models import Users
from passlib.hash import pbkdf2_sha256
import jwt
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

router = APIRouter(
  prefix="/auth",
  tags=["auth"],
)

SECRET_KEY = "nvpUREqrmpwnRUVP3528B4N1MB6BW45B6AER6qvrn6yn6uy48by6ae36VVt6n36uy46m"
ALGORYTHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

class token_model(BaseModel):
	access_token: str
	token_type: str

class CreateUserRequest(BaseModel):
	username: str = Field(min_length=3)
	email: str = Field(min_length=3)
	password: str = Field(min_length=3)
	is_active: bool = Field(default=True)
	role: str = Field(default="user")

templates = Jinja2Templates(directory="App/templates")

oath2_bearer= OAuth2PasswordBearer(tokenUrl="auth/token")

db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user(username: str, password: str, db):
  user = db.query(Users).filter(Users.username == username).first()
  if not user:
    return False
  if not pbkdf2_sha256.verify(password, user.hashed_password):
    return False
  return user

def create_access_token(username: str, user_id: int, role : str ,expires_delta: timedelta):
	encode = {"sub": username, "id": user_id , "role": role}
	expires = datetime.now(timezone.utc) + expires_delta
	encode.update({"exp": expires})
	return jwt.encode(encode, SECRET_KEY, algorithm=ALGORYTHM)

def get_current_user(token: Annotated[str, Depends(oath2_bearer)]):
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORYTHM])
    username: str = payload.get("sub")
    user_id: int = payload.get("id")
    user_role: str = payload.get("role")
    if username is None or user_id is None or user_role is None:  
      raise HTTPException(status_code=401, detail="Could not validate user.")
    return {"username": username, "id": user_id, "role": user_role}
  except jwt.JWTError:
    raise HTTPException(status_code=401, detail="Could not validate user.") 

def get_current_user_from_cookie(request: Request, access_token: str = Cookie(None)):
  token = None
  if access_token:
    if access_token.startswith('Bearer '):
      token = access_token[len('Bearer '):]
    else:
      token = access_token
  if not token:
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
      token = auth_header[len('Bearer '):]
  if not token:
    raise HTTPException(status_code=401, detail="Not authenticated")
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORYTHM])
    username: str = payload.get("sub")
    user_id: int = payload.get("id")
    user_role: str = payload.get("role")
    if username is None or user_id is None or user_role is None:
      raise HTTPException(status_code=401, detail="Could not validate user.")
    return {"username": username, "id": user_id, "role": user_role}
  except jwt.JWTError:
    raise HTTPException(status_code=401, detail="Could not validate user.")

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
  success = request.query_params.get("success")
  message = "Account created successfully!" if success == "1" else None
  return templates.TemplateResponse("login.html", {"request": request, "success_message": message})

@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
  return templates.TemplateResponse("register.html", {"request": request})

@router.post("/login")
def login_post(
  request: Request,
  db: db_dependency,
  username: str = Form(...),
  password: str = Form(...),

):
  user = authenticate_user(username, password, db)
  if not user:
    return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})
  access_token = create_access_token(user.username, user.id, user.role, timedelta(minutes=30))
  response = RedirectResponse(url="/dashboard", status_code=302)
  response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
  return response

@router.post("/register")
def register_post(
  request: Request,
  db: db_dependency,
  username: str = Form(...),
  email: str = Form(...),
  password: str = Form(...),
):
  existing_user = db.query(Users).filter(Users.username == username).first()
  if existing_user:
    return templates.TemplateResponse("register.html", {"request": request, "error": "Username already exists"})
  
  new_user = Users(
    username=username,
    email=email,
    hashed_password=pbkdf2_sha256.hash(password)
  )
  
  db.add(new_user)
  db.commit()
  
  response = RedirectResponse(url="/auth/login?success=1", status_code=302)
  return response

@router.post("/create_user" , status_code=201)
def create_user(db: db_dependency , createUserRequest: CreateUserRequest):
  new_user = Users(
    username=createUserRequest.username,
    email=createUserRequest.email,
    hashed_password=pbkdf2_sha256.hash(createUserRequest.password),
    is_active=createUserRequest.is_active,
    role=createUserRequest.role
  )
  db.add(new_user)
  db.commit()
  return {"message": "User created successfully", "username": new_user.username}

@router.post("/token" , response_model=token_model)
def login_for_access_token(formdata : Annotated[OAuth2PasswordRequestForm , Depends()], db: db_dependency):
  user = authenticate_user(formdata.username , formdata.password , db)
  if user is None:
    raise HTTPException(status_code=401, detail="Could not validate user.")
  token = create_access_token(user.username , user.id , user.role, timedelta(minutes=30))
  return {"access_token": token, "token_type": "bearer"}
