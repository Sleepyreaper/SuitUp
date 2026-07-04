# SuitUp 🀄 — Learn American Mah Jongg

A patient, hands-on web app that teaches a **total beginner** how to play
**American Mah Jongg** (National Mah Jongg League style). Built to go with a
fresh set (Majolica) and a green mat — it walks you from "I have a box of
mysterious tiles" to setting up a table, choosing who starts, running the
Charleston, and building hands.

Runs **entirely offline** in a single Docker container on **http://localhost:8092**.

## What's inside

- **The Tiles** — every tile in the set rendered as original SVG art, named and grouped.
- **Learn** — a step-by-step beginner curriculum (units → lessons → concrete steps).
- **Set Up a Table** — a live, reproducible deal: dealer selection, dice, and each seat's hand.
- **The Charleston** — the signature tile-passing ritual, in order, with the joker rule.
- **Groups Trainer** — click tiles to build Pairs / Pungs / Kongs / Quints and learn the joker rules interactively.
- **Rules Reference** — a beginner's rules card (original teaching material).

> SuitUp teaches mechanics with original materials. It does **not** reproduce the
> copyrighted NMJL card — use your own current card for real scored play.

## Tech

Python 3.11 + Flask, no external services. Rules engine in `suitup/` (tiles, wall/deal,
Charleston, groups, a simple 3-level practice AI); web UI in `suitup/web/`.

## Run it locally (without Docker)

```bash
pip install -r requirements.txt
python3 -m suitup.web.app
# open http://localhost:8092
```

## Run it with Docker

```bash
docker compose up -d --build
# open http://localhost:8092
```

## Run it on your server with Dockge

See **[DEPLOY.md](DEPLOY.md)** for step-by-step commands to stand it up on an
Ubuntu box running Docker + Dockge.

## Tests

```bash
pip install -r requirements.txt pytest
python3 -m pytest
```
