from pydantic import BaseModel, ConfigDict
from typing import  Optional
class Product(BaseModel):
    name: str
    description: str
    price: float

class ShowProduct(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    price: float

class DisplayProduct(BaseModel):
    name: str
    description: str
    class Config:
        orm_mode = True

class Seller(BaseModel):
    username: str
    email: str
    password: str

class DisplaySeller(BaseModel):
    username: str
    email: str
    model_config = ConfigDict(from_attributes=True)

class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None