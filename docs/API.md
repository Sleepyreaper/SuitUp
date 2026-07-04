# SuitUp Local API Contract

This document defines the offline-only JSON contracts for the SuitUp local practice app.

Base URL:
 http://localhost:8092

API style:
 REST-ish JSON over HTTP for a single-user local Flask app.

Versioning:
 All endpoints are rooted at /api/v1/.

Content type:
 Requests with bodies must send Content-Type: application/json.
 Responses use Content-Type: application/json except where noted.

Offline-only assumptions:
 - no authentication
 - no multi-user sessions
 - no remote sync
 - game data lives in local process memory unless later persisted explicitly
 - frontend calls endpoints asynchronously without full page reloads

General response rules:
 - 2xx responses return endpoint-specific JSON payloads
 - 4xx and 5xx responses return the standard ErrorResponse shape
 - unknown object fields in requests should be ignored unless otherwise stated
 - missing required fields should produce 400 invalid_request

Error response shape:
 {
 "error": {
 "code": "invalid_request",
 "message": "human-readable summary",
 "details": {
 "field": "optional field-specific detail"
 }
 }
 }

Standard error codes:
 - invalid_request
 - not_found
 - invalid_action
 - invalid_state
 - conflict
 - unsupported
 - internal_error

## State Model Names

The Flask routes and frontend should use these canonical state model names:

- CurriculumIndex
- CurriculumLesson
- RulesReference
- GameSummary
- GameState
- PlayerState
- TileRef
- Exposure
- DiscardEntry
- WallState
- TurnState
- CharlestonState
- PracticeTarget
- WinnerState
- ActionRequest
- ActionResult
- ErrorResponse

## Core Enumerations

Seat winds:
 - east
 - south
 - west
 - north

Player kinds:
 - human
 - ai

AI levels:
 - beginner
 - intermediate
 - advanced

Game phases:
 - setup
 - charleston
 - play
 - finished

Turn stages:
 - awaiting_draw
 - awaiting_discard
 - awaiting_call_window
 - resolving_call
 - hand_complete

Charleston phases:
 - none
 - first_right
 - first_across
 - first_left
 - optional_across
 - courtesy
 - complete

Action types:
 - draw
 - discard
 - pass
 - call
 - declare_mahjongg

Call types:
 - pung
 - kong
 - quint
 - sextet
 - mahjongg

Practice target visibility:
 - hidden
 - hint
 - revealed

Winner reasons:
 - mahjongg
 - wall_exhausted
 - stopped

Tile category codes:
 - suit
 - wind
 - dragon
 - joker
 - flower
 - season

Suit codes:
 - dots
 - bams
 - craks

Wind values:
 - east
 - south
 - west
 - north

Dragon values:
 - red
 - green
 - white

## Canonical TileRef Model

TileRef represents one tile instance known to the game engine.

Fields:
- tile_id: string, required
 Stable per-game identifier for a physical tile instance.
 Example: "tile_087"

- category: string, required
 One of suit, wind, dragon, joker, flower, season.

- suit: string or null
 Required when category is suit.
 One of dots, bams, craks.

- rank: integer or null
 Required when category is suit.
 Integer 1 through 9.

- honor: string or null
 Used for winds and dragons.
 Winds use east/south/west/north.
 Dragons use red/green/white.

- label: string, required
 Human-readable short label for UI.
 Examples: "5 Bam", "East", "Red Dragon", "Joker", "Flower"

- art_id: string, required
 Stable key for looking up packaged SVG art.
 Examples: "bam_5", "wind_east", "dragon_red", "joker", "flower"

Example:
 {
 "tile_id": "tile_087",
 "category": "suit",
 "suit": "bams",
 "rank": 5,
 "honor": null,
 "label": "5 Bam",
 "art_id": "bam_5"
 }

## PlayerState

Fields:
- player_id: string, required
 Example: "p1"

- name: string, required
 Example: "You"

- kind: string, required
 human or ai

- ai_level: string or null
 null for human; beginner, intermediate, or advanced for AI

- seat_wind: string, required
 east, south, west, or north

- is_dealer: boolean, required
 True for East in the current hand.

