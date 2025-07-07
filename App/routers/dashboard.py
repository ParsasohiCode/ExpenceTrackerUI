from fastapi import APIRouter, Request, Depends, Cookie, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter(
  prefix="/dashboard",
  tags=["dashboard"],
)

templates = Jinja2Templates(directory="App/templates")

@router.get("/", response_class=HTMLResponse)
def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})