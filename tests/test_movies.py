def test_home_lists_movies(client):
    r = client.get("/")
    assert r.status_code == 200
    assert b"Avengers: Doomsday" in r.data and b"Obsession" in r.data


def test_movie_detail_shows_showtimes(client):
    r = client.get("/movies/1")
    assert r.status_code == 200
    assert b"Showtimes" in r.data and b"Screen" in r.data


def test_unknown_movie_404(client):
    assert client.get("/movies/999").status_code == 404


def test_search_by_title(client):
    r = client.get("/?q=avengers")
    assert b"Avengers: Doomsday" in r.data and b"Obsession" not in r.data


def test_filter_by_genre_and_language(client):
    r = client.get("/?genre=Drama&language=English")
    assert b"I Play Rocky" in r.data and b"Avengers: Doomsday" not in r.data


def test_search_without_results(client):
    assert b"No movies match" in client.get("/?q=zzzz").data


def test_sql_injection_attempt_is_harmless(client):
    assert client.get("/?q=' OR 1=1 --").status_code == 200
