(function () {
 "use strict";

 const curriculum = {
 meta: {
 app: "SuitUp",
 title: "Beginner Curriculum",
 version: "1.0.0",
 lastUpdated: "2026-07-04",
 audience: "Total beginners learning American Mah Jongg with a physical set and the SuitUp practice UI",
 teachingStyle: "guitarhero",
 notes: [
 "This curriculum is data-driven frontend content. Lessons should be rendered by the UI rather than hardcoded as HTML.",
 "SuitUp teaches beginner mechanics and original practice patterns. Practice patterns are teaching tools only.",
 "The real National Mah Jongg League (NMJL) card is not embedded in the app. The learner must use their own current NMJL card for real play.",
 "SuitUp does not reproduce copyrighted NMJL hand card content.",
 "Every lesson ends with a concrete action the learner can perform physically at the table or in the practice UI."
 ]
 },

 boundaries: {
 copyright: {
 nmjlCardEmbedded: false,
 statement:
 "SuitUp does not embed, reprint, or paraphrase the official NMJL card. Use your own current NMJL card when choosing a real hand to pursue."
 },
 practicePatterns: {
 areTeachingTools: true,
 statement:
 "SuitUp practice patterns are original teaching exercises for learning tile recognition, setup flow, group shapes, and turn mechanics. They are not official NMJL card hands."
 }
 },

 learningObjectives: [
 "Recognize the American Mah Jongg tile set and basic table equipment.",
 "Set up the mat, racks, dealer markers, and walls correctly.",
 "Choose dealer by wind draw without guessing or inventing rituals.",
 "Deal a beginner hand with the right sequence and orientation.",
 "Understand the Charleston as a tile-passing phase before normal play.",
 "Play a first legal turn: draw, evaluate, and discard.",
 "Identify exposures and know when jokers can and cannot be used.",
 "Use original practice patterns to learn mechanics while relying on a personal NMJL card for real game play."
 ],

 units: [
 {
 id: "unit-1-orientation-and-setup",
 number: 1,
 title: "Meet the Table",
 summary:
 "Start with the physical basics: what is in the set, where it goes, and how to make the table feel familiar instead of intimidating.",
 lessons: [
 {
 id: "lesson-1-1-what-you-have",
 number: 1,
 title: "What Comes in an American Mah Jongg Set",
 objective:
 "Identify the major parts of the set and understand that the full tile set contains 152 tiles.",
 doThisNow:
 "Open your set, place the racks in front of you, and separate the tiles into a loose face-down pile so you can begin spotting categories.",
 steps: [
 {
 number: 1,
 title: "See the whole game before learning moves",
 objective:
 "Reduce beginner overwhelm by naming the equipment before asking the learner to make decisions.",
 content:
 "An American Mah Jongg set includes tiles, racks, pushers, and usually dice and wind indicators or other dealer markers. The complete tile set contains 152 tiles."
 },
 {
 number: 2,
 title: "Know the major tile families",
 objective:
 "Recognize that the set is not random; it is grouped into repeatable families.",
 content:
 "The tile families are suits, winds, dragons, flowers, and jokers. The three suits are Dots, Bams, and Craks, numbered 1 through 9."
 },
 {
 number: 3,
 title: "Know the exact set totals",
 objective:
 "Anchor the learner in the real American Mah Jongg tile count.",
 content:
 "There are 108 suit tiles, 16 winds, 12 dragons, 8 flowers, and 8 jokers, for 152 tiles total."
 },
 {
 number: 4,
 title: "Treat recognition as the first skill",
 objective:
 "Make clear that naming tiles comes before strategy.",
 content:
 "Before you can choose a hand or discard intelligently, you need to be able to spot suit tiles, honors, flowers, and jokers quickly."
 }
 ]
 },
 {
 id: "lesson-1-2-mat-and-racks",
 number: 2,
 title: "Set the Mat and Place the Racks",
 objective:
 "Arrange a comfortable beginner table with a mat and four racks so the learner knows where everything belongs.",
 doThisNow:
 "Put your mahjong mat on the table, place four racks around it, and sit in one seat as if you are Player 1.",
 steps: [
 {
 number: 1,
 title: "Use the mat as your work surface",
 objective:
 "Give the learner a stable visual center for the game.",
 content:
 "Place the mat in the middle of the table. The mat is where the walls will be built and where discards will collect."
 },
 {
 number: 2,
 title: "Give each player a rack space",
 objective:
 "Show where each player's concealed tiles live.",
 content:
 "Set one rack on each side of the mat. Each player manages their own concealed tiles on the rack in front of them."
 },
 {
 number: 3,
 title: "Leave room for walls and discards",
 objective:
 "Prevent crowding before the first build.",
 content:
 "Do not push the racks too close to the center. You need enough open mat space to build four walls and later to place discards where everyone can see them."
 },
 {
 number: 4,
 title: "Make physical setup part of the lesson",
 objective:
 "Connect table layout to calm play.",
 content:
 "When the table feels organized, the rules feel easier. SuitUp treats setup as a real skill, not a formality."
 }
 ]
 },
 {
 id: "lesson-1-3-tile-recognition",
 number: 3,
 title: "Learn to Spot Suits, Honors, Flowers, and Jokers",
 objective:
 "Build confidence by sorting tiles into broad categories before worrying about hand choice.",
 doThisNow:
 "Pull out one example of a Dot, one Bam, one Crak, one wind, one dragon, one flower, and one joker, then line them up in front of your rack.",
 steps: [
 {
 number: 1,
 title: "Start broad, not detailed",
 objective:
 "Teach categories before fine distinctions.",
 content:
 "First learn the difference between suit tiles, honors, flowers, and jokers. You do not need advanced strategy yet."
 },
 {
 number: 2,
 title: "Recognize suit tiles",
 objective:
 "Identify numbered tiles by family.",
 content:
 "Dots, Bams, and Craks are the three numbered suits. Each suit contains numbers 1 through 9."
 },
 {
 number: 3,
 title: "Recognize honors",
 objective:
 "Separate winds and dragons from numbered suits.",
 content:
 "Winds are East, South, West, and North. Dragons are Red, Green, and White."
 },
 {
 number: 4,
 title: "Recognize special tiles",
 objective:
 "Name flowers and jokers on sight.",
 content:
 "Flowers are a distinct group of eight tiles. Jokers are special wild tiles, but they are restricted and cannot be used everywhere."
 }
 ]
 }
 ]
 },

 {
 id: "unit-2-build-the-table",
 number: 2,
 title: "Build the Hand Before the Hand",
 summary:
 "Learn the pre-play procedures that make an American Mah Jongg game begin correctly: choosing dealer, building walls, and dealing tiles.",
 lessons: [
 {
 id: "lesson-2-1-dealer-wind-draw",
 number: 1,
 title: "Choose Dealer by Wind Draw",
 objective:
 "Use a simple wind draw to assign seats and identify dealer before building the walls.",
 doThisNow:
 "Shuffle the four winds face down, draw one for each seat, and label the seats East, South, West, and North around the table.",
 steps: [
 {
 number: 1,
 title: "Use wind tiles to assign seats",
 objective:
 "Tie seat identity to the actual tile set.",
 content:
 "A beginner-friendly way to choose dealer is to shuffle the four wind tiles face down and draw one for each seat."
 },
 {
 number: 2,
 title: "Know what East means",
 objective:
 "Mark dealer clearly.",
 content:
 "The player who draws East is the dealer. The other players take South, West, and North."
 },
 {
 number: 3,
 title: "Seat everyone in wind order",
 objective:
 "Set a stable table orientation for play.",
 content:
 "Arrange the seats around the table as East, South, West, and North so players can follow passing and turn order more easily."
 },
 {
 number: 4,
 title: "Keep the dealer marker visible",
 objective:
 "Help the learner track who is East during the hand.",
 content:
 "Once East is identified, place a dealer marker or the East wind tile where everyone can see it."
 }
 ]
 },
 {
 id: "lesson-2-2-build-the-walls",
 number: 2,
 title: "Build the Walls",
 objective:
 "Construct the four walls correctly so the learner can start a real hand without improvising.",
 doThisNow:
 "Mix all the tiles face down, then build one wall in front of each player, two tiles high and nineteen stacks long.",
 steps: [
 {
 number: 1,
 title: "Start from a mixed center",
 objective:
 "Show how tiles move from the wash to the walls.",
 content:
 "Turn the tiles face down and mix them thoroughly in the center of the mat."
 },
 {
 number: 2,
 title: "Build one wall per player",
 objective:
 "Introduce the standard wall shape.",
 content:
 "Each player builds a wall in front of their rack."
 },
 {
 number: 3,
 title: "Use the correct dimensions",
 objective:
 "Teach exact physical structure.",
 content:
 "Each wall should be two tiles high and nineteen stacks long, using 38 tiles per wall."
 },
 {
 number: 4,
 title: "Push the walls into a square",
 objective:
 "Create the table's starting shape.",
 content:
 "After all four walls are built, push them together to form the square in the center of the mat."
 }
 ]
 },
 {
 id: "lesson-2-3-deal-the-tiles",
 number: 3,
 title: "Deal a Beginner Hand",
 objective:
 "Understand the deal as a sequence rather than a blur of table rituals.",
 doThisNow:
 "Perform one full practice deal with your tiles and racks, then count your own rack to make sure you received a starting hand.",
 steps: [
 {
 number: 1,
 title: "Treat the deal as a repeatable routine",
 objective:
 "Replace mystery with sequence.",
 content:
 "A good beginner goal is not speed. It is calm, repeatable setup that gives each player a proper starting hand."
 },
 {
 number: 2,
 title: "Work in chunks, not single tiles",
 objective:
 "Make the process easier to track physically.",
 content:
 "Deal in the table's usual rhythm so tiles move from the wall to each player's rack in a consistent order."
 },
 {
 number: 3,
 title: "Face your own tiles toward yourself",
 objective:
 "Introduce concealed information.",
 content:
 "Place your own tiles on your rack facing you. Other players should not see your concealed rack."
 },
 {
 number: 4,
 title: "Count before moving on",
 objective:
 "Teach self-checking.",
 content:
 "After the deal, count your rack before starting the hand. Beginners should pause and verify rather than pushing ahead confused."
 }
 ]
 }
 ]
 },

 {
 id: "unit-3-the-charleston",
 number: 3,
 title: "Learn the Charleston",
 summary:
 "The Charleston is a tile-passing phase that feels strange at first. SuitUp breaks it into clear, repeatable actions.",
 lessons: [
 {
 id: "lesson-3-1-charleston-purpose",
 number: 1,
 title: "What the Charleston Is For",
 objective:
 "Understand why tiles are passed before normal turns begin.",
 doThisNow:
 "Pick any three tiles from a sample rack and hold them aside as if you are preparing a Charleston pass.",
 steps: [
 {
 number: 1,
 title: "Know when it happens",
 objective:
 "Place the Charleston in the timeline of a hand.",
 content:
 "The Charleston happens after the deal and before ordinary draw-and-discard turns."
 },
 {
 number: 2,
 title: "Understand the goal",
 objective:
 "Connect passing to hand improvement.",
 content:
 "Players pass tiles they do not want in hopes of improving their starting direction before normal play begins."
 },
 {
 number: 3,
 title: "Use exactly three tiles per pass",
 objective:
 "Anchor the learner in the basic passing action.",
 content:
 "Each Charleston pass uses three tiles selected from your rack."
 },
 {
 number: 4,
 title: "Separate passing from discarding",
 objective:
 "Avoid a common beginner confusion.",
 content:
 "A Charleston pass is not a discard to the center. It is a private exchange of tiles during the pre-play phase."
 }
 ]
 },
 {
 id: "lesson-3-2-charleston-flow",
 number: 2,
 title: "Practice the Charleston Flow",
 objective:
 "Follow the passing sequence without getting lost.",
 doThisNow:
 "Run one dry Charleston with four mock racks or four piles of tiles, moving exactly three tiles at each pass and pausing after every exchange.",
 steps: [
 {
 number: 1,
 title: "Think in passes, not in the whole procedure",
 objective:
 "Make a complicated phase manageable.",
 content:
 "Beginners learn the Charleston faster when they focus on one pass at a time instead of trying to memorize the entire phase at once."
 },
 {
 number: 2,
 title: "Prepare the pass before moving tiles",
 objective:
 "Promote deliberate choices.",
 content:
 "Choose your three least useful tiles first, then place them together so you do not lose track of what you meant to pass."
 },
 {
 number: 3,
 title: "Exchange together, then re-rack",
 objective:
 "Keep the process organized.",
 content:
 "All players complete the pass, receive incoming tiles, and then re-sort their racks before the next pass begins."
 },
 {
 number: 4,
 title: "Use SuitUp to rehearse the rhythm",
 objective:
 "Connect physical practice with UI practice.",
 content:
 "In the practice UI, the Charleston is taught as a sequence of clear prompts so you can build confidence before trying it at full table speed."
 }
 ]
 },
 {
 id: "lesson-3-3-charleston-decision-making",
 number: 3,
 title: "What to Pass as a Beginner",
 objective:
 "Learn a safe beginner rule for deciding which tiles to pass.",
 doThisNow:
 "Look at a practice rack and choose three tiles that least fit the direction you want, then confirm your choice in the practice UI or set them aside physically.",
 steps: [
 {
 number: 1,
 title: "Do not chase everything",
 objective:
 "Reduce beginner indecision.",
 content:
 "You cannot keep every interesting tile. The Charleston helps you move away from scattered tiles toward a more focused plan."
 },
 {
 number: 2,
 title: "Protect obvious value",
 objective:
 "Teach what not to throw away too quickly.",
 content:
 "Keep pairs, helpful flowers, and tiles that clearly support the hand direction you think you may want."
 },
 {
 number: 3,
 title: "Pass isolated misfits",
 objective:
 "Give a concrete beginner heuristic.",
 content:
 "Single tiles that do not connect to your likely direction are good Charleston candidates."
 },
 {
 number: 4,
 title: "Stay flexible",
 objective:
 "Avoid overcommitting too soon.",
 content:
 "Early passing is about reducing clutter, not proving you already know your final hand."
 }
 ]
 }
 ]
 },

 {
 id: "unit-4-first-turn-and-table-language",
 number: 4,
 title: "Play the First Turn",
 summary:
 "Now the learner sees a live turn: draw, decide, discard, and understand what other players may call.",
 lessons: [
 {
 id: "lesson-4-1-first-turn",
 number: 1,
 title: "Your First Normal Turn",
 objective:
 "Execute the basic turn sequence after the Charleston ends.",
 doThisNow:
 "Take one tile from the live wall, add it to your rack, choose one tile to release, and place that discard where the table can see it.",
 steps: [
 {
 number: 1,
 title: "Draw before you decide",
 objective:
 "Teach turn order.",
 content:
 "A normal turn begins by taking a tile from the wall."
 },
 {
 number: 2,
 title: "Evaluate your direction",
 objective:
 "Link each draw to a hand plan.",
 content:
 "After drawing, ask whether the new tile helps the pattern or direction you are building toward."
 },
 {
 number: 3,
 title: "Discard one tile",
 objective:
 "Establish the draw-and-discard rhythm.",
 content:
 "If you are not declaring Mah Jongg, you end the turn by discarding one tile face up where the table can see it."
 },
 {
 number: 4,
 title: "Use calm, visible motions",
 objective:
 "Make table play readable.",
 content:
 "Beginners learn faster when each action is visible and separate: draw, pause, decide, discard."
 }
 ]
 },
 {
 id: "lesson-4-2-exposures",
 number: 2,
 title: "What an Exposure Is",
 objective:
 "Understand the difference between concealed tiles on the rack and exposed sets called to the table.",
 doThisNow:
 "Take three matching tiles from a practice rack and place them in front of the rack as a mock exposure so you can feel the difference between concealed and exposed groups.",
 steps: [
 {
 number: 1,
 title: "Define the term",
 objective:
 "Teach table vocabulary in plain language.",
 content:
 "An exposure is a set of tiles moved out from the rack and shown on the table."
 },
 {
 number: 2,
 title: "Know why exposures matter",
 objective:
 "Connect exposures to game state.",
 content:
 "Once tiles are exposed, the table can see part of what you are building. This changes both your own options and what other players know."
 },
 {
 number: 3,
 title: "Separate exposure from discard",
 objective:
 "Prevent another common beginner mix-up.",
 content:
 "A discard is a single tile released to the center area. An exposure is a claimed set displayed in front of a rack."
 },
 {
 number: 4,
 title: "Use practice first",
 objective:
 "Reinforce confidence through repetition.",
 content:
 "SuitUp lets you practice the physical meaning of exposures before expecting strategic timing."
 }
 ]
 },
 {
 id: "lesson-4-3-jokers",
 number: 3,
 title: "How Jokers Work for Beginners",
 objective:
 "Teach the learner that jokers are powerful but restricted and cannot be used anywhere they like.",
 doThisNow:
 "Look at one sample group in the practice UI and decide whether a joker is legal in that group; then swap a physical joker into a matching practice set to test your understanding.",
 steps: [
 {
 number: 1,
 title: "Start with the plain-language rule",
 objective:
 "Give the learner a usable first principle.",
 content:
 "A joker is a wild tile, but it is not a free substitute for every missing tile in every situation."
 },
 {
 number: 2,
 title: "Use jokers only where allowed",
 objective:
 "Teach restriction rather than fantasy play.",
 content:
 "Jokers are allowed only in certain kinds of groups. SuitUp teaches this as a legality check, not as guesswork."
 },
 {
 number: 3,
 title: "Do not treat pairs as joker spaces",
 objective:
 "Prevent a frequent beginner error.",
 content:
 "Beginners should not assume a joker can fill any pair they are missing. Check the group type and the rules being taught by the practice scenario."
 },
 {
 number: 4,
 title: "Use the UI for legal-or-illegal drills",
 objective:
 "Convert a tricky rule into repeated recognition practice.",
 content:
 "SuitUp practice prompts ask you to judge whether a joker belongs in a particular group so the restriction becomes intuitive."
 }
 ]
 }
 ]
 },

 {
 id: "unit-5-practice-patterns-and-real-play",
 number: 5,
 title: "Practice Safely, Then Play for Real",
 summary:
 "SuitUp uses original teaching patterns to train mechanics and pattern recognition. Real wins still require the learner's own NMJL card.",
 lessons: [
 {
 id: "lesson-5-1-practice-patterns",
 number: 1,
 title: "Use Practice Patterns as Training Wheels",
 objective:
 "Explain exactly what SuitUp practice patterns are and are not.",
 doThisNow:
 "Open the practice area, pick one beginner pattern, and say out loud which tile groups you are trying to collect before taking your next turn.",
 steps: [
 {
 number: 1,
 title: "State the boundary clearly",
 objective:
 "Prevent confusion between teaching content and official hand cards.",
 content:
 "SuitUp practice patterns are original teaching tools created for beginner drills. They are not official NMJL hands."
 },
 {
 number: 2,
 title: "Know why they exist",
 objective:
 "Show the learner what problem the patterns solve.",
 content:
 "Practice patterns give beginners something concrete to build toward while learning tile groups, exposures, and discard choices."
 },
 {
 number: 3,
 title: "Use them to learn structure",
 objective:
 "Keep attention on transferable skills.",
 content:
 "The point is to learn shape vocabulary such as pairs, pungs, kongs, honor groups, and suit discipline without copying a copyrighted hand card."
 },
 {
 number: 4,
 title: "Say the disclaimer every time real play comes up",
 objective:
 "Protect the boundary between practice and real NMJL play.",
 content:
 "When you play a real game, you must use your own current NMJL card to choose and verify a legal winning hand."
 }
 ]
 },
 {
 id: "lesson-5-2-from-practice-to-card",
 number: 2,
 title: "Move from Practice Patterns to Your Own NMJL Card",
 objective:
 "Teach the learner how to transition from beginner drills into real card-based play without expecting SuitUp to supply the card.",
 doThisNow:
 "Take out your own current NMJL card, choose one line you want to pursue in a real game, and compare your rack to that line after each practice turn.",
 steps: [
 {
 number: 1,
 title: "Bring your own card",
 objective:
 "Set the real-play requirement explicitly.",
 content:
 "SuitUp does not include the official NMJL card. For real play, you must have your own current card in front of you."
 },
 {
 number: 2,
 title: "Pick one target hand",
 objective:
 "Reduce decision load during a real hand.",
 content:
 "At beginner level, do not try to keep every possibility alive. Choose one target hand or one small cluster of related options from your card."
 },
 {
 number: 3,
 title: "Check your rack against the card repeatedly",
 objective:
 "Teach card use as an ongoing habit.",
 content:
 "After each draw, discard, pass, or exposure, ask whether your tiles still fit the exact hand you are aiming for."
 },
 {
 number: 4,
 title: "Remember the winning condition",
 objective:
 "Anchor the core rule of American Mah Jongg.",
 content:
 "You win only when your tiles match one exact hand from your current NMJL card."
 }
 ]
 },
 {
 id: "lesson-5-3-beginner-practice-loop",
 number: 3,
 title: "Your Repeatable Beginner Practice Loop",
 objective:
 "Give the learner a simple routine they can repeat until table actions feel natural.",
 doThisNow:
 "Run one full loop: set the table, choose dealer by wind draw, build the walls, deal, make one Charleston pass, play one turn in the UI, and then reset to do it again.",
 steps: [
 {
 number: 1,
 title: "Rehearse setup often",
 objective:
 "Make the opening procedures automatic.",
 content:
 "Beginners improve faster when setup becomes familiar: mat, racks, wind draw, walls, and deal."
 },
 {
 number: 2,
 title: "Use short repetitions",
 objective:
 "Prevent overload.",
 content:
 "You do not need to finish every full hand while learning. Practicing the first clean turns is valuable."
 },
 {
 number: 3,
 title: "Mix physical and UI practice",
 objective:
 "Bridge tabletop handling and on-screen feedback.",
 content:
 "Use your real tiles for the feel of the game, and use SuitUp for guided prompts, legality checks, and patient repetition."
 },
 {
 number: 4,
 title: "Graduate when the table feels calm",
 objective:
 "Define success in beginner terms.",
 content:
 "The first milestone is not advanced strategy. It is being able to set up, follow the Charleston, and play a clean turn without panic."
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