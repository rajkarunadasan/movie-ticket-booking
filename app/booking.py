"""Seat selection and checkout (Sprints 2-3)."""
import secrets
import sqlite3
from datetime import datetime

from flask import (Blueprint, abort, flash, g, redirect, render_template,
                   request, url_for)

from .auth import login_required
from .db import get_db
from .validators import validate_payment, validate_seats

bp = Blueprint("booking", __name__)

ROWS = "ABCDE"
SEATS_PER_ROW = 8


def get_show(show_id):
    show = get_db().execute(
        "SELECT shows.*, movies.title FROM shows JOIN movies ON movies.id = shows.movie_id "
        "WHERE shows.id = ?", (show_id,)).fetchone()
    if show is None:
        abort(404)
    return show


def taken_seats(show_id):
    rows = get_db().execute("SELECT seat FROM booking_seats WHERE show_id = ?", (show_id,))
    return {r["seat"] for r in rows}


@bp.route("/shows/<int:show_id>/seats", methods=["GET", "POST"])
@login_required
def seats(show_id):
    show = get_show(show_id)
    taken = taken_seats(show_id)
    if request.method == "POST":
        chosen, error = validate_seats(request.form.getlist("seats"))
        if error:
            flash(error, "error")
        elif set(chosen) & taken:
            flash("Some selected seats were just taken. Please choose again.", "error")
        else:
            return redirect(url_for("booking.checkout", show_id=show_id, seats=",".join(chosen)))
        return render_template("seats.html", show=show, taken=taken, rows=ROWS,
                               per_row=SEATS_PER_ROW), 400
    return render_template("seats.html", show=show, taken=taken, rows=ROWS, per_row=SEATS_PER_ROW)


@bp.route("/shows/<int:show_id>/checkout", methods=["GET", "POST"])
@login_required
def checkout(show_id):
    show = get_show(show_id)
    raw = request.values.get("seats", "")
    chosen, error = validate_seats(raw.split(","))
    if error or set(chosen) & taken_seats(show_id):
        flash(error or "Some selected seats are no longer available.", "error")
        return redirect(url_for("booking.seats", show_id=show_id))
    total = len(chosen) * show["price"]
    if request.method == "POST":
        method, error = validate_payment(request.form.get("payment"))
        if error:
            flash(error, "error")
            return render_template("checkout.html", show=show, chosen=chosen, total=total), 400
        # Payment is simulated for this mini-project: any valid method succeeds.
        db = get_db()
        reference = "CB" + secrets.token_hex(4).upper()
        try:
            cur = db.execute(
                "INSERT INTO bookings (reference, user_id, show_id, total, payment, created_at) "
                "VALUES (?,?,?,?,?,?)",
                (reference, g.user["id"], show_id, total, method,
                 datetime.now().strftime("%Y-%m-%d %H:%M")))
            db.executemany("INSERT INTO booking_seats (booking_id, show_id, seat) VALUES (?,?,?)",
                           [(cur.lastrowid, show_id, seat) for seat in chosen])
            db.commit()
        except sqlite3.IntegrityError:
            db.rollback()
            flash("Sorry, one of those seats was just booked by someone else.", "error")
            return redirect(url_for("booking.seats", show_id=show_id))
        flash("Payment successful. Booking confirmed!", "success")
        return redirect(url_for("booking.ticket", reference=reference))
    return render_template("checkout.html", show=show, chosen=chosen, total=total)


def _booking_or_404(reference):
    booking = get_db().execute(
        "SELECT bookings.*, shows.hall, shows.show_time, movies.title FROM bookings "
        "JOIN shows ON shows.id = bookings.show_id JOIN movies ON movies.id = shows.movie_id "
        "WHERE reference = ? AND user_id = ?", (reference, g.user["id"])).fetchone()
    if booking is None:
        abort(404)
    return booking


@bp.route("/tickets/<reference>")
@login_required
def ticket(reference):
    booking = _booking_or_404(reference)
    seat_rows = get_db().execute("SELECT seat FROM booking_seats WHERE booking_id = ? ORDER BY seat",
                                 (booking["id"],))
    return render_template("ticket.html", booking=booking, seats=[r["seat"] for r in seat_rows])


@bp.route("/my-bookings")
@login_required
def my_bookings():
    rows = get_db().execute(
        "SELECT bookings.*, shows.show_time, movies.title, "
        "(SELECT GROUP_CONCAT(seat, ', ') FROM booking_seats WHERE booking_id = bookings.id) AS seats "
        "FROM bookings JOIN shows ON shows.id = bookings.show_id JOIN movies ON movies.id = shows.movie_id "
        "WHERE user_id = ? ORDER BY bookings.id DESC", (g.user["id"],)).fetchall()
    return render_template("my_bookings.html", bookings=rows)
