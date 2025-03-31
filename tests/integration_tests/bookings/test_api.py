import pytest

@pytest.mark.parametrize("room_id, date_from, date_to, status_code", [
    (1, "2024-08-01", "2024-10-01", 200),
    (1, "2024-08-01", "2024-10-01", 200),
    (1, "2024-08-01", "2024-10-01", 200),
    (1, "2024-08-01", "2024-10-01", 200),
    (1, "2024-08-01", "2024-10-01", 200),
    (1, "2024-08-11", "2024-08-15", 200),
])
async def test_add_booking(
        db,
        auth_user,
        room_id,
        date_from,
        date_to,
        status_code,
):
    response = await auth_user.post(
        "/bookings/create",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )
    res = response.json()
    assert response.status_code == status_code
    if status_code == 200:
        assert res["status"] == "OK"
        assert isinstance(res, dict)


