"""Tests for the win matcher, scoring, and the playable game engine."""
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from suitup.tiles import build_tile_set, is_joker, is_flower
from suitup.hands import (matches_hand, is_winning, hand_by_id, best_assessment,
                          assess_hand, WINNING_HANDS, AI_TARGET_HANDS)
from suitup.scoring import settle_win
from suitup.game import Game


def _by_ident():
    d = defaultdict(list)
    for t in build_tile_set(include_flowers=False):
        d[t.identifier().rsplit("_c", 1)[0]].append(t)
    return d


def test_all_winning_hands_total_14_and_have_no_runs():
    for h in WINNING_HANDS:
        if h.fixed is not None:
            assert sum(n for _, n in h.fixed) == 14, h.hand_id
            continue
        assert sum(h.group_sizes) == 14, h.hand_id
        assert all(s in (1, 2, 3, 4, 5) for s in h.group_sizes), h.hand_id  # no sequences


def test_double_quint_needs_jokers():
    b = _by_ident()
    jok = b["joker"]
    # two quints (4 naturals + 1 joker each) + a kong
    hand = (b["dots_1"][:4] + [jok[0]] + b["bams_2"][:4] + [jok[1]] + b["craks_3"][:4])
    assert matches_hand(hand, hand_by_id("double_quint"))


def test_news_soap_is_exact_tiles_and_rejects_jokers():
    b = _by_ident()
    good = (b["wind_north"][:1] + b["wind_east"][:1] + b["wind_west"][:1] + b["wind_south"][:1]
            + b["dragon_red"][:2] + b["dragon_green"][:2] + b["dragon_white"][:2]
            + b["dots_2"][:2] + b["dots_6"][:2])
    assert matches_hand(good, hand_by_id("news_soap"))
    with_joker = (b["wind_north"][:1] + b["wind_east"][:1] + b["wind_west"][:1] + b["wind_south"][:1]
                  + b["dragon_red"][:1] + b["joker"][:1] + b["dragon_green"][:2] + b["dragon_white"][:2]
                  + b["dots_2"][:2] + b["dots_6"][:2])
    assert not matches_hand(with_joker, hand_by_id("news_soap"))     # no jokers allowed
    wrong = (b["wind_north"][:2] + b["wind_east"][:1] + b["wind_west"][:1]
             + b["dragon_red"][:2] + b["dragon_green"][:2] + b["dragon_white"][:2]
             + b["dots_2"][:2] + b["dots_6"][:2])
    assert not matches_hand(wrong, hand_by_id("news_soap"))          # missing South


def test_ai_target_hands_exclude_no_joker_and_fixed():
    ids = {h.hand_id for h in AI_TARGET_HANDS}
    assert "news_soap" not in ids
    assert "double_quint" in ids and "four_pungs" in ids


def test_joker_exchange_swaps_tile_for_joker():
    from suitup.game import Game, Exposure
    g = Game.new_game(seed=3)
    g.phase = "play"; g.turn_index = g.human_index; g.sub = "discard"
    b = _by_ident()
    # opponent exposes a pung of 5-Dots using a joker; human holds a real 5-Dot
    opp = next(p for i, p in enumerate(g.players) if i != g.human_index)
    opp.exposures = [Exposure("pung", [b["dots_5"][0], b["dots_5"][1], b["joker"][0]])]
    me = g.players[g.human_index]
    me.concealed = [b["dots_5"][2]] + b["bams_1"][:12]
    opts = g._exchange_options()
    assert opts and opts[0]["identity"] == "dots_5"
    r = g.human_exchange_joker(opts[0]["seat_index"], opts[0]["exposure_index"], opts[0]["tile_id"])
    assert r["ok"]
    assert any(is_joker(t) for t in me.concealed)                    # got the joker
    assert not any(is_joker(t) for t in opp.exposures[0].tiles)      # exposure now all real
    assert opp.exposures[0].tiles[2].identifier().startswith("dots_5")


