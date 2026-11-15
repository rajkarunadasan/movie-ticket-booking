"""Application factory for the Movie Ticket Booking Application."""
import os

from flask import Flask, render_template

from . import db


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-only-change-me"),
        DATABASE=os.path.join(app.root_path, "..", "tickets.db"),
    )
    if test_config:
        app.config.update(test_config)
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    # BLUEPRINTS

    @app.errorhandler(404)
    def not_found(_e):
        return render_template("error.html", code=404, message="Page not found."), 404

    @app.errorhandler(500)
    def server_error(_e):
        return render_template("error.html", code=500, message="Something went wrong."), 500

    return app
