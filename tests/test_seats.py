from tests.helpers import signup_and_login


def test_seat_page_requires_login(client):
    r = client.get("/shows/1/seats")
    assert r.status_code == 302 and "/auth/login" in r.headers["Location"]


def test_seat_map_renders(client):
    signup_and_login(client)
    r = client.get("/shows/1/seats")
    assert r.status_code == 200 and b'value="A1"' in r.data and b'value="E8"' in r.data


def test_select_seats_redirects_to_checkout(client):
    signup_and_login(client)
    r = client.post("/shows/1/seats", data={"seats": ["A1", "A2"]})
    assert r.status_code == 302 and "seats=A1%2CA2" in r.headers["Location"].replace(",", "%2C")


def test_no_seat_selected_is_rejected(client):
    signup_and_login(client)
    assert client.post("/shows/1/seats", data={}).status_code == 400


def test_more_than_six_seats_rejected(client):
    signup_and_login(client)
    r = client.post("/shows/1/seats", data={"seats": [f"B{i}" for i in range(1, 8)]})
    assert r.status_code == 400


def test_invalid_seat_code_rejected(client):
    signup_and_login(client)
    assert client.post("/shows/1/seats", data={"seats": ["Z99"]}).status_code == 400


def test_checkout_total(client):
    signup_and_login(client)
    r = client.get("/shows/1/checkout?seats=A1,A2")
    assert b"Booking Summary" in r.data and b"A1, A2" in r.data


def test_unknown_show_404(client):
    signup_and_login(client)
    assert client.get("/shows/999/seats").status_code == 404