- hand: array of TileRef, required
 Concealed tiles currently held by this player.
 For opponents, the backend may return either full tile refs or redacted placeholders depending on view policy.
 First release recommendation: return full state because this is a teaching app.
 If redacted later, keep array length correct.

- hand_count: integer, required
 Count of concealed tiles in hand.

- exposures: array of Exposure, required
 Exposed sets declared by the player.

- discards: array of DiscardEntry, required
 Tiles discarded by this player in discard order.

- is_human_turn: boolean, required
 Convenience field for UI.

Example:
 {
 "player_id": "p1",
 "name": "You",
 "kind": "human",
 "ai_level": null,
 "seat_wind": "east",
 "is_dealer": true,
 "hand": [],
 "hand_count": 13,
 "exposures": [],
 "discards": [],
 "is_human_turn": true
 }

## Exposure

Fields:
- exposure_id: string, required
- set_type: string, required
 pung, kong, quint, sextet, or pair if later needed by engine internals
- tiles: array of TileRef, required
- called_from_seat: string or null
 Seat wind of player whose discard enabled this exposure, if any
- is_concealed: boolean, required

Example:
 {
 "exposure_id": "exp_001",
 "set_type": "pung",
 "tiles": [],
 "called_from_seat": "south",
 "is_concealed": false
 }

## DiscardEntry

Fields:
- discard_id: string, required
- tile: TileRef, required
- player_id: string, required
- seat_wind: string, required
- turn_number: integer, required
- is_claimable: boolean, required
 True while the call window is open.
- claimed_by_player_id: string or null

Example:
 {
 "discard_id": "d_014",
 "tile": {
 "tile_id": "tile_021",
 "category": "wind",
 "suit": null,
 "rank": null,
 "honor": "east",
 "label": "East",
 "art_id": "wind_east"
 },
 "player_id": "p2",
 "seat_wind": "south",
 "turn_number": 14,
 "is_claimable": false,
 "claimed_by_player_id": null
 }

## WallState

Fields:
- live_wall_count: integer, required
- dead_wall_count: integer, required
- total_remaining: integer, required
- last_draw_source: string or null
 live_wall or dead_wall
- wall_exhausted: boolean, required

Example:
 {
 "live_wall_count": 48,
 "dead_wall_count": 14,
 "total_remaining": 62,
 "last_draw_source": "live_wall",
 "wall_exhausted": false
 }

## TurnState

Fields:
- current_player_id: string, required
- current_seat_wind: string, required
- turn_number: integer, required
- stage: string, required
 awaiting_draw, awaiting_discard, awaiting_call_window, resolving_call, hand_complete
- last_action: string or null
 Human-readable summary for UI timeline
- last_discard: DiscardEntry or null
- call_window_open: boolean, required
- eligible_callers: array of string, required
 Player IDs permitted to call the current discard
- drawn_tile: TileRef or null
 The tile just drawn by the active player if relevant for UI

Example:
 {
 "current_player_id": "p1",
 "current_seat_wind": "east",
 "turn_number": 1,
 "stage": "awaiting_discard",
 "last_action": "You drew from the live wall.",
 "last_discard": null,
 "call_window_open": false,
 "eligible_callers": [],
 "drawn_tile": null
 }

## CharlestonState

Fields:
- phase: string, required
 none, first_right, first_across, first_left, optional_across, courtesy, complete

- is_active: boolean, required

- round_index: integer, required
 Zero-based internal counter.

- pass_direction: string or null
 right, across, left, or null

- pass_count_required: integer, required
 Usually 0 or 3 depending on the phase.

- selected_tiles_by_player: object, required
 Mapping of player_id to array of tile_id values chosen for the current pass.

- completed_phases: array of string, required

Example:
 {
 "phase": "first_right",
 "is_active": true,
 "round_index": 0,
 "pass_direction": "right",
 "pass_count_required": 3,
 "selected_tiles_by_player": {
 "p1": [],
 "p2": [],
 "p3": [],
 "p4": []
 },
 "completed_phases": []
 }

## PracticeTarget

Fields:
- pattern_id: string, required
 Identifier for the current practice target hand or lesson target.

