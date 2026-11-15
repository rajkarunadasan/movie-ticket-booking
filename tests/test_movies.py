def test_home_lists_movies(client):
    r = client.get("/")
    assert r.status_code == 200
    assert b"Midnight Harbor" in r.data and b"Galaxy Rangers" in r.data


def test_movie_detail_shows_showtimes(client):
    r = client.get("/movies/1")
    assert r.status_code == 200
    assert b"Showtimes" in r.data and b"Screen" in r.data


def test_unknown_movie_404(client):
    assert client.get("/movies/999").status_code == 404
