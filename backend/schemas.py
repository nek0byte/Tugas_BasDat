from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class StudentBase(BaseModel):
    name: str = Field(..., max_length=100)
    nim: str = Field(..., max_length=20)
    program_studi: Optional[str] = Field(default=None, max_length=100)
    angkatan: Optional[int] = None
    ipk: Optional[float] = Field(default=None, ge=0, le=4)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(default=None, max_length=20)


class StudentCreate(StudentBase):
    pass


class StudentUpdate(StudentBase):
    pass


class Student(StudentBase):
    id: int

    class Config:
        from_attributes = True

