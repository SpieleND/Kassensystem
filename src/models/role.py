from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from .db_context import Base
from .metadata import Metadata


class Role(Base, Metadata):
    __tablename__ = "roles"

    name = Column(String(50), unique=True, nullable=False)

    users = relationship("User", back_populates="role")