def test_four_pungs_and_pair_matches():
    b = _by_ident()
    hand = (b["dots_1"][:3] + b["dots_2"][:3] + b["bams_5"][:3]
            + b["craks_9"][:3] + b["wind_east"][:2])
    assert matches_hand(hand, hand_by_id("four_pungs"))
    assert is_winning(hand)


def test_joker_completes_pung_but_never_a_pair():
    b = _by_ident()
    jok = b["joker"]
    ok = (b["dots_1"][:2] + [jok[0]] + b["dots_2"][:3] + b["bams_5"][:3]
          + b["craks_9"][:3] + b["wind_east"][:2])
    assert matches_hand(ok, hand_by_id("four_pungs"))
    bad = (b["dots_1"][:3] + b["dots_2"][:3] + b["bams_5"][:3]
           + b["craks_9"][:3] + b["wind_east"][:1] + [jok[0]])   # joker in the pair
    assert not matches_hand(bad, hand_by_id("four_pungs"))


def test_single_suit_hand_rejects_mixed_suits():
    b = _by_ident()
    pure = (b["dots_1"][:3] + b["dots_2"][:3] + b["dots_3"][:3]
            + b["dots_4"][:3] + b["dots_5"][:2])
    mixed = (b["dots_1"][:3] + b["dots_2"][:3] + b["dots_3"][:3]
             + b["bams_4"][:3] + b["dots_5"][:2])
    assert matches_hand(pure, hand_by_id("one_suit"))
    assert not matches_hand(mixed, hand_by_id("one_suit"))
    assert matches_hand(mixed, hand_by_id("four_pungs"))     # still a plain four-pungs


def test_junk_hand_is_not_a_win():
    b = _by_ident()
    junk = (b["dots_1"][:1] + b["dots_3"][:1] + b["bams_4"][:2] + b["bams_6"][:2]
            + b["craks_7"][:2] + b["craks_9"][:2] + b["wind_east"][:2] + b["wind_west"][:2])
    assert len(junk) == 14 and not is_winning(junk)


def test_assessment_flags_deadwood():
    b = _by_ident()
    hand = b["dots_1"][:3] + b["dots_2"][:3] + b["bams_5"][:3] + b["wind_east"][:2] + b["craks_9"][:1] + b["bams_1"][:1]
    a = assess_hand(hand, hand_by_id("four_pungs"))
    assert a.placed >= 11
    assert any(_id_of(t) == "bams_1" for t in a.deadwood)


def _id_of(t):
    return t.identifier().rsplit("_c", 1)[0]


def test_settle_self_pick_jokerless_doubles():
    b = _by_ident()
    tiles = (b["dots_1"][:3] + b["dots_2"][:3] + b["bams_5"][:3]
             + b["craks_9"][:3] + b["wind_east"][:2])
    val = hand_by_id("four_pungs").points
    s = settle_win(hand_by_id("four_pungs"), tiles, winner_index=0,
                   self_drawn=True, discarder_index=None)
    assert s["jokerless"] and s["jokers_used"] == 0
    # self-pick x2 and jokerless x2 -> each of 3 losers pays val*4
    assert all(a == val * 4 for a in s["payments"].values())
    assert s["total"] == val * 4 * 3


def test_settle_discard_thrower_pays_double():
    b = _by_ident()
    jok = b["joker"]
    tiles = (b["dots_1"][:2] + [jok[0]] + b["dots_2"][:3] + b["bams_5"][:3]
             + b["craks_9"][:3] + b["wind_east"][:2])          # uses a joker -> not jokerless
    val = hand_by_id("four_pungs").points
    s = settle_win(hand_by_id("four_pungs"), tiles, winner_index=0,
                   self_drawn=False, discarder_index=2)
    assert not s["jokerless"]
    assert s["payments"][2] == val * 2                          # thrower pays double
    assert s["payments"][1] == val and s["payments"][3] == val  # others single
    assert s["total"] == val * 4


