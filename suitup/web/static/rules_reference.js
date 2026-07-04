(function () {
 const rulesReference = {
 version: "v1",
 title: "SuitUp Rules Reference",
 audience: "beginner",
 last_updated: "2026-07-04",
 disclaimer:
 "This reference teaches American Mah Jongg mechanics for beginners using original SuitUp teaching materials. It does not reproduce National Mah Jongg League (NMJL) card text. SuitUp practice patterns are teaching-only patterns, not the real NMJL card.",
 sections: [
 {
 id: "tile_set",
 order: 1,
 title: "Tile set",
 summary: "A standard American Mah Jongg set for SuitUp contains 152 tiles.",
 facts: [
 {
 label: "Suits",
 value: "Dots (Circles), Bams (Bamboo), and Craks (Characters), numbered 1 through 9, four of each tile."
 },
 {
 label: "Suit tile total",
 value: "108 tiles."
 },
 {
 label: "Winds",
 value: "East, South, West, North; four of each."
 },
 {
 label: "Wind total",
 value: "16 tiles."
 },
 {
 label: "Dragons",
 value: "Red, Green, White; four of each."
 },
 {
 label: "Dragon total",
 value: "12 tiles."
 },
 {
 label: "Flowers",
 value: "8 tiles."
 },
 {
 label: "Jokers",
 value: "8 tiles."
 },
 {
 label: "Grand total",
 value: "152 tiles."
 }
 ],
 beginner_notes: [
 "If your first reaction is 'these all look the same,' that is normal.",
 "Start by separating suits, winds, dragons, flowers, and jokers before you worry about strategy."
 ]
 },
 {
 id: "table_setup",
 order: 2,
 title: "Table setup",
 summary: "SuitUp teaches a physical setup that helps a beginner orient the tiles before play starts.",
 facts: [
 {
 label: "Mat",
 value: "Place the mat centered on the table."
 },
 {
 label: "Racks",
 value: "Use one rack per player. Keep matching pushers nearby if your set includes them."
 },
 {
 label: "Seats",
 value: "Players sit as East, South, West, and North."
 },
 {
 label: "Open center",
 value: "Keep the center clear for the wall square."
 }
 ],
 beginner_notes: [
 "Neat physical setup reduces confusion later.",
 "A clean center area makes wall building and dealing easier to follow."
 ]
 },
 {
 id: "dealer_selection",
 order: 3,
 title: "Dealer selection",
 summary: "SuitUp teaches dealer selection by East draw.",
 facts: [
 {
 label: "Preparation",
 value: "Mix the tiles face down."
 },
 {
 label: "Draw",
 value: "Each player draws one tile."
 },
 {
 label: "Dealer rule",
 value: "The player who draws East becomes the dealer."
 },
 {
 label: "Seat rule",
 value: "The dealer takes the East seat."
 }
 ],
 beginner_notes: [
 "This is an easy ritual for learning that seats matter and East matters.",
 "Say the seat order around the table until it feels natural."
 ]
 },
 {
 id: "walls",
 order: 4,
 title: "Walls",
 summary: "Each player builds part of the square from which the game is dealt and played.",
 facts: [
 {
 label: "Per-player wall",
 value: "19 tiles long and 2 tiles high."
 },
 {
 label: "Total structure",
 value: "Four walls form a square."
 },
 {
 label: "Why the count works",
 value: "Four walls of 19 stacks, with 2 tiles per stack, use all 152 tiles."
 }
 ],
 beginner_notes: [
 "Build carefully first. Speed can come later.",
 "Straight walls make the rest of the hand easier to manage."
 ]
 },
 {
 id: "dealing",
 order: 5,
 title: "Dealing",
 summary: "Dealing turns the wall square into the starting hand from which the Charleston and normal play begin.",
 facts: [
 {
 label: "Purpose",
 value: "Players receive starting tiles from the walls before normal turns begin."
 },
 {
 label: "Learning approach",
 value: "SuitUp teaches the dealing sequence as a series of small visual steps rather than as a memorized block of table ritual."
 },
 {
 label: "Hand-building goal",
 value: "The game revolves around building a 14-tile hand shape."
 }
 ],
 beginner_notes: [
 "At first, focus on sequence and calm handling, not speed.",
 "If you lose your place during the deal, stop and re-orient before continuing."
 ]
 },
 {
 id: "charleston",
 order: 6,
 title: "Charleston",
 summary: "The Charleston is the tile-passing sequence that happens after the initial deal and before ordinary play.",
 facts: [
 {
 label: "When it happens",
 value: "After the initial deal and before normal table turns."
 },
 {
 label: "What it does",
 value: "Lets players pass tiles and reshape their starting hands."
 },
 {
 label: "Teaching focus",
 value: "SuitUp emphasizes following the pass order correctly and noticing how the hand becomes more organized."
 }
 ],
 beginner_notes: [
 "Your first goal is procedural accuracy: pass correctly and receive correctly.",
 "You do not need advanced passing strategy on your first day."
 ]
 },
 {
 id: "groups_and_hand_structure",
 order: 7,
 title: "Groups and hand structure",
 summary: "SuitUp teaches hand reading through original practice patterns built from visible tile groups.",
 facts: [
 {
 label: "Pair",
 value: "Two matching tiles."
 },
 {
 label: "Pung",
 value: "Three matching tiles."
 },
 {
 label: "Kong",
 value: "Four matching tiles."
 },
 {
 label: "Quint",
 value: "Five matching tiles (always needs at least one joker, since there are only four of each tile — except Flowers)."
 },
 {
 label: "No runs / sequences",
 value: "American Mah Jongg has NO runs. You never make a 1-2-3. Every group is IDENTICAL tiles. 'Consecutive Run' hands on the card use consecutive numbers (e.g. 111 222 3333), but each number is still its own matching group."
 },
 {
 label: "Pattern idea",
 value: "A hand is exactly 14 tiles that match ONE line on the current card — read as groups, not loose tiles."
 }
 ],
 beginner_notes: [
 "Reading a hand gets easier when you stop seeing 14 separate tiles and start seeing possible groups.",
 "The #1 beginner mistake from other mahjong: trying to make a 1-2-3. There are no sequences here."
 ]
 },
 {
 id: "jokers",
 order: 8,
 title: "Jokers",
 summary: "Jokers are wild substitutes in bigger groups, but they are banned in singles and pairs.",
 facts: [
 {
 label: "Count",
 value: "8 jokers in the set."
 },
 {
 label: "Where jokers ARE allowed",
 value: "Only in groups of 3 or more of the same tile: Pungs (3), Kongs (4), Quints (5), and Sextets (6). A joker stands in for the tile that group needs."
 },
 {
 label: "Where jokers are NEVER allowed",
 value: "Never in a Pair, never as a Single. So year hands (e.g. the 2026 digits), NEWS wind singles, and any Singles-and-Pairs hand cannot use jokers at all."
 },
 {
 label: "Joker exchange (redemption)",
 value: "If any player's EXPOSED group contains a joker, and you hold the real tile it stands for, you may swap your real tile for that joker on your turn — even from an opponent's exposure. Jokers are valuable; get them back when you can."
 },
 {
 label: "Never pass a joker",
 value: "A joker may never be passed during the Charleston."
 }
 ],
 beginner_notes: [
 "A joker is powerful but not universal — it cannot help a pair, a single, or a year/NEWS hand.",
 "Grabbing a joker back off an exposure with your natural tile is a classic advanced move worth learning."
 ]
 },
 {
 id: "reading_the_card",
 order: 12,
 title: "Reading the card (colors, soap, dragons)",
 summary: "The card's colors and symbols are instructions — learn to read them before you sit down.",
 facts: [
 {
 label: "Colors mean suits",
 value: "A hand printed in ONE color = all one suit. TWO colors = two different suits. THREE colors = three different suits. The actual color (red/blue/green) does NOT force a specific suit — it just tells you how many suits and which groups share one."
 },
 {
 label: "Soap = zero",
 value: "The White Dragon is called 'Soap' and is used as the ZERO — e.g. in a 2026 hand the 0's are Soaps."
 },
 {
 label: "Matching dragons",
 value: "Craks match the Red Dragon, Bams match the Green Dragon, Dots match the White Dragon (Soap). Some hands want matching dragons, others want opposite — read carefully."
 },
 {
 label: "Flowers",
 value: "Flowers belong to no suit and are used wherever the card prints an 'F'."
 },
 {
 label: "Hand value",
 value: "Each hand has a number next to it (its point value). Harder hands are worth more. Concealed-only hands are marked with a 'C'."
 }
 ],
 beginner_notes: [
 "Turn the card over — joker rules and color/suit guidance are printed on the back.",
 "You MUST build a hand that appears on the CURRENT year's card. Nothing else counts."
 ]
 },
 {
 id: "calling",
 order: 13,
 title: "Calling a discard (exposing)",
 summary: "You can grab another player's discard to complete a group — but you must expose it and it must fit a card hand.",
 facts: [
 {
 label: "How to call",
 value: "The instant a tile is discarded, before the next player draws, say 'Call' or 'Take'. Take the tile and expose the completed group (Pung/Kong/etc.) face-up on top of your rack, then discard."
 },
 {
 label: "You need the naturals",
 value: "To call for a Pung you must already hold 2 matching tiles (3 for a Kong). You expose those plus the called tile."
 },
 {
 label: "No calling for pairs/singles",
 value: "You cannot call a discard to make a Pair or a Single — only groups of 3+. The one exception: calling the final tile for Mah Jongg."
 },
 {
 label: "Turn jumps to you",
 value: "After you call and discard, play continues to YOUR right — players between the discarder and you are skipped for that go-around."
 }
 ],
 beginner_notes: [
 "Exposing commits you: everyone now sees part of your hand, and it locks you toward hands that fit that group.",
 "When in doubt on your first day, just draw and discard — calling is optional."
 ]
 },
 {
 id: "count_and_dead",
 order: 14,
 title: "The 13-tile rule and going dead",
 summary: "You must hold exactly 13 tiles at all times, except for a few specific moments.",
 facts: [
 {
 label: "Always 13",
 value: "Between turns every player has exactly 13 tiles. You only hold 14 as East at the very start, at the moment you have picked but not yet discarded, and when you declare Mah Jongg."
 },
 {
 label: "Wrong count = dead",
 value: "If you miscount and have more or fewer than 13, your hand is declared DEAD and you're out of that hand (though play continues around you)."
 },
 {
 label: "Impossible exposure = dead",
 value: "If your exposures can no longer match ANY hand on the card, your hand is also dead."
 },
 {
 label: "Wall game",
 value: "If the wall runs out before anyone makes Mah Jongg, the hand is a draw ('wall game') — no one scores."
 }
 ],
 beginner_notes: [
 "Count your tiles every single turn until it's automatic. Wrong count is the most common beginner penalty.",
 "A dead hand isn't the end of the world — you can still watch and learn the rest of the hand."
 ]
 },
 {
 id: "the_2026_card",
 order: 15,
 title: "The 2026 card (what to bring to the JCC)",
 summary: "American Mah Jongg is played from the National Mah Jongg League card, which changes every year.",
 facts: [
 {
 label: "Buy the current card",
 value: "Get the 2026 NMJL card (nationalmahjonggleague.org) — standard or large-print. Everyone at the table plays from the same year's card."
 },
 {
 label: "Sections you'll see in 2026",
 value: "Common categories include Year (2026), 2468, Any Like Numbers, Quints, Consecutive Run, 13579, Winds-Dragons, 369, and Singles & Pairs. The exact hands change yearly."
 },
 {
 label: "Jokers on year/NEWS hands",
 value: "The 2026 digits and NEWS (N-E-W-S winds) are played as singles/pairs — no jokers. This trips up newcomers every year."
 },
 {
 label: "SuitUp's boundary",
 value: "SuitUp teaches the MECHANICS and terminology with original practice hands. It does not reproduce the copyrighted card — bring your own 2026 card for real scored play."
 }
 ],
 beginner_notes: [
 "Great references: the printable 'Modern American Mah-Jongg' rules, Sloperama's 2026 Card FAQ, modernmahjong.com, and mahjong4friends.com.",
 "Before the JCC: know the tiles, the Charleston order, jokers (3+ only, exchange), calling, and the 13-tile rule. The card teaches the hands."
 ]
 },
 {
 id: "normal_turn",
 order: 9,
 title: "Normal turn flow",
 summary: "After setup and the Charleston, play settles into a draw-and-discard rhythm.",
 facts: [
 {
 label: "Draw",
 value: "Take a tile and evaluate whether it improves your hand."
 },
 {
 label: "Decision",
 value: "Keep tiles that support your hand plan and release tiles that do not."
 },
 {
 label: "Discard",
 value: "A discard removes the least useful tile from your current plan."
 }
 ],
 beginner_notes: [
 "A beginner does not need perfect strategy; a clear plan is enough.",
 "Useful question: 'What am I building toward?'"
 ]
 },
 {
 id: "practice_patterns_boundary",
 order: 10,
 title: "Teaching-only patterns versus the real NMJL card",
 summary: "SuitUp teaches with original practice patterns and does not reproduce NMJL card text.",
 facts: [
 {
 label: "What SuitUp includes",
 value: "Original beginner teaching patterns that explain hand structure, suit relationships, groups, and joker mechanics."
 },
 {
 label: "What SuitUp does not include",
 value: "The copyrighted text of the current National Mah Jongg League card."
 },
 {
 label: "Real-life play",
 value: "For official real-life scored play, use your own legally obtained current NMJL card."
 }
 ],
 beginner_notes: [
 "Think of SuitUp patterns as training wheels for mechanics.",
 "The goal is to make the real card less intimidating later, not to replace it."
 ]
 },
 {
 id: "beginner_table_play",
 order: 11,
 title: "Beginning table play",
 summary: "The first goal of live practice is to complete legal, understandable turns against patient opposition.",
 facts: [
 {
 label: "Best starting mode",
 value: "Start on the easiest AI level."
 },
 {
 label: "Focus",
 value: "Follow turn order, identify groups, and make intentional discards."
 },
 {
 label: "Progress marker",
 value: "Moving from random tile handling to visible hand-shaping is early success."
 }
 ],
 beginner_notes: [
 "Surviving the procedure is step one.",
 "Planning your hand on purpose is step two."
 ]
 }
 ],
 quick_reference: {
 checklist_title: "First practice hand checklist",
 items: [
 "Confirm the set has 152 tiles.",
 "Set out the mat and four racks.",
 "Mix tiles face down.",
 "Draw for East to choose the dealer.",
 "Seat players as East, South, West, and North.",
 "Build four walls, each 19 tiles long and 2 tiles high.",
 "Work through the initial deal.",
 "Complete the Charleston as prompted.",
 "Read your hand as possible groups, not just loose tiles.",
 "Begin normal draw-and-discard play."
 ]
 }
 };

 window.SUITUP_RULES_REFERENCE = rulesReference;
})();