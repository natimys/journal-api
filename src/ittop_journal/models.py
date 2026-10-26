"""Pydantic response models for known API families.

Fields confirmed from supplied API payloads are explicit; other models remain provisional until
their raw responses are available.
"""

from __future__ import annotations

from datetime import date as Date
from datetime import datetime as DateTime
from datetime import time as Time
from typing import Any

from pydantic import BaseModel, ConfigDict


class JournalModel(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)


class AuthToken(JournalModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int | None = None


class UserInfo(JournalModel):
    id: int | str | None = None
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    group: str | None = None
    email: str | None = None


class ScheduleLesson(JournalModel):
    date: Date
    lesson: int
    started_at: Time
    finished_at: Time
    teacher_name: str
    subject_name: str
    room_name: str


class VisitRecord(JournalModel):
    date_visit: Date
    lesson_number: int
    status_was: int
    spec_id: int
    subject_source: int
    subject_id: int
    teacher_name: str
    spec_name: str
    lesson_theme: str
    # The captured record had these fields set to null; their non-null types need another sample.
    control_work_mark: Any
    home_work_mark: Any
    lab_work_mark: Any
    class_work_mark: Any
    practical_work_mark: Any
    final_work_mark: Any
    final_work_mark_type: Any


class MetricPoint(JournalModel):
    date: Date | DateTime | None = None
    value: float | int | None = None
    label: str | None = None


class RatingEntry(JournalModel):
    position: int | None = None
    student_id: int | str | None = None
    name: str | None = None
    score: int | float | None = None


class Feedback(JournalModel):
    id: int | str | None = None
    date: Date | DateTime | None = None
    teacher: str | None = None
    subject: str | None = None
    text: str | None = None


class EvaluationLesson(JournalModel):
    id: int | str | None = None
    date: Date | DateTime | None = None
    subject: str | None = None
    teacher: str | None = None
    evaluated: bool | None = None


def _unwrap(payload: Any) -> Any:
    if isinstance(payload, dict):
        for key in ("data", "items", "results"):
            value = payload.get(key)
            if isinstance(value, (list, dict)):
                return value
    return payload


def parse_one(model: type[JournalModel], payload: Any) -> JournalModel:
    value = _unwrap(payload)
    if isinstance(value, list):
        value = value[0] if value else {}
    return model.model_validate(value if isinstance(value, dict) else {"value": value})


def parse_many(model: type[JournalModel], payload: Any) -> list[JournalModel]:
    value = _unwrap(payload)
    if isinstance(value, dict):
        if value and all(key.isdecimal() for key in value) and all(
            isinstance(item, dict) for item in value.values()
        ):
            value = list(value.values())
        else:
            value = [value]
    if not isinstance(value, list):
        return []
    return [
        model.model_validate(item if isinstance(item, dict) else {"value": item}) for item in value
    ]
