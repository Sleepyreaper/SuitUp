(function () {
 const curriculum = {
 version: "v1",
 title: "SuitUp Beginner Curriculum",
 audience: "total_beginner",
 last_updated: "2026-07-04",
 teaching_style: "patient_concrete_step_by_step",
 disclaimer:
 "SuitUp teaches American Mah Jongg mechanics for beginners using original teaching materials. It does not reproduce National Mah Jongg League (NMJL) card text. Practice patterns in this app are teaching-only patterns, not the real NMJL card.",
 units: [
 {
 id: "unit_1_orientation",
 order: 1,
 title: "Meet the Set",
 objective: "Learn what comes in an American Mah Jongg set so the tiles stop feeling mysterious.",
 lessons: [
 {
 id: "lesson_tile_families",
 order: 1,
 title: "Tile families and counts",
 objective: "Identify the five big tile groups and know the full 152-tile inventory.",
 steps: [
 {
 number: 1,
 title: "Start with the three suits",
 body: "American Mah Jongg uses three numbered suits: Dots, Bams, and Craks. Each suit has tiles numbered 1 through 9, and there are four copies of each tile. That makes 108 suit tiles total.",
 learner_action: "Sort your suit tiles into three families: Dots, Bams, and Craks."
 },
 {
 number: 2,
 title: "Find the winds",
 body: "The wind tiles are East, South, West, and North. There are four of each wind, for 16 wind tiles total.",
 learner_action: "Pull out one example of each wind and say the four seat names out loud: East, South, West, North."
 },
 {
 number: 3,
 title: "Find the dragons",
 body: "The dragon tiles are Red, Green, and White. There are four of each dragon, for 12 dragon tiles total.",
 learner_action: "Place the three dragon types in a row and label them for yourself: Red, Green, White."
 },
 {
 number: 4,
 title: "Set aside flowers and jokers",
 body: "A standard American Mah Jongg set also has 8 flowers and 8 jokers. Flowers are special tiles used in hands and for dealing. Jokers are flexible tiles, but they do not work everywhere.",
 learner_action: "Count your flowers to 8 and your jokers to 8, then place them in two separate small groups."
 },
 {
 number: 5,
 title: "Confirm the full inventory",
 body: "If you add 108 suit tiles, 16 winds, 12 dragons, 8 flowers, and 8 jokers, you get 152 tiles total. This full count helps you trust that your set is complete before you learn table procedure.",
 learner_action: "Do one full count or spot-check each family so you know your set reaches 152 tiles."
 }
 ]
 },
 {
 id: "lesson_tile_names",
 order: 2,
 title: "Names you will hear at the table",
 objective: "Get comfortable with beginner table vocabulary before play starts.",
 steps: [
 {
 number: 1,
 title: "Learn the suit nicknames",
 body: "You may hear Dots called Circles, Bams called Bamboo, and Craks called Characters. Different players use different habits, so it helps to recognize both names.",
 learner_action: "Point to each suit and say both names: Dots or Circles, Bams or Bamboo, Craks or Characters."
 },
 {
 number: 2,
 title: "Learn honors versus suits",
 body: "Suits are the numbered tiles. Winds and dragons are often called honors because they are not numbered suit tiles. Flowers and jokers are special tiles.",
 learner_action: "Make four piles labeled in your mind: suits, winds, dragons, special tiles."
 },
 {
 number: 3,
 title: "Notice what beginners confuse first",
 body: "At first, many beginners mix up Bams and Craks or forget that White Dragon is a dragon and not a blank tile. That is normal. The goal is recognition, not speed.",
 learner_action: "Pick the two tile types you confuse most and compare them side by side for one minute."
 }
 ]
 }
 ]
 },
 {
 id: "unit_2_table_setup",
 order: 2,
 title: "Set Up the Table",
 objective: "Learn the physical setup so you can turn a loose pile of tiles into a ready table.",
 lessons: [
 {
 id: "lesson_racks_and_mat",
 order: 1,
 title: "Racks, pushers, and the mat",
 objective: "Place the physical equipment in a way that supports easy learning and clean tile handling.",
 steps: [
 {
 number: 1,
 title: "Place the mat first",
 body: "Start with the mat centered on the table. The mat keeps tiles from sliding and gives the walls a clear surface.",
 learner_action: "Lay your mahjong mat flat and clear enough space for four sides of play."
 },
 {
 number: 2,
 title: "Place one rack at each side",
 body: "Each player uses a rack to hold concealed tiles. If your set includes pushers, keep each pusher with its matching rack.",
 learner_action: "Set four racks around the table, one on each side, with pushers nearby if you have them."
 },
 {
 number: 3,
 title: "Keep the center open",
 body: "The center space is where the walls will form a square. Beginners learn more easily when the center is uncluttered and every player's area is obvious.",
 learner_action: "Remove extra objects from the middle so the center is ready for walls."
 }
 ]
 },
 {
 id: "lesson_choose_seats_and_dealer",
 order: 2,
 title: "Choose seats and find East",
 objective: "Use the beginner East-draw method to assign the dealer and seat directions.",
 steps: [
 {
 number: 1,
 title: "Mix the tiles face down",
 body: "Before anyone sits as East, mix the tiles face down so the draw is random. This is part of the beginner procedure SuitUp teaches.",
 learner_action: "Turn the tiles face down and gently mix them together."
 },
 {
 number: 2,
 title: "Draw for East",
 body: "Each player draws a tile. In SuitUp's teaching flow, the player who draws East becomes the dealer.",
 learner_action: "Have each player draw one tile and check whether anyone drew East."
 },
 {
 number: 3,
 title: "Seat the dealer as East",
 body: "The player who drew East takes the East seat. The other players sit South, West, and North around the table.",
 learner_action: "Assign the East seat to the dealer and label the remaining seats South, West, and North."
 },
 {
 number: 4,
 title: "Understand why this matters",
 body: "Dealer selection is not just a ritual. It teaches that seats matter, East matters, and table actions will follow seat order.",
 learner_action: "Say the seat order clockwise so you can picture turn flow around the table."
 }
 ]
 },
 {
 id: "lesson_build_walls",
 order: 3,
 title: "Build the walls",
 objective: "Build the four walls correctly and understand why the wall shape matters.",
 steps: [
 {
 number: 1,
 title: "Build your own wall",
 body: "Each player builds one wall that is 19 tiles long and 2 tiles high. Together, the four walls use the full 152-tile set.",
 learner_action: "Stack your wall into 19 short stacks of 2 tiles each."
 },
 {
 number: 2,
 title: "Push the walls together",
 body: "The four walls form a square in the center of the mat. This square is the source for dealing and later drawing.",
 learner_action: "Move the four walls inward until they form a neat square."
 },
 {
 number: 3,
 title: "Check for a clean build",
 body: "A straight wall prevents confusion during the deal. Beginners should value neatness over speed.",
 learner_action: "Walk your eyes around the square and fix any leaning or broken stacks."
 }
 ]
 }
 ]
 },
 {
 id: "unit_3_deal_and_charleston",
 order: 3,
 title: "Deal the Hand and Complete the Charleston",
 objective: "Learn the pre-play procedure that turns walls into a real starting hand.",
 lessons: [
 {
 id: "lesson_dealing_overview",
 order: 1,
 title: "What dealing is trying to accomplish",
 objective: "Understand the goal of the deal before memorizing small motions.",
 steps: [
 {
 number: 1,
 title: "Know the target hand size",
 body: "American Mah Jongg play revolves around building a 14-tile hand, but players do not all begin with the same count in the same moment. The dealer starts the hand in the dealer role, and all players receive tiles from the walls before normal turns begin.",
 learner_action: "Remind yourself that the deal exists to create a playable starting hand from the walls."
 },
 {
 number: 2,
 title: "Use a calm, repeatable routine",
 body: "Beginners learn dealing best when they treat it as a sequence of small physical tasks instead of one giant ritual. SuitUp teaches it step by step for that reason.",
 learner_action: "Take a breath and commit to learning the procedure one small motion at a time."
 }
 ]
 },
 {
 id: "lesson_charleston_basics",
 order: 2,
 title: "Charleston basics",
 objective: "Understand what the Charleston is and why beginners must learn it early.",
 steps: [
 {
 number: 1,
 title: "Define the Charleston",
 body: "The Charleston is the tile-passing sequence that happens after the initial deal and before normal table play. It is a signature part of American Mah Jongg and one of the first things that feels unfamiliar to a new player.",
 learner_action: "Say to yourself: the Charleston happens after the deal and before normal turns."
 },
 {
 number: 2,
 title: "Focus on the beginner goal",
 body: "At first, your only job is to follow the pass directions correctly and notice how your hand changes. You do not need advanced strategy yet.",
 learner_action: "Choose three tiles from a practice hand and imagine passing them away without worrying whether they are perfect choices."
 },
 {
 number: 3,
 title: "Treat passing as hand shaping",
 body: "The Charleston lets you improve your hand before full play starts. Even if you do not yet know the best pass, you can still learn the rhythm and purpose.",
 learner_action: "Look at a mixed group of tiles and identify one kind of tile you have too many of and might pass away."
 }
 ]
 },
 {
 id: "lesson_charleston_flow",
 order: 3,
 title: "Follow the Charleston flow",
 objective: "Practice the passing sequence as an ordered routine you can repeat at the table.",
 steps: [
 {
 number: 1,
 title: "Pass tiles in the required direction for the current pass",
 body: "During the Charleston, players pass tiles according to the table sequence currently in progress. SuitUp's interface teaches the order visually so the learner can follow the motion rather than memorize a wall of text all at once.",
 learner_action: "In practice mode, follow the prompted pass direction and move the shown number of tiles."
 },
 {
 number: 2,
 title: "Receive before reorganizing",
 body: "When tiles come in, place them into your hand and only then reorganize. Beginners often lose track when they sort too early or mix outgoing and incoming tiles.",
 learner_action: "After a pass, put the received tiles into your rack first and sort second."
 },
 {
 number: 3,
 title: "Use the Charleston to reduce chaos",
 body: "A good beginner result is simple: your hand looks less random than it did before. You might collect more matching tiles, move toward one suit idea, or improve a group shape.",
 learner_action: "After each practice pass, name one way your hand became more organized."
 }
 ]
 }
 ]
 },
 {
 id: "unit_4_first_turn_and_groups",
 order: 4,
 title: "Read Your Hand and Take the First Turn",
 objective: "Learn what you are building and how a normal turn begins.",
 lessons: [
 {
 id: "lesson_group_vocabulary",
 order: 1,
 title: "Pairs, pungs, kongs, quints, and runs",
 objective: "Recognize the building blocks used in SuitUp's teaching-only practice patterns.",
 steps: [
 {
 number: 1,
 title: "Start with a pair",
 body: "A pair is two matching tiles. In many beginner practice hands, exactly one pair anchors the hand structure.",
 learner_action: "Take two matching tiles from your set and place them together as a pair."
 },
 {
 number: 2,
 title: "Learn pungs and kongs",
 body: "A pung is three matching tiles. A kong is four matching tiles. These matching groups are easier for beginners to spot than abstract hand categories.",
 learner_action: "Build one sample pung and one sample kong from matching tiles."
 },
 {
 number: 3,
 title: "There are NO runs in American Mah Jongg",
 body: "Unlike Chinese or Japanese mahjong, American Mah Jongg has NO sequences or 'runs' — you never make a 1-2-3. Every group is a set of IDENTICAL tiles: a Pair (2), Pung (3), Kong (4), Quint (5), or Sextet (6). Some card hands (the 'Consecutive Run' category) do use consecutive NUMBERS — but each number is still its own matching group, e.g. 111 222 3333, never a 1-2-3.",
 learner_action: "Say it out loud: 'No sequences. Every group is the same tile.' Build 111 and 222 as two separate pungs."
 },
 {
 number: 4,
 title: "Learn quints as a special teaching case",
 body: "A quint is five matching tiles. SuitUp includes this as part of its original teaching system so the learner can understand bigger groups and joker substitution limits in a controlled way.",
 learner_action: "Look at five matching or nearly matching tiles and picture what a quint would require."
 }
 ]
 },
 {
 id: "lesson_jokers_beginner_use",
 order: 2,
 title: "How beginners should think about jokers",
 objective: "Understand that jokers are flexible but restricted, not magical wildcards for every situation.",
 steps: [
 {
 number: 1,
 title: "Jokers help in certain groups",
 body: "SuitUp teaches jokers as substitute tiles that can help complete some group types. They are powerful, but they are not allowed everywhere.",
 learner_action: "Set one joker next to a pung or kong and imagine it standing in for a missing tile."
 },
 {
 number: 2,
 title: "Do not treat jokers like pair tiles",
 body: "A key beginner lesson is that joker use has limits. If you think of jokers as universal replacements, you will make illegal ideas without realizing it.",
 learner_action: "Say out loud: a joker is flexible, but not for everything."
 },
 {
 number: 3,
 title: "Let the app teach the exact legal move",
 body: "SuitUp's guided practice and rules reference will tell you when a joker use is legal in the teaching system. You do not need to memorize every edge case before your first hand.",
 learner_action: "When a practice hand highlights a joker choice, pause and read why it is legal before you click."
 }
 ]
 },
 {
 id: "lesson_first_turn",
 order: 3,
 title: "Your first normal turn",
 objective: "Understand the draw-and-discard rhythm that drives table play after setup is complete.",
 steps: [
 {
 number: 1,
 title: "Draw, then evaluate",
 body: "Once the deal and Charleston are finished, normal table play begins with drawing and checking whether the new tile improves your hand.",
 learner_action: "Practice picking one tile from a wall and asking: does this help my hand shape?"
 },
 {
 number: 2,
 title: "Keep the hand moving toward a goal",
 body: "Beginners improve faster when they stop asking 'What is the perfect play?' and instead ask 'What am I building toward?' A hand becomes clearer when you keep tiles that serve one plan and release tiles that do not.",
 learner_action: "Choose one tile from a sample hand that clearly does not fit your current plan and mark it as your discard."
 },
 {
 number: 3,
 title: "Discard with purpose",
 body: "A discard is not random housekeeping. It is your way of removing a tile that helps less than the others. This is one of the first strategic habits SuitUp tries to build.",
 learner_action: "Place one chosen discard in front of your rack and explain to yourself why it was the easiest tile to let go."
 }
 ]
 }
 ]
 },
 {
 id: "unit_5_patterns_and_table_play",
 order: 5,
 title: "Practice Patterns and Beginning Table Play",
 objective: "Use original teaching-only patterns to learn hand reading without reproducing the real NMJL card.",
 lessons: [
 {
 id: "lesson_teaching_patterns_not_nmjl_card",
 order: 1,
 title: "Teaching patterns are not the NMJL card",
 objective: "Understand the copyright boundary and why SuitUp uses original practice patterns.",
 steps: [
 {
 number: 1,
 title: "Know what SuitUp is teaching",
 body: "SuitUp teaches hand structure, group vocabulary, joker limits, and practical turn flow using original practice patterns written for beginners.",
 learner_action: "Read the on-screen disclaimer and repeat the idea that these are teaching patterns."
 },
 {
 number: 2,
 title: "Know what SuitUp is not shipping",
 body: "SuitUp does not reproduce the text of the real National Mah Jongg League card. The official card is separate, copyrighted, and needed for real scored play outside this teaching app.",
 learner_action: "Make a mental note: learning mechanics here is different from reading an official NMJL card."
 },
 {
 number: 3,
 title: "Use practice patterns as training wheels",
 body: "The app's patterns are simpler and more explicit than a real annual card. That is intentional. They help a beginner see pairs, pungs, kongs, runs, honors, and suit relationships before dealing with official card complexity.",
 learner_action: "Open a practice pattern and identify the pair slot and the larger group slots."
 }
 ]
 },
 {
 id: "lesson_read_a_pattern",
 order: 2,
 title: "How to read a practice pattern",
 objective: "Translate a pattern description into a visible plan for your rack.",
 steps: [
 {
 number: 1,
 title: "Look for the group recipe",
 body: "A practice pattern tells you what kinds of groups make the hand, such as one pair plus several pungs, kongs, or runs. Start by reading the structure before you worry about exact tiles.",
 learner_action: "Take one practice pattern and list its required group types in order."
 },
 {
 number: 2,
 title: "Notice suit relationships",
 body: "Some pattern slots can be any suit, some must match a chosen suit, and some are honors. This teaches how hand logic works without copying the official card.",
 learner_action: "For one pattern, mark which groups are same-suit, any-suit, or honor-only."
 },
 {
 number: 3,
 title: "Match your rack to the pattern",
 body: "Once you know the recipe, compare your actual tiles against it. You are looking for progress, not perfection: completed groups, almost-groups, useful jokers, and likely discards.",
 learner_action: "Choose one practice pattern and count how many of its groups your current tiles already partially support."
 }
 ]
 },
 {
 id: "lesson_beginning_table_play",
 order: 3,
 title: "Beginning table play against the app",
 objective: "Move from lessons into full beginner practice with AI opponents.",
 steps: [
 {
 number: 1,
 title: "Start on easy difficulty",
 body: "Begin with the easiest AI level so you can focus on mechanics: reading your rack, making a legal discard, following turn order, and noticing group progress.",
 learner_action: "Launch a practice hand on the easiest AI setting."
 },
 {
 number: 2,
 title: "Use the lesson language during play",
 body: "When you draw or discard, talk yourself through what you see: pair, pung, kong, honor, joker, pass, keep, discard. Naming patterns helps new knowledge stick.",
 learner_action: "On your next practice turn, say one sentence out loud describing what the drawn tile does for your hand."
 },
 {
 number: 3,
 title: "Graduate from surviving to planning",
 body: "At first, success means keeping up with the procedure. Soon after, success means shaping a hand on purpose and spotting why one discard is better than another.",
 learner_action: "After a practice hand ends, name one moment where you changed your plan based on a tile you drew or passed."
 }
 ]
 }
 ]
 }
 ]
 };

 window.SUITUP_CURRICULUM = curriculum;
})();