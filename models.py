from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    stock = Column(Integer)

    # Связь с OrderItem
    order_items = relationship("OrderItem", back_populates="product")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    now = datetime.now().replace(second=0, microsecond=0)
    formatted_datetime = now.strftime('%Y-%m-%d %H:%M')
    created_at = Column(String, default=formatted_datetime)
    status = Column(String, index=True)

    order_items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)

    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")
