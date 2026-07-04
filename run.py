"""Local development entrypoint for SuitUp.

Run with:

    python run.py

This is a thin convenience wrapper around ``suitup.web.app.main()`` for
contributors who prefer ``python run.py`` over
``python3 -m suitup.web.app``. The Docker image always uses the module
entrypoint (see Dockerfile); this file exists purely for local iteration
outside a container.
"""

from __future__ import annotations

from suitup.web.app import main

if __name__ == "__main__":
    main()