- card_section: string, required
 Human-readable grouping label from the bundled teaching content.

- name: string, required
 Human-readable target pattern name.

- description: string, required
 Beginner-facing explanation of what the player is aiming for.

- visibility: string, required
 hidden, hint, or revealed

- target_tiles: array of object, required
 Minimal target descriptors used by UI guidance.
 Each item shape:
 - category: string
 - suit: string or null
 - rank: integer or null
 - honor: string or null
 - count: integer

Example:
 {
 "pattern_id": "basic_001",
 "card_section": "Beginner Practice",
 "name": "Simple Pung Hand",
 "description": "Practice building a hand around a few easy matching sets.",
 "visibility": "hint",
 "target_tiles": [
 {
 "category": "suit",
 "suit": "dots",
 "rank": 3,
 "honor": null,
 "count": 3
 }
 ]
 }

## WinnerState

Fields:
- status: string, required
 pending or decided

- winner_player_id: string or null

- winner_seat_wind: string or null

- reason: string or null
 mahjongg, wall_exhausted, or stopped

- winning_tiles: array of TileRef, required

- message: string, required
 Friendly summary for UI.

Example:
 {
 "status": "pending",
 "winner_player_id": null,
 "winner_seat_wind": null,
 "reason": null,
 "winning_tiles": [],
 "message": ""
 }

## GameSummary

Fields:
- game_id: string, required
- phase: string, required
- created_at: string, required
 ISO 8601 timestamp in local app time
- updated_at: string, required
 ISO 8601 timestamp in local app time
- human_player_id: string, required
- current_player_id: string, required
- winner: WinnerState, required

Example:
 {
 "game_id": "game_20260704_0001",
 "phase": "play",
 "created_at": "2026-07-04T10:15:33",
 "updated_at": "2026-07-04T10:21:00",
 "human_player_id": "p1",
 "current_player_id": "p2",
 "winner": {
 "status": "pending",
 "winner_player_id": null,
 "winner_seat_wind": null,
 "reason": null,
 "winning_tiles": [],
 "message": ""
 }
 }

## GameState

GameState is the canonical full state payload returned by gameplay endpoints.

Fields:
- game: GameSummary, required
- players: array of PlayerState, required
 Always four players in seat order east, south, west, north.
- dealer_player_id: string, required
- dealer_seat_wind: string, required
- wall: WallState, required
- turn: TurnState, required
- charleston: CharlestonState, required
- practice_target: PracticeTarget or null
- discards: array of DiscardEntry, required
 Table-wide discard history in chronological order.
- available_actions: array of string, required
 Action names available to the human player right now.
- rules_context: object, required
 Lightweight teaching hints for the current state.
 Shape:
 - can_call: boolean
 - can_declare_mahjongg: boolean
 - current_phase_help: string
- winner: WinnerState, required

Example:
 {
 "game": {
 "game_id": "game_20260704_0001",
 "phase": "charleston",
 "created_at": "2026-07-04T10:15:33",
 "updated_at": "2026-07-04T10:16:01",
 "human_player_id": "p1",
 "current_player_id": "p1",
 "winner": {
 "status": "pending",
 "winner_player_id": null,
 "winner_seat_wind": null,
 "reason": null,
 "winning_tiles": [],
 "message": ""
 }
 },
 "players": [],
 "dealer_player_id": "p1",
 "dealer_seat_wind": "east",
 "wall": {
 "live_wall_count": 65,
 "dead_wall_count": 14,
 "total_remaining": 79,
 "last_draw_source": null,
 "wall_exhausted": false
 },
 "turn": {
 "current_player_id": "p1",
 "current_seat_wind": "east",
 "turn_number": 0,
 "stage": "awaiting_draw",
 "last_action": null,
 "last_discard": null,
 "call_window_open": false,
 "eligible_callers": [],
 "drawn_tile": null
 },
 "charleston": {
 "phase": "first_right",
 "is_active": true,
 "round_index": 0,
 "pass_direction": "right",
 "pass_count_required": 3,
 "selected_tiles_by_player": {
 "p1": [],
 "p2": [],
 "p3": [],
 "p4": []
 },
 "completed_phases": []
 },
 "practice_target": null,
 "discards": [],
 "available_actions": ["pass"],
 "rules_context": {
 "can_call": false,
 "can_declare_mahjongg": false,
 "current_phase_help": "Select Charleston tiles when prompted, then confirm the pass."
 },
 "winner": {
 "status": "pending",
 "winner_player_id": null,
 "winner_seat_wind": null,
 "reason": null,
 "winning_tiles": [],
 "message": ""
 }
 }

