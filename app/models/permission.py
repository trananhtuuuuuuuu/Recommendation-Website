# app/models/permission.py
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.enums import MethodEnum
from app.models.association import permission_role

class Permission(Base):
    __tablename__ = "permission"

    id = Column(Integer, primary_key=True)
    endpoint = Column(String)
    description = Column(String)
    method = Column(Enum(MethodEnum))

    roles = relationship(
        "Role",
        secondary=permission_role,
        back_populates="permissions"
    )