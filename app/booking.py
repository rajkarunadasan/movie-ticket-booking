"""Seat selection and checkout (Sprints 2-3)."""
from flask import (Blueprint, abort, flash, redirect, render_template,
                   request, url_for)

from .auth import login_required
from .db import get_db
from .validators import validate_seats

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


@bp.route("/shows/<int:show_id>/checkout")
@login_required
def checkout(show_id):
    show = get_show(show_id)
    chosen, error = validate_seats(request.args.get("seats", "").split(","))
    if error or set(chosen) & taken_seats(show_id):
        flash(error or "Some selected seats are no longer available.", "error")
        return redirect(url_for("booking.seats", show_id=show_id))
    return render_template("checkout.html", show=show, chosen=chosen, total=len(chosen) * show["price"])
