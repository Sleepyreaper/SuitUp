"use strict";
/* SuitUp — the playable simulator UI ("Play" tab).
   A full table: your rack, 3 AI opponents, wall, discards, Charleston, calling,
   scoring, and a toggleable Coach overlay that teaches as you play. Talks to the
   stateful /api/game/* endpoints. Dependency-free vanilla JS. */
(function () {
  const T = window.SUITUP_TUTORIAL || { contextual: {}, glossary: {}, intro: {} };
  const PLAY = { id: null, snap: null, selected: [], coach: true, guided: true, level: "mixed" };

  const LEVELS = {
    easy: [1, 1, 1], mixed: [1, 2, 3], hard: [3, 3, 3],
  };

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  }

  async function post(url, body) {
    const r = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body || {}),
    });
    return r.json();
  }
  async function get(url) {
    const r = await fetch(url);
    return r.json();
  }

  /* ---------- lifecycle ---------- */
  async function renderPlay() {
    const host = document.getElementById("view");
    if (!PLAY.id) {
      let hands = [];
      try { hands = (await get("/api/game-hands")).hands || []; } catch (e) { hands = []; }
      host.innerHTML = setupHTML(hands);
      wireSetup(host);
      return;
    }
    const data = await get(`/api/game/${PLAY.id}`);
    if (data.error) { PLAY.id = null; return renderPlay(); }
    PLAY.snap = data.state;
    draw(host);
  }

  function setupHTML(hands) {
    const intro = T.intro || { title: "", points: [] };
    const handRows = (hands || []).map((h) =>
      `<li><strong>${esc(h.name)}</strong> <span class="pill ${h.difficulty === "intro" ? "" : h.difficulty === "building" ? "gold" : "optional"}">${esc(h.difficulty)}</span> — ${esc(h.structure)} · <em>${h.points} pts</em><br><span class="muted">${esc(h.teaches)}</span></li>`
    ).join("");
    return `
      <h2 class="section-title">Play — Mah Jongg Simulator 🀄</h2>
      <div class="card">
        <h3>${esc(intro.title)}</h3>
        <ul class="intro-list">${(intro.points || []).map((p) => `<li>${esc(p)}</li>`).join("")}</ul>
      </div>
      ${handRows ? `<div class="card"><h3>Hands you can win with</h3>
        <ul class="hand-list">${handRows}</ul>
        <p class="muted">At a real table you'd match a line on the 2026 NMJL card instead — the mechanics are the same.</p></div>` : ""}
      <div class="card setup-card">
        <h3>Start a new game</h3>
        <label class="setup-row">Opponent difficulty:
          <select id="lvl">
            <option value="easy">Easy — 3 beginner bots</option>
            <option value="mixed" selected>Mixed — beginner, improver, sharp</option>
            <option value="hard">Hard — 3 sharp bots</option>
          </select>
        </label>
        <label class="setup-row"><input type="checkbox" id="guideChk" checked>
          <strong>Guided walkthrough</strong> — walk me through every step (best for your first game)</label>
        <label class="setup-row"><input type="checkbox" id="coachChk" checked>
          Show the Coach overlay (teaches terms as you play)</label>
        <button id="newGameBtn" class="btn btn-primary">Deal &amp; Start</button>
      </div>`;
  }

  function wireSetup(host) {
    host.querySelector("#newGameBtn").onclick = async () => {
      PLAY.level = host.querySelector("#lvl").value;
      PLAY.coach = host.querySelector("#coachChk").checked;
      PLAY.guided = host.querySelector("#guideChk").checked;
      const data = await post("/api/game/new", { ai_levels: LEVELS[PLAY.level] });
      PLAY.id = data.game_id;
      PLAY.snap = data.state;
      PLAY.selected = [];
      draw(host);
    };
  }

  /* ---------- main table render ---------- */
  function draw(host) {
    const s = PLAY.snap;
    const step = guideStep(s);
    PLAY._step = step;
    PLAY._guideIds = new Set((step && step.tiles) || []);
    host.innerHTML = `
      <div class="table-top">
        <div class="tbl-info">
          <strong>Hand ${s.hand_number}</strong> · Dealer ${esc(s.dealer)} · Target ${s.target_score} pts
        </div>
        <div class="tbl-actions">
          <button id="guideToggle" class="btn btn-ghost">${PLAY.guided ? "Guidance: ON" : "Guidance: off"}</button>
          <button id="coachToggle" class="btn btn-ghost">${PLAY.coach ? "Hide" : "Show"} Coach</button>
          <button id="quitBtn" class="btn btn-ghost">New Game</button>
        </div>
      </div>
      ${PLAY.guided && step ? guideBannerHTML(step) : ""}
      <div class="mj-wrap">
        <div class="mj-table">
          <div class="seat-slot slot-top">${oppPanel(POS(s).top, "top")}</div>
          <div class="seat-slot slot-left">${oppPanel(POS(s).left, "left")}</div>
          <div class="seat-slot slot-right">${oppPanel(POS(s).right, "right")}</div>
          <div class="mj-center">
            <div class="phase-banner ${s.your_turn ? "you-turn" : ""}">${esc(phaseLabel(s))}</div>
            ${wallHTML(s)}
          </div>
          <div class="seat-slot slot-you">${youPanel(s)}</div>
        </div>
        ${PLAY.coach ? coachHTML(s) : ""}
      </div>
      ${correctionHTML()}
      <div class="action-bar" id="actionBar">${actionHTML(s)}</div>
      ${logHTML(s)}`;
    wire(host);
  }

  /* ---------- guided walkthrough ---------- */
  function isFlowerId(id) { return String(id).indexOf("flower") === 0; }

  function recommendedPass(s) {
    const dead = ((s.hint && s.hint.deadwood) || [])
      .filter((t) => !t.joker && !t.flower && !isFlowerId(t.id)).map((t) => t.id);
    if (dead.length >= 3) return dead.slice(0, 3);
    const extra = s.you.concealed
      .filter((t) => !t.joker && !t.flower && !isFlowerId(t.id) && dead.indexOf(t.id) < 0)
      .map((t) => t.id);
    return dead.concat(extra).slice(0, 3);
  }

  function recommendedDiscard(s) {
    const flower = s.you.concealed.find((t) => t.flower || isFlowerId(t.id));
    if (flower) return flower.id;                          // flowers rarely help — shed first
    const dead = (s.hint && s.hint.deadwood) || [];
    if (dead.length) return dead[0].id;
    const nonJ = s.you.concealed.filter((t) => !t.joker);
    return (nonJ[0] || s.you.concealed[0]).id;
  }

  function guideStep(s) {
    if (!PLAY.guided) return null;
    if (s.phase === "charleston" && s.charleston) {
      const tiles = recommendedPass(s);
      return { do: `Pass 3 tiles to your ${s.charleston.direction.toUpperCase()}.`,
        why: "The highlighted tiles help your hand the least. Click all 3 (or use “Do it for me”), then Pass. Never pass Jokers or Flowers.",
        tiles, btn: "#passBtn", act: "pass" };
    }
    if (s.phase === "charleston" && s.charleston_second_offered) {
      return { do: `Click “Start playing”.`,
        why: "The first Charleston is done. New players usually skip the optional second round.",
        btn: "#secondNo", act: "click" };
    }
    if (s.phase === "play" && s.pending_calls && s.pending_calls.length) {
      if (s.pending_calls.indexOf("win") >= 0)
        return { do: `You can WIN — click “Declare Mah Jongg!”`, btn: ".callBtn.btn-win", act: "click" };
      return { do: `While you're learning, click “Pass”.`,
        why: "You could call this tile to expose a group, but that reveals part of your hand and locks you in. Passing keeps you flexible.",
        btn: "#passCall", act: "click" };
    }
    if (s.phase === "play" && s.your_turn && s.sub === "draw") {
      return { do: `Click “Draw a tile”.`,
        why: "Your turn always starts by drawing one tile from the wall.",
        btn: "#drawBtn", act: "click" };
    }
    if (s.phase === "play" && s.your_turn && s.sub === "discard") {
      if (PLAY._canWin)
        return { do: `Your hand is complete — click “Declare Mah Jongg”!`, btn: "#declareBtn", act: "click" };
      const rec = recommendedDiscard(s);
      return { do: `Discard the highlighted tile to end your turn.`,
        why: `It's your least useful tile for your best hand${s.hint ? " (" + s.hint.target + ")" : ""}. Click it, then Discard — you'll be back to 13 tiles.`,
        tiles: rec ? [rec] : [], btn: "#discardBtn", act: "discard", one: rec };
    }
    if (s.phase === "hand_over")
      return { do: `Hand over — click “Deal next hand” to keep practicing.`, btn: "#nextHand", act: "click" };
    if (s.phase === "game_over")
      return { do: `Game over! Start a new game whenever you like.`, btn: "#quitBtn2", act: "click" };
    return { do: `Watch the other players draw and discard — your turn is coming.`, wait: true };
  }

  function guideBannerHTML(step) {
    const doBtn = step.wait ? "" : `<button id="guideDo" class="btn btn-primary">✨ Do it for me</button>`;
    return `<div class="guide-banner">
      <div class="guide-lead">👉 Do this now</div>
      <div class="guide-text"><strong>${esc(step.do)}</strong>${step.why ? `<p>${esc(step.why)}</p>` : ""}</div>
      <div class="guide-btns">${doBtn}<button id="guideOff" class="btn btn-ghost">Turn off guidance</button></div>
    </div>`;
  }

  async function doGuided(host) {
    const step = PLAY._step;
    if (!step) return;
    if (step.act === "pass") {
      PLAY.selected = (step.tiles || []).slice(0, 3);
      draw(host);
      const r = await act(`/api/game/${PLAY.id}/charleston`, { tile_ids: PLAY.selected });
      if (!correct(r)) PLAY.selected = [];
      draw(host);
    } else if (step.act === "discard") {
      const r = await act(`/api/game/${PLAY.id}/discard`, { tile_id: step.one });
      if (!correct(r)) { PLAY.selected = []; PLAY._canWin = false; PLAY._justDrew = null; }
      draw(host);
    } else if (step.act === "click" && step.btn) {
      const el = host.querySelector(step.btn);
      if (el) el.click();
    }
  }

  const SEAT_ORDER = ["East", "South", "West", "North"];
  function POS(s) {
    const hi = SEAT_ORDER.indexOf(s.you.seat);
    const out = {};
    (s.opponents || []).forEach((o) => {
      const off = (SEAT_ORDER.indexOf(o.seat) - hi + 4) % 4;
      out[off === 1 ? "right" : off === 2 ? "top" : "left"] = o;
    });
    return out;
  }

  function tileHTML(t, opts) {
    opts = opts || {};
    const cls = ["tile"];
    if (opts.selectable) cls.push("selectable");
    if (PLAY.selected.includes(t.id)) cls.push("selected");
    if (opts.dead) cls.push("dead");
    if (opts.drew) cls.push("drew");
    if (opts.fresh) cls.push("enter");
    if (opts.joker || t.joker) cls.push("joker");
    if (PLAY._guideIds && PLAY._guideIds.has(t.id)) cls.push("guide");
    return `<span class="${cls.join(" ")}" data-id="${esc(t.id)}" title="${esc(t.name)}">${t.svg || esc(t.name)}</span>`;
  }

  function backHTML(n, cls) {
    let out = "";
    for (let i = 0; i < n; i++) out += `<span class="tile back ${cls || ""}"></span>`;
    return out;
  }

  function expHTML(exps) {
    if (!exps || !exps.length) return "";
    return exps.map((e) => {
      const jk = e.joker_count ? `<span class="exp-jk" title="uses ${e.joker_count} joker(s)">J</span>` : "";
      return `<span class="exposure" title="${esc(e.group_type)}">${e.tiles.map((t) => tileHTML(t)).join("")}${jk}</span>`;
    }).join(" ");
  }

  function oppPanel(o, where) {
    if (!o) return "";
    return `<div class="opp ${where} ${o.is_turn ? "turn" : ""}">
      <div class="opp-head">
        <span class="seat-tag">${esc(o.seat)}</span>
        <span class="lvl-badge">AI ${o.level}</span>
        <span class="opp-score">${o.score}★${o.hands_won || 0}</span>
        ${o.is_turn ? '<span class="turn-dot">●</span>' : ""}
      </div>
      <div class="opp-rack">${backHTML(o.concealed_count, "mini")}</div>
      ${o.exposures.length ? `<div class="opp-exp">${expHTML(o.exposures)}</div>` : ""}
    </div>`;
  }

  const DICE_FACES = ["", "⚀", "⚁", "⚂", "⚃", "⚄", "⚅"];
  function diceHTML(d) {
    if (!d) return "";
    return `<div class="dice-roll" title="The dealer's roll sets where the wall is broken">
      <span class="die">${DICE_FACES[d.die1] || d.die1}</span>
      <span class="die">${DICE_FACES[d.die2] || d.die2}</span>
      <span class="dice-total">= ${d.total}</span>
    </div>`;
  }

  function wallHTML(s) {
    const n = s.wall_remaining;
    const stacks = Math.ceil(n / 2);                 // real walls are stacked 2 high
    const per = Math.ceil(stacks / 4);
    let rem = stacks;
    const take = () => { const k = Math.max(0, Math.min(per, rem)); rem -= k; return k; };
    const top = take(), right = take(), bottom = take(), left = Math.max(0, rem);
    const stk = (k, cls) => { let o = ""; for (let i = 0; i < k; i++) o += `<span class="wall-stack ${cls}"></span>`; return o; };
    const last = s.discards.length - 1;
    const disc = s.discards.length
      ? s.discards.map((t, i) => tileHTML(t, { discard: true, fresh: i === last })).join("")
      : `<span class="muted">no discards yet</span>`;
    return `<div class="wall-area">
      ${diceHTML(s.dice)}
      <div class="wall-ring">
        <div class="wr-top">${stk(top, "h")}</div>
        <div class="wr-left">${stk(left, "v")}</div>
        <div class="wr-center">
          <div class="discards-label">Discards${s.last_discarder ? " · last by " + esc(s.last_discarder) : ""}</div>
          <div class="discard-grid">${disc}</div>
        </div>
        <div class="wr-right">${stk(right, "v")}</div>
        <div class="wr-bottom">${stk(bottom, "h")}</div>
      </div>
      <div class="wall-label">🀫 Wall — <strong>${n}</strong> tiles (${stacks} stacks, 2 high)</div>
    </div>`;
  }

  function youPanel(s) {
    const you = s.you;
    const deadIds = (s.hint && s.hint.deadwood ? s.hint.deadwood : []).map((t) => t.id);
    const selectable = canSelectTiles(s);
    const rack = you.concealed.map((t) =>
      tileHTML(t, { selectable, dead: deadIds.includes(t.id), drew: t.id === PLAY._justDrew })).join("");
    return `<div class="you-panel ${s.your_turn ? "turn" : ""}">
      <div class="you-head">
        <span class="seat-tag you-tag">You · ${esc(you.seat)}${s.dealer === you.seat ? " · Dealer" : ""}</span>
        <span class="you-score">${you.score} pts · ${you.hands_won}★ won</span>
      </div>
      ${you.exposures.length ? `<div class="you-exp"><span class="lbl">Exposed:</span> ${expHTML(you.exposures)}</div>` : ""}
      <div class="rack">${rack}</div>
    </div>`;
  }

  function correctionHTML() {
    const c = PLAY._correction;
    if (!c) return "";
    return `<div class="correction">
      <span class="cx-icon">🛑</span>
      <div class="cx-body"><strong>${esc(c.msg)}</strong>${c.why ? `<p>${esc(c.why)}</p>` : ""}</div>
      <button id="cxClose" class="btn btn-ghost">Got it</button>
    </div>`;
  }

  function correct(data) {
    const r = data && data.result;
    if (r && r.ok === false) {
      const msg = r.error || "That move isn't allowed.";
      let why = "";
      (T.illegal || []).some((e) => {
        if (msg.toLowerCase().includes(e.match.toLowerCase())) { why = e.why; return true; }
        return false;
      });
      PLAY._correction = { msg, why };
      return true;
    }
    PLAY._correction = null;
    return false;
  }

  function phaseLabel(s) {
    if (s.phase === "charleston") {
      if (s.charleston) return `Charleston — pass ${s.charleston.direction.toUpperCase()}`;
      if (s.charleston_second_offered) return "Charleston — second round?";
      return "Charleston";
    }
    if (s.phase === "play") {
      if (s.pending_calls && s.pending_calls.length) return "You can call the discard!";
      if (s.your_turn) return s.sub === "draw" ? "Your turn — draw" : "Your turn — discard";
      return `${esc(s.turn)} is playing…`;
    }
    if (s.phase === "hand_over") return "Hand over";
    if (s.phase === "game_over") return "Game over";
    return s.phase;
  }

  /* ---------- selection rules ---------- */
  function canSelectTiles(s) {
    if (s.phase === "charleston" && s.charleston) return true;
    if (s.phase === "play" && s.your_turn && s.sub === "discard") return true;
    return false;
  }
  function maxSelect(s) {
    if (s.phase === "charleston" && s.charleston) return 3;
    return 1;
  }

  /* ---------- action bar ---------- */
  function actionHTML(s) {
    if (s.phase === "charleston" && s.charleston) {
      return `<div class="hintline">${esc(s.charleston.note)}</div>
        <button id="passBtn" class="btn btn-primary">Pass 3 tiles (${PLAY.selected.length}/3)</button>`;
    }
    if (s.phase === "charleston" && s.charleston_second_offered) {
      return `<div class="hintline">First Charleston done. A second round is optional — any player may stop.</div>
        <button id="secondYes" class="btn">Do a second Charleston</button>
        <button id="secondNo" class="btn btn-primary">Start playing</button>`;
    }
    if (s.phase === "play" && s.pending_calls && s.pending_calls.length) {
      const btns = s.pending_calls.map((k) => {
        const label = k === "win" ? "Declare Mah Jongg!" : "Call " + k.toUpperCase();
        const cls = k === "win" ? "btn btn-win" : "btn btn-primary";
        return `<button class="${cls} callBtn" data-kind="${k}">${label}</button>`;
      }).join("");
      return `<div class="hintline">A tile you can use was discarded.</div>${btns}
        <button id="passCall" class="btn btn-ghost">Pass</button>`;
    }
    if (s.phase === "play" && s.your_turn && s.sub === "draw") {
      return `<button id="drawBtn" class="btn btn-primary">Draw a tile</button>${exchangeHTML(s)}`;
    }
    if (s.phase === "play" && s.your_turn && s.sub === "discard") {
      const win = `<button id="declareBtn" class="btn btn-win">Declare Mah Jongg</button>`;
      return `<button id="discardBtn" class="btn btn-primary">Discard selected (${PLAY.selected.length}/1)</button>
        ${(PLAY._canWin ? win : "")}${exchangeHTML(s)}`;
    }
    if (s.phase === "hand_over") {
      return winSummaryHTML(s) + `<button id="nextHand" class="btn btn-primary">Deal next hand</button>`;
    }
    if (s.phase === "game_over") {
      return winSummaryHTML(s) + finalScoresHTML(s) + `<button id="quitBtn2" class="btn btn-primary">New game</button>`;
    }
    return `<div class="muted">Waiting…</div>`;
  }

  function exchangeHTML(s) {
    const ex = s.joker_exchanges || [];
    if (!ex.length) return "";
    const btns = ex.map((e, i) =>
      `<button class="btn btn-ghost redeemBtn" data-i="${i}">♻ Redeem Joker from ${esc(e.seat)} — give your ${esc(e.tile_name)}</button>`
    ).join("");
    return `<div class="redeem-box"><div class="hintline">Joker exchange available: swap a real tile you hold for a Joker sitting in an exposure (yours or an opponent's).</div>${btns}</div>`;
  }

  function winSummaryHTML(s) {
    const wi = s.win_info;
    if (!wi) return "";
    if (wi.wall_game) return `<div class="win-box">🁢 Wall game — the wall ran out. A draw, nobody pays.</div>`;
    const sc = wi.scoring;
    const who = wi.is_human ? "You" : esc(wi.winner);
    const tiles = (wi.hand_tiles || []).map((t) => tileHTML(t)).join("");
    const dbl = [];
    if (sc.self_drawn) dbl.push("self-pick ×2");
    if (sc.jokerless) dbl.push("jokerless ×2");
    const lines = (sc.lines || []).map((l) =>
      `<div class="pay-line"><span>${esc(l.seat)}</span> pays <strong>${l.amount}</strong> <span class="muted">(${esc(l.reason)})</span></div>`).join("");
    return `<div class="win-box">
      <div class="win-head">🎉 ${who} won — ${esc(sc.hand_name)}</div>
      <div class="win-tiles">${tiles}</div>
      <div class="win-score">Hand value ${sc.value}${dbl.length ? " · " + dbl.join(" · ") : ""} · jokers used ${sc.jokers_used}</div>
      <div class="settlement">
        <div class="pay-head">💰 Settlement — ${who} collects <strong>${sc.total}</strong>:</div>
        ${lines}
      </div>
    </div>`;
  }

  function finalScoresHTML(s) {
    const rows = [{ seat: s.you.seat + " (You)", score: s.you.score }]
      .concat(s.opponents.map((o) => ({ seat: o.seat, score: o.score })))
      .sort((a, b) => b.score - a.score);
    return `<div class="final-scores"><strong>Final scores</strong>${rows.map((r) =>
      `<div>${esc(r.seat)}: ${r.score}</div>`).join("")}</div>`;
  }

  function logHTML(s) {
    return `<details class="log"><summary>Table log</summary>
      <ul>${(s.log || []).slice().reverse().map((l) => `<li>${esc(l)}</li>`).join("")}</ul></details>`;
  }

  /* ---------- coach overlay ---------- */
  function coachKey(s) {
    if (s.phase === "charleston") return s.charleston ? "charleston" : "charleston_second";
    if (s.phase === "play") {
      if (s.pending_calls && s.pending_calls.length) return "play:calls";
      if (s.your_turn) return "play:" + s.sub;
      return "play:watch";
    }
    return s.phase;
  }

  function coachHTML(s) {
    const ctx = T.contextual[coachKey(s)] || { title: "Coach", body: "", terms: [] };
    const hint = s.hint ? `
      <div class="coach-hint">
        <div class="coach-hint-head">Your best target</div>
        <div><strong>${esc(hint_target(s))}</strong> — ${esc(s.hint.target_desc)}</div>
        <div class="bar"><span style="width:${Math.round(s.hint.completeness * 100)}%"></span></div>
        <div class="muted">${s.hint.needed} tile(s) to go · deadwood is dimmed in your rack</div>
      </div>` : "";
    const terms = (ctx.terms || []).map((t) =>
      `<button class="term-chip" data-term="${esc(t)}">${esc(t)}</button>`).join("");
    return `<aside class="coach">
      <div class="coach-head">🧑‍🏫 Coach</div>
      <div class="coach-body">
        <h4>${esc(ctx.title)}</h4>
        <p>${esc(ctx.body)}</p>
        ${terms ? `<div class="coach-terms">${terms}</div>` : ""}
        ${hint}
        <div id="glossaryBox" class="glossary-box"></div>
      </div>
    </aside>`;
  }
  function hint_target(s) { return s.hint ? s.hint.target : ""; }

  /* ---------- wiring ---------- */
  function wire(host) {
    const s = PLAY.snap;
    const q = (id) => host.querySelector(id);
    const on = (id, fn) => { const e = q(id); if (e) e.onclick = fn; };

    on("#coachToggle", () => { PLAY.coach = !PLAY.coach; draw(host); });
    on("#guideToggle", () => { PLAY.guided = !PLAY.guided; draw(host); });
    on("#guideOff", () => { PLAY.guided = false; draw(host); });
    on("#guideDo", () => doGuided(host));
    const quit = () => { PLAY.id = null; PLAY.selected = []; PLAY._correction = null; renderPlay(); };
    on("#quitBtn", quit); on("#quitBtn2", quit);
    on("#cxClose", () => { PLAY._correction = null; draw(host); });

    // guided: glow the recommended action button
    if (PLAY.guided && PLAY._step && PLAY._step.btn) {
      const gb = host.querySelector(PLAY._step.btn);
      if (gb) gb.classList.add("guide-btn");
    }

    // tile selection
    if (canSelectTiles(s)) {
      host.querySelectorAll(".rack .tile.selectable").forEach((el) => {
        el.onclick = () => {
          const id = el.dataset.id;
          const i = PLAY.selected.indexOf(id);
          if (i >= 0) PLAY.selected.splice(i, 1);
          else if (PLAY.selected.length < maxSelect(s)) PLAY.selected.push(id);
          draw(host);
        };
      });
    }

    on("#passBtn", async () => {
      if (PLAY.selected.length !== 3) return flash(host, "Select exactly 3 tiles to pass.");
      const r = await act(`/api/game/${PLAY.id}/charleston`, { tile_ids: PLAY.selected });
      if (!correct(r)) PLAY.selected = [];
      draw(host);
    });
    on("#secondYes", async () => { await act(`/api/game/${PLAY.id}/charleston-second`, { continue: true }); PLAY.selected = []; draw(host); });
    on("#secondNo", async () => { await act(`/api/game/${PLAY.id}/charleston-second`, { continue: false }); PLAY.selected = []; draw(host); });

    on("#drawBtn", async () => {
      const r = await act(`/api/game/${PLAY.id}/draw`, {});
      correct(r);
      PLAY._justDrew = (r && r.result && r.result.drew) || null;
      PLAY._canWin = !!(r && r.result && r.result.can_declare_win);
      draw(host);
    });
    on("#discardBtn", async () => {
      if (PLAY.selected.length !== 1) return flash(host, "Click one tile to discard.");
      const r = await act(`/api/game/${PLAY.id}/discard`, { tile_id: PLAY.selected[0] });
      if (!correct(r)) { PLAY.selected = []; PLAY._canWin = false; PLAY._justDrew = null; }
      draw(host);
    });
    on("#declareBtn", async () => {
      const r = await act(`/api/game/${PLAY.id}/declare-win`, {});
      correct(r);
      draw(host);
    });
    host.querySelectorAll(".callBtn").forEach((el) => {
      el.onclick = async () => { const r = await act(`/api/game/${PLAY.id}/call`, { kind: el.dataset.kind }); correct(r); PLAY.selected = []; draw(host); };
    });
    on("#passCall", async () => { await act(`/api/game/${PLAY.id}/pass-call`, {}); PLAY._justDrew = null; draw(host); });
    on("#nextHand", async () => { await act(`/api/game/${PLAY.id}/next-hand`, {}); PLAY.selected = []; PLAY._justDrew = null; PLAY._correction = null; draw(host); });

    host.querySelectorAll(".redeemBtn").forEach((el) => {
      el.onclick = async () => {
        const e = (PLAY.snap.joker_exchanges || [])[+el.dataset.i];
        if (!e) return;
        const r = await act(`/api/game/${PLAY.id}/exchange-joker`,
          { seat_index: e.seat_index, exposure_index: e.exposure_index, tile_id: e.tile_id });
        correct(r);
        draw(host);
      };
    });

    // glossary chips
    host.querySelectorAll(".term-chip").forEach((el) => {
      el.onclick = () => {
        const box = host.querySelector("#glossaryBox");
        const term = el.dataset.term;
        box.innerHTML = `<div class="gloss"><strong>${esc(term)}</strong><p>${esc(T.glossary[term] || "")}</p></div>`;
      };
    });
  }

  async function act(url, body) {
    const data = await post(url, body);
    if (data.state) PLAY.snap = data.state;
    return data;
  }

  function flash(host, msg) {
    const bar = host.querySelector("#actionBar");
    if (!bar) return;
    const n = document.createElement("div");
    n.className = "flash";
    n.textContent = msg;
    bar.prepend(n);
    setTimeout(() => n.remove(), 2600);
  }

  window.renderPlay = renderPlay;
})();
