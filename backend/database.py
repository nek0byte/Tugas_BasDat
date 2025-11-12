from __future__ import annotations

import os
from functools import lru_cache
from typing import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


@lru_cache(maxsize=1)
def _load_env() -> None:
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(env_path, override=False)
    load_dotenv(override=False)


def get_database_url() -> str:
    _load_env()
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASS", "")
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "3306")
    name = os.getenv("DB_NAME", "student_db")
    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{name}"


DATABASE_URL = get_database_url()

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    future=True,
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)

Base = declarative_base()


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

