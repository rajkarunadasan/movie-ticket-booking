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


def test_search_by_title(client):
    r = client.get("/?q=galaxy")
    assert b"Galaxy Rangers" in r.data and b"Midnight Harbor" not in r.data


def test_filter_by_genre_and_language(client):
    r = client.get("/?genre=Drama&language=Tamil")
    assert b"The Last Lighthouse" in r.data and b"Galaxy Rangers" not in r.data


def test_search_without_results(client):
    assert b"No movies match" in client.get("/?q=zzzz").data


def test_sql_injection_attempt_is_harmless(client):
    assert client.get("/?q=' OR 1=1 --").status_code == 200
