from typing import List

from pydantic import BaseModel


class Product(BaseModel):
    id: int
    title: str
    description: str
    price: float
    stock: int

    class Config:
        from_attributes = True


class ProductCreate(BaseModel):
    title: str
    description: str
    price: float
    stock: int


class OrderCreate(BaseModel):
    status: str


class Order(OrderCreate):
    id: int
    created_at: str

    class Config:
        from_attributes = True


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int


class OrderItem(OrderItemCreate):
    id: int

    class Config:
        from_attributes = True


class OrderWithItems(Order):
    order_items: List[OrderItem] = []

    class Config:
        from_attributes = True
