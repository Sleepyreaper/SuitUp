# SuitUp Browser/API Contract

Version: v1
Status: frozen for release slice t02
Applies to: offline Flask app served at http://localhost:8092
Related architecture: docs/architecture.md

## Purpose

This document freezes the browser/backend contract for SuitUp's first release so frontend and backend work can proceed independently. It defines:

- HTTP routes between the web UI and Flask backend
- JSON request and response payloads
- Error response shape and status codes
- Stable curriculum content schema
- Stable rules reference schema
- Stable practice game-state schema

All payloads are JSON.
All timestamps, if present in future revisions, must use RFC 3339 strings.
All IDs are opaque strings.
All enum values are lowercase snake_case unless otherwise noted.

## Transport Rules

### Base URL

The app is served locally at:

 http://localhost:8092

The frontend must call relative paths rooted at:

 /api/v1/

### Content Type

Requests with bodies:

 Content-Type: application/json

Responses:

 Content-Type: application/json

### Error Envelope

All non-2xx responses return the same JSON shape:

 {
 "error": {
 "code": "string_machine_code",
 "message": "Human-readable explanation.",
 "details": {
 "optional_key": "optional value"
 }
 }
 }

Fields:
- error.code: stable machine-readable error code
- error.message: human-readable summary
- error.details: optional object with field-specific context

### Common Error Codes

- invalid_request
- invalid_json
- invalid_difficulty
- invalid_action
- invalid_phase
- invalid_turn
- game_not_found
- lesson_not_found
- rules_not_found
- action_not_allowed
- ai_not_ready
- state_conflict
- internal_error

## Route Index

1. GET /api/v1/curriculum
2. GET /api/v1/rules-reference
3. POST /api/v1/practice-games
4. GET /api/v1/practice-games/<game_id>
5. POST /api/v1/practice-games/<game_id>/actions
6. POST /api/v1/practice-games/<game_id>/ai-turn
7. POST /api/v1/practice-games/<game_id>/reset

---

## 1) Load curriculum

### GET /api/v1/curriculum

Loads the full guided beginner curriculum rendered by the teaching UI.

### Request

No request body.

Optional query parameters:
- unit_id: string, optional; if present, backend may return only that unit while preserving top-level shape
- include_steps: boolean-like string, optional; default true

For release v1, frontend should call without query parameters and expect the full curriculum.

### Success Response

Status: 200 OK

 {
 "curriculum": {
 "version": "v1",
 "title": "SuitUp Beginner Course",
 "audience": "absolute_beginner",
 "estimated_total_minutes": 180,
 "units": [
 {
 "id": "welcome_and_setup",
 "slug": "welcome-and-setup",
 "title": "Welcome and Table Setup",
 "description": "Learn what comes in the set and how to prepare the table.",
 "estimated_minutes": 20,
 "order": 1,
 "prerequisite_unit_ids": [],
 "learning_objectives": [
 "Identify the main tile groups.",
 "Set up racks, dice, and wall basics."
 ],
 "lessons": [
 {
 "id": "meet_the_tiles",
 "slug": "meet-the-tiles",
 "title": "Meet the Tiles",
 "description": "A visual introduction to suits, honors, flowers, and jokers.",
 "estimated_minutes": 8,
 "order": 1,
 "step_count": 3,
 "steps": [
 {
 "id": "tiles_intro",
 "order": 1,
 "type": "content",
 "title": "The American Mah Jongg Tile Set",
 "body_markdown": "American Mah Jongg uses 152 tiles...",
 "media": {
 "kind": "svg_plate",
 "asset_id": "tile-groups-overview"
 },
 "callouts": [
 {
 "tone": "tip",
 "title": "Beginner tip",
 "body": "Flowers and jokers are special groups."
 }
 ],
 "knowledge_checks": [],
 "practice_link": null
 }
 ]
 }
 ]
 }
 ]
 }
 }

### Response Fields

Top-level:
- curriculum.version: string
- curriculum.title: string
- curriculum.audience: string enum
- curriculum.estimated_total_minutes: integer
- curriculum.units: array of curriculum units

### Error Responses

Status: 404 Not Found

 {
 "error": {
 "code": "lesson_not_found",
 "message": "The requested curriculum unit was not found.",
 "details": {
 "unit_id": "bad_unit"
 }
 }
 }

Status: 500 Internal Server Error

 {
 "error": {
 "code": "internal_error",
 "message": "Unable to load curriculum.",
 "details": {}
 }
 }

---

## 2) Load rules reference

### GET /api/v1/rules-reference

Loads the structured rules reference used by the rules pages and contextual help panels.

### Request

No request body.

