from __future__ import annotations

import ast
import logging
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional

import pandas as pd
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from . import models, schemas

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).resolve().parent / "data"

COLUMN_ALIASES: Dict[str, List[str]] = {
    "name": ["name", "nama", "nama_lengkap", "student_name", "full_name"],
    "nim": ["nim", "student_id", "id", "nrp"],
    "program_studi": ["program_studi", "programstudi", "prodi", "program", "study_program"],
    "angkatan": ["angkatan", "tahun_masuk", "tahun", "batch"],
    "ipk": ["ipk", "gpa", "ipk_akhir"],
    "email": ["email", "e-mail"],
    "phone": ["phone", "telepon", "nohp", "no_hp", "hp", "handphone", "telp"],
}


def _standardise_column_name(name: str) -> str:
    return (
        name.strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
        .replace(".", "_")
    )


def _rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    if isinstance(df.columns, pd.RangeIndex) or all(str(col).isdigit() for col in df.columns):
        default_map = {
            0: "nim",
            1: "name",
            2: "angkatan",
            3: "program_studi",
            4: "email",
            5: "phone",
            6: "ipk",
        }
        df = df.rename(
            columns={
                col: default_map.get(int(col), col)
                for col in df.columns
                if str(col).isdigit()
            }
        )
    name_map = {}
    for col in df.columns:
        formatted = _standardise_column_name(str(col))
        matched = None
        for target, aliases in COLUMN_ALIASES.items():
            if formatted == target or formatted in aliases:
                matched = target
                break
        name_map[col] = matched if matched else formatted
    df = df.rename(columns=name_map)
    return df


def _parse_tuple_rows(df: pd.DataFrame) -> pd.DataFrame:
    if df.shape[1] != 1:
        return df
    column = df.columns[0]
    parsed_rows = []
    for raw in df[column].dropna():
        text = str(raw).strip().rstrip(",")
        try:
            value = ast.literal_eval(text)
        except (SyntaxError, ValueError):
            continue
        if isinstance(value, (list, tuple)) and len(value) >= 2:
            parsed_rows.append(list(value))
    if not parsed_rows:
        return df
    max_len = max(len(row) for row in parsed_rows)
    normalized = [row + [None] * (max_len - len(row)) for row in parsed_rows]
    return pd.DataFrame(normalized)


def _coerce_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = _parse_tuple_rows(df)
    normalized_columns = {_standardise_column_name(str(col)) for col in df.columns}
    if "nim" not in normalized_columns or "name" not in normalized_columns:
        header_row_idx = None
        for idx, row in df.iterrows():
            row_values = [_standardise_column_name(str(val)) for val in row.tolist()]
            if "nim" in row_values and any(x in row_values for x in ("name", "nama", "nama_mahasiswa")):
                header_row_idx = idx
                break
        if header_row_idx is not None:
            new_columns = []
            for val in df.iloc[header_row_idx].tolist():
                label = _standardise_column_name(str(val)) if pd.notna(val) else ""
                new_columns.append(label)
            df = df.iloc[header_row_idx + 1 :].reset_index(drop=True)
            df.columns = new_columns
    df = _rename_columns(df)
    for column in ("name", "nim", "program_studi", "email", "phone"):
        if column in df.columns:
            df[column] = (
                df[column]
                .astype(str)
                .str.strip()
                .str.strip("'\"")
                .replace({"nan": None, "": None, "none": None})
            )
    if "nim" in df.columns:
        df = df[df["nim"].notna()]
        df = df[~df["nim"].astype(str).str.lower().str.contains("^nim$", na=False)]
    if "angkatan" in df.columns:
        df["angkatan"] = pd.to_numeric(df["angkatan"], errors="coerce").astype("Int64")
    if "ipk" in df.columns:
        df["ipk"] = pd.to_numeric(df["ipk"], errors="coerce")
    return df


