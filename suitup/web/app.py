"""Flask application factory and entrypoint for the SuitUp local web app.

This module wires together the birdwatcher-style Flask package layout
described in docs/architecture.md. Right now it exposes:

- ``create_app()`` — the Flask app factory used by tests, run.py, and any
  future WSGI runner
- ``GET /api/v1/health`` — a lightweight liveness endpoint compatible with
  the error/response conventions in docs/API.md
- ``GET /`` — a placeholder root route until the guided curriculum UI lands
  in a later release slice
- a JSON 404 handler for unknown ``/api/v1/*`` routes, matching the
  ErrorResponse shape defined in docs/API.md

Domain logic (rules engine, curriculum, AI opponents) is intentionally
absent from this module. Later slices will register additional blueprints
here that import from suitup.rules, suitup.curriculum, and suitup.ai —
never the other way around. No network calls are made anywhere in this
module, in keeping with the offline-only runtime contract.
"""

from __future__ import annotations

import os

from flask import Blueprint, Flask, Response, jsonify, request

__all__ = ["create_app", "main"]

APP_VERSION = "0.1.0"
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8092

api_v1 = Blueprint("api_v1", __name__, url_prefix="/api/v1")


@api_v1.get("/health")
def health() -> Response:
    """Return a small liveness/readiness payload.

    This endpoint has no dependency on domain services and is safe to call
    before any game state exists. It backs the Docker HEALTHCHECK and any
    frontend boot check that confirms the server is up before rendering
    the curriculum UI.
    """
    payload = {
        "status": "ok",
        "service": "suitup",
        "version": APP_VERSION,
    }
    return jsonify(payload)


def _handle_404(_error):
    """Render 404s.

    Requests under ``/api/`` get the ErrorResponse JSON shape from
    docs/API.md. Everything else (future static/template routes) gets a
    plain-text 404 so browsers navigating around the placeholder UI don't
    get a raw JSON blob.
    """
    if request.path.startswith("/api/"):
        body = {
            "error": {
                "code": "not_found",
                "message": "The requested resource does not exist.",
                "details": {
                    "field": request.path,
                },
            }
        }
        return jsonify(body), 404
    return Response("Not Found", status=404, mimetype="text/plain")


def _placeholder_root() -> Response:
    """Serve a minimal placeholder page for the app root.

    Later slices replace this with the guided curriculum UI rendered from
    suitup/web/templates/. This placeholder exists only so the container
    is verifiably alive when you point a browser at
    http://localhost:8092 and run `docker compose up`.
    """
    html = (
        "<!doctype html>"
        "<html lang=\"en\">"
        "<head><meta charset=\"utf-8\"><title>SuitUp</title></head>"
        "<body>"
        "<h1>SuitUp</h1>"
        "<p>The American Mah Jongg teaching app is booting up. "
        "The guided curriculum UI lands in a later release slice.</p>"
        "<p>API health check: <code>/api/v1/health</code></p>"
        "</body>"
        "</html>"
    )
    return Response(html, mimetype="text/html")


def create_app() -> Flask:
    """Application factory for the SuitUp Flask app.

    Returns a fully configured Flask app with the ``/api/v1`` blueprint
    registered, a JSON-aware 404 handler, and a placeholder root route.
    No external network calls are made anywhere in this factory or its
    routes, in keeping with the offline-only runtime contract in
    docs/architecture.md.
    """
    app = Flask(
        __name__,
        static_folder="static",
        template_folder="templates",
    )
    app.config["JSON_SORT_KEYS"] = False

    app.register_blueprint(api_v1)
    app.register_error_handler(404, _handle_404)
    app.add_url_rule("/", view_func=_placeholder_root, methods=["GET"])

    return app


def main() -> None:
    """Run the Flask development server bound to 0.0.0.0:8092.

    Host/port/debug are overridable via ``SUITUP_HOST``, ``SUITUP_PORT``,
    and ``SUITUP_DEBUG`` environment variables for local flexibility, but
    the Docker image always targets 8092 per the non-negotiable runtime
    contract in docs/architecture.md.
    """
    host = os.environ.get("SUITUP_HOST", DEFAULT_HOST)
    port = int(os.environ.get("SUITUP_PORT", str(DEFAULT_PORT)))
    debug = os.environ.get("SUITUP_DEBUG", "0") == "1"

    app = create_app()
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    main()