Optional query parameters:
- section: string, optional

### Success Response

Status: 200 OK

 {
 "rules_reference": {
 "version": "v1",
 "title": "American Mah Jongg Rules Reference",
 "sections": [
 {
 "id": "tile_set",
 "title": "Tile Set",
 "order": 1,
 "summary": "The full American Mah Jongg set contains 152 tiles.",
 "entries": [
 {
 "id": "tile_set_counts",
 "label": "Tile count",
 "body_markdown": "Three suits 1-9, four of each, plus winds, dragons, flowers, and jokers.",
 "facts": [
 {
 "key": "total_tiles",
 "value": 152
 },
 {
 "key": "jokers",
 "value": 8
 }
 ]
 }
 ]
 }
 ]
 }
 }

### Response Fields

Top-level:
- rules_reference.version: string
- rules_reference.title: string
- rules_reference.sections: array of rule sections

### Error Responses

Status: 404 Not Found

 {
 "error": {
 "code": "rules_not_found",
 "message": "The requested rules section was not found.",
 "details": {
 "section": "bad_section"
 }
 }
 }

Status: 500 Internal Server Error

 {
 "error": {
 "code": "internal_error",
 "message": "Unable to load rules reference.",
 "details": {}
 }
 }

---

## 3) Create practice game

### POST /api/v1/practice-games

Creates a new local practice game for one human player versus three AI opponents.

### Request Body

 {
 "difficulty": "beginner",
 "player_name": "Player",
 "curriculum_context": {
 "unit_id": "welcome_and_setup",
 "lesson_id": "meet_the_tiles",
 "step_id": "tiles_intro"
 },
 "seed": 12345
 }

### Request Fields

- difficulty: required string enum
 - beginner
 - intermediate
 - challenger
- player_name: optional string, 1-40 chars; defaults to "Player"
- curriculum_context: optional object for analytics-free local UI context only
- seed: optional integer for deterministic local debugging/replay

### Success Response

Status: 201 Created

 {
 "game": {
 "game_id": "game_01hx8r7w2m3p",
 "created": true,
 "difficulty": "beginner",
 "state": {
 "game_id": "game_01hx8r7w2m3p",
 "status": "in_progress",
 "phase": "charleston",
 "difficulty": "beginner",
 "dealer_seat": "east",
 "player_seat": "east",
 "current_turn_seat": "east",
 "hand_number": 1,
 "charleston": {
 "phase": "right",
 "pass_index": 1,
 "pass_direction": "right",
 "optional": false,
 "pending_seats": ["east", "south", "west", "north"],
 "completed_passes": []
 },
 "wall": {
 "tiles_remaining": 96,
 "live_wall_remaining": 96,
 "dead_wall_remaining": 0
 },
 "players": [
 {
 "seat": "east",
 "name": "Player",
 "is_human": true,
 "difficulty": null,
 "hand": [],
 "hand_count": 13,
 "exposures": [],
 "discards_taken": [],
 "declared": false,
 "mahjong": false
 },
 {
 "seat": "south",
 "name": "Bot 1",
 "is_human": false,
 "difficulty": "beginner",
 "hand": [],
 "hand_count": 13,
 "exposures": [],
 "discards_taken": [],
 "declared": false,
 "mahjong": false
 }
 ],
 "discard_pile": [],
 "last_discard": null,
 "turn_prompt": {
 "actor_seat": "east",
 "allowed_actions": ["charleston_pass"],
 "message": "Choose three tiles to pass right."
 },
 "winner": null,
 "winning_source": null,
 "winning_hand_name": null
 }
 }
 }

### Error Responses

Status: 400 Bad Request

 {
 "error": {
 "code": "invalid_difficulty",
 "message": "Difficulty must be one of beginner, intermediate, challenger.",
 "details": {
 "difficulty": "expert"
 }
 }
 }

Status: 400 Bad Request

 {
 "error": {
 "code": "invalid_json",
 "message": "Request body must be valid JSON.",
 "details": {}
 }
 }

Status: 500 Internal Server Error

 {
 "error": {
 "code": "internal_error",
 "message": "Unable to create practice game.",
 "details": {}
 }
 }

---

## 4) Poll practice game state

### GET /api/v1/practice-games/<game_id>

Returns the complete current game state for rendering the practice table.

### Request

No request body.

Path parameters:
- game_id: required string

### Success Response

