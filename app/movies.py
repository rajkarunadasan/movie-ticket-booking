"""Browse movies and showtimes (Sprint 1)."""
from flask import (Blueprint, abort, flash, g, redirect, render_template,
                   request, url_for)

from .auth import login_required
from .db import get_db
from .validators import validate_review

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
    reviews = db.execute(
        "SELECT reviews.*, users.name FROM reviews JOIN users ON users.id = reviews.user_id "
        "WHERE movie_id = ? ORDER BY reviews.id DESC", (movie_id,)).fetchall()
    average = round(sum(r["stars"] for r in reviews) / len(reviews), 1) if reviews else None
    return render_template("movie.html", movie=movie, shows=shows, reviews=reviews, average=average)


@bp.route("/movies/<int:movie_id>/review", methods=["POST"])
@login_required
def add_review(movie_id):
    db = get_db()
    if db.execute("SELECT 1 FROM movies WHERE id = ?", (movie_id,)).fetchone() is None:
        abort(404)
    stars, comment, error = validate_review(request.form.get("stars"), request.form.get("comment"))
    if error:
        flash(error, "error")
    else:
        # one review per user per movie: a new submission replaces the old one
        db.execute(
            "INSERT INTO reviews (user_id, movie_id, stars, comment) VALUES (?,?,?,?) "
            "ON CONFLICT(user_id, movie_id) DO UPDATE SET stars = excluded.stars, comment = excluded.comment",
            (g.user["id"], movie_id, stars, comment))
        db.commit()
        flash("Thanks for your review!", "success")
    return redirect(url_for("movies.detail", movie_id=movie_id))
