# app/models/association.py
from sqlalchemy import Table, Column, ForeignKey, Integer
from app.db.base import Base

permission_role = Table(
    "permission_role",
    Base.metadata,
    Column("role_id", ForeignKey("role.id"), primary_key=True),
    Column("permission_id", ForeignKey("permission.id"), primary_key=True),
)