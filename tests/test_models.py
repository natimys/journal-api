from ittop_journal.models import AuthToken, ScheduleLesson, VisitRecord, parse_many


def test_models_allow_forward_compatible_fields() -> None:
    token = AuthToken.model_validate({"access_token": "x", "new_field": True})
    assert token.access_token == "x"
    assert token.model_extra == {"new_field": True}


def test_schedule_list_envelope_is_preserved_as_models() -> None:
    lessons = parse_many(
        ScheduleLesson,
        {
            "items": [
                {
                    "date": "2026-10-26",
                    "lesson": 4,
                    "started_at": "14:35",
                    "finished_at": "16:05",
                    "teacher_name": "T",
                    "subject_name": "Math",
                    "room_name": "Room 1",
                    "backend_flag": 1,
                }
            ]
        },
    )
    assert lessons[0].subject_name == "Math"
    assert lessons[0].model_extra == {"backend_flag": 1}


def test_student_visits_numeric_object_is_parsed_as_records() -> None:
    visits = parse_many(
        VisitRecord,
        {
            "0": {
                "date_visit": "2026-10-23",
                "lesson_number": 5,
                "status_was": 1,
                "spec_id": 51,
                "subject_source": 1,
                "subject_id": 51,
                "teacher_name": "T",
                "spec_name": "Math",
                "lesson_theme": "Reports",
                "control_work_mark": None,
                "home_work_mark": None,
                "lab_work_mark": None,
                "class_work_mark": None,
                "practical_work_mark": None,
                "final_work_mark": None,
                "final_work_mark_type": None,
            }
        },
    )
    assert len(visits) == 1
    assert visits[0].date_visit.isoformat() == "2026-10-23"
    assert visits[0].lesson_theme == "Reports"
