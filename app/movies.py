"""Browse movies and showtimes (Sprint 1)."""
from flask import Blueprint, abort, render_template, request

from .db import get_db

bp = Blueprint("movies", __name__)


@bp.route("/")
def index():
    db = get_db()
    q = request.args.get("q", "").strip()[:60]
    genre = request.args.get("genre", "").strip()
    language = request.args.get("language", "").strip()
    sql, params = "SELECT * FROM movies WHERE title LIKE ?", [f"%{q}%"]
    if genre:
        sql += " AND genre = ?"
        params.append(genre)
    if language:
        sql += " AND language = ?"
        params.append(language)
    movies = db.execute(sql + " ORDER BY title", params).fetchall()
    genres = [r[0] for r in db.execute("SELECT DISTINCT genre FROM movies ORDER BY genre")]
    languages = [r[0] for r in db.execute("SELECT DISTINCT language FROM movies ORDER BY language")]
    return render_template("index.html", movies=movies, q=q, genre=genre, language=language,
                           genres=genres, languages=languages)


@bp.route("/movies/<int:movie_id>")
def detail(movie_id):
    db = get_db()
    movie = db.execute("SELECT * FROM movies WHERE id = ?", (movie_id,)).fetchone()
    if movie is None:
        abort(404)
    shows = db.execute("SELECT * FROM shows WHERE movie_id = ? ORDER BY show_time",
                       (movie_id,)).fetchall()
    return render_template("movie.html", movie=movie, shows=shows)
