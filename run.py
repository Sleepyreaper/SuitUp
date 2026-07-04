"""Convenience local entrypoint for running SuitUp outside Docker.

Docker's CMD uses `python3 -m suitup.web.app` directly (see Dockerfile),
but this run.py is kept at the repo root as a friendly, single-command
way to run SuitUp during local development without Docker, e.g.:

    python3 run.py

It simply imports the Flask app factory from the suitup package and
runs it on the same host/port the container uses, so behavior stays
identical between local runs and containerized runs.
"""

from suitup.web.app import app, APP_HOST, APP_PORT


def main():
    """Run the SuitUp Flask app for local, non-Docker development."""
    app.run(host=APP_HOST, port=APP_PORT)


if __name__ == "__main__":
    main()