Status: 200 OK

 {
 "game": {
 "state": {
 "game_id": "game_01hx8r7w2m3p",
 "status": "in_progress",
 "phase": "player_turn",
 "difficulty": "beginner",
 "dealer_seat": "east",
 "player_seat": "east",
 "current_turn_seat": "east",
 "hand_number": 1,
 "charleston": {
 "phase": "complete",
 "pass_index": 3,
 "pass_direction": "across",
 "optional": false,
 "pending_seats": [],
 "completed_passes": [
 {
 "direction": "right",
 "from_seat": "east",
 "tile_count": 3
 }
 ]
 },
 "wall": {
 "tiles_remaining": 64,
 "live_wall_remaining": 64,
 "dead_wall_remaining": 0
 },
 "players": [
 {
 "seat": "east",
 "name": "Player",
 "is_human": true,
 "difficulty": null,
 "hand": [
 {
 "tile_id": "tile_001",
 "code": "1_dot",
 "group": "suit",
 "suit": "dots",
 "rank": 1,
 "label": "1 Dot",
 "art_asset": "tiles/1_dot.svg"
 }
 ],
 "hand_count": 14,
 "exposures": [],
 "discards_taken": [],
 "declared": false,
 "mahjong": false
 },
 {
 "seat": "south",
 "name": "Bot 1",
 "is_human": false,
 "difficulty": "beginner",
 "hand": null,
 "hand_count": 13,
 "exposures": [],
 "discards_taken": [],
 "declared": false,
 "mahjong": false
 },
 {
 "seat": "west",
 "name": "Bot 2",
 "is_human": false,
 "difficulty": "beginner",
 "hand": null,
 "hand_count": 13,
 "exposures": [],
 "discards_taken": [],
 "declared": false,
 "mahjong": false
 },
 {
 "seat": "north",
 "name": "Bot 3",
 "is_human": false,
 "difficulty": "beginner",
 "hand": null,
 "hand_count": 13,
 "exposures": [],
 "discards_taken": [],
 "declared": false,
 "mahjong": false
 }
 ],
 "discard_pile": [
 {
 "tile_id": "tile_089",
 "code": "west_wind",
 "group": "wind",
 "suit": null,
 "rank": null,
 "label": "West",
 "art_asset": "tiles/west_wind.svg"
 }
 ],
 "last_discard": {
 "seat": "north",
 "tile": {
 "tile_id": "tile_089",
 "code": "west_wind",
 "group": "wind",
 "suit": null,
 "rank": null,
 "label": "West",
 "art_asset": "tiles/west_wind.svg"
 }
 },
 "turn_prompt": {
 "actor_seat": "east",
 "allowed_actions": ["draw", "discard", "declare_mahjong"],
 "message": "Draw a tile or declare mahjong if valid."
 },
 "winner": null,
 "winning_source": null,
 "winning_hand_name": null
 }
 }
 }

### Error Responses

Status: 404 Not Found

 {
 "error": {
 "code": "game_not_found",
 "message": "No practice game exists for the given game_id.",
 "details": {
 "game_id": "game_missing"
 }
 }
 }

Status: 500 Internal Server Error

 {
 "error": {
 "code": "internal_error",
 "message": "Unable to load game state.",
 "details": {}
 }
 }

---

## 5) Submit player action

### POST /api/v1/practice-games/<game_id>/actions

Submits a human player's action. This route is used for Charleston passing and table play.

### Request Body

 {
 "action": "discard",
 "seat": "east",
 "payload": {
 "tile_id": "tile_001"
 }
 }

### Request Fields

- action: required string enum
 - charleston_pass
 - draw
 - discard
 - call
 - declare_mahjong
- seat: required string enum
 - east
 - south
 - west
 - north
- payload: required object, shape depends on action

### Action Payload Shapes

#### charleston_pass

 {
 "action": "charleston_pass",
 "seat": "east",
 "payload": {
 "tile_ids": ["tile_001", "tile_010", "tile_099"]
 }
 }

Rules:
- exactly 3 tile_ids required
- only legal during charleston phase
- only legal for the acting seat
- backend resolves exchange only after all required seats submit

#### draw

 {
 "action": "draw",
 "seat": "east",
 "payload": {}
 }

Rules:
- only legal during player_turn
- only legal when current_turn_seat matches seat
- no tile_id required

#### discard

 {
 "action": "discard",
 "seat": "east",
 "payload": {
 "tile_id": "tile_001"
 }
 }

Rules:
- tile_id required
- tile_id must exist in human player's hand
- only legal during player_turn after draw state is satisfied

#### call

 {
 "action": "call",
 "seat": "east",
 "payload": {
 "call_type": "pass"
 }
 }

Or:

 {
 "action": "call",
 "seat": "east",
 "payload": {
 "call_type": "pon",
 "tile_id": "tile_089"
 }
 }

Supported call_type values for v1:
- pass
- pon
- kong
- quint
- mahjong

