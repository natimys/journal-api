import httpx
import pytest
import respx

from ittop_journal import JournalClient


@pytest.mark.asyncio
@respx.mock
async def test_login_sets_in_memory_token() -> None:
    respx.post("https://msapi.top-academy.ru/api/v2/auth/login").mock(
        return_value=httpx.Response(200, json={"access_token": "abc", "token_type": "bearer"})
    )
    async with JournalClient() as client:
        token = await client.auth.login("user", "password", "application-key")
        assert token.access_token == "abc"
        assert client.token == "abc"


@pytest.mark.asyncio
@respx.mock
async def test_schedule_date_parameter() -> None:
    route = respx.get(
        "https://msapi.top-academy.ru/api/v2/schedule/operations/get-by-date",
        params={"date_filter": "2026-09-24"},
    ).mock(
        return_value=httpx.Response(
            200,
            json=[
                {
                    "date": "2026-09-24",
                    "lesson": 4,
                    "started_at": "14:35",
                    "finished_at": "16:05",
                    "teacher_name": "T",
                    "subject_name": "Math",
                    "room_name": "Room 1",
                }
            ],
        )
    )
    async with JournalClient(token="t") as client:
        lessons = await client.schedule.get_by_date("2026-09-24")
    assert route.called
    assert lessons[0].subject_name == "Math"


@pytest.mark.asyncio
@respx.mock
async def test_schedule_date_range_parameters() -> None:
    route = respx.get(
        "https://msapi.top-academy.ru/api/v2/schedule/operations/get-by-date-range",
        params={"date_start": "2026-10-26", "date_end": "2026-11-01"},
    ).mock(
        return_value=httpx.Response(
            200,
            json=[
                {
                    "date": "2026-10-26",
                    "lesson": 4,
                    "started_at": "14:35",
                    "finished_at": "16:05",
                    "teacher_name": "T",
                    "subject_name": "Math",
                    "room_name": "Room 1",
                }
            ],
        )
    )
    async with JournalClient(token="t") as client:
        lessons = await client.schedule.get_by_date_range("2026-10-26", "2026-11-01")
    assert route.called
    assert lessons[0].subject_name == "Math"
