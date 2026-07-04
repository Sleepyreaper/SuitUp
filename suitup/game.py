"""The playable American Mah Jongg game engine for SuitUp.

A full, seedable, serializable state machine: deal -> Charleston -> play loop
(draw / discard / call a discard for a Pung, Kong, or Mah Jongg) -> win detection
via `suitup.hands` -> scoring -> next hand. One seat is the human; the other three
are AI opponents (`suitup.ai`) that target a real winning hand and adapt in level.

The engine is UI-agnostic: it exposes actions and a `snapshot()` the web layer or a
headless test harness can drive. All randomness flows through a seeded RNG so games
are reproducible for teaching and testing.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from suitup.charleston import charleston_sequence, illegal_pass_tiles
from suitup.groups import _non_joker_key
from suitup.hands import (AI_TARGET_HANDS, WINNING_HANDS, assess_hand,
                          best_assessment, matches_hand, winning_hands_for)
from suitup.scoring import score_win
from suitup.tiles import Tile, build_tile_set, is_joker, is_flower

SEATS = ["East", "South", "West", "North"]
START_HAND = 13


def _key(tile: Tile) -> str:
    return _non_joker_key(tile)


@dataclass
class Exposure:
    group_type: str          # "pung" | "kong"
    tiles: List[Tile]

    def identity(self) -> Optional[str]:
        nat = next((t for t in self.tiles if not is_joker(t)), None)
        return _key(nat) if nat else None

    def joker_count(self) -> int:
        return sum(1 for t in self.tiles if is_joker(t))

    def to_dict(self) -> dict:
        return {"group_type": self.group_type,
                "identity": self.identity(),
                "joker_count": self.joker_count(),
                "tiles": [{"id": t.identifier(), "name": t.display_name(),
                           "joker": is_joker(t)} for t in self.tiles]}


@dataclass
class Player:
    seat: str
    is_human: bool
    level: int = 1
    concealed: List[Tile] = field(default_factory=list)
    exposures: List[Exposure] = field(default_factory=list)
    score: int = 0
    hands_won: int = 0
    target_id: Optional[str] = None

    def all_tiles(self) -> List[Tile]:
        return list(self.concealed) + [t for e in self.exposures for t in e.tiles]

    def size(self) -> int:
        return len(self.all_tiles())


class Game:
    def __init__(self, seed: Optional[int] = None):
        self.rng = random.Random(seed)
        self.seed = seed
        self.players: List[Player] = []
        self.human_index = 0
        self.dealer_index = 0
        self.turn_index = 0
        self.wall: List[Tile] = []
        self.discards: List[Tile] = []
        self.last_discard: Optional[Tile] = None
        self.last_discarder: Optional[int] = None
        self.seen: Dict[str, int] = {}
        self.phase = "setup"                 # setup|charleston|play|hand_over|game_over
        self.sub = ""                        # draw|discard|calls
        self.charleston_queue: List = []
        self.charleston_second_offered = False
        self.log: List[str] = []
        self.hand_number = 1
        self.winner_index: Optional[int] = None
        self.win_info: Optional[dict] = None
        self.target_score = 150
        self.pending_human_calls: List[dict] = []

    # ---- setup ---------------------------------------------------------------
    @classmethod
    def new_game(cls, human_seat: str = "East", ai_levels: Optional[List[int]] = None,
                 seed: Optional[int] = None, target_score: int = 150) -> "Game":
        g = cls(seed=seed)
        g.target_score = target_score
        levels = ai_levels or [1, 2, 3]
        g.human_index = SEATS.index(human_seat)
        li = 0
        for i, seat in enumerate(SEATS):
            if i == g.human_index:
                g.players.append(Player(seat=seat, is_human=True))
            else:
                g.players.append(Player(seat=seat, is_human=False,
                                        level=levels[li % len(levels)]))
                li += 1
        g.dealer_index = g.human_index          # human is dealer for hand 1 (learn the flow)
        g._deal()
        return g

    def _deal(self) -> None:
        tiles = build_tile_set(include_flowers=True)
        self.rng.shuffle(tiles)
        for p in self.players:
            p.concealed = []
            p.exposures = []
        pos = 0
        for _ in range(START_HAND):
            for p in self.players:
                p.concealed.append(tiles[pos]); pos += 1
        self.players[self.dealer_index].concealed.append(tiles[pos]); pos += 1
        self.wall = tiles[pos:]
        self.discards = []
        self.last_discard = None
        self.last_discarder = None
        self.seen = {}
        self.winner_index = None
        self.win_info = None
        for p in self.players:
            p.concealed.sort(key=lambda t: t.identifier())
            if not p.is_human:
                p.target_id = best_assessment(p.concealed, AI_TARGET_HANDS).hand.hand_id
        self.charleston_queue = charleston_sequence(second_charleston=False, courtesy=False)
        self.charleston_second_offered = False
        self.phase = "charleston"
        self.sub = ""
        self._log(f"Hand {self.hand_number}: {self.players[self.dealer_index].seat} is dealer "
                  f"and starts with 14 tiles. Charleston begins.")

    # ---- charleston ----------------------------------------------------------
    def current_charleston(self) -> Optional[dict]:
        if self.phase != "charleston" or not self.charleston_queue:
            return None
        s = self.charleston_queue[0]
        return {"order": s.order, "phase": s.phase, "direction": s.direction,
                "count": s.count, "blind_allowed": s.blind_allowed, "note": s.note}

    def _charleston_target(self, giver: int, direction: str) -> int:
        # Passing "right" moves one seat forward in play order; left one back; across two.
        if direction == "right":
            return (giver + 1) % 4
        if direction == "left":
            return (giver - 1) % 4
        return (giver + 2) % 4          # across / opposite

    def _ai_charleston_pick(self, p: Player) -> List[Tile]:
        assess = best_assessment(p.concealed, AI_TARGET_HANDS)
        passable = lambda t: not is_joker(t) and not is_flower(t)  # never pass jokers/flowers
        dead = [t for t in assess.deadwood if passable(t)]
        pool = dead + [t for t in p.concealed if passable(t) and t not in dead]
        return pool[:3]

    def submit_charleston(self, tile_ids: List[str]) -> dict:
        """Human passes exactly 3 tiles for the current step; all seats pass
        simultaneously in the step's direction. Advances the Charleston."""
        if self.phase != "charleston" or not self.charleston_queue:
            return {"ok": False, "error": "No Charleston step is active."}
        step = self.charleston_queue[0]
        human = self.players[self.human_index]
        chosen = [t for t in human.concealed if t.identifier() in set(tile_ids)]
        if len(chosen) != 3:
            return {"ok": False, "error": "Select exactly 3 tiles to pass."}
        bad = illegal_pass_tiles(chosen)
        if bad:
            names = ", ".join(t.display_name() for t in bad)
            return {"ok": False, "error": f"You cannot pass Jokers or Flowers: {names}."}

        passing: Dict[int, List[Tile]] = {}
        for i, p in enumerate(self.players):
            passing[i] = chosen if i == self.human_index else self._ai_charleston_pick(p)
        for i, tiles in passing.items():
            tgt = self._charleston_target(i, step.direction)
            for t in tiles:
                self.players[i].concealed.remove(t)
            self.players[tgt].concealed.extend(tiles)
        for p in self.players:
            p.concealed.sort(key=lambda t: t.identifier())
            if not p.is_human:
                p.target_id = best_assessment(p.concealed, AI_TARGET_HANDS).hand.hand_id
        self._log(f"Charleston pass {step.order} ({step.direction}) complete.")
        self.charleston_queue.pop(0)
        if not self.charleston_queue and not self.charleston_second_offered:
            self.charleston_second_offered = True
        return {"ok": True}

    def continue_second_charleston(self, do_it: bool) -> dict:
        if self.phase != "charleston":
            return {"ok": False, "error": "Charleston is not active."}
        if do_it and not self.charleston_queue:
            self.charleston_queue = charleston_sequence(second_charleston=True,
                                                        courtesy=False)[3:]
            self._log("Table agreed to a second Charleston.")
            return {"ok": True}
        return self.finish_charleston()

    def finish_charleston(self) -> dict:
        self.phase = "play"
        self.turn_index = self.dealer_index
        self.sub = "discard"          # dealer opens by discarding (already holds 14)
        self._log(f"Play begins. {self.players[self.turn_index].seat} discards first.")
        self._advance()
        return {"ok": True}

    # ---- play: helpers -------------------------------------------------------
    def _log(self, msg: str) -> None:
        self.log.append(msg)
        self.log = self.log[-60:]

    def _mark_seen(self, tile: Tile) -> None:
        if not is_joker(tile):
            self.seen[_key(tile)] = self.seen.get(_key(tile), 0) + 1

    def _next(self, i: int) -> int:
        return (i + 1) % 4

    def _draw_from_wall(self, p: Player) -> Optional[Tile]:
        if not self.wall:
            return None
        t = self.wall.pop(0)
        p.concealed.append(t)
        p.concealed.sort(key=lambda t: t.identifier())
        return t

    def _hand_wins(self, tiles: List[Tile]):
        won = winning_hands_for(tiles)
        return won[0] if won else None

    # ---- play: human actions -------------------------------------------------
    def human_draw(self) -> dict:
        if self.phase != "play" or self.sub != "draw" or self.turn_index != self.human_index:
            return {"ok": False, "error": "It is not yours to draw right now."}
        t = self._draw_from_wall(self.players[self.human_index])
        if t is None:
            return self._wall_game()
        self.sub = "discard"
        self._log(f"You drew {t.display_name()}.")
        win = self._hand_wins(self.players[self.human_index].all_tiles())
        return {"ok": True, "drew": t.identifier(),
                "can_declare_win": bool(win),
                "win_hand": win.hand_id if win else None}

    def human_discard(self, tile_id: str) -> dict:
        p = self.players[self.human_index]
        if self.phase != "play" or self.sub != "discard" or self.turn_index != self.human_index:
            return {"ok": False, "error": "You cannot discard right now."}
        tile = next((t for t in p.concealed if t.identifier() == tile_id), None)
        if tile is None:
            return {"ok": False, "error": "That tile is not in your hand."}
        p.concealed.remove(tile)
        self._place_discard(self.human_index, tile)
        self._log(f"You discarded {tile.display_name()}.")
        self._advance()
        return {"ok": True}

    def human_declare_win(self) -> dict:
        p = self.players[self.human_index]
        won = self._hand_wins(p.all_tiles())
        if not won:
            return {"ok": False, "error": "Your hand does not complete a winning pattern yet."}
        self_drawn = self.sub == "discard" and self.turn_index == self.human_index
        self._record_win(self.human_index, won, self_drawn)
        return {"ok": True}

    def human_call(self, kind: str) -> dict:
        opt = next((c for c in self.pending_human_calls if c["kind"] == kind), None)
        if not opt:
            return {"ok": False, "error": "That call is not available."}
        if kind == "win":
            won = self._hand_wins(self.players[self.human_index].all_tiles()
                                  + [self.last_discard])
            self.players[self.human_index].concealed.append(self.last_discard)
            self._record_win(self.human_index, won, self_drawn=False)
            return {"ok": True}
        self._perform_claim(self.human_index, kind)
        self.pending_human_calls = []
        self.sub = "discard"
        self._log(f"You called {kind.upper()} on {self.last_discard.display_name()}.")
        return {"ok": True}

    def human_pass_call(self) -> dict:
        self.pending_human_calls = []
        self._resolve_calls(skip_human=True)
        self._advance()
        return {"ok": True}

    # ---- play: joker exchange (redemption) -----------------------------------
    def _exchange_options(self) -> List[dict]:
        """Joker redemptions the human may do right now: on their turn, before or
        after drawing, swap a real tile they hold for a joker in ANY exposure
        (their own or an opponent's)."""
        if (self.phase != "play" or self.turn_index != self.human_index
                or self.sub not in ("draw", "discard")):
            return []
        me = self.players[self.human_index]
        opts: List[dict] = []
        for si, p in enumerate(self.players):
            for ei, exp in enumerate(p.exposures):
                if exp.joker_count() <= 0:
                    continue
                ident = exp.identity()
                match = next((t for t in me.concealed
                              if not is_joker(t) and _key(t) == ident), None)
                if match:
                    opts.append({"seat": p.seat, "seat_index": si,
                                 "exposure_index": ei, "identity": ident,
                                 "tile_id": match.identifier(),
                                 "tile_name": match.display_name()})
        return opts

    def human_exchange_joker(self, seat_index: int, exposure_index: int,
                             tile_id: str) -> dict:
        if (self.phase != "play" or self.turn_index != self.human_index
                or self.sub not in ("draw", "discard")):
            return {"ok": False, "error": "You can only redeem a joker on your turn."}
        if not (0 <= seat_index < 4):
            return {"ok": False, "error": "No such player."}
        tgt = self.players[seat_index]
        if not (0 <= exposure_index < len(tgt.exposures)):
            return {"ok": False, "error": "No such exposure."}
        exp = tgt.exposures[exposure_index]
        jpos = next((k for k, t in enumerate(exp.tiles) if is_joker(t)), None)
        if jpos is None:
            return {"ok": False, "error": "That group has no joker to redeem."}
        ident = exp.identity()
        me = self.players[self.human_index]
        tile = next((t for t in me.concealed if t.identifier() == tile_id
                     and not is_joker(t) and _key(t) == ident), None)
        if tile is None:
            return {"ok": False, "error": "Give the real tile that matches the group."}
        joker = exp.tiles[jpos]
        exp.tiles[jpos] = tile
        me.concealed.remove(tile)
        me.concealed.append(joker)
        me.concealed.sort(key=lambda t: t.identifier())
        self._log(f"You redeemed a Joker from {tgt.seat}'s {tile.display_name()} group.")
        return {"ok": True}

    def _ai_reclaim_jokers(self, i: int) -> None:
        """An AI swaps a spare/deadwood tile for a joker sitting in any exposure —
        jokers are always worth reclaiming."""
        p = self.players[i]
        target = self._ai_target(p)
        dead = {_key(t) for t in assess_hand(p.concealed, target).deadwood
                if not is_joker(t)}
        for sp in self.players:
            for exp in sp.exposures:
                if exp.joker_count() <= 0:
                    continue
                ident = exp.identity()
                give = next((t for t in p.concealed if not is_joker(t)
                             and _key(t) == ident and _key(t) in dead), None)
                if give:
                    jpos = next(k for k, t in enumerate(exp.tiles) if is_joker(t))
                    joker = exp.tiles[jpos]
                    exp.tiles[jpos] = give
                    p.concealed.remove(give)
                    p.concealed.append(joker)
                    self._log(f"{p.seat} redeemed a Joker from {sp.seat}'s exposure.")
                    return

    # ---- play: claim mechanics -----------------------------------------------
    def _place_discard(self, who: int, tile: Tile) -> None:
        self.discards.append(tile)
        self.last_discard = tile
        self.last_discarder = who
        self._mark_seen(tile)
        self.sub = "calls"

    def _matching_naturals(self, p: Player, tile: Tile) -> List[Tile]:
        return [t for t in p.concealed if not is_joker(t) and _key(t) == _key(tile)]

    def _can_claim(self, i: int, tile: Tile) -> List[str]:
        if i == self.last_discarder:
            return []
        p = self.players[i]
        kinds = []
        if self._hand_wins(p.all_tiles() + [tile]):
            kinds.append("win")
        n = len(self._matching_naturals(p, tile))
        if n >= 3:
            kinds.append("kong")
        if n >= 2:
            kinds.append("pung")
        return kinds

    def _perform_claim(self, i: int, kind: str) -> None:
        p = self.players[i]
        tile = self.last_discard
        need = 3 if kind == "kong" else 2
        matches = self._matching_naturals(p, tile)[:need]
        for t in matches:
            p.concealed.remove(t)
        group = matches + [tile]
        p.exposures.append(Exposure(group_type=kind, tiles=group))
        self.discards.pop()                    # claimed tile leaves the pile
        self.turn_index = i
        self.last_discard = None

    # ---- play: AI ------------------------------------------------------------
    def _ai_target(self, p: Player):
        return next((h for h in WINNING_HANDS if h.hand_id == p.target_id),
                    best_assessment(p.concealed, AI_TARGET_HANDS).hand)

    def _ai_choose_discard(self, p: Player) -> Tile:
        assess = assess_hand(p.concealed, self._ai_target(p))
        dead = [t for t in assess.deadwood if not is_joker(t)]
        if dead:
            counts: Dict[str, int] = {}
            for t in p.concealed:
                counts[_key(t)] = counts.get(_key(t), 0) + 1
            dead.sort(key=lambda t: (self.seen.get(_key(t), 0)
                                     if p.level >= 3 else 0))
            return dead[0]
        naturals = [t for t in p.concealed if not is_joker(t)]
        counts = {}
        for t in naturals:
            counts[_key(t)] = counts.get(_key(t), 0) + 1
        naturals.sort(key=lambda t: (counts[_key(t)], self.seen.get(_key(t), 0)))
        return naturals[0] if naturals else p.concealed[0]

    def _ai_wants_claim(self, i: int, tile: Tile, kinds: List[str]) -> Optional[str]:
        if "win" in kinds:
            return "win"
        p = self.players[i]
        target = self._ai_target(p)
        before = assess_hand(p.concealed, target).placed
        for kind in ("kong", "pung"):
            if kind in kinds:
                need = 3 if kind == "kong" else 2
                hypothetical = [t for t in p.concealed
                                if not (not is_joker(t) and _key(t) == _key(tile))][:]
                # a claim only helps if the target still has an open group slot
                open_slots = [s for s in target.group_sizes if s >= need]
                if open_slots and p.level >= 2:
                    return kind
                if p.level >= 3 and open_slots:
                    return kind
        return None

    def _run_ai_turn(self, i: int) -> None:
        p = self.players[i]
        drew = self._draw_from_wall(p)
        if drew is None:
            self._wall_game(); return
        won = self._hand_wins(p.all_tiles())
        if won:
            self._record_win(i, won, self_drawn=True); return
        if p.level >= 2:
            self._ai_reclaim_jokers(i)
        tile = self._ai_choose_discard(p)
        p.concealed.remove(tile)
        self._place_discard(i, tile)
        self._log(f"{p.seat} drew and discarded {tile.display_name()}.")

    # ---- play: driver --------------------------------------------------------
    def _advance(self) -> None:
        """Run the game forward through AI turns and AI/no calls until the human
        must act (draw, discard, or decide on a call) or the hand ends."""
        guard = 0
        while self.phase == "play" and guard < 400:
            guard += 1
            if self.sub == "calls":
                if self._resolve_calls(skip_human=False):
                    return                       # paused for a human call decision
                continue
            if self.turn_index == self.human_index:
                return                           # human must draw or discard
            if self.sub == "draw":
                self._run_ai_turn(self.turn_index)
            elif self.sub == "discard":
                p = self.players[self.turn_index]
                tile = self._ai_choose_discard(p)
                p.concealed.remove(tile)
                self._place_discard(self.turn_index, tile)
                self._log(f"{p.seat} discarded {tile.display_name()}.")

    def _resolve_calls(self, skip_human: bool) -> bool:
        """Resolve claims on the current discard. Returns True if we paused for a
        human decision. Priority: a Mah Jongg claim beats an exposure; otherwise
        the claimer nearest to the discarder's right wins the tile."""
        tile = self.last_discard
        if tile is None:
            self._pass_to_next(); return False

        if not skip_human:
            human_kinds = self._can_claim(self.human_index, tile)
            if human_kinds:
                self.pending_human_calls = [{"kind": k} for k in human_kinds]
                return True                      # wait for human_call / human_pass_call

        winners = []
        exposers = []
        order = [(self.last_discarder + k) % 4 for k in range(1, 4)]
        for i in order:
            if i == self.human_index:
                continue
            kinds = self._can_claim(i, tile)
            if "win" in kinds:
                winners.append(i)
            elif kinds:
                want = self._ai_wants_claim(i, tile, kinds)
                if want:
                    exposers.append((i, want))
        if winners:
            i = winners[0]
            won = self._hand_wins(self.players[i].all_tiles() + [tile])
            self.players[i].concealed.append(tile)
            self._record_win(i, won, self_drawn=False)
            return False
        if exposers:
            i, kind = exposers[0]
            self._perform_claim(i, kind)
            self._log(f"{self.players[i].seat} called {kind.upper()} "
                      f"on {tile.display_name()}.")
            self.sub = "discard"
            return False
        self._pass_to_next()
        return False

    def _pass_to_next(self) -> None:
        self.last_discard = None
        self.turn_index = self._next(self.last_discarder if self.last_discarder is not None
                                     else self.turn_index)
        self.sub = "draw"

    # ---- end of hand ---------------------------------------------------------
    def _wall_game(self) -> dict:
        self.phase = "hand_over"
        self.win_info = {"wall_game": True}
        self._log("The wall is exhausted — this hand is a draw (wall game). No score.")
        return {"ok": True, "wall_game": True}

    def _record_win(self, i: int, hand, self_drawn: bool) -> None:
        p = self.players[i]
        breakdown = score_win(hand, p.all_tiles(), self_drawn)
        p.score += breakdown["total"]
        p.hands_won += 1
        self.winner_index = i
        self.phase = "hand_over"
        self.pending_human_calls = []
        self.win_info = {"wall_game": False, "winner": p.seat,
                         "is_human": p.is_human, "scoring": breakdown,
                         "hand_tiles": [{"id": t.identifier(), "name": t.display_name(),
                                         "joker": is_joker(t)} for t in p.all_tiles()]}
        who = "You" if p.is_human else p.seat
        self._log(f"MAH JONGG! {who} won with {hand.name} (+{breakdown['total']} pts).")
        if any(pl.score >= self.target_score for pl in self.players):
            self.phase = "game_over"

    def next_hand(self) -> dict:
        if self.phase not in ("hand_over",):
            return {"ok": False, "error": "The current hand is not over."}
        self.hand_number += 1
        self.dealer_index = self._next(self.dealer_index)
        self._deal()
        return {"ok": True}

    # ---- serialization -------------------------------------------------------
    def _tile_json(self, t: Tile) -> dict:
        return {"id": t.identifier(), "name": t.display_name(), "joker": is_joker(t)}

    def snapshot(self) -> dict:
        me = self.players[self.human_index]
        assess = best_assessment(me.concealed) if me.concealed else None
        opponents = []
        for i, p in enumerate(self.players):
            if i == self.human_index:
                continue
            opponents.append({
                "seat": p.seat, "level": p.level, "concealed_count": len(p.concealed),
                "exposures": [e.to_dict() for e in p.exposures],
                "score": p.score, "hands_won": p.hands_won,
                "is_turn": i == self.turn_index and self.phase == "play",
            })
        return {
            "phase": self.phase, "sub": self.sub,
            "hand_number": self.hand_number, "target_score": self.target_score,
            "dealer": self.players[self.dealer_index].seat,
            "turn": self.players[self.turn_index].seat if self.phase == "play" else None,
            "your_turn": self.turn_index == self.human_index and self.phase == "play",
            "wall_remaining": len(self.wall),
            "you": {
                "seat": me.seat, "score": me.score, "hands_won": me.hands_won,
                "concealed": [self._tile_json(t) for t in me.concealed],
                "exposures": [e.to_dict() for e in me.exposures],
            },
            "opponents": opponents,
            "discards": [self._tile_json(t) for t in self.discards[-24:]],
            "last_discard": self._tile_json(self.last_discard) if self.last_discard else None,
            "last_discarder": (self.players[self.last_discarder].seat
                               if self.last_discarder is not None else None),
            "charleston": self.current_charleston(),
            "charleston_second_offered": (self.charleston_second_offered
                                          and not self.charleston_queue
                                          and self.phase == "charleston"),
            "pending_calls": [c["kind"] for c in self.pending_human_calls],
            "joker_exchanges": self._exchange_options(),
            "hint": ({"target": assess.hand.name, "target_desc": assess.hand.describe(),
                      "needed": assess.needed, "completeness": assess.completeness,
                      "wants": assess.wants,
                      "deadwood": [self._tile_json(t) for t in assess.deadwood]}
                     if assess else None),
            "win_info": self.win_info,
            "log": self.log[-14:],
        }