## Curriculum Models

### CurriculumIndex

Fields:
- lessons: array of CurriculumLessonSummary, required
 Summary item shape:
 - lesson_id: string
 - slug: string
 - title: string
 - order_index: integer
 - estimated_minutes: integer
 - unlocked: boolean

### CurriculumLesson

Fields:
- lesson_id: string, required
- slug: string, required
- title: string, required
- order_index: integer, required
- estimated_minutes: integer, required
- summary: string, required
- objectives: array of string, required
- body: array of content blocks, required
 Content block shape:
 - type: string
 - text: string
- related_rules: array of string, required
 Rule topic IDs for the rules reference endpoint.
- next_lesson_id: string or null

## RulesReference

Fields:
- topics: array of RulesTopicSummary, required
 Summary item shape:
 - topic_id: string
 - title: string
 - summary: string

Single-topic shape:
- topic_id: string, required
- title: string, required
- summary: string, required
- body: array of content blocks, required
- glossary: array of object, required
 Each object:
 - term: string
 - definition: string

## API Endpoints

### GET /api/v1/health

Purpose:
 Lightweight local status check for the frontend and Docker health checks.

Response 200:
 {
 "status": "ok",
 "app": "suitup",
 "offline": true
 }

Errors:
 500 internal_error

### GET /api/v1/curriculum

Purpose:
 Return the ordered beginner curriculum index used to render lesson navigation.

Response 200 shape:
 {
 "curriculum": {
 "lessons": [
 {
 "lesson_id": "lesson_01",
 "slug": "what-is-american-mah-jongg",
 "title": "What Is American Mah Jongg?",
 "order_index": 1,
 "estimated_minutes": 8,
 "unlocked": true
 }
 ]
 }
 }

Errors:
 500 internal_error

### GET /api/v1/curriculum/{lesson_id}

Purpose:
 Return one lesson in full detail.

Path params:
- lesson_id: string

Response 200 shape:
 {
 "lesson": {
 "lesson_id": "lesson_03",
 "slug": "the-charleston",
 "title": "The Charleston",
 "order_index": 3,
 "estimated_minutes": 12,
 "summary": "Learn the opening tile exchange.",
 "objectives": [
 "Understand the pass directions.",
 "Recognize when the Charleston is active."
 ],
 "body": [
 {
 "type": "paragraph",
 "text": "The Charleston is a sequence of tile passes before normal play."
 }
 ],
 "related_rules": ["charleston", "dealer_selection"],
 "next_lesson_id": "lesson_04"
 }
 }

Errors:
 404 not_found
 500 internal_error

### GET /api/v1/rules

Purpose:
 Return the rules topic index used for quick reference.

Optional query params:
- q: string
 Simple local substring search over topic title and summary.

Response 200 shape:
 {
 "rules": {
 "topics": [
 {
 "topic_id": "charleston",
 "title": "The Charleston",
 "summary": "Opening tile exchange before play."
 }
 ]
 }
 }

Errors:
 500 internal_error

### GET /api/v1/rules/{topic_id}

Purpose:
 Return one rules reference topic in full detail.

Path params:
- topic_id: string

Response 200 shape:
 {
 "rule": {
 "topic_id": "charleston",
 "title": "The Charleston",
 "summary": "Opening tile exchange before play.",
 "body": [
 {
 "type": "paragraph",
 "text": "Players pass tiles in a defined sequence before normal drawing and discarding."
 }
 ],
 "glossary": [
 {
 "term": "courtesy pass",
 "definition": "A pass where fewer than three tiles may be exchanged if agreed."
 }
 ]
 }
 }

Errors:
 404 not_found
 500 internal_error

### POST /api/v1/games

