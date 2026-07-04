# SuitUp Architecture — First Release Contract

This document fixes the brownfield architecture, package layout, and release slice map for the first release of SuitUp.

SuitUp is a self-contained, locally-runnable Docker web app that teaches a total beginner how to play American Mah Jongg using National Mah Jongg League style play concepts, served locally at http://localhost:8092.

## Release goals

First release must ship as one offline-capable local web application with:

- a Python package named `suitup/`
- a Flask-based web app using a birdwatcher-style package layout
- a guided beginner curriculum flow in the web UI using a guitarhero-style progression
- a rules engine capable of modeling core American Mah Jongg play concepts
- original local SVG tile art and static assets
- AI opponents with three difficulty levels
- local Docker execution on port `8092`
- no network dependency at runtime

## Non-negotiable runtime contract

- The app must run locally at `http://localhost:8092`.
- The app must be fully usable offline after the container image is built.
- Runtime must not require external APIs, hosted model calls, CDNs, or internet access.
- Static assets, curriculum content, tile art, and rules behavior must be packaged with the app.
- The app must be startable through `docker compose up` and through local Python execution via `run.py`.
- The first release is a single deployable unit; no separate frontend server, worker, database service, or cache service is allowed.

## License preservation rule

If a `LICENSE` file already exists in the repository, it must be retained untouched.

That means:

- do not delete it
- do not rewrite it
- do not replace it with a different license
- do not add contradictory licensing text elsewhere

If no `LICENSE` exists, later tasks may add one only if explicitly requested. This task does not create or modify licensing files.

## Architectural style

SuitUp uses a birdwatcher-style Flask package layout:

- application package rooted at `suitup/`
- web concerns isolated in `suitup/web/`
- templates in `suitup/web/templates/`
- static assets in `suitup/web/static/`
- app factory pattern for Flask app creation
- domain logic independent from Flask request handling
- routes call domain services; domain services never import route modules

SuitUp uses a guitarhero-style curriculum flow:

- learning progresses in a fixed, beginner-friendly sequence
- each lesson unlocks the next concept
- the user can replay drills without penalty
- UI emphasizes guided repetition, visual examples, and progressive practice
- gameplay practice mode reuses the same rules engine as guided lessons

## Top-level project tree

The first release is fixed to this top-level structure:.
 ├── Dockerfile
 ├── docker-compose.yml
 ├── requirements.txt
 ├── run.py
 ├── docs/
 │ └── architecture.md
 ├── suitup/
 │ ├── __init__.py
 │ ├── tiles.py
 │ ├── wall.py
 │ ├── charleston.py
 │ ├── groups.py
 │ ├── patterns.py
 │ ├── game.py
 │ ├── ai.py
 │ ├── assets.py
 │ ├── curriculum.py
 │ └── web/
 │ ├── __init__.py
 │ ├── app.py
 │ ├── routes.py
 │ ├── api.py
 │ ├── templates/
 │ │ ├── base.html
 │ │ ├── index.html
 │ │ ├── lesson.html
 │ │ ├── practice.html
 │ │ └── play.html
 │ └── static/
 │ ├── css/
 │ │ └── app.css
 │ ├── js/
 │ │ └── app.js
 │ └── img/
 │ └── tiles/
 └── tests/
 ├── test_tiles.py
 ├── test_wall.py
 ├── test_charleston.py
 ├── test_groups.py
 ├── test_patterns.py
 ├── test_game.py
 ├── test_ai.py
 └── test_web.py

Later tasks may add files inside these directories, but must not violate these boundaries.

## Package boundaries