Notes:
- pass means decline the most recent discard
- exposed sequence calls are not part of American Mah Jongg and must not be supported
- payload requirements depend on call_type and rules-engine legality

#### declare_mahjong

 {
 "action": "declare_mahjong",
 "seat": "east",
 "payload": {}
 }

Rules:
- backend validates hand legality
- returns 409 if declaration is invalid

### Success Response

Status: 200 OK

 {
 "result": {
 "accepted": true,
 "action": "discard",
 "resolved": true,
 "state": {
 "game_id": "game_01hx8r7w2m3p",
 "status": "in_progress",
 "phase": "awaiting_calls",
 "difficulty": "beginner",
 "dealer_seat": "east",
 "player_seat": "east",
 "current_turn_seat": "south",
 "hand_number": 1,
 "charleston": {
 "phase": "complete",
 "pass_index": 3,
 "pass_direction": "across",
 "optional": false,
 "pending_seats": [],
 "completed_passes": []
 },
 "wall": {
 "tiles_remaining": 63,
 "live_wall_remaining": 63,
 "dead_wall_remaining": 0
 },
 "players": [],
 "discard_pile": [],
 "last_discard": {
 "seat": "east",
 "tile": {
 "tile_id": "tile_001",
 "code": "1_dot",
 "group": "suit",
 "suit": "dots",
 "rank": 1,
 "label": "1 Dot",
 "art_asset": "tiles/1_dot.svg"
 }
 },
 "turn_prompt": {
 "actor_seat": "south",
 "allowed_actions": ["resolve_ai_turn"],
 "message": "Waiting for AI decisions."
 },
 "winner": null,
 "winning_source": null,
 "winning_hand_name": null
 }
 }
 }

### Error Responses

Status: 400 Bad Request

 {
 "error": {
 "code": "invalid_action",
 "message": "Action must be one of charleston_pass, draw, discard, call, declare_mahjong.",
 "details": {
 "action": "swap"
 }
 }
 }

Status: 400 Bad Request

 {
 "error": {
 "code": "invalid_request",
 "message": "Discard requires payload.tile_id.",
 "details": {
 "field": "payload.tile_id"
 }
 }
 }

Status: 403 Forbidden

 {
 "error": {
 "code": "invalid_turn",
 "message": "It is not this seat's turn.",
 "details": {
 "seat": "south",
 "current_turn_seat": "east"
 }
 }
 }

Status: 409 Conflict

 {
 "error": {
 "code": "action_not_allowed",
 "message": "This action is not legal in the current phase.",
 "details": {
 "phase": "charleston",
 "action": "discard"
 }
 }
 }

Status: 409 Conflict

 {
 "error": {
 "code": "state_conflict",
 "message": "Mahjong declaration is not valid for the current hand.",
 "details": {
 "action": "declare_mahjong"
 }
 }
 }

Status: 404 Not Found

 {
 "error": {
 "code": "game_not_found",
 "message": "No practice game exists for the given game_id.",
 "details": {
 "game_id": "game_missing"
 }
 }
 }

---

## 6) Resolve AI turn

### POST /api/v1/practice-games/<game_id>/ai-turn

Advances one AI decision cycle. The frontend calls this route whenever the current prompt indicates AI resolution is needed.

For v1 this route is intentionally explicit rather than automatic, so the UI can animate turns and present beginner explanations.

### Request Body

 {
 "seat": "south"
 }

### Request Fields

- seat: optional string enum
 - east
 - south
 - west
 - north

If seat is omitted, backend resolves the current non-human actor.
If seat is provided and does not match the next resolvable AI actor, backend returns 409.

### Success Response

Status: 200 OK

 {
 "result": {
 "accepted": true,
 "resolved_actor_seat": "south",
 "decision_summary": {
 "action": "draw_then_discard",
 "reasoning_level": "beginner",
 "message": "Bot 1 drew from the wall and discarded West."
 },
 "state": {
 "game_id": "game_01hx8r7w2m3p",
 "status": "in_progress",
 "phase": "player_turn",
 "difficulty": "beginner",
 "dealer_seat": "east",
 "player_seat": "east",
 "current_turn_seat": "east",
 "hand_number": 1,
 "charleston": {
 "phase": "complete",
 "pass_index": 3,
 "pass_direction": "across",
 "optional": false,
 "pending_seats": [],
 "completed_passes": []
 },
 "wall": {
 "tiles_remaining": 62,
 "live_wall_remaining": 62,
 "dead_wall_remaining": 0
 },
 "players": [],
 "discard_pile": [],
 "last_discard": {
 "seat": "south",
 "tile": {
 "tile_id": "tile_089",
 "code": "west_wind",
 "group": "wind",
 "suit": null,
 "rank": null,
 "label": "West",
 "art_asset": "tiles/west_wind.svg"
 }
 },
 "turn_prompt": {
 "actor_seat": "east",
 "allowed_actions": ["draw", "call", "declare_mahjong"],
 "message": "Your turn."
 },
 "winner": null,
 "winning_source": null,
 "winning_hand_name": null
 }
 }
 }

