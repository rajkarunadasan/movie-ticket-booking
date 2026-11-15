def register(client, **over):
    data = {"name": "Asha Devi", "email": "asha@example.com", "password": "secret123"}
    data.update(over)
    return client.post("/auth/register", data=data)


def login(client, email="asha@example.com", password="secret123"):
    return client.post("/auth/login", data={"email": email, "password": password})


def test_register_success(client):
    assert register(client).status_code == 302


def test_register_validation_errors(client):
    assert register(client, email="bad").status_code == 400
    assert register(client, password="short").status_code == 400
    assert register(client, name="1").status_code == 400


def test_duplicate_email_rejected(client):
    register(client)
    assert register(client).status_code == 409


def test_login_and_logout(client):
    register(client)
    assert login(client).status_code == 302
    assert b"Asha Devi" in client.get("/auth/register").data
    client.get("/auth/logout")
    assert b"Log in" in client.get("/auth/register").data


def test_login_wrong_password(client):
    register(client)
    assert login(client, password="wrongpass1").status_code == 401


def test_login_unknown_user(client):
    assert login(client, email="nobody@example.com").status_code == 401


def test_open_redirect_is_blocked(client):
    register(client)
    r = client.post("/auth/login?next=//evil.com", data={"email": "asha@example.com", "password": "secret123"})
    assert r.headers["Location"] == "/"
