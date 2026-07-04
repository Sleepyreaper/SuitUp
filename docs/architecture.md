# SuitUp Architecture Brief — Release 1

## Purpose

SuitUp is a self-contained, locally-runnable Docker web application that teaches a total beginner how to play American Mah Jongg using National Mah Jongg League style play concepts while shipping only original educational content. Release 1 must run entirely offline and be served at:

 http://localhost:8092

This first release combines four product surfaces in one local app:

1. A beginner curriculum that teaches setup, tile groups, wall building, dealer selection, the Charleston, draws, discards, calls, exposure, and the flow of a hand.
2. A rules engine that models the tile set, turn sequence, Charleston phases, legal actions, exposure rules, and win validation for original practice hands.
3. A three-level AI opponent system that can play legal turns against the learner.
4. An original art pipeline that renders a complete set of original SVG tile faces and UI illustrations without copying commercial art.

The design is modeled after a birdwatcher-style Flask container pattern for a small, self-contained, server-rendered application with clear package boundaries, and a guided-teaching flow modeled after a guitarhero-style lesson progression where each concept builds on the last, then unlocks structured practice.

## Release 1 boundaries

Release 1 includes:

- Local-only Docker runtime.
- Flask application as the web entrypoint.
- Server-rendered teaching UI with lightweight client-side enhancement only.
- Original tile art in SVG.
- Original beginner lessons and practice drills.
- Rules engine for American Mah Jongg style play using the specified physical tile set and game flow.
- Original practice pattern system used for teaching and AI play.
- Three AI difficulty levels:
 - Beginner: legal but simple play
 - Intermediate: discard and keep heuristics
 - Advanced: stronger pattern fit and defensive discard logic
- Offline persistence limited to local lightweight storage if needed for progress, settings, and saved practice state.

Release 1 explicitly does not include:

- Real National Mah Jongg League card text.
- Any scanned, transcribed, paraphrased, or reconstructed NMJL yearly card content.
- Online multiplayer.
- Cloud services.
- User accounts.
- Analytics, telemetry, or external APIs.
- Mobile app packaging.
- Tournament scoring systems beyond the teaching scope needed for practice play.

## Copyright and content constraints

SuitUp must avoid shipping copyrighted NMJL card material.

Required constraints:

- Do not include real NMJL card text.
- Do not include yearly NMJL hand names, exact card groupings, exact card wording, or near-copy derivatives.
- Do not include photographed or traced tile art from any manufacturer.
- Do not imply the app is an official NMJL product.

Allowed content for Release 1:

- Original practice patterns created specifically for teaching.
- Original explanatory text that teaches general American Mah Jongg mechanics.
- Original SVG tile art created from scratch.
- Original drills, quizzes, and lesson scenarios.
- Rule abstractions needed to support educational practice play.

The app teaches the game format and physical flow of play, but real NMJL card content is not shipped.

## Brownfield preservation

This repository may already contain unrelated files or legal documents. Builders must preserve the existing repo unless a task explicitly says otherwise.

Rules:

- Preserve any existing LICENSE file exactly as-is if present.
- Do not delete unrelated repo files.
- Do not rename unrelated top-level directories.
- Add new files only within the scope required for SuitUp.
- If a conflict appears between new work and an existing LICENSE, preserve the LICENSE and adapt the new work around it.
- Prefer additive changes over destructive changes.

## Runtime and offline constraints

Release 1 is offline-first and locally runnable only.

Operational requirements:

- Runs fully in Docker on the user’s own machine.
- Exposes HTTP on port 8092.
- Does not require internet connectivity at runtime.
- Does not fetch remote assets, fonts, rules, or AI data.
- Ships all lesson content, SVG tile art, and practice rules inside the container image.
- Uses local process memory and local disk only.
- Keeps startup simple and deterministic.

Recommended container posture:

- Single container.
- Flask app served by a production WSGI server inside the container.
- Static assets bundled into the image.
- Local writable directory only for progress saves, if enabled.

## Flask entrypoints

Release 1 uses Flask as the application shell.

Required entrypoints:

- WSGI module for production container startup:
 - `suitup.app:create_app`
- Flask development entry support:
 - `app.py` importing `create_app()` and exposing `app`
- Container runtime binding:
 - host `0.0.0.0`
 - port `8092`

Expected request surfaces:

- HTML lesson pages
- Practice game routes
- JSON endpoints for in-session actions where needed
- Static asset delivery for SVG tile art, CSS, and small JS bundles

## Package layout

The package tree below defines the Release 1 structure..
 ├── app.py
 ├── docs/
 │ └── architecture.md
 ├── suitup/
 │ ├── __init__.py
 │ ├── app.py
 │ ├── config.py
 │ ├── web/
 │ │ ├── __init__.py
 │ │ ├── routes_home.py
 │ │ ├── routes_lessons.py
 │ │ ├── routes_practice.py
 │ │ ├── routes_api.py
 │ │ ├── presenters.py
 │ │ ├── forms.py
 │ │ └── session_state.py
 │ ├── curriculum/
 │ │ ├── __init__.py
 │ │ ├── lessons.py
 │ │ ├── drills.py
 │ │ ├── glossary.py
 │ │ ├── tutorials.py
 │ │ └── progression.py
 │ ├── rules/
 │ │ ├── __init__.py
 │ │ ├── tiles.py
 │ │ ├── wall.py
 │ │ ├── seats.py
 │ │ ├── deal.py
 │ │ ├── charleston.py
 │ │ ├── actions.py
 │ │ ├── exposures.py
 │ │ ├── state.py
 │ │ ├── validation.py
 │ │ ├── scoring.py
 │ │ └── practice_patterns.py
 │ ├── ai/
 │ │ ├── __init__.py
 │ │ ├── difficulty.py
 │ │ ├── policy_base.py
 │ │ ├── beginner.py
 │ │ ├── intermediate.py
 │ │ ├── advanced.py
 │ │ ├── evaluator.py
 │ │ └── discard_safety.py
 │ ├── art/
 │ │ ├── __init__.py
 │ │ ├── tile_specs.py
 │ │ ├── svg_tiles.py
 │ │ ├── board_art.py
 │ │ └── export_assets.py
 │ ├── services/
 │ │ ├── __init__.py
 │ │ ├── game_service.py
 │ │ ├── lesson_service.py
 │ │ ├── practice_service.py
 │ │ └── storage_service.py
 │ ├── templates/
 │ │ ├── base.html
 │ │ ├── home.html
 │ │ ├── lessons/
 │ │ ├── practice/
 │ │ └── components/
 │ ├── static/
 │ │ ├── css/
 │ │ ├── js/
 │ │ ├── img/
 │ │ └── tiles/
 │ └── data/
 │ ├── curriculum/
 │ ├── practice_patterns/
 │ └── seeds/
 ├── tests/
 │ ├── test_rules/
 │ ├── test_ai/
 │ ├── test_curriculum/
 │ └── test_web/
 ├── Dockerfile
 ├── requirements.txt
 └── docker-compose.yml

## Module responsibilities