Purpose:
 Create a new local practice game and return the initial canonical GameState.

Request body:
 {
 "human_name": "You",
 "ai_levels": {
 "south": "beginner",
 "west": "intermediate",
 "north": "advanced"
 },
 "starting_dealer_seat": "east",
 "include_charleston": true,
 "practice_target": {
 "pattern_id": "basic_001",
 "visibility": "hint"
 }
 }

Request fields:
- human_name: string, optional, default "You"
- ai_levels: object, optional
 Keys must be south, west, north.
 Values must be beginner, intermediate, or advanced.
- starting_dealer_seat: string, optional, default east
 For first release this should normally be east.
- include_charleston: boolean, optional, default true
- practice_target: object or null, optional
 Shape:
 - pattern_id: string
 - visibility: hidden, hint, or revealed

Response 201 shape:
 {
 "game_state": { GameState }
 }

Errors:
 400 invalid_request
 409 conflict
 500 internal_error

Conflict guidance:
 If the app supports only one active game at a time and another active game exists, return:
 {
 "error": {
 "code": "conflict",
 "message": "An active game already exists.",
 "details": {
 "active_game_id": "game_20260704_0001"
 }
 }
 }

### GET /api/v1/games/{game_id}

Purpose:
 Fetch the full current GameState for polling or initial page hydration.

Path params:
- game_id: string

Response 200 shape:
 {
 "game_state": { GameState }
 }

Errors:
 404 not_found
 500 internal_error

### POST /api/v1/games/{game_id}/actions

Purpose:
 Submit one human gameplay action without reloading the page.

This endpoint is the canonical mutating endpoint for:
 - draw
 - discard
 - pass
 - call
 - declare_mahjongg

Request shape:
 {
 "action": {
 "type": "discard",
 "player_id": "p1",
 "tile_id": "tile_087",
 "call_type": null,
 "claim_discard_id": null,
 "selected_tile_ids": [],
 "metadata": {}
 }
 }

ActionRequest fields:
- type: string, required
 draw, discard, pass, call, declare_mahjongg

- player_id: string, required
 Usually the local human player ID.

- tile_id: string or null
 Required for discard.
 Forbidden for draw unless later used for special draw source resolution.

- call_type: string or null
 Required when type is call.
 pung, kong, quint, sextet, or mahjongg

- claim_discard_id: string or null
 Required when claiming another player's discard.

- selected_tile_ids: array of string, required
 Used for Charleston pass selection and may also support certain declarations.
 Empty array when unused.

- metadata: object, required
 Reserved for small route-level flags.
 First release should accept but ignore unknown keys.

Action-specific validation rules:
- draw:
 - tile_id must be null
 - selected_tile_ids must be empty
 - valid only when it is that player's turn and stage is awaiting_draw

- discard:
 - tile_id required
 - valid only when it is that player's turn and stage is awaiting_discard

- pass:
 - during Charleston, selected_tile_ids length must equal pass_count_required unless courtesy rules apply
 - during a discard call window, selected_tile_ids should be empty and the action means "decline to call"

- call:
 - call_type required
 - claim_discard_id required
 - valid only while call_window_open is true and player is eligible

- declare_mahjongg:
 - may include claim_discard_id when winning on a discard
 - may omit claim_discard_id when self-drawn
 - engine validates the hand

Success response 200 shape:
 {
 "result": {
 "accepted": true,
 "action_type": "discard",
 "message": "You discarded 5 Bam.",
 "game_state": { GameState }
 }
 }

ActionResult fields:
- accepted: boolean, required
- action_type: string, required
- message: string, required
- game_state: GameState, required

Errors:
 400 invalid_request
 404 not_found
 409 invalid_state
 422 invalid_action
 500 internal_error

Recommended invalid action response:
 {
 "error": {
 "code": "invalid_action",
 "message": "Tile tile_087 is not available to discard.",
 "details": {
 "action_type": "discard",
 "tile_id": "tile_087"
 }
 }
 }

### POST /api/v1/games/{game_id}/ai-turn

Purpose:
 Advance exactly one AI decision step for the current game.

This endpoint allows the frontend to animate AI play step-by-step instead of collapsing all AI behavior into server-side loops.

