# app/models/role.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.association import permission_role

class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True)
    role_name = Column(String)
    description = Column(String)

    permissions = relationship(
        "Permission",
        secondary=permission_role,
        back_populates="roles"
    )

    users = relationship("User", back_populates="role") 