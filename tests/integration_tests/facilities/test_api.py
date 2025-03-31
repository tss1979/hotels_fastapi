async def test_add_facility(ac):
    response = await ac.post(
        "/facilities/create",
        json={
            "title": "wi-fi",
        }
    )
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

async def test_get_facilities(ac):
    response = await ac.get(
        "/facilities",
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
