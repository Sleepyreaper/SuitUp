# SuitUp Architecture Blueprint

## Purpose

SuitUp is a self-contained, locally-runnable Docker application that teaches a total beginner how to play American Mah Jongg using National Mah Jongg League-style play. The application must run fully offline on the user's machine, expose a web app at http://localhost:8092, and include a rules engine, original SVG tile art, a guided curriculum UI, and AI opponents with three difficulty levels.

This document fixes the architecture so later engineers can build independently without changing structure or runtime assumptions.

## Non-Negotiable Product Contract

1. Local-only runtime:
 - The app runs on the user's machine only.
 - The app is served at http://localhost:8092.
 - The app is launched via Docker.
 - Flask is the web server framework inside the container.

2. Offline-only operation:
 - No network calls at runtime.
 - No CDN assets.
 - No API dependencies.
 - No telemetry exporters that require outbound connectivity.
 - All curriculum content, SVG art, rules data, and AI logic ship inside the image.

3. Brownfield preservation:
 - Preserve any existing LICENSE file exactly as-is if present.
 - Do not rename, overwrite, replace, or regenerate an existing LICENSE.
 - New work must be added around the existing LICENSE.

4. Release shape:
 - Single self-contained app repository.
 - Web UI, rules engine, AI, assets, docs, and tests live in one codebase.
 - No microservices.
 - No external databases required for first release.
 - No background workers required for first release.

## Architecture Style

SuitUp follows a birdwatcher-style Flask container pattern and a guitarhero-style teaching flow.

### Birdwatcher-style Flask container pattern

This means:

- One container.
- One Flask app process.
- Static assets and templates are bundled with the app.
- Core game logic lives in importable Python modules, not inside route handlers.
- The web layer is thin and delegates to domain modules.
- Local state for a session can live in signed Flask session storage or in-memory process state for first release, as long as the app remains self-contained and offline.

### Guitarhero-style teaching flow

This means:

- The product teaches by progressive mastery.
- The UI is structured as short guided lessons, drills, and playable practice.
- Users move from setup and tile recognition to turn flow, Charleston, calling, and complete-hand play.
- The curriculum and playable game share the same rules engine to avoid drift.
- Practice modes may simplify choices at first, but they must still sit on the same core domain model.

## Top-Level Repository Layout

The repository layout is fixed as follows:.
 ├── LICENSE
 ├── Dockerfile
 ├── docker-compose.yml
 ├── requirements.txt
 ├── suitup/
 │ ├── __init__.py
 │ ├── app.py
 │ ├── config.py
 │ ├── tiles.py
 │ ├── wall.py
 │ ├── charleston.py
 │ ├── groups.py
 │ ├── patterns.py
 │ ├── game.py
 │ ├── ai.py
 │ ├── curriculum.py
 │ ├── serializers.py
 │ ├── assets/
 │ │ ├── tile_art/
 │ │ ├── lessons/
 │ │ └── cards/
 │ └── web/
 │ ├── __init__.py
 │ ├── routes.py
 │ ├── templates/
 │ └── static/
 ├── docs/
 │ ├── architecture.md
 │ └──...
 └── tests/
 ├── test_tiles.py
 ├── test_wall.py
 ├── test_charleston.py
 ├── test_groups.py
 ├── test_patterns.py
 ├── test_game.py
 ├── test_ai.py
 └── test_web.py

Only additive growth is allowed beneath this shape. Engineers may add new files inside the established folders, but must not move the listed responsibilities to different top-level locations.

## Runtime Contract

### Hosting

- Flask application listens on 0.0.0.0 inside the container.
- Container publishes port 8092 to host port 8092.
- The expected user entrypoint is:
 - docker compose up --build
 or
 - docker build / docker run equivalents.

### URL Contract

- Root experience is served from:
 - http://localhost:8092/
- All lesson, drill, and game interactions are served from that same local app.
- No feature in first release requires account creation, login, or internet access.

### Data Contract

- First release stores all canonical game data in code and bundled files.
- Tile definitions, wall construction, Charleston logic, grouping logic, patterns, and AI decision rules must be deterministic and testable.
- No remote rules download.
- No remote card download.
- No dependence on online NMJL services.

### Process Contract

- One Flask process per container is acceptable for first release.
- If a WSGI server is added later, it must still preserve the single-container local app contract.
- Runtime must succeed with outbound network disabled.

## Brownfield Preservation Rules

1. If LICENSE exists:
 - Keep it unchanged.
 - Preserve filename and content exactly.

2. If other brownfield files exist:
 - Prefer additive changes over structural rewrites.
 - Preserve working local run commands unless they conflict with the fixed contract in this document.

3. This architecture document is authoritative for package boundaries:
 - New engineers must implement within these boundaries.
 - Do not collapse domain logic into Flask routes.
 - Do not split the app into separate services for first release.

## Package and Module Boundaries

The package boundary is strict:

- suitup/ contains application and domain code.
- suitup/web/ contains only presentation and request/response wiring.
- docs/ contains human-readable project documentation.
- tests/ contains automated tests.
- Docker files live at repo root.

The following modules define the first-release contract.