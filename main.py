from fastapi import FastAPI, Form
from pydantic import BaseModel, Field, HttpUrl
from typing import Set,List
from uuid import UUID
from datetime import date, datetime, time, timedelta


class Profile(BaseModel):
    age: int
    email: str
    name: str = None

class Event(BaseModel):
    event_id: UUID
    start_date: date
    start_time: datetime
    end_time: datetime
    repeat_time: time
    execute_after: timedelta


class Image(BaseModel):
    url: HttpUrl
    name: str = None

class Product(BaseModel):
    name: str
    price: int = Field( title="Price of the product", description="The price of the product in USD", gt=0)
    discount: int 
    discounted_price: float
    tags: Set[str] = []
    images: List[Image] = []

    class Config:
        schema_extra = {
            "example": {
                "name": "Phone",
                "price": 100,
                "discount": 10,
                "discounted_price": 90.0,
                "tags": ["Electronics", "Smartphone"],
                "images": [
                    {"url": "http://example.com/image1.jpg", "name": "Image 1"},
                    {"url": "http://example.com/image2.jpg", "name": "Image 2"}
                ]
            }
        }

class Offer(BaseModel):
    name: str
    description: str
    price: float
    products: List[Product] = []

class User(BaseModel):
    name: str
    email: str

app = FastAPI()

@app.post("/purchase")
def purchase(user: User, product: Product):
    product.discounted_price = product.price - (product.price * product.discount / 100)
    return {"user": user, "product": product}

@app.post("/addproduct/{product_id}")
def addproduct(product: Product, product_id: int, category: str):
    product.discounted_price = product.price - (product.price * product.discount / 100)
    return {"product": product, "product_id": product_id, "category": category}

@app.get("/")
def index():
    return "Hello, World"

@app.get("/user/admin")
def admin():
    return {f'This is an admin endpoint for user: admin'}

@app.get("/user/{username}")
def user(username: str):
    return {f'This is a user endpoint for user: {username}'}

@app.get("/products")
def products(id:int=None,price:int= None):
    return {f'product with an id: {id} and price: {price}'}

@app.get("/property/{id}")
def property(id: int):
    return {f'This is a property endpoint for property {id}'}

@app.get("/profile/{username}")
def profile(username: str):
    return {f'This is a profile page for user: {username}'}

@app.get("/profile/{userid}/comments")
def profile(userid: int, commentid: int):
    return {f'This is a profile page for user: {userid} and comment: {commentid}'}

@app.post("/users")
def adduser(profile: Profile):
    return {'user data': profile.dict()}

@app.get("/movies")
def movies():
    return {"movie list":['Movie1','Movie2']}

@app.post("/addoffer")
def addoffers(offer: Offer):
    return {'offer data': offer.dict()}

@app.post("/addevent")
def addevent(event: Event):
    return {'event data': event.dict()}

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username}   