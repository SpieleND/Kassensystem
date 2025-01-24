from sqlalchemy import Column, String, Float
from .db_context import Base
from .metadata import Metadata

class Product(Base, Metadata):
    __tablename__ = "products"

    name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)