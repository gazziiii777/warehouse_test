# app/products.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, database, schemas

router = APIRouter()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.get("/", response_model=list[schemas.Product])
def get_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products


@router.get("/{id}", response_model=schemas.Product)
def get_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@router.put("/{id}", response_model=schemas.Product)
def update_product(id: int, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in product.dict().items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product


@router.delete("/{id}", response_model=dict)
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(db_product)
    db.commit()
    return {"detail": "Product deleted"}
