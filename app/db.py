"""SQLite helpers: schema creation and demo data seeding."""
import sqlite3
from datetime import datetime, timedelta

from flask import current_app, g

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT NOT NULL,
    email         TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS movies (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    title       TEXT NOT NULL,
    genre       TEXT NOT NULL,
    language    TEXT NOT NULL,
    duration    INTEGER NOT NULL,
    description TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS shows (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    movie_id INTEGER NOT NULL REFERENCES movies(id),
    hall     TEXT NOT NULL,
    show_time TEXT NOT NULL,
    price    INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS bookings (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    reference  TEXT NOT NULL UNIQUE,
    user_id    INTEGER NOT NULL REFERENCES users(id),
    show_id    INTEGER NOT NULL REFERENCES shows(id),
    total      INTEGER NOT NULL,
    payment    TEXT NOT NULL,
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS booking_seats (
    booking_id INTEGER NOT NULL REFERENCES bookings(id),
    show_id    INTEGER NOT NULL REFERENCES shows(id),
    seat       TEXT NOT NULL,
    UNIQUE (show_id, seat)
);
CREATE TABLE IF NOT EXISTS reviews (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id  INTEGER NOT NULL REFERENCES users(id),
    movie_id INTEGER NOT NULL REFERENCES movies(id),
    stars    INTEGER NOT NULL CHECK (stars BETWEEN 1 AND 5),
    comment  TEXT NOT NULL,
    UNIQUE (user_id, movie_id)
);
"""

MOVIES = [
    ("Midnight Harbor", "Thriller", "English", 124,
     "A night-shift detective uncovers a smuggling ring hidden inside a sleepy port town."),
    ("Monsoon Melodies", "Romance", "Tamil", 138,
     "Two street musicians in Madurai find love while competing for a festival stage."),
    ("Galaxy Rangers", "Sci-Fi", "English", 142,
     "A ragtag crew races across the galaxy to deliver a message that could stop a war."),
    ("Laugh Out Loud", "Comedy", "Hindi", 116,
     "A wedding planner's perfect week falls apart when the groom's family arrives early."),
    ("The Last Lighthouse", "Drama", "Tamil", 129,
     "An aging keeper and a young engineer clash over the future of a historic lighthouse."),
]
HALLS = ["Screen 1", "Screen 2", "Screen 3"]


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(_error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def seed_demo_data(db):
    """Insert demo movies and shows the first time the database is created."""
    if db.execute("SELECT COUNT(*) FROM movies").fetchone()[0]:
        return
    base = datetime.now().replace(minute=0, second=0, microsecond=0)
    for i, (title, genre, language, duration, desc) in enumerate(MOVIES):
        cur = db.execute(
            "INSERT INTO movies (title, genre, language, duration, description) VALUES (?,?,?,?,?)",
            (title, genre, language, duration, desc))
        for j, hour in enumerate((11, 15, 19)):
            when = (base + timedelta(days=1 + j % 2)).replace(hour=hour)
            db.execute(
                "INSERT INTO shows (movie_id, hall, show_time, price) VALUES (?,?,?,?)",
                (cur.lastrowid, HALLS[(i + j) % 3], when.strftime("%Y-%m-%d %H:%M"), 150 + 50 * (j % 3)))
    db.commit()


def init_app(app):
    app.teardown_appcontext(close_db)
    with app.app_context():
        db = get_db()
        db.executescript(SCHEMA)
        seed_demo_data(db)
