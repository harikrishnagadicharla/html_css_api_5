# main.py
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates") 

# In-memory storage
internal_db = []

# Internal model with full data
class InternalProduct(BaseModel):
    id: int
    name: str
    price: float
    supplier: str
    internal_code: str
    stock: int
    warranty_years: int

# Public model (filtered output)
class PublicProduct(BaseModel):
    id: int
    name: str
    price: float

#homepage route
@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    public_view = [PublicProduct(**{k: v for k, v in item.dict().items() if k in PublicProduct.__annotations__}) for item in internal_db]
    return templates.TemplateResponse("index.html", {"request": request, "products": public_view})

# Route to add a new product
@app.post("/add", response_class=RedirectResponse)
async def add_product(
    id: int = Form(...),
    name: str = Form(...),
    price: float = Form(...),
    supplier: str = Form(...),
    internal_code: str = Form(...),
    stock: int = Form(...),
    warranty_years: int = Form(...)
):
    new_product = InternalProduct(
        id=id,
        name=name,
        price=price,
        supplier=supplier,
        internal_code=internal_code,
        stock=stock,
        warranty_years=warranty_years
    )
    internal_db.append(new_product)
    return RedirectResponse(url="/", status_code=303)
