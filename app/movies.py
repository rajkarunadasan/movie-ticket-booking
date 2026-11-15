"""Browse movies and showtimes (Sprint 1)."""
from flask import Blueprint, abort, render_template

from .db import get_db

bp = Blueprint("movies", __name__)


@bp.route("/")
def index():
    movies = get_db().execute("SELECT * FROM movies ORDER BY title").fetchall()
    return render_template("index.html", movies=movies)


@bp.route("/movies/<int:movie_id>")
def detail(movie_id):
    db = get_db()
    movie = db.execute("SELECT * FROM movies WHERE id = ?", (movie_id,)).fetchone()
    if movie is None:
        abort(404)
    shows = db.execute("SELECT * FROM shows WHERE movie_id = ? ORDER BY show_time",
                       (movie_id,)).fetchall()
    return render_template("movie.html", movie=movie, shows=shows)
