"use strict";
/* SuitUp teaching UI — a small dependency-free single-page app. */

const CURRICULUM = window.SUITUP_CURRICULUM || { units: [] };
const RULES = window.SUITUP_RULES_REFERENCE || { sections: [], quick_reference: {} };

const TABS = [
  { id: "play", label: "▶ Play" },
  { id: "start", label: "Start Here" },
  { id: "learn", label: "Learn" },
  { id: "tiles", label: "The Tiles" },
  { id: "table", label: "Set Up a Table" },
  { id: "charleston", label: "The Charleston" },
  { id: "groups", label: "Groups Trainer" },
  { id: "rules", label: "Rules Reference" },
];

const el = (id) => document.getElementById(id);
const view = () => el("view");

function esc(s) {
  return String(s == null ? "" : s).replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

async function getJSON(url, opts) {
  const r = await fetch(url, opts);
  if (!r.ok) throw new Error("HTTP " + r.status);
  return r.json();
}

/* ---------- navigation ---------- */
function buildNav() {
  const nav = el("nav");
  nav.innerHTML = "";
  TABS.forEach((t) => {
    const b = document.createElement("button");
    b.textContent = t.label;
    b.dataset.tab = t.id;
    b.onclick = () => go(t.id);
    nav.appendChild(b);
  });
}

function setActive(id) {
  document.querySelectorAll("#nav button").forEach((b) =>
    b.classList.toggle("active", b.dataset.tab === id));
}

const RENDERERS = {
  play: () => window.renderPlay(),
  start: renderStart,
  learn: renderLearn,
  tiles: renderTiles,
  table: renderTable,
  charleston: renderCharleston,
  groups: renderGroups,
  rules: renderRules,
};

function go(id) {
  setActive(id);
  location.hash = id;
  view().innerHTML = '<p class="loading">Loading…</p>';
  Promise.resolve(RENDERERS[id]()).catch((e) => {
    view().innerHTML = `<div class="card"><h3>Something went wrong</h3><p>${esc(e.message)}</p></div>`;
  });
}

/* ---------- views ---------- */
function renderStart() {
  view().innerHTML = `
    <h2 class="section-title">Welcome to SuitUp 🀄</h2>
    <p class="lead">A patient, hands-on guide to American Mah Jongg — built for a total beginner
       with a brand-new set and a green mat.</p>
    <div class="card">
      <h3>You just got your set — now what?</h3>
      <p>American Mah Jongg can feel like a wall of mysterious tiles. SuitUp breaks it into small,
         doable steps: meet the tiles, set up the table, choose who starts, run the Charleston, and
         learn how hands are built — then practice against friendly bots.</p>
      <p><strong>Suggested path:</strong></p>
      <ol>
        <li><strong>The Tiles</strong> — see and name every tile in your set.</li>
        <li><strong>Learn</strong> — the step-by-step beginner curriculum.</li>
        <li><strong>Set Up a Table</strong> — watch a real deal happen.</li>
        <li><strong>The Charleston</strong> — the signature tile-passing ritual.</li>
        <li><strong>Groups Trainer</strong> — practice building Pairs, Pungs, and Kongs.</li>
      </ol>
      <button class="btn" onclick="go('tiles')">Start with the tiles →</button>
    </div>
    <div class="note">${esc(CURRICULUM.disclaimer || "")}</div>`;
}

function renderLearn() {
  const units = (CURRICULUM.units || []).slice().sort((a, b) => a.order - b.order);
  const html = units.map((u) => `
    <div class="unit">
      <h3>Unit ${u.order}: ${esc(u.title)}</h3>
      <p class="lead">${esc(u.objective || "")}</p>
      ${(u.lessons || []).map((l) => `
        <div class="lesson">
          <h4>${esc(l.title)}</h4>
          <p class="objective">${esc(l.objective || "")}</p>
          <ol>
            ${(l.steps || []).map((s) => `
              <li><strong>${esc(s.title)}</strong> — ${esc(s.body)}
                ${s.learner_action ? `<br><em>Try it: ${esc(s.learner_action)}</em>` : ""}</li>`).join("")}
          </ol>
        </div>`).join("")}
    </div>`).join("");
  view().innerHTML = `<h2 class="section-title">${esc(CURRICULUM.title || "Learn")}</h2>
    <p class="lead">Work top to bottom. Each lesson ends with something you can actually do.</p>${html}`;
}

function tileCell(t, opts) {
  opts = opts || {};
  const cls = "tile" + (opts.small ? " small" : "") + (opts.selectable ? " selectable" : "");
  const nm = opts.hideName ? "" : `<span class="tile-name">${esc(t.name)}</span>`;
  return `<span class="tile-cell"><span class="${cls}" data-id="${esc(t.id)}">${t.svg}</span>${nm}</span>`;
}

async function renderTiles() {
  const data = await getJSON("/api/tiles");
  const byKind = { suited: [], wind: [], dragon: [], joker: [] };
  data.tiles.forEach((t) => (byKind[t.kind] || (byKind[t.kind] = [])).push(t));
  const groups = [
    ["Suits — Dots, Bams, Craks (1–9, four of each = 108 tiles)", byKind.suited],
    ["Winds — East, South, West, North (four each = 16)", byKind.wind],
    ["Dragons — Red, Green, White (four each = 12)", byKind.dragon],
    ["Jokers — wild in groups of 3+ (8 tiles)", byKind.joker],
  ];
  view().innerHTML = `<h2 class="section-title">The Tiles</h2>
    <p class="lead">Every face in your set (${data.count_unique} unique tiles; a full set has 152 counting copies).
      Hover to lift a tile.</p>
    ${groups.map(([title, tiles]) => `
      <div class="tile-group"><h4>${esc(title)}</h4>
        <div>${tiles.map((t) => tileCell(t)).join("")}</div></div>`).join("")}`;
}

async function renderTable() {
  const data = await getJSON("/api/setup");
  const seatHtml = data.seats.map((seat) => {
    const isDealer = seat === data.dealer_seat;
    return `<div class="seat ${isDealer ? "dealer" : ""}">
      <h4>${esc(seat)} ${isDealer ? '<span class="pill gold">Dealer / starts</span>' : ""}
        <span style="opacity:.7;font-weight:400">${data.hand_counts[seat]} tiles</span></h4>
      <div class="hand-row">${data.hands[seat].map((t) => tileCell(t, { small: true, hideName: true })).join("")}</div>
    </div>`;
  }).join("");
  view().innerHTML = `<h2 class="section-title">Set Up a Table</h2>
    <p class="lead">A real, freshly-dealt table. Everyone builds a wall (19 tiles × 2 high), the dealer
      is chosen by drawing Winds, then 13 tiles go to each seat — the dealer takes a 14th to start.</p>
    <div class="felt">
      <p><strong>Dealer:</strong> ${esc(data.dealer_seat)} drew East.
        &nbsp; <strong>Dice:</strong> <span class="dice">🎲 ${data.dice.die1} + ${data.dice.die2} = ${data.dice.total}</span>
        &nbsp; <strong>Wall left:</strong> ${data.wall_remaining} tiles.</p>
      ${seatHtml}
    </div>
    <button class="btn" onclick="go('table')">🔀 Deal a new table</button>`;
}

async function renderCharleston() {
  const data = await getJSON("/api/charleston");
  const arrow = { right: "➡️", left: "⬅️", across: "↔️", opposite: "🔄" };
  view().innerHTML = `<h2 class="section-title">The Charleston</h2>
    <p class="lead">Before play, players pass tiles to improve everyone's hand. Follow these in order.</p>
    <div class="note"><strong>The one rule beginners forget:</strong> you may <strong>never</strong>
      pass a Joker (or a Flower) during the Charleston.</div>
    <div class="card">
      ${data.steps.map((s) => `
        <div class="step">
          <div class="num">${s.order}</div>
          <div>
            <strong>${esc(s.phase[0].toUpperCase() + s.phase.slice(1))} Charleston</strong>
            <span class="pill ${s.mandatory ? "" : "optional"}">${s.mandatory ? "Required" : "Optional"}</span>
            <br><span class="arrow">${arrow[s.direction] || ""}</span> ${esc(s.note)}
          </div>
        </div>`).join("")}
    </div>`;
}

/* Groups trainer — pick tiles, we tell you if it's a legal group. */
let picked = new Set();
async function renderGroups() {
  const data = await getJSON("/api/tiles");
  // Offer a friendly subset: a few identical-looking options + a joker so pairs-with-joker can be tried.
  const sample = data.tiles.filter((t) =>
    ["dots_1", "dots_2", "bams_3", "craks_5", "wind_east", "dragon_red"].some((k) => t.id.startsWith(k)) || t.is_joker);
  picked = new Set();
  view().innerHTML = `<h2 class="section-title">Groups Trainer</h2>
    <p class="lead">American Mah Jongg hands are built from exact groups — <strong>Pair</strong> (2),
      <strong>Pung</strong> (3), <strong>Kong</strong> (4), <strong>Quint</strong> (5) — of the same tile.
      Jokers are wild in groups of 3+, but never in a Pair. Click tiles to build a group.</p>
    <div class="card">
      <p>Tap tiles to add them (you can tap the same face more than once):</p>
      <div id="palette">${sample.map((t, i) => `
        <span class="tile-cell"><span class="tile selectable" data-id="${esc(t.id)}" data-idx="${i}">${t.svg}</span>
          <span class="tile-name">${esc(t.name)}</span></span>`).join("")}</div>
      <hr>
      <p><strong>Your group:</strong></p>
      <div id="chosen" class="hand-row"><em style="color:var(--muted)">nothing selected yet</em></div>
      <p id="verdict"></p>
      <button class="btn secondary" onclick="renderGroups()">Clear</button>
    </div>`;

  const palette = el("palette");
  const chosenTiles = [];
  palette.querySelectorAll(".tile").forEach((node) => {
    node.onclick = () => {
      const id = node.dataset.id;
      const t = data.tiles.find((x) => x.id === id);
      chosenTiles.push(t);
      renderChosen(chosenTiles);
    };
  });
}

async function renderChosen(chosenTiles) {
  const chosen = el("chosen");
  chosen.innerHTML = chosenTiles.length
    ? chosenTiles.map((t) => `<span class="tile small">${t.svg}</span>`).join("")
    : '<em style="color:var(--muted)">nothing selected yet</em>';
  if (chosenTiles.length >= 2) {
    const res = await getJSON("/api/check-group", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ tile_ids: chosenTiles.map((t) => t.id) }),
    });
    el("verdict").innerHTML = `<span class="${res.valid ? "result-good" : "result-bad"}">${esc(res.explanation)}</span>`;
  } else {
    el("verdict").innerHTML = '<span style="color:var(--muted)">Add at least 2 tiles…</span>';
  }
}