Request body:
 {
 "player_id": "p2"
 }

Request fields:
- player_id: string, optional
 If provided, must match the current AI player when it is an AI turn.
 If omitted, the server resolves the current AI player automatically.

Success response 200 shape:
 {
 "result": {
 "accepted": true,
 "action_type": "ai_turn",
 "message": "South discarded White Dragon.",
 "game_state": { GameState }
 }
 }

Behavior:
 - If current player is AI and is awaiting_draw, the server may draw and discard within one call, or perform one stage transition only.
 - First release should choose one behavior and keep it stable.
 - Recommendation: one complete AI turn per call unless a call window interrupts.

Errors:
 400 invalid_request
 404 not_found
 409 invalid_state
 422 invalid_action
 500 internal_error

Suggested invalid state response:
 {
 "error": {
 "code": "invalid_state",
 "message": "It is not currently an AI turn.",
 "details": {
 "current_player_id": "p1",
 "current_player_kind": "human"
 }
 }
 }

### POST /api/v1/games/{game_id}/stop

Purpose:
 End a practice game early and mark the winner state as stopped.

Request body:
 {
 "reason": "user_requested"
 }

Response 200 shape:
 {
 "game_state": { GameState }
 }

Behavior:
 - winner.status becomes decided
 - winner.reason becomes stopped
 - winner.message becomes a friendly stop summary
 - game.phase becomes finished

Errors:
 404 not_found
 409 invalid_state
 500 internal_error

### POST /api/v1/art/build

Purpose:
 Optional local-only build hook for generating packaged SVG art manifests or derived sprite metadata.

This endpoint should only exist if the implementation actually uses a server-triggered local build step.
If no runtime art build exists, do not implement this route.

Request body:
 {
 "force": false
 }

Response 200 shape:
 {
 "art_build": {
 "status": "ok",
 "generated_files": [
 "suitup/web/static/art/tiles/manifest.json"
 ]
 }
 }

Errors:
 400 invalid_request
 501 unsupported
 500 internal_error

Implementation guidance:
 For first release, prefer prebuilt packaged SVG assets and omit this endpoint entirely.

## HTTP Status Code Usage

200 OK
 Successful fetch or action application.

201 Created
 New game created.

400 Bad Request
 Malformed JSON, missing fields, bad enum value, invalid path/query/body combination.

404 Not Found
 Unknown lesson, topic, game, or other resource identifier.

409 Conflict
 Request is well-formed but impossible in current server state, such as creating a second active game when only one is allowed.

422 Unprocessable Entity
 Request shape is valid but the attempted move is illegal under current game rules.

500 Internal Server Error
 Unhandled local application error.

501 Not Implemented
 Optional endpoint recognized by contract but not enabled, such as art/build when omitted.

## Minimal Request/Response Examples

### Example: fetch curriculum index

Request:
 GET /api/v1/curriculum

Response:
 {
 "curriculum": {
 "lessons": [
 {
 "lesson_id": "lesson_01",
 "slug": "welcome-to-your-set",
 "title": "Welcome to Your Set",
 "order_index": 1,
 "estimated_minutes": 10,
 "unlocked": true
 }
 ]
 }
 }

### Example: fetch one rules topic

Request:
 GET /api/v1/rules/charleston

Response:
 {
 "rule": {
 "topic_id": "charleston",
 "title": "The Charleston",
 "summary": "Opening tile exchange before play.",
 "body": [
 {
 "type": "paragraph",
 "text": "The Charleston happens before normal play and teaches players to improve awkward hands."
 }
 ],
 "glossary": [
 {
 "term": "pass",
 "definition": "A tile given to another player during the Charleston."
 }
 ]
 }
 }

### Example: create a new practice game

Request:
 POST /api/v1/games
 {
 "human_name": "You",
 "ai_levels": {
 "south": "beginner",
 "west": "beginner",
 "north": "intermediate"
 },
 "starting_dealer_seat": "east",
 "include_charleston": true,
 "practice_target": {
 "pattern_id": "basic_001",
 "visibility": "hint"
 }
 }

