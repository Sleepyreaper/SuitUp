"use strict";
/* SuitUp — the playable simulator UI ("Play" tab).
   A full table: your rack, 3 AI opponents, wall, discards, Charleston, calling,
   scoring, and a toggleable Coach overlay that teaches as you play. Talks to the
   stateful /api/game/* endpoints. Dependency-free vanilla JS. */
(function () {
  const T = window.SUITUP_TUTORIAL || { contextual: {}, glossary: {}, intro: {} };
  const PLAY = { id: null, snap: null, selected: [], coach: true, level: "mixed" };

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
      host.innerHTML = setupHTML();
      wireSetup(host);
      return;
    }
    const data = await get(`/api/game/${PLAY.id}`);
    if (data.error) { PLAY.id = null; return renderPlay(); }
    PLAY.snap = data.state;
    draw(host);
  }

  function setupHTML() {
    const intro = T.intro || { title: "", points: [] };
    return `
      <h2 class="section-title">Play — Mah Jongg Simulator 🀄</h2>
      <div class="card">
        <h3>${esc(intro.title)}</h3>
        <ul class="intro-list">${(intro.points || []).map((p) => `<li>${esc(p)}</li>`).join("")}</ul>
      </div>
      <div class="card setup-card">
        <h3>Start a new game</h3>
        <label class="setup-row">Opponent difficulty:
          <select id="lvl">
            <option value="easy">Easy — 3 beginner bots</option>
            <option value="mixed" selected>Mixed — beginner, improver, sharp</option>
            <option value="hard">Hard — 3 sharp bots</option>
          </select>
        </label>
        <label class="setup-row"><input type="checkbox" id="coachChk" checked>
          Show the Coach overlay (teaches terms as you play)</label>
        <button id="newGameBtn" class="btn btn-primary">Deal &amp; Start</button>
      </div>`;
  }

  function wireSetup(host) {
    host.querySelector("#newGameBtn").onclick = async () => {
      PLAY.level = host.querySelector("#lvl").value;
      PLAY.coach = host.querySelector("#coachChk").checked;
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
    host.innerHTML = `
      <div class="table-top">
        <div class="tbl-info">
          <strong>Hand ${s.hand_number}</strong> · Dealer: ${esc(s.dealer)} ·
          Wall: ${s.wall_remaining} tiles · Target: ${s.target_score} pts
        </div>
        <div class="tbl-actions">
          <button id="coachToggle" class="btn btn-ghost">${PLAY.coach ? "Hide" : "Show"} Coach</button>
          <button id="quitBtn" class="btn btn-ghost">New Game</button>
        </div>
      </div>
      <div class="table-layout">
        <div class="table-main">
          ${opponentsHTML(s)}
          ${centerHTML(s)}
          ${youHTML(s)}
          <div class="action-bar" id="actionBar">${actionHTML(s)}</div>
          ${logHTML(s)}
        </div>
        ${PLAY.coach ? coachHTML(s) : ""}
      </div>`;
    wire(host);
  }

  function tileHTML(t, opts) {
    opts = opts || {};
    const cls = ["tile"];
    if (opts.selectable) cls.push("selectable");
    if (PLAY.selected.includes(t.id)) cls.push("selected");
    if (opts.dead) cls.push("dead");
    if (opts.joker || t.joker) cls.push("joker");
    return `<span class="${cls.join(" ")}" data-id="${esc(t.id)}" title="${esc(t.name)}">${t.svg || esc(t.name)}</span>`;
  }

  function backHTML(n) {
    let out = "";
    for (let i = 0; i < n; i++) out += `<span class="tile back"></span>`;
    return out;
  }

  function expHTML(exps) {
    if (!exps || !exps.length) return `<span class="muted">none</span>`;
    return exps.map((e) =>
      `<span class="exposure" title="${esc(e.group_type)}">${e.tiles.map((t) => tileHTML(t)).join("")}</span>`
    ).join(" ");
  }

  function opponentsHTML(s) {
    return `<div class="opponents">${s.opponents.map((o) => `
      <div class="opp ${o.is_turn ? "turn" : ""}">
        <div class="opp-head">
          <span class="seat">${esc(o.seat)}</span>
          <span class="lvl-badge">AI ${o.level}</span>
          <span class="score">${o.score} pts</span>
          ${o.is_turn ? '<span class="turn-dot">● turn</span>' : ""}
        </div>
        <div class="opp-tiles">${backHTML(o.concealed_count)}</div>
        <div class="opp-exp">${expHTML(o.exposures)}</div>
      </div>`).join("")}</div>`;
  }

  function centerHTML(s) {
    const last = s.last_discard
      ? `<div class="last-discard"><span class="lbl">Last discard${s.last_discarder ? " (" + esc(s.last_discarder) + ")" : ""}:</span>${tileHTML(s.last_discard)}</div>`
      : "";
    const disc = s.discards.length
      ? s.discards.map((t) => tileHTML(t)).join("")
      : `<span class="muted">no discards yet</span>`;
    return `<div class="center">
      <div class="phase-banner">${esc(phaseLabel(s))}</div>
      ${last}
      <div class="discard-pile"><span class="lbl">Discards:</span>${disc}</div>
    </div>`;
  }

  function youHTML(s) {
    const you = s.you;
    const deadIds = (s.hint && s.hint.deadwood ? s.hint.deadwood : []).map((t) => t.id);
    const selectable = canSelectTiles(s);
    const rack = you.concealed.map((t) =>
      tileHTML(t, { selectable, dead: deadIds.includes(t.id) })).join("");
    return `<div class="you">
      <div class="you-head">
        <span class="seat">You (${esc(you.seat)})</span>
        <span class="score">${you.score} pts · ${you.hands_won} won</span>
      </div>
      <div class="you-exp"><span class="lbl">Exposed:</span> ${expHTML(you.exposures)}</div>
      <div class="rack">${rack}</div>
    </div>`;
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
      return `<button id="drawBtn" class="btn btn-primary">Draw a tile</button>`;
    }
    if (s.phase === "play" && s.your_turn && s.sub === "discard") {
      const win = `<button id="declareBtn" class="btn btn-win">Declare Mah Jongg</button>`;
      return `<button id="discardBtn" class="btn btn-primary">Discard selected (${PLAY.selected.length}/1)</button>
        ${(PLAY._canWin ? win : "")}`;
    }
    if (s.phase === "hand_over") {
      return winSummaryHTML(s) + `<button id="nextHand" class="btn btn-primary">Deal next hand</button>`;
    }
    if (s.phase === "game_over") {
      return winSummaryHTML(s) + finalScoresHTML(s) + `<button id="quitBtn2" class="btn btn-primary">New game</button>`;
    }
    return `<div class="muted">Waiting…</div>`;
  }

  function winSummaryHTML(s) {
    const wi = s.win_info;
    if (!wi) return "";
    if (wi.wall_game) return `<div class="win-box">🁢 Wall game — the wall ran out. A draw, no score.</div>`;
    const sc = wi.scoring;
    const who = wi.is_human ? "You" : esc(wi.winner);
    const tiles = (wi.hand_tiles || []).map((t) => tileHTML(t)).join("");
    const bonus = (sc.bonuses || []).map((b) => `+${b.points} ${esc(b.label)}`).join(", ");
    return `<div class="win-box">
      <div class="win-head">🎉 ${who} won — ${esc(sc.hand_name)} (+${sc.total} pts)</div>
      <div class="win-tiles">${tiles}</div>
      <div class="win-score">Base ${sc.base}${bonus ? " · " + esc(bonus) : ""} · Jokers used: ${sc.jokers_used}</div>
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
    const quit = () => { PLAY.id = null; PLAY.selected = []; renderPlay(); };
    on("#quitBtn", quit); on("#quitBtn2", quit);

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
      if (r && r.result && r.result.ok === false) flash(host, r.result.error);
      PLAY.selected = []; draw(host);
    });
    on("#secondYes", async () => { await act(`/api/game/${PLAY.id}/charleston-second`, { continue: true }); PLAY.selected = []; draw(host); });
    on("#secondNo", async () => { await act(`/api/game/${PLAY.id}/charleston-second`, { continue: false }); PLAY.selected = []; draw(host); });

    on("#drawBtn", async () => {
      const r = await act(`/api/game/${PLAY.id}/draw`, {});
      PLAY._canWin = !!(r && r.result && r.result.can_declare_win);
      draw(host);
    });
    on("#discardBtn", async () => {
      if (PLAY.selected.length !== 1) return flash(host, "Click one tile to discard.");
      await act(`/api/game/${PLAY.id}/discard`, { tile_id: PLAY.selected[0] });
      PLAY.selected = []; PLAY._canWin = false; draw(host);
    });
    on("#declareBtn", async () => {
      const r = await act(`/api/game/${PLAY.id}/declare-win`, {});
      if (r && r.result && r.result.ok === false) flash(host, r.result.error);
      draw(host);
    });
    host.querySelectorAll(".callBtn").forEach((el) => {
      el.onclick = async () => { await act(`/api/game/${PLAY.id}/call`, { kind: el.dataset.kind }); PLAY.selected = []; draw(host); };
    });
    on("#passCall", async () => { await act(`/api/game/${PLAY.id}/pass-call`, {}); draw(host); });
    on("#nextHand", async () => { await act(`/api/game/${PLAY.id}/next-hand`, {}); PLAY.selected = []; draw(host); });

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