def test_win_moves_points_between_players():
    g = Game.new_game(seed=5)
    before = [p.score for p in g.players]
    hand = hand_by_id("four_pungs")
    b = _by_ident()
    g.players[0].concealed = (b["dots_1"][:3] + b["dots_2"][:3] + b["bams_5"][:3]
                              + b["craks_9"][:3] + b["wind_east"][:2])
    g.players[0].exposures = []
    g._record_win(0, hand, self_drawn=True)
    assert g.players[0].score > before[0]                       # winner gains
    assert all(g.players[i].score < before[i] for i in (1, 2, 3))  # losers pay
    # zero-sum: winner's gain equals total losses
    assert g.players[0].score == sum(before[i] - g.players[i].score for i in (1, 2, 3))


def test_human_can_call_pung_without_crashing():
    # regression: human_call logged self.last_discard AFTER it was cleared -> crash
    from suitup.game import Game
    g = Game.new_game(seed=4)
    g.roll_dice(); g.deal_tiles()
    g.phase = "play"; g.sub = "calls"
    b = _by_ident()
    hi = g.human_index
    other = (hi + 1) % 4
    g.players[hi].concealed = b["dots_3"][:2] + b["bams_7"][:11]
    tile = b["dots_3"][2]
    g.last_discard = tile
    g.last_discarder = other
    g.discards.append(tile)
    g.pending_human_calls = [{"kind": "pung"}]
    r = g.human_call("pung")                       # must not raise
    assert r["ok"]
    assert any(e.group_type == "pung" for e in g.players[hi].exposures)


def test_human_can_expose_kong_and_quint_on_turn():
    from suitup.game import Game
    b = _by_ident()
    g = Game.new_game(seed=6)
    g.phase = "play"; g.turn_index = g.human_index; g.sub = "discard"
    me = g.players[g.human_index]
    me.concealed = b["dots_5"][:4] + b["bams_2"][:3] + b["craks_9"][:3] + b["wind_east"][:4]
    opts = g._meld_options()
    assert any(o["kind"] == "kong" and o["identity"] == "dots_5" for o in opts)
    assert g.human_meld("dots_5", 4)["ok"]
    assert any(e.group_type == "kong" and len(e.tiles) == 4 for e in me.exposures)
    # quint from 4 naturals + a joker
    g2 = Game.new_game(seed=7)
    g2.phase = "play"; g2.turn_index = g2.human_index; g2.sub = "discard"
    me2 = g2.players[g2.human_index]
    me2.concealed = b["bams_2"][:4] + [b["joker"][0]] + b["craks_9"][:3] + b["dots_5"][:3] + b["wind_east"][:3]
    assert any(o["kind"] == "quint" for o in g2._meld_options())
    assert g2.human_meld("bams_2", 5)["ok"]
    assert any(len(e.tiles) == 5 for e in me2.exposures)


def test_meld_only_on_your_discard_turn():
    from suitup.game import Game
    g = Game.new_game(seed=8)          # still in setup
    assert g._meld_options() == []
    assert g.human_meld("dots_1", 4)["ok"] is False


def test_setup_phase_then_roll_and_deal():
    g = Game.new_game(seed=1)
    # a new game starts in the SETUP phase — nothing dealt yet, whole wall built
    assert g.phase == "setup" and g.sub == "roll"
    assert all(p.size() == 0 for p in g.players)
    assert len(g.wall) == 152 and g.dice is None
    r = g.roll_dice()
    assert r["ok"] and g.dice and 2 <= g.dice["total"] <= 12 and g.sub == "deal"
    r = g.deal_tiles()
    assert r["ok"] and g.phase == "charleston"
    assert g.players[g.dealer_index].size() == 14
    assert all(p.size() == 13 for i, p in enumerate(g.players) if i != g.dealer_index)
    assert sum(p.size() for p in g.players) + len(g.wall) == 152


