"""SuitUp Flask application entrypoint.

This module is the runtime entrypoint invoked by:

    python3 -m suitup.web.app

It creates a minimal Flask app and, when run as the main module,
serves it on 0.0.0.0:8092 so it is reachable at http://localhost:8092
from the host machine via Docker's port mapping.

This is a scaffold-only module for this release slice. It exposes a
single health-check-style route so the container can be verified as
"up" before the rules engine, AI, and curriculum UI are layered in on
top by later tasks. No game logic lives here, per architecture.md.
"""

from flask import Flask, jsonify

APP_NAME = "SuitUp"
APP_PORT = 8092
APP_HOST = "0.0.0.0"


def create_app():
    """Build and configure the Flask application instance.

    Kept as a factory function (rather than a bare module-level
    Flask object) so later tasks can import create_app() for testing
    or for wiring in blueprints without changing this module's shape.
    """
    app = Flask(__name__)

    @app.route("/")
    def index():
        """Placeholder landing route.

        The real guided curriculum UI is added in a later release
        slice. For this scaffold, it just confirms the app is
        running so the container can be smoke-tested.
        """
        return jsonify(
            {
                "app": APP_NAME,
                "status": "scaffold-running",
                "message": "SuitUp is up. Curriculum UI arrives in a later release slice.",
            }
        )

    @app.route("/healthz")
    def healthz():
        """Simple health-check endpoint for local verification."""
        return jsonify({"status": "ok"})

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host=APP_HOST, port=APP_PORT)