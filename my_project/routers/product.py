from fastapi import APIRouter,status, Response, HTTPException
from fastapi.params import Depends
from product import schemas, models
from sqlalchemy.orm import Session
from database import get_db
from routers.login import get_current_user
from typing import List
router = APIRouter(
    prefix="/product",
    tags=["Products"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def add(request: schemas.Product, db:Session = Depends(get_db)):
    new_product = models.Product(name=request.name, description=request.description, price=request.price, seller_id=request.seller_id)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.get("/", response_model=List[schemas.DisplayProduct])
def get_products( db:Session = Depends(get_db), current_user: schemas.Seller = Depends(get_current_user)):
    return db.query(models.Product).all()

@router.put("/{id}",tags=["Products"])
def update_product(id: int, request: schemas.Product, db:Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id)
    if not product.first():
        pass
    product.update(request.dict())
    db.commit()
    db.refresh(product)
    return {'Product Successfully Updated'}

@router.get("/{id}", response_model=schemas.DisplayProduct)
def get_product(id: int, response: Response, db:Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {id} not found")
    return product

@router.delete("/{id}")
def delete_product(id: int, db:Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if product:
        db.delete(product)
        db.commit()
    return product