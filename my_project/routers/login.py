from urllib import request

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from product import schemas, models
from database import get_db
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from product.schemas import TokenData

router = APIRouter()
SECRET_KEY = "5d28de4e9df2bf25dfbdadcb78639ddcf6d4fa26b4104c59365672c929271eaa"
ALFORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALFORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
        token_data = TokenData(username=username)
    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    return token_data

@router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    seller = db.query(models.Seller).filter(models.Seller.username == request.username).first()
    if not seller:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    if not pwd_context.verify(request.password, seller.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": seller.username})
    return {"access_token": access_token, "token_type": "bearer"}

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALFORITHM)
    return encoded_jwt