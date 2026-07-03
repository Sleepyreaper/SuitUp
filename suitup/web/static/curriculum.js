(function () {
 "use strict";

 const curriculum = {
 version: "1.0.0",
 lastUpdated: "2026-07-03",
 audience: "Total beginners learning American Mah Jongg with a physical set and SuitUp's guided offline practice app",
 disclaimer: {
 summary: "SuitUp teaches American Mah Jongg mechanics and original teaching patterns for beginner practice.",
 important: [
 "SuitUp does not include, reproduce, scan, or recreate the copyrighted National Mah Jongg League (NMJL) annual card.",
 "SuitUp's practice patterns are original teaching content and are not official NMJL card hands.",
 "Use SuitUp to learn setup, tile handling, table flow, the Charleston, turn order, and beginner practice play.",
 "If you later play real NMJL card games, use a legally obtained current NMJL card outside the app."
 ]
 },
 units: [
 {
 id: "unit-1-getting-oriented",
 title: "Unit 1: Meet Your Set",
 summary: "Start with the physical pieces so nothing on the table feels mysterious.",
 lessons: [
 {
 id: "lesson-1-what-is-in-the-box",
 title: "Lesson 1: What You Have",
 objective: "Identify the main parts of an American Mah Jongg setup before trying to play.",
 steps: [
 {
 number: 1,
 title: "Lay out the gear",
 objective: "Recognize the basic equipment you will use in every practice session.",
 action: "Place your mat, four racks, pushers if your set has them, and all tile trays or stacks where you can reach them."
 },
 {
 number: 2,
 title: "Separate table tools from tiles",
 objective: "Avoid mixing racks and accessories into the tile count.",
 action: "Keep racks and pushers in one area and move only the tiles onto the mat or table surface."
 },
 {
 number: 3,
 title: "Notice the teaching boundary",
 objective: "Understand what SuitUp is teaching right now.",
 action: "In the browser, open the beginner curriculum intro and confirm that SuitUp teaches mechanics and original practice patterns, not the official NMJL card."
 }
 ]
 },
 {
 id: "lesson-2-identify-the-tiles",
 title: "Lesson 2: Identify the Tiles",
 objective: "Learn the tile families well enough to sort a real set without guessing.",
 steps: [
 {
 number: 1,
 title: "Find the three suits",
 objective: "Distinguish Dots, Bams, and Craks by appearance.",
 action: "Pull out one example of each suit from your set and place them in three separate columns on the mat."
 },
 {
 number: 2,
 title: "Find the honor tiles",
 objective: "Tell winds and dragons apart from numbered suit tiles.",
 action: "Make two more groups: one for winds and one for dragons, and compare their symbols with the labels shown in the browser."
 },
 {
 number: 3,
 title: "Find flowers and jokers",
 objective: "Recognize the special tiles that do not behave like regular suit tiles.",
 action: "Set all flowers in one row and all jokers in another row so you can visually spot them quickly later."
 },
 {
 number: 4,
 title: "Do a confidence check",
 objective: "Practice naming tiles aloud instead of silently hoping you are right.",
 action: "Pick up 10 random tiles, name each one out loud, then verify each answer against the browser tile guide."
 }
 ]
 },
 {
 id: "lesson-3-check-that-the-set-is-complete",
 title: "Lesson 3: Check That the Set Is Complete",
 objective: "Verify that your set has the standard 152 tiles before you build walls.",
 steps: [
 {
 number: 1,
 title: "Count the suits",
 objective: "Confirm the suit total is correct.",
 action: "Sort Dots, Bams, and Craks by number and verify there are four copies each of 1 through 9 in every suit."
 },
 {
 number: 2,
 title: "Count winds and dragons",
 objective: "Confirm the honor tile totals are correct.",
 action: "Verify there are four each of East, South, West, North, Red dragon, Green dragon, and White dragon."
 },
 {
 number: 3,
 title: "Count flowers and jokers",
 objective: "Finish the set check with the special tiles.",
 action: "Count 8 flowers and 8 jokers, then confirm in the browser that the full set total is 152 tiles."
 }
 ]
 }
 ]
 },
 {
 id: "unit-2-table-setup",
 title: "Unit 2: Set Up the Table",
 summary: "Get comfortable with the physical ritual before you worry about tactics.",
 lessons: [
 {
 id: "lesson-4-seat-the-players",
 title: "Lesson 4: Seats, Mat, and Racks",
 objective: "Prepare the table so every player has a clear position and rack space.",
 steps: [
 {
 number: 1,
 title: "Place the mat",
 objective: "Create a stable play area with room for walls and racks.",
 action: "Center your mahjong mat on the table and leave enough space around the edges for four racks."
 },
 {
 number: 2,
 title: "Place four racks",
 objective: "Understand where each player manages their concealed hand.",
 action: "Set one rack on each side of the mat, even if you are practicing alone."
 },
 {
 number: 3,
 title: "Name the seats",
 objective: "Start thinking in table positions, not just chair locations.",
 action: "In the browser, label the four player positions and then point to each matching seat around your table."
 }
 ]
 },
 {
 id: "lesson-5-mix-and-build-the-walls",
 title: "Lesson 5: Mix Tiles and Build the Walls",
 objective: "Learn the first big table action: washing tiles and building four walls.",
 steps: [
 {
 number: 1,
 title: "Wash the tiles",
 objective: "Randomize the set before building.",
 action: "Turn all tiles face down on the mat and mix them gently with both hands."
 },
 {
 number: 2,
 title: "Build your wall section",
 objective: "Make neat stacks that can join the full square wall.",
 action: "Practice making face-down stacks two tiles high, then line them up into a straight wall segment in front of one rack."
 },
 {
 number: 3,
 title: "Complete four walls",
 objective: "See the full table shape used before the deal.",
 action: "Build a square of four walls around the center of the mat, one wall in front of each rack."
 },
 {
 number: 4,
 title: "Do a physical reset",
 objective: "Build muscle memory instead of doing the setup only once.",
 action: "Knock down the walls and rebuild them one more time without looking away from the table."
 }
 ]
 }
 ]
 },
 {
 id: "unit-3-start-the-hand",
 title: "Unit 3: Start a Hand",
 summary: "Choose the dealer and learn the structure of dealing before live play begins.",
 lessons: [
 {
 id: "lesson-6-choose-the-dealer",
 title: "Lesson 6: Choose the Dealer",
 objective: "Understand who starts and why the dealer matters.",
 steps: [
 {
 number: 1,
 title: "Learn the dealer role",
 objective: "Understand that the dealer begins with one extra tile and starts play.",
 action: "In the browser, read the dealer note and then place a marker at one rack to represent the dealer seat."
 },
 {
 number: 2,
 title: "Practice a fair selection method",
 objective: "Use a simple beginner-safe way to choose the dealer for home practice.",
 action: "Choose a random method for your practice table, such as drawing seat markers or using the browser's seat assignment helper."
 },
 {
 number: 3,
 title: "Lock in the starting seat",
 objective: "Associate the dealer with a specific physical position before any tiles are dealt.",
 action: "Say out loud which rack is dealer, then point to the player on the dealer's right because that direction matters during passing."
 }
 ]
 },
 {
 id: "lesson-7-deal-the-tiles",
 title: "Lesson 7: Deal the Tiles",
 objective: "Carry out a full beginner deal without losing track of whose hand is whose.",
 steps: [
 {
 number: 1,
 title: "Understand the target hand sizes",
 objective: "Know what success looks like before you start dealing.",
 action: "In the browser, confirm that each player starts with 13 tiles and the dealer starts with 14."
 },
 {
 number: 2,
 title: "Distribute the tiles carefully",
 objective: "Practice dealing in an orderly way rather than rushing.",
 action: "Deal tiles around the table using the guided dealing view until every non-dealer rack has 13 tiles and the dealer rack has 14."
 },
 {
 number: 3,
 title: "Rack and sort the hand",
 objective: "Get used to arranging concealed tiles for reading and decision-making.",
 action: "Place each player's tiles on their rack, then sort your own rack by suits, honors, flowers, and jokers."
 },
 {
 number: 4,
 title: "Do a count check before continuing",
 objective: "Catch setup mistakes before the Charleston begins.",
 action: "Count each rack out loud and fix any mismatch before moving on."
 }
 ]
 }
 ]
 },
 {
 id: "unit-4-the-charleston",
 title: "Unit 4: Learn the Charleston",
 summary: "Practice the pass sequence slowly until it feels routine instead of intimidating.",
 lessons: [
 {
 id: "lesson-8-why-the-charleston-exists",
 title: "Lesson 8: What the Charleston Is",
 objective: "Understand the Charleston as a tile-passing phase that happens before regular play.",
 steps: [
 {
 number: 1,
 title: "Separate setup from play",
 objective: "Know that the Charleston happens after the deal and before normal draws and discards.",
 action: "In the browser, step through the hand timeline and identify the Charleston segment before the first live turn."
 },
 {
 number: 2,
 title: "Practice choosing passable tiles",
 objective: "Start identifying tiles you are less likely to keep.",
 action: "Look at a sample beginner hand and mark three tiles you would be comfortable passing away."
 }
 ]
 },
 {
 id: "lesson-9-first-charleston-pass-sequence",
 title: "Lesson 9: First Charleston Sequence",
 objective: "Learn the standard three-pass rhythm at a beginner pace.",
 steps: [
 {
 number: 1,
 title: "Pass three to the right",
 objective: "Execute the first pass in the correct direction.",
 action: "Select three tiles from your practice hand and move them to the player on your right, using either real tiles or the browser simulator."
 },
 {
 number: 2,
 title: "Pass three across",
 objective: "Continue the sequence without changing the number of tiles passed.",
 action: "Choose three tiles and pass them to the player across from you."
 },
 {
 number: 3,
 title: "Pass three to the left",
 objective: "Complete the first Charleston cycle in order.",
 action: "Choose three tiles and pass them to the player on your left, then recount your rack."
 }
 ]
 },
 {
 id: "lesson-10-second-charleston-and-courtesy",
 title: "Lesson 10: Second Charleston and Courtesy Pass",
 objective: "Finish a beginner Charleston sequence and understand the optional final exchange.",
 steps: [
 {
 number: 1,
 title: "Repeat the passing rhythm",
 objective: "Build comfort with the idea that Charleston passing is structured, not random.",
 action: "Run a second guided Charleston sequence in the browser and physically move tiles on your rack as prompted."
 },
 {
 number: 2,
 title: "Learn the courtesy pass",
 objective: "Understand the final optional exchange without overcomplicating your first hand.",
 action: "Practice offering up to three tiles to the player across from you and imagine accepting fewer if that is all they want to trade."
 },
 {
 number: 3,
 title: "Pause and re-read your hand",
 objective: "Notice how passing changes what you are building toward.",
 action: "Sort your rack again and say which groups now look most promising."
 }
 ]
 }
 ]
 },
 {
 id: "unit-5-from-groups-to-a-first-hand",
 title: "Unit 5: Build Toward a First Hand",
 summary: "Learn the shapes of a hand and start playing toward a concrete beginner target.",
 lessons: [
 {
 id: "lesson-11-groups-you-are-trying-to-make",
 title: "Lesson 11: Pairs, Pungs, Kongs, and Runs",
 objective: "Recognize the common group shapes used in SuitUp's beginner practice hands.",
 steps: [
 {
 number: 1,
 title: "Spot a pair",
 objective: "See the smallest matching group clearly.",
 action: "Find two identical tiles in your rack or in the browser and place them together as a pair."
 },
 {
 number: 2,
 title: "Spot a pung and a kong",
 objective: "Distinguish three-of-a-kind from four-of-a-kind.",
 action: "Make one three-tile matching group and one four-tile matching group with sample tiles in the browser."
 },
 {
 number: 3,
 title: "Spot a run",
 objective: "Understand that a run is an ordered same-suit sequence in SuitUp's teaching patterns.",
 action: "Arrange three consecutive suit tiles in order, such as 3-4-5 of the same suit, in the browser practice tray."
 }
 ]
 },
 {
 id: "lesson-12-jokers-beginners-need-the-boundary",
 title: "Lesson 12: Jokers for Beginners",
 objective: "Learn the basic beginner-safe joker rule boundary used in SuitUp practice.",
 steps: [
 {
 number: 1,
 title: "Treat jokers as special helpers",
 objective: "Understand that jokers are not ordinary suit tiles.",
 action: "Pull one joker from your set and place it beside a sample pung or kong to visualize substitution."
 },
 {
 number: 2,
 title: "Avoid overusing them too early",
 objective: "Build pattern-reading skill before leaning on substitutions.",
 action: "Play one browser drill with joker-free practice turned on so you can focus on reading real tile groups."
 }
 ]
 },
 {
 id: "lesson-13-practice-patterns-vs-real-card-play",
 title: "Lesson 13: Teaching Patterns Are Not the NMJL Card",
 objective: "Explicitly separate SuitUp's original teaching hands from real NMJL card play.",
 steps: [
 {
 number: 1,
 title: "Read the practice-pattern warning",
 objective: "Know exactly what the browser targets mean.",
 action: "Open the practice pattern screen and read the note that these are original SuitUp teaching patterns, not official NMJL hands."
 },
 {
 number: 2,
 title: "Compare the two modes mentally",
 objective: "Understand what you are practicing right now.",
 action: "Say out loud: 'I am practicing mechanics and group-building, not memorizing the official card.'"
 },
 {
 number: 3,
 title: "Choose a first teaching target",
 objective: "Start play with a manageable goal.",
 action: "Select one beginner practice pattern in the browser and pin it as your target for the next lesson."
 }
 ]
 }
 ]
 },
 {
 id: "unit-6-play-a-first-beginner-hand",
 title: "Unit 6: Play Your First Beginner Hand",
 summary: "Move from setup ritual into actual turns with a clear, achievable target.",
 lessons: [
 {
 id: "lesson-14-how-a-turn-works",
 title: "Lesson 14: Draw, Evaluate, Discard",
 objective: "Understand the rhythm of a normal turn once the Charleston is over.",
 steps: [
 {
 number: 1,
 title: "Start with the dealer",
 objective: "Recognize who begins live play.",
 action: "Place the dealer marker by the correct rack and begin with the dealer's turn in the browser simulator."
 },
 {
 number: 2,
 title: "Read the rack after each tile change",
 objective: "Build the habit of evaluating before discarding.",
 action: "Draw one tile in the simulator, sort your hand, and say whether it helps your chosen practice pattern."
 },
 {
 number: 3,
 title: "Make one discard on purpose",
 objective: "Avoid random discards by tying each discard to your target hand.",
 action: "Discard one tile that does not help your current teaching pattern and watch how the browser updates your progress."
 }
 ]
 },
 {
 id: "lesson-15-call-or-keep-going",
 title: "Lesson 15: Learn the Beginner Decision Loop",
 objective: "Practice the basic question that repeats throughout the hand: does this tile help enough to matter?",
 steps: [
 {
 number: 1,
 title: "Check every new tile against your target",
 objective: "Reduce overwhelm by using one simple filter.",
 action: "After each browser draw or discard event, ask whether the tile helps your chosen teaching pattern and click the matching prompt."
 },
 {
 number: 2,
 title: "Stay rack-focused",
 objective: "Keep the beginner goal on structure, not advanced table-reading.",
 action: "Ignore advanced opponent-reading for now and keep sorting your rack after every two or three turns."
 }
 ]
 },
 {
 id: "lesson-16-finish-a-first-playable-hand",
 title: "Lesson 16: Complete a First Practice Hand",
 objective: "Play all the way through a beginner-friendly hand target against the app.",
 steps: [
 {
 number: 1,
 title: "Choose your difficulty",
 objective: "Start with an opponent level that teaches instead of punishing.",
 action: "Select the easiest AI opponent in the browser for your first full hand."
 },
 {
 number: 2,
 title: "Play toward one teaching pattern",
 objective: "Experience a full hand with a concrete objective.",
 action: "Play until you either complete your chosen original practice pattern or the hand ends, using the in-browser pattern helper as needed."
 },
 {
 number: 3,
 title: "Review what happened",
 objective: "Turn one hand into a repeatable learning loop.",
 action: "At the end of the hand, name one group you built correctly and one discard you would change if you played it again."
 }
 ]
 }
 ]
 }
 ]
 };

 if (typeof window!== "undefined") {
 window.SUITUP_CURRICULUM = curriculum;
 }

 if (typeof module!== "undefined" && module.exports) {
 module.exports = curriculum;
 }
})();