### Error Responses

Status: 409 Conflict

 {
 "error": {
 "code": "ai_not_ready",
 "message": "No AI turn is ready to resolve.",
 "details": {
 "phase": "player_turn"
 }
 }
 }

Status: 409 Conflict

 {
 "error": {
 "code": "invalid_turn",
 "message": "The requested AI seat is not the next actor.",
 "details": {
 "seat": "west",
 "expected_seat": "south"
 }
 }
 }

Status: 404 Not Found

 {
 "error": {
 "code": "game_not_found",
 "message": "No practice game exists for the given game_id.",
 "details": {
 "game_id": "game_missing"
 }
 }
 }

Status: 500 Internal Server Error

 {
 "error": {
 "code": "internal_error",
 "message": "Unable to resolve AI turn.",
 "details": {}
 }
 }

---

## 7) Reset practice game

### POST /api/v1/practice-games/<game_id>/reset

Resets an existing practice game back to a fresh initial state, preserving the selected difficulty unless a new difficulty is provided.

### Request Body

 {
 "difficulty": "intermediate",
 "player_name": "Player"
 }

All fields optional.

### Request Fields

- difficulty: optional string enum
 - beginner
 - intermediate
 - challenger
- player_name: optional string

### Success Response

Status: 200 OK

 {
 "game": {
 "reset": true,
 "state": {
 "game_id": "game_01hx8r7w2m3p",
 "status": "in_progress",
 "phase": "charleston",
 "difficulty": "intermediate",
 "dealer_seat": "east",
 "player_seat": "east",
 "current_turn_seat": "east",
 "hand_number": 1,
 "charleston": {
 "phase": "right",
 "pass_index": 1,
 "pass_direction": "right",
 "optional": false,
 "pending_seats": ["east", "south", "west", "north"],
 "completed_passes": []
 },
 "wall": {
 "tiles_remaining": 96,
 "live_wall_remaining": 96,
 "dead_wall_remaining": 0
 },
 "players": [],
 "discard_pile": [],
 "last_discard": null,
 "turn_prompt": {
 "actor_seat": "east",
 "allowed_actions": ["charleston_pass"],
 "message": "Choose three tiles to pass right."
 },
 "winner": null,
 "winning_source": null,
 "winning_hand_name": null
 }
 }
 }

### Error Responses

Status: 400 Bad Request

 {
 "error": {
 "code": "invalid_difficulty",
 "message": "Difficulty must be one of beginner, intermediate, challenger.",
 "details": {
 "difficulty": "master"
 }
 }
 }

Status: 404 Not Found

 {
 "error": {
 "code": "game_not_found",
 "message": "No practice game exists for the given game_id.",
 "details": {
 "game_id": "game_missing"
 }
 }
 }

Status: 500 Internal Server Error

 {
 "error": {
 "code": "internal_error",
 "message": "Unable to reset practice game.",
 "details": {}
 }
 }

---

# Stable Curriculum Content Schema

This schema defines the JSON data file loaded by the backend and returned from GET /api/v1/curriculum.

## Top-Level Shape

 {
 "version": "v1",
 "title": "SuitUp Beginner Course",
 "audience": "absolute_beginner",
 "estimated_total_minutes": 180,
 "units": []
 }

## Curriculum Object

Fields:
- version: required string
- title: required string
- audience: required string enum
 - absolute_beginner
- estimated_total_minutes: required integer, minimum 1
- units: required array of CurriculumUnit, minimum 1

## CurriculumUnit

 {
 "id": "welcome_and_setup",
 "slug": "welcome-and-setup",
 "title": "Welcome and Table Setup",
 "description": "Learn what comes in the set and how to prepare the table.",
 "estimated_minutes": 20,
 "order": 1,
 "prerequisite_unit_ids": [],
 "learning_objectives": [
 "Identify the main tile groups."
 ],
 "lessons": []
 }

Fields:
- id: required string, unique across units
- slug: required string, unique across units
- title: required string
- description: required string
- estimated_minutes: required integer, minimum 1
- order: required integer, minimum 1
- prerequisite_unit_ids: required array of unit ids
- learning_objectives: required array of strings, minimum 1
- lessons: required array of CurriculumLesson, minimum 1

