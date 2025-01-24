from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .db_context import Base
from .metadata import Metadata


class User(Base, Metadata):
    __tablename__ = "users"

    username = Column(String(50), unique=True, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"))
    rfid_key = Column(String(255), unique=True)

    role = relationship("Role", back_populates="users")
