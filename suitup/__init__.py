"""SuitUp — a self-contained, locally-runnable teaching app for American
Mah Jongg (National Mah Jongg League style play).

This package roots the entire first-release application: the Flask web
shell (``suitup.web``), and in later release slices, the rules engine,
curriculum content, and AI opponents described in docs/architecture.md.

Nothing in this package makes network calls at runtime. SuitUp is designed
to run fully offline inside a single Docker container on port 8092.
"""

from __future__ import annotations

__version__ = "0.1.0"

__all__ = ["__version__"]