## CurriculumLesson

 {
 "id": "meet_the_tiles",
 "slug": "meet-the-tiles",
 "title": "Meet the Tiles",
 "description": "A visual introduction to suits, honors, flowers, and jokers.",
 "estimated_minutes": 8,
 "order": 1,
 "step_count": 3,
 "steps": []
 }

Fields:
- id: required string, unique within curriculum
- slug: required string
- title: required string
- description: required string
- estimated_minutes: required integer, minimum 1
- order: required integer, minimum 1
- step_count: required integer; must equal length of steps
- steps: required array of CurriculumStep, minimum 1

## CurriculumStep

 {
 "id": "tiles_intro",
 "order": 1,
 "type": "content",
 "title": "The American Mah Jongg Tile Set",
 "body_markdown": "American Mah Jongg uses 152 tiles...",
 "media": {
 "kind": "svg_plate",
 "asset_id": "tile-groups-overview"
 },
 "callouts": [
 {
 "tone": "tip",
 "title": "Beginner tip",
 "body": "Flowers and jokers are special groups."
 }
 ],
 "knowledge_checks": [],
 "practice_link": null
 }

Fields:
- id: required string, unique within lesson
- order: required integer, minimum 1
- type: required string enum
 - content
 - guided_check
 - drill
 - practice_bridge
- title: required string
- body_markdown: required string
- media: nullable object of type StepMedia
- callouts: required array of StepCallout
- knowledge_checks: required array of KnowledgeCheck
- practice_link: nullable object of type PracticeLink

## StepMedia

 {
 "kind": "svg_plate",
 "asset_id": "tile-groups-overview"
 }

Fields:
- kind: required string enum
 - svg_tile
 - svg_plate
 - svg_rack
 - diagram
 - none
- asset_id: required string unless kind is none

## StepCallout

 {
 "tone": "tip",
 "title": "Beginner tip",
 "body": "Flowers and jokers are special groups."
 }

Fields:
- tone: required string enum
 - tip
 - warning
 - remember
- title: required string
- body: required string

## KnowledgeCheck

 {
 "id": "kc_tile_total",
 "prompt": "How many tiles are in an American Mah Jongg set?",
 "type": "multiple_choice",
 "options": [
 {
 "id": "a",
 "label": "144"
 },
 {
 "id": "b",
 "label": "152"
 }
 ],
 "correct_option_ids": ["b"],
 "explanation_markdown": "American Mah Jongg uses 152 tiles."
 }

Fields:
- id: required string
- prompt: required string
- type: required string enum
 - multiple_choice
 - multi_select
 - true_false
- options: required array of CheckOption, minimum 2
- correct_option_ids: required array of option ids, minimum 1
- explanation_markdown: required string

## CheckOption

 {
 "id": "b",
 "label": "152"
 }

Fields:
- id: required string
- label: required string

## PracticeLink

 {
 "mode": "charleston_demo",
 "difficulty": "beginner",
 "focus": "right_pass"
 }

Fields:
- mode: required string enum
 - setup_demo
 - charleston_demo
 - full_hand_practice
- difficulty: required string enum
 - beginner
 - intermediate
 - challenger
- focus: required string

---

# Stable Rules Reference Schema

This schema defines the JSON data returned from GET /api/v1/rules-reference.

## Top-Level Shape

 {
 "version": "v1",
 "title": "American Mah Jongg Rules Reference",
 "sections": []
 }

## RuleSection

 {
 "id": "tile_set",
 "title": "Tile Set",
 "order": 1,
 "summary": "The full American Mah Jongg set contains 152 tiles.",
 "entries": []
 }

Fields:
- id: required string, unique across sections
- title: required string
- order: required integer, minimum 1
- summary: required string
- entries: required array of RuleEntry, minimum 1

## RuleEntry

 {
 "id": "tile_set_counts",
 "label": "Tile count",
 "body_markdown": "Three suits 1-9, four of each, plus winds, dragons, flowers, and jokers.",
 "facts": [
 {
 "key": "total_tiles",
 "value": 152
 }
 ]
 }

Fields:
- id: required string
- label: required string
- body_markdown: required string
- facts: required array of RuleFact

## RuleFact

 {
 "key": "total_tiles",
 "value": 152
 }

Fields:
- key: required string
- value: required scalar
 - string, number, or boolean

---

# Stable Practice Game-State Schema

This schema defines the exact game-state object the practice table expects.
The backend must always return the full state object, not patches.

