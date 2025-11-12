from __future__ import annotations

from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import Base, engine, get_db

app = FastAPI(title="Student Dashboard API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/health", tags=["system"])
def health_check() -> dict:
    return {"status": "ok"}


@app.get(
    "/students",
    response_model=List[schemas.Student],
    tags=["students"],
)
def read_students(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    search: Optional[str] = Query(default=None, min_length=1),
    db: Session = Depends(get_db),
) -> List[schemas.Student]:
    return crud.get_students(db, skip=skip, limit=limit, search=search)


@app.get(
    "/students/{student_id}",
    response_model=schemas.Student,
    tags=["students"],
)
def read_student(student_id: int, db: Session = Depends(get_db)) -> schemas.Student:
    student = crud.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return student


@app.get(
    "/students/search",
    response_model=List[schemas.Student],
    tags=["students"],
)
def search_students(
    name: str = Query(..., min_length=1),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
) -> List[schemas.Student]:
    return crud.search_students(db, name=name, limit=limit)


@app.post(
    "/sync",
    tags=["students"],
)
def sync_students(db: Session = Depends(get_db)) -> dict:
    stats = crud.sync_from_files(db)
    return {"message": "Sync completed", "stats": stats}