Response:
 {
 "game_state": {
 "game": {
 "game_id": "game_20260704_0001",
 "phase": "charleston",
 "created_at": "2026-07-04T10:15:33",
 "updated_at": "2026-07-04T10:15:33",
 "human_player_id": "p1",
 "current_player_id": "p1",
 "winner": {
 "status": "pending",
 "winner_player_id": null,
 "winner_seat_wind": null,
 "reason": null,
 "winning_tiles": [],
 "message": ""
 }
 },
 "players": [],
 "dealer_player_id": "p1",
 "dealer_seat_wind": "east",
 "wall": {
 "live_wall_count": 65,
 "dead_wall_count": 14,
 "total_remaining": 79,
 "last_draw_source": null,
 "wall_exhausted": false
 },
 "turn": {
 "current_player_id": "p1",
 "current_seat_wind": "east",
 "turn_number": 0,
 "stage": "awaiting_draw",
 "last_action": null,
 "last_discard": null,
 "call_window_open": false,
 "eligible_callers": [],
 "drawn_tile": null
 },
 "charleston": {
 "phase": "first_right",
 "is_active": true,
 "round_index": 0,
 "pass_direction": "right",
 "pass_count_required": 3,
 "selected_tiles_by_player": {
 "p1": [],
 "p2": [],
 "p3": [],
 "p4": []
 },
 "completed_phases": []
 },
 "practice_target": {
 "pattern_id": "basic_001",
 "card_section": "Beginner Practice",
 "name": "Simple Pung Hand",
 "description": "Practice building a hand around a few easy matching sets.",
 "visibility": "hint",
 "target_tiles": []
 },
 "discards": [],
 "available_actions": ["pass"],
 "rules_context": {
 "can_call": false,
 "can_declare_mahjongg": false,
 "current_phase_help": "Choose tiles for the opening Charleston pass."
 },
 "winner": {
 "status": "pending",
 "winner_player_id": null,
 "winner_seat_wind": null,
 "reason": null,
 "winning_tiles": [],
 "message": ""
 }
 }
 }

### Example: discard a tile

Request:
 POST /api/v1/games/game_20260704_0001/actions
 {
 "action": {
 "type": "discard",
 "player_id": "p1",
 "tile_id": "tile_087",
 "call_type": null,
 "claim_discard_id": null,
 "selected_tile_ids": [],
 "metadata": {}
 }
 }

Response:
 {
 "result": {
 "accepted": true,
 "action_type": "discard",
 "message": "You discarded 5 Bam.",
 "game_state": {
 "game": {
 "game_id": "game_20260704_0001",
 "phase": "play",
 "created_at": "2026-07-04T10:15:33",
 "updated_at": "2026-07-04T10:25:10",
 "human_player_id": "p1",
 "current_player_id": "p2",
 "winner": {
 "status": "pending",
 "winner_player_id": null,
 "winner_seat_wind": null,
 "reason": null,
 "winning_tiles": [],
 "message": ""
 }
 },
 "players": [],
 "dealer_player_id": "p1",
 "dealer_seat_wind": "east",
 "wall": {
 "live_wall_count": 48,
 "dead_wall_count": 14,
 "total_remaining": 62,
 "last_draw_source": "live_wall",
 "wall_exhausted": false
 },
 "turn": {
 "current_player_id": "p2",
 "current_seat_wind": "south",
 "turn_number": 14,
 "stage": "awaiting_call_window",
 "last_action": "You discarded 5 Bam.",
 "last_discard": {
 "discard_id": "d_014",
 "tile": {
 "tile_id": "tile_087",
 "category": "suit",
 "suit": "bams",
 "rank": 5,
 "honor": null,
 "label": "5 Bam",
 "art_id": "bam_5"
 },
 "player_id": "p1",
 "seat_wind": "east",
 "turn_number": 14,
 "is_claimable": true,
 "claimed_by_player_id": null
 },
 "call_window_open": true,
 "eligible_callers": ["p2", "p3", "p4"],
 "drawn_tile": null
 },
 "charleston": {
 "phase": "complete",
 "is_active": false,
 "round_index": 5,
 "pass_direction": null,
 "pass_count_required": 0,
 "selected_tiles_by_player": {
 "p1": [],
 "p2": [],
 "p3": [],
 "p4": []
 },
 "completed_phases": [
 "first_right",
 "first_across",
 "first_left"
 ]
 },
 "practice_target": null,
 "discards": [],
 "available_actions": ["pass"],
 "rules_context": {
 "can_call": false,
 "can_declare_mahjongg": false,
 "current_phase_help": "Other players may now call the discard if eligible."
 },
 "winner": {
 "status": "pending",
 "winner_player_id": null,
 "winner_seat_wind": null,
 "reason": null,
 "winning_tiles": [],
 "message": ""
 }
 }
 }
 }