## Top-Level Game State

 {
 "game_id": "game_01hx8r7w2m3p",
 "status": "in_progress",
 "phase": "player_turn",
 "difficulty": "beginner",
 "dealer_seat": "east",
 "player_seat": "east",
 "current_turn_seat": "east",
 "hand_number": 1,
 "charleston": {
 "phase": "complete",
 "pass_index": 3,
 "pass_direction": "across",
 "optional": false,
 "pending_seats": [],
 "completed_passes": []
 },
 "wall": {
 "tiles_remaining": 64,
 "live_wall_remaining": 64,
 "dead_wall_remaining": 0
 },
 "players": [],
 "discard_pile": [],
 "last_discard": null,
 "turn_prompt": {
 "actor_seat": "east",
 "allowed_actions": ["draw", "discard", "declare_mahjong"],
 "message": "Your turn."
 },
 "winner": null,
 "winning_source": null,
 "winning_hand_name": null
 }

## GameState Fields

- game_id: required string
- status: required string enum
 - in_progress
 - complete
 - aborted
- phase: required string enum
 - charleston
 - player_turn
 - awaiting_calls
 - ai_turn
 - scored
- difficulty: required string enum
 - beginner
 - intermediate
 - challenger
- dealer_seat: required string enum
 - east
 - south
 - west
 - north
- player_seat: required string enum
 - east
 - south
 - west
 - north
- current_turn_seat: required string enum
 - east
 - south
 - west
 - north
- hand_number: required integer, minimum 1
- charleston: required CharlestonState
- wall: required WallState
- players: required array of 4 PlayerState objects in fixed seat order:
 - east
 - south
 - west
 - north
- discard_pile: required array of TileView
- last_discard: nullable LastDiscard
- turn_prompt: required TurnPrompt
- winner: nullable WinnerSummary
- winning_source: nullable string enum
 - self_draw
 - discard_call
- winning_hand_name: nullable string

## CharlestonState

 {
 "phase": "right",
 "pass_index": 1,
 "pass_direction": "right",
 "optional": false,
 "pending_seats": ["east", "south", "west", "north"],
 "completed_passes": [
 {
 "direction": "right",
 "from_seat": "east",
 "tile_count": 3
 }
 ]
 }

Fields:
- phase: required string enum
 - not_started
 - right
 - across
 - left
 - optional_across
 - complete
- pass_index: required integer, minimum 0
- pass_direction: nullable string enum
 - right
 - across
 - left
- optional: required boolean
- pending_seats: required array of seat enums
- completed_passes: required array of CharlestonPassSummary

## CharlestonPassSummary

 {
 "direction": "right",
 "from_seat": "east",
 "tile_count": 3
 }

Fields:
- direction: required string enum
 - right
 - across
 - left
- from_seat: required string enum
 - east
 - south
 - west
 - north
- tile_count: required integer; for v1 must be 3

## WallState

 {
 "tiles_remaining": 64,
 "live_wall_remaining": 64,
 "dead_wall_remaining": 0
 }

Fields:
- tiles_remaining: required integer, minimum 0
- live_wall_remaining: required integer, minimum 0
- dead_wall_remaining: required integer, minimum 0

Constraint:
- tiles_remaining must equal live_wall_remaining + dead_wall_remaining

## PlayerState

 {
 "seat": "east",
 "name": "Player",
 "is_human": true,
 "difficulty": null,
 "hand": [
 {
 "tile_id": "tile_001",
 "code": "1_dot",
 "group": "suit",
 "suit": "dots",
 "rank": 1,
 "label": "1 Dot",
 "art_asset": "tiles/1_dot.svg"
 }
 ],
 "hand_count": 14,
 "exposures": [],
 "discards_taken": [],
 "declared": false,
 "mahjong": false
 }

Fields:
- seat: required string enum
 - east
 - south
 - west
 - north
- name: required string
- is_human: required boolean
- difficulty: nullable string enum for AI players
 - beginner
 - intermediate
 - challenger
- hand: array of TileView for human player; null for hidden AI hands
- hand_count: required integer, minimum 0
- exposures: required array of Exposure
- discards_taken: required array of TileView
- declared: required boolean
- mahjong: required boolean

## Exposure

 {
 "kind": "pon",
 "tiles": [
 {
 "tile_id": "tile_021",
 "code": "red_dragon",
 "group": "dragon",
 "suit": null,
 "rank": null,
 "label": "Red Dragon",
 "art_asset": "tiles/red_dragon.svg"
 }
 ],
 "called_from_seat": "north"
 }

Fields:
- kind: required string enum
 - pon
 - kong
 - quint
 - pair
 - declared_set
- tiles: required array of TileView, minimum 2
- called_from_seat: nullable seat enum