def _load_file(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        try:
            df = pd.read_csv(path)
        except pd.errors.ParserError:
            df = pd.read_csv(path, header=None, engine="python")
        normalized_columns = {_standardise_column_name(str(col)) for col in df.columns}
        if df.empty or not {"nim", "name"} & normalized_columns:
            df = pd.read_csv(path, header=None)
    elif suffix in {".xls", ".xlsx"}:
        df = pd.read_excel(path)
    elif suffix == ".ods":
        df = pd.read_excel(path, engine="odf")
    elif suffix == ".json":
        df = pd.read_json(path)
    else:
        raise ValueError(f"Unsupported file type: {path.suffix}")
    return df


def _iter_student_records() -> Iterable[schemas.StudentCreate]:
    if not DATA_DIR.exists():
        logger.warning("Data directory %s does not exist.", DATA_DIR)
        return []

    aggregated: Dict[str, Dict] = {}
    for file_path in sorted(DATA_DIR.glob("*")):
        if file_path.suffix.lower() not in {".csv", ".json", ".xls", ".xlsx", ".ods"}:
            continue
        try:
            df = _load_file(file_path)
        except Exception as exc:  # pylint: disable=broad-except
            logger.error("Failed loading %s: %s", file_path.name, exc)
            continue
        df = _coerce_dataframe(df)
        if "nim" not in df.columns or "name" not in df.columns:
            logger.warning(
                "Skipping %s because required columns are missing.", file_path.name
            )
            continue
        for _, row in df.iterrows():
            nim = str(row.get("nim") or "").strip()
            name = row.get("name")
            if not nim or not name:
                continue
            record = aggregated.get(nim, defaultdict(lambda: None))
            record.update(
                {
                    "nim": nim,
                    "name": name,
                    "program_studi": row.get("program_studi") or record.get("program_studi"),
                    "angkatan": row.get("angkatan") if pd.notna(row.get("angkatan")) else record.get("angkatan"),
                    "ipk": row.get("ipk") if pd.notna(row.get("ipk")) else record.get("ipk"),
                    "email": row.get("email") or record.get("email"),
                    "phone": row.get("phone") or record.get("phone"),
                }
            )
            aggregated[nim] = record
    for value in aggregated.values():
        angkatan = value.get("angkatan")
        ipk = value.get("ipk")
        yield schemas.StudentCreate(
            **{
                "nim": value.get("nim"),
                "name": value.get("name"),
                "program_studi": value.get("program_studi"),
                "angkatan": int(angkatan) if isinstance(angkatan, (int, float)) and not pd.isna(angkatan) else None,
                "ipk": float(ipk) if isinstance(ipk, (int, float)) and not pd.isna(ipk) else None,
                "email": value.get("email"),
                "phone": value.get("phone"),
            }
        )


def upsert_students(db: Session, students: Iterable[schemas.StudentCreate]) -> Dict[str, int]:
    created = 0
    updated = 0
    students = list(students)
    if not students:
        return {"created": created, "updated": updated}

    nim_list = [student.nim for student in students]
    existing_students = {
        student.nim: student
        for student in db.execute(
            select(models.Student).where(models.Student.nim.in_(nim_list))
        ).scalars()
    }
    for student in students:
        current = existing_students.get(student.nim)
        if current:
            current.name = student.name
            current.program_studi = student.program_studi
            current.angkatan = student.angkatan
            current.ipk = student.ipk
            current.email = student.email
            current.phone = student.phone
            updated += 1
        else:
            new_student = models.Student(
                name=student.name,
                nim=student.nim,
                program_studi=student.program_studi,
                angkatan=student.angkatan,
                ipk=student.ipk,
                email=student.email,
                phone=student.phone,
            )
            db.add(new_student)
            created += 1
    try:
        db.commit()
    except SQLAlchemyError as exc:
        db.rollback()
        logger.exception("Failed to upsert students: %s", exc)
        raise
    return {"created": created, "updated": updated}


def sync_from_files(db: Session) -> Dict[str, int]:
    students = list(_iter_student_records())
    stats = upsert_students(db, students)
    stats["total_processed"] = len(students)
    return stats


def get_students(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
) -> List[models.Student]:
    query = select(models.Student).offset(skip).limit(limit)
    if search:
        like_pattern = f"%{search.lower()}%"
        query = (
            select(models.Student)
            .where(models.Student.name.ilike(like_pattern))
            .offset(skip)
            .limit(limit)
        )
    return list(db.execute(query).scalars())


def get_student(db: Session, student_id: int) -> Optional[models.Student]:
    return db.get(models.Student, student_id)


def search_students(db: Session, name: str, limit: int = 50) -> List[models.Student]:
    query = (
        select(models.Student)
        .where(models.Student.name.ilike(f"%{name.lower()}%"))
        .limit(limit)
    )
    return list(db.execute(query).scalars())