function renderRules() {
  const secs = (RULES.sections || []).slice().sort((a, b) => a.order - b.order);
  const qr = RULES.quick_reference || {};
  view().innerHTML = `<h2 class="section-title">${esc(RULES.title || "Rules Reference")}</h2>
    ${qr.items ? `<div class="card"><h3>${esc(qr.checklist_title || "Quick checklist")}</h3>
      <ol>${qr.items.map((i) => `<li>${esc(i)}</li>`).join("")}</ol></div>` : ""}
    ${secs.map((s) => `
      <div class="card">
        <h3>${esc(s.title)}</h3>
        <p class="lead">${esc(s.summary || "")}</p>
        <dl class="rules">
          ${(s.facts || []).map((f) => `<dt>${esc(f.label)}</dt><dd>${esc(f.value)}</dd>`).join("")}
        </dl>
        ${s.beginner_notes ? `<div class="note">${esc(s.beginner_notes)}</div>` : ""}
      </div>`).join("")}
    <div class="note">${esc(RULES.disclaimer || "")}</div>`;
}

/* ---------- boot ---------- */
buildNav();
window.addEventListener("hashchange", () => {
  const id = location.hash.replace("#", "");
  if (RENDERERS[id]) go(id);
});
go(location.hash && RENDERERS[location.hash.replace("#", "")] ? location.hash.replace("#", "") : "start");
