from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .db import engine, Base
from .routers import admin, auth, expenses, user, dashboard

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="App/static"), name="static")

@app.get("/")
async def read_root():
  return {"message": "Hello, World!"}

app.include_router(auth.router)
app.include_router(admin.admin_router)
app.include_router(expenses.expenses_router)
app.include_router(user.user_router)
app.include_router(dashboard.router)