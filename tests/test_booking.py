from tests.helpers import signup_and_login


def pay(client, seats="A1,A2", payment="UPI", show=1):
    return client.post(f"/shows/{show}/checkout", data={"seats": seats, "payment": payment})


def test_successful_booking_creates_ticket(client):
    signup_and_login(client)
    r = pay(client)
    assert r.status_code == 302 and "/tickets/CB" in r.headers["Location"]
    page = client.get(r.headers["Location"])
    assert b"Booking Confirmed" in page.data and b"A1, A2" in page.data


def test_booked_seats_become_unavailable(client):
    signup_and_login(client)
    pay(client)
    assert b'value="A1" disabled' in client.get("/shows/1/seats").data
    assert client.post("/shows/1/seats", data={"seats": ["A1"]}).status_code == 400


def test_double_booking_is_prevented(client):
    signup_and_login(client)
    pay(client, seats="C3")
    r = pay(client, seats="C3")
    assert r.status_code == 302 and "/seats" in r.headers["Location"]
    # each booking appears as one table row (header row + 1 booking)
    assert client.get("/my-bookings").data.count(b"<tr>") == 2


def test_invalid_payment_method_rejected(client):
    signup_and_login(client)
    assert pay(client, payment="Cash").status_code == 400


def test_my_bookings_lists_booking(client):
    signup_and_login(client)
    pay(client, seats="D4")
    assert b"D4" in client.get("/my-bookings").data


def test_ticket_belongs_to_owner_only(client, app):
    signup_and_login(client)
    ref = pay(client).headers["Location"].rsplit("/", 1)[1]
    other = app.test_client()
    signup_and_login(other, email="ravi@example.com")
    assert other.get(f"/tickets/{ref}").status_code == 404
