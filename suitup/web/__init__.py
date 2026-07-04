"""Web layer for SuitUp.

This subpackage isolates all Flask concerns per the birdwatcher-style
layout fixed in docs/architecture.md:

- ``suitup.web.app`` holds the application factory and route registration
- ``suitup/web/templates/`` (added in a later slice) holds Jinja templates
- ``suitup/web/static/`` (added in a later slice) holds static assets and
  original SVG tile art

Domain logic (rules engine, curriculum, AI) must never import from this
subpackage. Routes defined here call domain services, never the reverse.
"""

from __future__ import annotations

from suitup.web.app import create_app

__all__ = ["create_app"]