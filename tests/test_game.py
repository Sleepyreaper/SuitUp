"""Tests for the win matcher, scoring, and the playable game engine."""
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from suitup.tiles import build_tile_set, is_joker, is_flower
from suitup.hands import (matches_hand, is_winning, hand_by_id, best_assessment,
                          assess_hand, WINNING_HANDS, AI_TARGET_HANDS)
from suitup.scoring import score_win
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


def test_score_win_bonuses():
    b = _by_ident()
    tiles = (b["dots_1"][:3] + b["dots_2"][:3] + b["bams_5"][:3]
             + b["craks_9"][:3] + b["wind_east"][:2])
    s = score_win(hand_by_id("four_pungs"), tiles, self_drawn=True)
    assert s["jokers_used"] == 0
    assert s["total"] == hand_by_id("four_pungs").points + 20  # self-draw + jokerless


def test_new_game_deals_correctly():
    g = Game.new_game(seed=1)
    assert g.phase == "charleston"
    assert g.players[g.dealer_index].size() == 14
    assert all(p.size() == 13 for i, p in enumerate(g.players) if i != g.dealer_index)
    total = sum(p.size() for p in g.players) + len(g.wall)
    assert total == 152                      # full American set incl. 8 Flowers


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
        if g.phase not in ("charleston", "play"):
            return
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
