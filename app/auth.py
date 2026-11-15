"""User registration, login and logout (Sprint 1)."""
import functools
import sqlite3

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db
from .validators import validate_email, validate_name, validate_password

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    g.user = None
    if user_id is not None:
        g.user = get_db().execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()


def login_required(view):
    @functools.wraps(view)
    def wrapped(**kwargs):
        if g.user is None:
            flash("Please log in to continue.", "error")
            return redirect(url_for("auth.login", next=request.path))
        return view(**kwargs)
    return wrapped


@bp.route("/register", methods=["GET", "POST"])
def register():
    form = {"name": "", "email": ""}
    if request.method == "POST":
        form = {k: request.form.get(k, "") for k in form}
        name, e1 = validate_name(form["name"])
        email, e2 = validate_email(form["email"])
        password, e3 = validate_password(request.form.get("password"))
        errors = [e for e in (e1, e2, e3) if e]
        if errors:
            for message in errors:
                flash(message, "error")
            return render_template("register.html", form=form), 400
        try:
            db = get_db()
            db.execute("INSERT INTO users (name, email, password_hash) VALUES (?,?,?)",
                       (name, email, generate_password_hash(password)))
            db.commit()
        except sqlite3.IntegrityError:
            flash("An account with this email already exists.", "error")
            return render_template("register.html", form=form), 409
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html", form=form)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email, _ = validate_email(request.form.get("email"))
        password = request.form.get("password") or ""
        user = None
        if email:
            user = get_db().execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if user is None or not check_password_hash(user["password_hash"], password):
            flash("Invalid email or password.", "error")
            return render_template("login.html"), 401
        session.clear()
        session["user_id"] = user["id"]
        flash(f"Welcome back, {user['name']}!", "success")
        target = request.args.get("next", "")
        return redirect(target if target.startswith("/") and not target.startswith("//") else "/")
    return render_template("login.html")


@bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect("/")
