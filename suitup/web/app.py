"""SuitUp — American Mah Jongg teaching app (Flask).

Serves a beginner-first, offline single-page teaching experience on port 8092:
a guided curriculum, a gallery of all original SVG tiles, a live table-setup
(dealer + deal) demo, the Charleston walkthrough, and an interactive groups
trainer. All data comes from the local rules engine — no cloud, no network.
"""
from __future__ import annotations

import threading
import uuid

from flask import Flask, jsonify, render_template, request

from suitup import art, charleston, groups, wall
from suitup.game import Game
from suitup.tiles import Tile, TileKind, build_tile_set, is_joker
from suitup.patterns import list_patterns

APP_NAME = "SuitUp"
APP_PORT = 8092
APP_HOST = "0.0.0.0"

_GAMES: dict = {}
_GAMES_LOCK = threading.Lock()
_MAX_GAMES = 200


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


_SVG_BY_KEY: dict = {}
for _t in build_tile_set(include_flowers=False):
    _k = _t.identifier().rsplit("_c", 1)[0]
    _SVG_BY_KEY.setdefault(_k, tile_svg(_t))


def _svg_for(tile_id: str) -> str:
    return _SVG_BY_KEY.get(tile_id.rsplit("_c", 1)[0], "")


def _enrich_tile(d: dict) -> dict:
    if isinstance(d, dict) and "id" in d and "svg" not in d:
        d["svg"] = _svg_for(d["id"])
    return d


def _enrich_snapshot(snap: dict) -> dict:
    """Attach tile SVGs to every tile dict in a game snapshot (engine stays
    UI-agnostic; the web layer owns rendering)."""
    for t in snap.get("you", {}).get("concealed", []):
        _enrich_tile(t)
    for e in snap.get("you", {}).get("exposures", []):
        for t in e.get("tiles", []):
            _enrich_tile(t)
    for opp in snap.get("opponents", []):
        for e in opp.get("exposures", []):
            for t in e.get("tiles", []):
                _enrich_tile(t)
    for t in snap.get("discards", []):
        _enrich_tile(t)
    if snap.get("last_discard"):
        _enrich_tile(snap["last_discard"])
    hint = snap.get("hint")
    if hint:
        for t in hint.get("deadwood", []):
            _enrich_tile(t)
    wi = snap.get("win_info")
    if wi and wi.get("hand_tiles"):
        for t in wi["hand_tiles"]:
            _enrich_tile(t)
    return snap


def _get_game(game_id: str):
    with _GAMES_LOCK:
        return _GAMES.get(game_id)


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

    # ---- playable game (simulator) ------------------------------------------
    def _snap(game_id, game):
        return jsonify({"game_id": game_id, "state": _enrich_snapshot(game.snapshot())})

    @app.route("/api/game/new", methods=["POST"])
    def api_game_new():
        data = request.get_json(silent=True) or {}
        levels = data.get("ai_levels") or [1, 2, 3]
        try:
            levels = [max(1, min(3, int(x))) for x in levels][:3]
        except (TypeError, ValueError):
            levels = [1, 2, 3]
        seed = data.get("seed")
        try:
            seed = int(seed) if seed is not None else None
        except (TypeError, ValueError):
            seed = None
        target = data.get("target_score", 150)
        try:
            target = max(25, int(target))
        except (TypeError, ValueError):
            target = 150
        game = Game.new_game(human_seat="East", ai_levels=levels, seed=seed,
                             target_score=target)
        game_id = uuid.uuid4().hex[:12]
        with _GAMES_LOCK:
            if len(_GAMES) >= _MAX_GAMES:
                for old in list(_GAMES)[: len(_GAMES) - _MAX_GAMES + 1]:
                    _GAMES.pop(old, None)
            _GAMES[game_id] = game
        return _snap(game_id, game)

    @app.route("/api/game/<game_id>")
    def api_game_state(game_id):
        game = _get_game(game_id)
        if not game:
            return jsonify({"error": "Game not found. Start a new game."}), 404
        return _snap(game_id, game)

    def _action(game_id, fn):
        game = _get_game(game_id)
        if not game:
            return jsonify({"error": "Game not found. Start a new game."}), 404
        result = fn(game)
        payload = {"game_id": game_id, "state": _enrich_snapshot(game.snapshot())}
        if isinstance(result, dict):
            payload["result"] = result
        return jsonify(payload)

    @app.route("/api/game/<game_id>/charleston", methods=["POST"])
    def api_game_charleston(game_id):
        ids = (request.get_json(silent=True) or {}).get("tile_ids", [])
        return _action(game_id, lambda g: g.submit_charleston(ids))

    @app.route("/api/game/<game_id>/charleston-second", methods=["POST"])
    def api_game_charleston_second(game_id):
        do_it = bool((request.get_json(silent=True) or {}).get("continue", False))
        return _action(game_id, lambda g: g.continue_second_charleston(do_it))

    @app.route("/api/game/<game_id>/draw", methods=["POST"])
    def api_game_draw(game_id):
        return _action(game_id, lambda g: g.human_draw())

    @app.route("/api/game/<game_id>/discard", methods=["POST"])
    def api_game_discard(game_id):
        tile_id = (request.get_json(silent=True) or {}).get("tile_id", "")
        return _action(game_id, lambda g: g.human_discard(tile_id))

    @app.route("/api/game/<game_id>/call", methods=["POST"])
    def api_game_call(game_id):
        kind = (request.get_json(silent=True) or {}).get("kind", "")
        return _action(game_id, lambda g: g.human_call(kind))

    @app.route("/api/game/<game_id>/pass-call", methods=["POST"])
    def api_game_pass_call(game_id):
        return _action(game_id, lambda g: g.human_pass_call())

    @app.route("/api/game/<game_id>/exchange-joker", methods=["POST"])
    def api_game_exchange_joker(game_id):
        d = request.get_json(silent=True) or {}
        return _action(game_id, lambda g: g.human_exchange_joker(
            int(d.get("seat_index", -1)), int(d.get("exposure_index", -1)),
            d.get("tile_id", "")))

    @app.route("/api/game/<game_id>/declare-win", methods=["POST"])
    def api_game_declare_win(game_id):
        return _action(game_id, lambda g: g.human_declare_win())

    @app.route("/api/game/<game_id>/next-hand", methods=["POST"])
    def api_game_next_hand(game_id):
        return _action(game_id, lambda g: g.next_hand())

    @app.route("/api/game-hands")
    def api_game_hands():
        from suitup.hands import WINNING_HANDS
        return jsonify({"hands": [
            {"id": h.hand_id, "name": h.name, "difficulty": h.difficulty,
             "structure": h.describe(), "points": h.points, "teaches": h.teaches}
            for h in WINNING_HANDS]})

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host=APP_HOST, port=APP_PORT)
