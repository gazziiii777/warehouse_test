from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import models, database, schemas

router = APIRouter()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    db_order = models.Order(status=order.status)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


@router.get("/", response_model=list[schemas.Order])
def get_orders(db: Session = Depends(get_db)):
    orders = db.query(models.Order).all()
    return orders


@router.post("/items/", response_model=schemas.OrderItem)
def create_order_item(order_item: schemas.OrderItemCreate, db: Session = Depends(get_db)):
    db_order = models.Order(status="в процессе")
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    db_order_item = models.OrderItem(
        order_id=db_order.id,
        product_id=order_item.product_id,
        quantity=order_item.quantity
    )
    db.add(db_order_item)
    db.commit()
    db.refresh(db_order_item)
    return db_order_item
