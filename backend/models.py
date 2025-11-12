from __future__ import annotations

from sqlalchemy import Column, Float, Integer, String, UniqueConstraint

from .database import Base


class Student(Base):
    __tablename__ = "students"
    __table_args__ = (UniqueConstraint("nim", name="uq_students_nim"),)

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    nim = Column(String(20), nullable=False, index=True)
    program_studi = Column(String(100), nullable=True)
    angkatan = Column(Integer, nullable=True)
    ipk = Column(Float, nullable=True)
    email = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)

