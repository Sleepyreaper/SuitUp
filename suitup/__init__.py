"""SuitUp package root.

This package contains the SuitUp application: a self-contained, offline,
locally-runnable teaching tool for American Mah Jongg (NMJL-style play).

Sub-packages (added in later release slices, not this one):
    suitup.web    - Thin Flask web layer (routes, templates, static assets).
    suitup.rules  - Rules engine (tiles, hands, Charleston, scoring).
    suitup.ai     - AI opponents at three difficulty levels.
    suitup.data   - Bundled curriculum content and card data.

This file intentionally contains no game logic. It only marks the
top-level package and exposes a version string for diagnostics.
"""

__version__ = "0.1.0"