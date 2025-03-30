from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .db_context import Base
from .metadata import Metadata


class Order(Base, Metadata):
    __tablename__ = "orders"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)

    user = relationship("User", back_populates="orders")
    product = relationship("Product", back_populates="orders")
