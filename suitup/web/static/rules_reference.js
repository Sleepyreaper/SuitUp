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
 value: "Five matching tiles."
 },
 {
 label: "Run",
 value: "Three consecutive numbers in the same suit."
 },
 {
 label: "Pattern idea",
 value: "Teaching patterns specify a group recipe, such as a pair plus larger groups."
 }
 ],
 beginner_notes: [
 "Reading a hand gets easier when you stop seeing 14 separate tiles and start seeing possible groups.",
 "Runs require both order and one suit; matching groups depend on duplicates."
 ]
 },
 {
 id: "jokers",
 order: 8,
 title: "Jokers",
 summary: "Jokers are flexible substitute tiles, but they are not legal everywhere.",
 facts: [
 {
 label: "Count",
 value: "8 jokers in the set."
 },
 {
 label: "Teaching role",
 value: "SuitUp teaches jokers as substitute tiles that can complete certain groups."
 },
 {
 label: "Important limit",
 value: "Jokers are powerful but restricted; beginners should not treat them as universal replacements."
 }
 ],
 beginner_notes: [
 "A joker is useful, but it is not magic.",
 "If you are unsure whether a joker use is legal in a teaching hand, rely on the app's guided prompt."
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