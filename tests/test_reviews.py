from tests.helpers import signup_and_login


def test_review_requires_login(client):
    r = client.post("/movies/1/review", data={"stars": "5", "comment": "Great"})
    assert r.status_code == 302 and "/auth/login" in r.headers["Location"]


def test_add_review_and_average(client):
    signup_and_login(client)
    client.post("/movies/1/review", data={"stars": "4", "comment": "Gripping story"})
    page = client.get("/movies/1").data
    assert b"Gripping story" in page and b"4.0 / 5" in page


def test_review_is_updated_not_duplicated(client):
    signup_and_login(client)
    client.post("/movies/1/review", data={"stars": "2", "comment": "Slow"})
    client.post("/movies/1/review", data={"stars": "5", "comment": "Better on second watch"})
    page = client.get("/movies/1").data
    assert b"Better on second watch" in page and b"Slow" not in page


def test_invalid_review_rejected(client):
    signup_and_login(client)
    client.post("/movies/1/review", data={"stars": "9", "comment": "x"})
    assert b"No reviews yet" in client.get("/movies/1").data


def test_review_unknown_movie_404(client):
    signup_and_login(client)
    assert client.post("/movies/999/review", data={"stars": "5", "comment": "x"}).status_code == 404
