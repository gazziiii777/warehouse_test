from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, database, schemas

router = APIRouter()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[schemas.Order])
def get_orders(db: Session = Depends(get_db)):
    orders = db.query(models.Order).all()
    return orders


@router.post("/", response_model=schemas.OrderItem)
def create_order_item(order_item: schemas.OrderItemCreate, db: Session = Depends(get_db)):
    # Проверка существования продукта и его количества на складе
    db_product = db.query(models.Product).filter(models.Product.id == order_item.product_id).first()

    if not db_product:
        raise HTTPException(status_code=404, detail="Product не найден")

    if db_product.stock < order_item.quantity:
        raise HTTPException(status_code=400,
                            detail=f"Недостаточно товара с ID {order_item.product_id}. Доступно: {db_product.stock}, запрошено: {order_item.quantity}")

    # Если продукт существует и его достаточно, создаем заказ
    db_order = models.Order(status="в процессе")
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # Создаем элемент заказа
    db_order_item = models.OrderItem(
        order_id=db_order.id,
        product_id=order_item.product_id,
        quantity=order_item.quantity
    )
    db.add(db_order_item)

    # Уменьшение количества товара на складе
    db_product.stock -= order_item.quantity
    db.commit()

    # Обновление элемента заказа и возврат
    db.refresh(db_order_item)
    return db_order_item


@router.get("/item/{order_item_id}", response_model=schemas.OrderWithItems)
def get_order_by_order_item_id(order_item_id: int, db: Session = Depends(get_db)):
    # Поиск элемента заказа (OrderItem) по его id
    db_order_item = db.query(models.OrderItem).filter(models.OrderItem.id == order_item_id).first()

    # Если элемент заказа не найден, возвращаем ошибку 404
    if db_order_item is None:
        raise HTTPException(status_code=404, detail="OrderItem не найден")

    # Извлекаем order_id из найденного OrderItem
    order_id = db_order_item.order_id

    # Поиск заказа (Order) по order_id
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()

    # Если заказ не найден, возвращаем ошибку 404
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order не найден")

    # Возвращаем информацию о заказе и его элементах
    return db_order


@router.patch("/orders/{id}/status", response_model=schemas.Order)
def update_order_status(id: int, status: str, db: Session = Depends(get_db)):
    # Получение заказа по id
    db_order = db.query(models.Order).filter(models.Order.id == id).first()

    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    # Обновление статуса заказа
    db_order.status = status
    db.commit()
    db.refresh(db_order)

    return db_order
