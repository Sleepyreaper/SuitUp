"use strict";
/* SuitUp tutorial content — contextual, beginner-first teaching for the live
   simulator. Grounded in current (2026) American Mah Jongg rules. This is the
   text the toggleable "Coach" overlay shows as the game state changes. */

window.SUITUP_TUTORIAL = {
  /* Short teaching note keyed by game phase/sub-phase. Shown in the Coach panel. */
  contextual: {
    charleston: {
      title: "The Charleston",
      body:
        "Before play, everyone passes tiles to reshape their hands. Pick exactly 3 " +
        "tiles you don't want and pass them. Order: RIGHT, then ACROSS, then LEFT. " +
        "One hard rule: you may NEVER pass a Joker.",
      terms: ["Charleston", "Joker"],
    },
    charleston_second: {
      title: "Second Charleston?",
      body:
        "The first Charleston (right/across/left) is done. The table may now do a " +
        "second one (left/across/right) — but ANY player can stop here. New players " +
        "often stop after the first. Your call.",
      terms: ["Charleston"],
    },
    "play:discard": {
      title: "Your turn — discard",
      body:
        "You're holding one extra tile. Get rid of your least useful tile (your " +
        "'deadwood', highlighted below). Click a tile, then Discard. Remember: you " +
        "must be back to 13 tiles when your turn ends.",
      terms: ["Discard", "Deadwood", "13-tile rule"],
    },
    "play:draw": {
      title: "Your turn — draw",
      body:
        "Draw the next tile from the wall, then you'll discard one. Watch for a tile " +
        "that completes a group — if it finishes your whole hand, you can declare " +
        "Mah Jongg!",
      terms: ["Wall", "Mah Jongg"],
    },
    "play:calls": {
      title: "A tile was discarded — you can CALL it",
      body:
        "Another player discarded a tile you can use. Call it to expose a Pung (3) or " +
        "Kong (4) — you must already hold the matching tiles. Or Pass and wait for " +
        "your turn. Calling shows part of your hand to everyone.",
      terms: ["Call", "Pung", "Kong", "Expose"],
    },
    "play:watch": {
      title: "Opponents are playing",
      body:
        "The bots draw and discard in turn (play goes to the RIGHT). Watch the discards " +
        "— they tell you what others don't want. Your turn is coming up.",
      terms: ["Discard"],
    },
    hand_over: {
      title: "Hand over",
      body:
        "This hand is finished. Review who won and how they scored, then deal the next " +
        "hand. The dealer rotates to the next seat.",
      terms: ["Mah Jongg", "Wall game"],
    },
    game_over: {
      title: "Game over",
      body: "Someone reached the target score. Start a new game to play again — " +
            "bump the AI level once you're comfortable.",
      terms: [],
    },
  },

  /* Glossary of the terms a JCC beginner needs. Click a term to see this. */
  glossary: {
    "Charleston": "The pre-game tile-passing ritual: pass 3 tiles right, across, then " +
      "left (mandatory), optionally a second round left/across/right, then an optional " +
      "courtesy swap across. Never pass a Joker.",
    "Pung": "Three identical tiles (e.g. three 5-Dots). A joker may stand in for one.",
    "Kong": "Four identical tiles. A joker may stand in. In American Mah Jongg a kong " +
      "counts as its full 4 tiles toward your 14 — there's no bonus draw.",
    "Quint": "Five identical tiles — only possible using a joker (there are only four " +
      "of each tile), except a quint of Flowers.",
    "Pair": "Two identical tiles. A joker can NEVER be used in a pair.",
    "Joker": "A wild tile. Legal ONLY in groups of 3+ (pung/kong/quint/sextet), NEVER " +
      "in a pair or single. You may swap your real tile for a joker sitting in any " +
      "exposure (joker exchange). Never pass a joker in the Charleston.",
    "Soap": "The White Dragon. It's used as the ZERO (e.g. the 0's in a 2026 hand).",
    "Deadwood": "Tiles that don't help the hand you're building — your best discards.",
    "Call": "Taking another player's discard (instead of drawing) to complete and " +
      "EXPOSE a group. You must already hold the matching tiles. You can't call for a " +
      "pair or single — only groups of 3+ (or the final tile for Mah Jongg).",
    "Expose": "Placing a completed called group face-up on your rack for all to see. " +
      "It commits you toward hands that contain that group.",
    "Mah Jongg": "Winning — completing all 14 tiles of a legal hand. Call it out loud.",
    "Wall": "The face-down tiles you draw from. When it runs out with no winner, the " +
      "hand is a 'wall game' (a draw) and no one scores.",
    "Wall game": "A drawn hand: the wall ran out before anyone made Mah Jongg. No score.",
    "13-tile rule": "You must hold exactly 13 tiles at all times — 14 only as the " +
      "opening dealer, mid-pick before discarding, and when you declare Mah Jongg. A " +
      "wrong count makes your hand 'dead'.",
    "Honor tiles": "The Winds (E/S/W/N) and Dragons (Red/Green/White). Not part of any " +
      "number suit.",
    "Flower": "A bonus tile (there are 8, all interchangeable). Flowers belong to no suit " +
      "and are used only in hands that call for them. You may NEVER pass a Flower in the " +
      "Charleston, and a Flower can't help a hand that doesn't use Flowers.",
  },

  /* When a move is rejected, the Coach explains WHY (matched on the error text). */
  illegal: [
    { match: "Jokers and Flowers",
      why: "Jokers and Flowers are special — they can never be passed in the Charleston. " +
           "Keep them; pass ordinary tiles you don't need instead." },
    { match: "exactly 3",
      why: "Every Charleston pass is exactly 3 tiles — no more, no less. Click three tiles, " +
           "then pass." },
    { match: "does not complete",
      why: "Your 14 tiles don't yet match any hand you can win with. Keep drawing and " +
           "building toward the target in the Coach panel." },
    { match: "real tile that matches",
      why: "To redeem a Joker you must give the EXACT tile it's standing in for (same " +
           "number/suit or honor). You don't hold that tile." },
    { match: "redeem a joker on your turn",
      why: "You can only redeem a Joker on your own turn, before or after you draw." },
    { match: "call",
      why: "You can only call a discard to complete a Pung or Kong you already hold most " +
           "of — or the final tile for Mah Jongg. You can't call for a pair or single." },
    { match: "not yours to draw",
      why: "It isn't your turn yet. Watch the opponents draw and discard — your turn is " +
           "coming around." },
    { match: "cannot discard",
      why: "You can only discard right after you've drawn, on your turn, and you must end " +
           "the turn holding 13 tiles." },
  ],

  /* One-time 'read me first' shown when you open Play for the first time. */
  intro: {
    title: "How this simulator teaches you",
    points: [
      "You play the East seat against 3 bots. Learn by doing a real hand.",
      "The Coach panel (right) explains what's happening and every term as you go. " +
        "Toggle it off once it feels natural.",
      "Winning = completing one of SuitUp's original 14-tile practice hands. At the " +
        "real table you'll use the 2026 NMJL card instead — the mechanics are identical.",
      "American Mah Jongg has NO runs (no 1-2-3). Every group is identical tiles.",
    ],
  },
};