### Example: invalid action

Response:
 {
 "error": {
 "code": "invalid_action",
 "message": "You cannot discard before drawing.",
 "details": {
 "required_stage": "awaiting_discard",
 "actual_stage": "awaiting_draw"
 }
 }
 }

### Example: execute AI turn

Request:
 POST /api/v1/games/game_20260704_0001/ai-turn
 {
 "player_id": "p2"
 }

Response:
 {
 "result": {
 "accepted": true,
 "action_type": "ai_turn",
 "message": "South drew and discarded White Dragon.",
 "game_state": {
 "game": {
 "game_id": "game_20260704_0001",
 "phase": "play",
 "created_at": "2026-07-04T10:15:33",
 "updated_at": "2026-07-04T10:26:41",
 "human_player_id": "p1",
 "current_player_id": "p3",
 "winner": {
 "status": "pending",
 "winner_player_id": null,
 "winner_seat_wind": null,
 "reason": null,
 "winning_tiles": [],
 "message": ""
 }
 },
 "players": [],
 "dealer_player_id": "p1",
 "dealer_seat_wind": "east",
 "wall": {
 "live_wall_count": 47,
 "dead_wall_count": 14,
 "total_remaining": 61,
 "last_draw_source": "live_wall",
 "wall_exhausted": false
 },
 "turn": {
 "current_player_id": "p3",
 "current_seat_wind": "west",
 "turn_number": 15,
 "stage": "awaiting_call_window",
 "last_action": "South discarded White Dragon.",
 "last_discard": null,
 "call_window_open": true,
 "eligible_callers": ["p1", "p3", "p4"],
 "drawn_tile": null
 },
 "charleston": {
 "phase": "complete",
 "is_active": false,
 "round_index": 5,
 "pass_direction": null,
 "pass_count_required": 0,
 "selected_tiles_by_player": {
 "p1": [],
 "p2": [],
 "p3": [],
 "p4": []
 },
 "completed_phases": [
 "first_right",
 "first_across",
 "first_left"
 ]
 },
 "practice_target": null,
 "discards": [],
 "available_actions": ["pass", "call"],
 "rules_context": {
 "can_call": true,
 "can_declare_mahjongg": false,
 "current_phase_help": "You may call the latest discard if your hand allows it."
 },
 "winner": {
 "status": "pending",
 "winner_player_id": null,
 "winner_seat_wind": null,
 "reason": null,
 "winning_tiles": [],
 "message": ""
 }
 }
 }
 }

## Canonical Field Notes for Later Flask Routes

These names are fixed for later implementation:
- game_id
- player_id
- seat_wind
- is_dealer
- hand
- exposures
- discards
- current_player_id
- current_seat_wind
- turn_number
- charleston.phase
- charleston.pass_direction
- practice_target.visibility
- winner.status
- winner.reason
- available_actions
- rules_context.current_phase_help

Frontend assumptions:
- The frontend can fully render the table from GameState alone.
- Polling or event-loop behavior should always reconcile against GameState from the server.
- Mutations should never require the frontend to infer rule outcomes locally.

Backend assumptions:
- Routes should validate all enum values exactly as written here.
- Illegal moves should use invalid_action unless the failure is due to broader lifecycle state, in which case use invalid_state.
- For a beginner-teaching build, returning complete opponent hands is allowed and even encouraged if the selected practice mode is instructional.

Out of scope for first release:
- accounts
- save slots
- cloud sync
- multiplayer over network
- websockets
- long-running background jobs
- analytics beacons