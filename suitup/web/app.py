"""SuitUp — American Mah Jongg teaching app (Flask).

Serves a beginner-first, offline single-page teaching experience on port 8092:
a guided curriculum, a gallery of all original SVG tiles, a live table-setup
(dealer + deal) demo, the Charleston walkthrough, and an interactive groups
trainer. All data comes from the local rules engine — no cloud, no network.
"""
from __future__ import annotations

from flask import Flask, jsonify, render_template, request

from suitup import art, charleston, groups, wall
from suitup.tiles import Tile, TileKind, build_tile_set, is_joker
from suitup.patterns import list_patterns

APP_NAME = "SuitUp"
APP_PORT = 8092
APP_HOST = "0.0.0.0"


def tile_svg(tile: Tile) -> str:
    """Dispatch a tile to the right SVG renderer in suitup.art."""
    if tile.kind == TileKind.SUITED:
        return art.render_suited(tile.suit, tile.rank)
    if tile.kind == TileKind.WIND:
        return art.render_wind(tile.honor)
    if tile.kind == TileKind.DRAGON:
        return art.render_dragon(tile.honor)
    return art.render_joker()


def tile_json(tile: Tile) -> dict:
    return {
        "id": tile.identifier(),
        "name": tile.display_name(),
        "kind": tile.kind.value,
        "svg": tile_svg(tile),
        "is_joker": is_joker(tile),
    }


def create_app() -> Flask:
    app = Flask(__name__)

    @app.route("/")
    def index():
        return render_template("index.html", app_name=APP_NAME)

    @app.route("/healthz")
    def healthz():
        return jsonify({"status": "ok"})

    @app.route("/api/tiles")
    def api_tiles():
        """Every unique tile face (one per identity, not all copies) with art."""
        seen = set()
        out = []
        for t in build_tile_set(include_flowers=False):
            key = t.identifier().rsplit("_c", 1)[0]
            if key in seen:
                continue
            seen.add(key)
            out.append(tile_json(t))
        return jsonify({"tiles": out, "count_unique": len(out)})

    @app.route("/api/setup")
    def api_setup():
        """A reproducible table setup: dealer, dice, and every seat's hand."""
        try:
            seed = int(request.args.get("seed", ""))
        except (TypeError, ValueError):
            seed = None
        setup = wall.deal(seed=seed)
        hands = {
            seat: [tile_json(t) for t in sorted(tiles, key=lambda x: x.identifier())]
            for seat, tiles in setup.hands.items()
        }
        return jsonify({
            "dealer_seat": setup.dealer_seat,
            "dice": {"die1": setup.dice.die1, "die2": setup.dice.die2, "total": setup.dice.total},
            "seats": wall.SEATS,
            "hand_counts": setup.hand_counts(),
            "hands": hands,
            "wall_remaining": len(setup.wall_remaining),
        })

    @app.route("/api/charleston")
    def api_charleston():
        steps = charleston.charleston_sequence()
        return jsonify({"steps": [
            {"order": s.order, "phase": s.phase, "direction": s.direction,
             "count": s.count, "mandatory": s.mandatory, "blind_allowed": s.blind_allowed,
             "note": s.note}
            for s in steps
        ]})

    @app.route("/api/patterns")
    def api_patterns():
        out = []
        for p in list_patterns():
            out.append({
                "id": p.pattern_id,
                "name": p.display_name,
                "difficulty": getattr(p.difficulty, "value", str(p.difficulty)),
                "description": p.explanation,
                "total_tiles": p.total_tiles(),
                "requires_pair": p.requires_pair,
            })
        return jsonify({"patterns": out})

    @app.route("/api/check-group", methods=["POST"])
    def api_check_group():
        """Validate a selection of tile identities as a Pair/Pung/Kong/Quint."""
        data = request.get_json(silent=True) or {}
        ids = data.get("tile_ids", [])
        by_id = {t.identifier(): t for t in build_tile_set()}
        picked = [by_id[i] for i in ids if i in by_id]
        return jsonify({
            "valid": groups.is_valid_group(picked),
            "explanation": groups.describe_group(picked),
            "count": len(picked),
        })

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host=APP_HOST, port=APP_PORT)
