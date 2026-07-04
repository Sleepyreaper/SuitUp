"""SuitUp web layer package.

Holds the thin Flask application (suitup.web.app) plus, in later
release slices, routes/, templates/, and static/ for the guided
curriculum UI. Per architecture.md, this layer stays thin and
delegates all real game logic to suitup.rules and suitup.ai once
those packages exist.
"""