def test_cannot_deal_before_rolling():
    g = Game.new_game(seed=2)
    assert g.deal_tiles()["ok"] is False        # must roll first
    g.roll_dice()
    assert g.roll_dice()["ok"] is False          # can't roll twice
    assert g.deal_tiles()["ok"] is True


def test_flower_basket_uses_any_flowers_and_soap():
    b = _by_ident()
    from suitup.tiles import build_tile_set, is_flower
    flowers = [t for t in build_tile_set(include_flowers=True) if is_flower(t)]
    # a Flower Kong is any 4 of the 8 flowers (they're interchangeable)
    hand = (flowers[:4] + b["dragon_red"][:3] + b["dragon_green"][:3]
            + b["dragon_white"][:2] + b["wind_east"][:2])
    assert matches_hand(hand, hand_by_id("flower_basket"))
    # a different four flowers still works
    hand2 = (flowers[4:8] + b["dragon_red"][:3] + b["dragon_green"][:3]
             + b["dragon_white"][:2] + b["wind_east"][:2])
    assert matches_hand(hand2, hand_by_id("flower_basket"))


def test_flowers_cannot_fill_a_number_pung():
    b = _by_ident()
    from suitup.tiles import build_tile_set, is_flower
    flowers = [t for t in build_tile_set(include_flowers=True) if is_flower(t)]
    # 3 flowers must NOT count as one of the four pungs in a numbers hand
    hand = (flowers[:3] + b["dots_2"][:3] + b["bams_5"][:3]
            + b["craks_9"][:3] + b["wind_east"][:2])
    assert not matches_hand(hand, hand_by_id("four_pungs"))


def _auto_play(g, max_steps=3000):
    """Drive the human seat with an honest auto-policy to force the hand to a
    terminal state; used to prove the engine never deadlocks and only legal wins."""
    for _ in range(max_steps):
        if g.phase not in ("setup", "charleston", "play"):
            return
        if g.phase == "setup":
            g.roll_dice() if g.sub == "roll" else g.deal_tiles()
            continue
        if g.phase == "charleston":
            if g.current_charleston():
                me = g.players[g.human_index]
                a = best_assessment(me.concealed)
                dead = [t for t in a.deadwood if not is_joker(t) and not is_flower(t)]
                pool = dead + [t for t in me.concealed
                               if not is_joker(t) and not is_flower(t)]
                g.submit_charleston([t.identifier() for t in pool[:3]])
            else:
                g.continue_second_charleston(False)
            continue
        if g.pending_human_calls:
            kinds = [c["kind"] for c in g.pending_human_calls]
            g.human_call("win") if "win" in kinds else g.human_pass_call()
            continue
        if g.turn_index == g.human_index:
            if g.sub == "draw":
                r = g.human_draw()
                if r.get("can_declare_win"):
                    g.human_declare_win(); continue
            if g.sub == "discard":
                if g._hand_wins(g.players[g.human_index].all_tiles()):
                    g.human_declare_win(); continue
                d = g._ai_choose_discard(g.players[g.human_index])
                g.human_discard(d.identifier())
            continue
        g._advance()


def test_full_games_reach_legal_terminal_states():
    legit = 0
    for seed in range(40):
        g = Game.new_game(seed=seed, ai_levels=[1, 2, 3])
        _auto_play(g)
        assert g.phase in ("hand_over", "game_over"), (seed, g.phase)
        wi = g.win_info
        if wi and not wi.get("wall_game"):
            w = g.players[g.winner_index]
            assert len(w.all_tiles()) == 14
            assert matches_hand(w.all_tiles(), hand_by_id(wi["scoring"]["hand_id"]))
            legit += 1
    assert legit >= 30  # the vast majority of hands resolve to a genuine win


def test_snapshot_hides_opponent_tiles():
    g = Game.new_game(seed=2)
    snap = g.snapshot()
    assert "concealed" in snap["you"]
    for opp in snap["opponents"]:
        assert "concealed_count" in opp and "concealed" not in opp