## TileView

 {
 "tile_id": "tile_001",
 "code": "1_dot",
 "group": "suit",
 "suit": "dots",
 "rank": 1,
 "label": "1 Dot",
 "art_asset": "tiles/1_dot.svg"
 }

Fields:
- tile_id: required string, unique within a game instance
- code: required string stable tile code
- group: required string enum
 - suit
 - wind
 - dragon
 - flower
 - joker
- suit: nullable string enum
 - dots
 - bams
 - craks
- rank: nullable integer
 - 1 through 9 for suit tiles only
- label: required string
- art_asset: required string relative asset path

## LastDiscard

 {
 "seat": "north",
 "tile": {
 "tile_id": "tile_089",
 "code": "west_wind",
 "group": "wind",
 "suit": null,
 "rank": null,
 "label": "West",
 "art_asset": "tiles/west_wind.svg"
 }
 }

Fields:
- seat: required seat enum
- tile: required TileView

## TurnPrompt

 {
 "actor_seat": "east",
 "allowed_actions": ["draw", "discard", "declare_mahjong"],
 "message": "Your turn."
 }

Fields:
- actor_seat: required seat enum
- allowed_actions: required array of action enums
 - charleston_pass
 - draw
 - discard
 - call
 - declare_mahjong
 - resolve_ai_turn
- message: required string

## WinnerSummary

 {
 "seat": "east",
 "name": "Player"
 }

Fields:
- seat: required seat enum
- name: required string

---

# Route-to-Schema Mapping

## GET /api/v1/curriculum

Returns:

 {
 "curriculum": Curriculum
 }

## GET /api/v1/rules-reference

Returns:

 {
 "rules_reference": RulesReference
 }

## POST /api/v1/practice-games

Request:

 {
 "difficulty": Difficulty,
 "player_name": "string?",
 "curriculum_context": {
 "unit_id": "string?",
 "lesson_id": "string?",
 "step_id": "string?"
 },
 "seed": "integer?"
 }

Response:

 {
 "game": {
 "game_id": "string",
 "created": true,
 "difficulty": Difficulty,
 "state": GameState
 }
 }

## GET /api/v1/practice-games/<game_id>

Returns:

 {
 "game": {
 "state": GameState
 }
 }

## POST /api/v1/practice-games/<game_id>/actions

Request:

 {
 "action": ActionName,
 "seat": Seat,
 "payload": {}
 }

Response:

 {
 "result": {
 "accepted": true,
 "action": ActionName,
 "resolved": true,
 "state": GameState
 }
 }

## POST /api/v1/practice-games/<game_id>/ai-turn

Request:

 {
 "seat": "Seat?"
 }

Response:

 {
 "result": {
 "accepted": true,
 "resolved_actor_seat": Seat,
 "decision_summary": {
 "action": "string",
 "reasoning_level": Difficulty,
 "message": "string"
 },
 "state": GameState
 }
 }

## POST /api/v1/practice-games/<game_id>/reset

Request:

 {
 "difficulty": "Difficulty?",
 "player_name": "string?"
 }

Response:

 {
 "game": {
 "reset": true,
 "state": GameState
 }
 }

---

# Frontend Expectations

The frontend may assume:

- every successful practice-game route returns a complete GameState
- players array is always length 4 in seat order east, south, west, north
- only the human player's hand is exposed in full
- AI hands are hidden by returning hand: null and hand_count as the visible count
- last_discard is null when no discard exists yet
- winner, winning_source, and winning_hand_name are null until the hand ends
- charleston is always present, even after completion
- difficulty is repeated on the game and state objects for convenience and stability

The backend may assume:

- frontend will only send action names listed in this document
- frontend will treat unknown future fields as ignorable
- frontend will not infer rules from UI state that are not explicitly returned by the API

---

# Backward Compatibility Rules for v1

- Existing field names and enum values in this document are frozen for v1.
- New optional fields may be added without breaking clients.
- Required fields may not be removed or renamed in v1.
- Enum values may not be repurposed in v1.
- Route paths may not change in v1.
- Response wrappers curriculum, rules_reference, game, and result are stable and required.

---

# Minimal Validation Requirements

Backend validators must enforce at least:

- create game difficulty is valid
- reset difficulty is valid if provided
- action is known
- seat is valid
- charleston_pass contains exactly 3 tile_ids
- discard contains one tile_id that exists in the acting hand
- call_type is supported
- declared mahjong is rules-legal before completing the action
- actions match current game phase and current actor
- game_id must exist for all game-specific routes

Frontend validators should enforce at least:

- required payload fields before submit
- only allowed_actions for the current prompt are presented as clickable controls
- AI turn button only appears when allowed_actions includes resolve_ai_turn