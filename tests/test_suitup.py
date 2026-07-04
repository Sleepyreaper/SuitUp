"""Smoke tests for the SuitUp rules engine and web API."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from suitup.tiles import build_tile_set, verify_standard_set, count_by_kind, is_joker
from suitup.wall import deal, SEATS
from suitup.charleston import charleston_sequence, validate_pass, can_pass_tile
from suitup.groups import is_valid_group, describe_group
from suitup.ai import bot_take_turn
from suitup.web.app import create_app


def test_standard_set_is_144_and_correct():
    ts = build_tile_set(include_flowers=False)
    assert len(ts) == 144
    assert verify_standard_set(ts)
    c = count_by_kind(ts)
    assert c["suited"] == 108 and c["wind"] == 16 and c["dragon"] == 12 and c["joker"] == 8


def test_deal_gives_dealer_14_others_13():
    s = deal(seed=1)
    assert s.hand_counts()[s.dealer_seat] == 14
    assert sum(s.hand_counts().values()) == 53  # 14 + 13*3
    assert all(s.hand_counts()[seat] == 13 for seat in SEATS if seat != s.dealer_seat)


def test_charleston_order_and_joker_rule():
    steps = charleston_sequence()
    assert [s.direction for s in steps[:3]] == ["right", "across", "left"]
    jokers = [t for t in build_tile_set() if is_joker(t)]
    assert not can_pass_tile(jokers[0])
    assert validate_pass(jokers[:3])  # non-empty problems


def test_group_recognition():
    ts = build_tile_set()
    dots1 = [t for t in ts if t.identifier().startswith("dots_1_")]
    jokers = [t for t in ts if is_joker(t)]
    assert is_valid_group(dots1[:3])            # pung
    assert is_valid_group(dots1[:2])            # pair
    assert not is_valid_group([dots1[0], jokers[0]])  # pair can't use joker
    assert "Joker" in describe_group([dots1[0], jokers[0]])


def test_bot_turn_keeps_hand_size():
    s = deal(seed=3)
    hand = s.hands["South"]
    n = len(hand)
    bot_take_turn(hand, s.wall_remaining, level=2)
    assert len(hand) == n  # drew one, discarded one


def test_web_endpoints():
    app = create_app()
    c = app.test_client()
    assert c.get("/healthz").status_code == 200
    assert c.get("/").status_code == 200
    tiles = c.get("/api/tiles").get_json()
    assert tiles["count_unique"] == 35  # 27 suited + 4 winds + 3 dragons + 1 joker
    setup = c.get("/api/setup?seed=9").get_json()
    assert setup["dice"]["total"] == setup["dice"]["die1"] + setup["dice"]["die2"]
    char = c.get("/api/charleston").get_json()
    assert len(char["steps"]) == 7
    grp = c.post("/api/check-group", json={"tile_ids": ["dots_1_c0", "dots_1_c1", "dots_1_c2"]}).get_json()
    assert grp["valid"] is True
