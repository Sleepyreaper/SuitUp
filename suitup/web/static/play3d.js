// SuitUp 3D table — a WebGL (Three.js) renderer for the Mah Jongg simulator.
// Reads the same game snapshot the 2D view uses and draws a real 3D table:
// ivory tiles with the actual SVG faces, a wall that shrinks, tumbling dice,
// click-to-select, lighting and gentle motion. Exposes window.SuitUp3D; play.js
// falls back to the 2D table if this is unavailable or throws.
import * as THREE from "./vendor/three.module.js";

const TILE = { w: 0.9, h: 1.2, t: 0.34 };
const IVORY = 0xf6efe0, EDGE = 0xdccba6, BACKCOL = 0x148a52, BACKDK = 0x0b3f27;

let renderer, scene, camera, raf, mount, ready = false, lastErr = null;
let rackGroup, oppGroup, wallGroup, discardGroup, diceGroup, tableGroup;
let raycaster, pointer, pickables = [], onPick = null;
let camOrbit = { theta: 0, phi: 0.9, r: 13.2, target: new THREE.Vector3(0, 0.55, 0.9) };
let drag = null;
const texCache = new Map();
const anims = [];
let backTex = null;

function webglOK() {
  try {
    const c = document.createElement("canvas");
    return !!(window.WebGLRenderingContext && (c.getContext("webgl") || c.getContext("experimental-webgl")));
  } catch (e) { return false; }
}

/* ---------- textures ---------- */
function backTexture() {
  if (backTex) return backTex;
  const c = document.createElement("canvas"); c.width = c.height = 128;
  const x = c.getContext("2d");
  const g = x.createLinearGradient(0, 0, 128, 128);
  g.addColorStop(0, "#2aa06a"); g.addColorStop(1, "#0f5132");
  x.fillStyle = g; x.fillRect(0, 0, 128, 128);
  x.strokeStyle = "rgba(255,255,255,.16)"; x.lineWidth = 4;
  for (let i = -128; i < 128; i += 16) { x.beginPath(); x.moveTo(i, 0); x.lineTo(i + 128, 128); x.stroke(); }
  x.strokeStyle = "rgba(255,255,255,.28)"; x.lineWidth = 6; x.strokeRect(8, 8, 112, 112);
  backTex = new THREE.CanvasTexture(c);
  return backTex;
}

function faceTexture(tile) {
  const key = (tile.id || "").replace(/_c\d+$/, "");
  if (texCache.has(key)) return texCache.get(key);
  const c = document.createElement("canvas"); c.width = 160; c.height = 214;
  const x = c.getContext("2d");
  x.fillStyle = "#fbf7ec"; x.fillRect(0, 0, c.width, c.height);
  const tex = new THREE.CanvasTexture(c);
  tex.anisotropy = 4;
  texCache.set(key, tex);
  if (tile.svg) {
    const img = new Image();
    img.onload = () => {
      try {
        x.clearRect(0, 0, c.width, c.height);
        x.fillStyle = "#fbf7ec"; x.fillRect(0, 0, c.width, c.height);
        const pad = 8;
        x.drawImage(img, pad, pad, c.width - 2 * pad, c.height - 2 * pad);
        tex.needsUpdate = true;
      } catch (e) {}
    };
    img.onerror = () => {};
    // The engine SVG already carries xmlns/viewBox — use it verbatim (adding a
    // second xmlns produces invalid markup that silently fails to load).
    img.src = "data:image/svg+xml;base64," + btoa(unescape(encodeURIComponent(tile.svg)));
  }
  return tex;
}

function tileMaterials(face) {
  const ivory = () => new THREE.MeshStandardMaterial({ color: IVORY, roughness: 0.55, metalness: 0.02 });
  const edge = () => new THREE.MeshStandardMaterial({ color: EDGE, roughness: 0.7 });
  // BoxGeometry material order: +x,-x,+y,-y,+z,-z. Front face (+z) shows the art.
  const front = face
    ? new THREE.MeshStandardMaterial({ map: face, roughness: 0.5 })
    : new THREE.MeshStandardMaterial({ color: BACKCOL, roughness: 0.6 });
  const back = new THREE.MeshStandardMaterial({
    map: face ? null : backTexture(), color: face ? EDGE : 0xffffff, roughness: 0.6,
  });
  return [edge(), edge(), ivory(), ivory(), front, back];
}

function makeTile(tile, faceUp) {
  const geo = new THREE.BoxGeometry(TILE.w, TILE.h, TILE.t);
  const mesh = new THREE.Mesh(geo, tileMaterials(faceUp ? faceTexture(tile) : null));
  mesh.castShadow = true; mesh.receiveShadow = true;
  mesh.userData.tileId = tile && tile.id;
  return mesh;
}

/* ---------- scene setup ---------- */
function build() {
  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x0c2f1f);
  camera = new THREE.PerspectiveCamera(46, 1, 0.1, 100);

  const hemi = new THREE.HemisphereLight(0xffffff, 0x2a5540, 0.75);
  scene.add(hemi);
  const key = new THREE.DirectionalLight(0xfff4e0, 1.05);
  key.position.set(6, 14, 8); key.castShadow = true;
  key.shadow.mapSize.set(1024, 1024);
  key.shadow.camera.left = -12; key.shadow.camera.right = 12;
  key.shadow.camera.top = 12; key.shadow.camera.bottom = -12;
  scene.add(key);
  scene.add(new THREE.DirectionalLight(0xbfe0ff, 0.25).translateX(-8).translateZ(-6));

  tableGroup = new THREE.Group(); scene.add(tableGroup);
  // felt base
  const felt = new THREE.Mesh(
    new THREE.BoxGeometry(15, 0.5, 15),
    new THREE.MeshStandardMaterial({ color: 0x0f5132, roughness: 0.95 }));
  felt.position.y = -0.25; felt.receiveShadow = true; tableGroup.add(felt);
  // playing cloth
  const cloth = new THREE.Mesh(
    new THREE.CircleGeometry(6.6, 60).rotateX(-Math.PI / 2),
    new THREE.MeshStandardMaterial({ color: 0x1a7a4c, roughness: 0.98 }));
  cloth.position.y = 0.006; cloth.receiveShadow = true; tableGroup.add(cloth);
  // thin gold trim ring
  const trim = new THREE.Mesh(
    new THREE.RingGeometry(6.7, 6.95, 64).rotateX(-Math.PI / 2),
    new THREE.MeshStandardMaterial({ color: 0xc8952b, roughness: 0.5, metalness: 0.3 }));
  trim.position.y = 0.02; tableGroup.add(trim);
  // wooden rim (thin flat ring, not a torus)
  const rim = new THREE.Mesh(
    new THREE.RingGeometry(6.95, 7.7, 64).rotateX(-Math.PI / 2),
    new THREE.MeshStandardMaterial({ color: 0x6b4a2b, roughness: 0.7 }));
  rim.position.y = 0.015; tableGroup.add(rim);

  rackGroup = new THREE.Group(); scene.add(rackGroup);
  oppGroup = new THREE.Group(); scene.add(oppGroup);
  wallGroup = new THREE.Group(); scene.add(wallGroup);
  discardGroup = new THREE.Group(); scene.add(discardGroup);
  diceGroup = new THREE.Group(); scene.add(diceGroup);

  raycaster = new THREE.Raycaster();
  pointer = new THREE.Vector2();
}

function clear(group) {
  while (group.children.length) {
    const c = group.children[0];
    group.remove(c);
    c.traverse && c.traverse((o) => {
      if (o.geometry) o.geometry.dispose();
      if (o.material) {
        const mats = Array.isArray(o.material) ? o.material : [o.material];
        // dispose materials but NOT their .map (face/back textures are cached & shared)
        mats.forEach((m) => m && m.dispose && m.dispose());
      }
    });
  }
}

/* ---------- layout from snapshot ---------- */
function layoutRack(snap) {
  clear(rackGroup); pickables = [];
  const tiles = (snap.you && snap.you.concealed) || [];
  const sel = new Set(currentSelected);
  const dead = new Set(((snap.hint && snap.hint.deadwood) || []).map((t) => t.id));
  const RS = 0.92;                                  // rack tile scale so all ~14 fit
  const sp = TILE.w * RS + 0.05;
  const x0 = -((tiles.length - 1) * sp) / 2;
  tiles.forEach((t, i) => {
    const m = makeTile(t, true);
    m.scale.set(RS, RS, RS);
    m.position.set(x0 + i * sp, 0.8, 4.5);
    m.rotation.x = -0.72;                          // lean back so faces angle up to the camera
    if (sel.has(t.id)) {
      m.position.y += 0.5; m.position.z -= 0.3;
      m.material[4].emissive = new THREE.Color(0xc8952b);
      m.material[4].emissiveIntensity = 0.4;
    } else if (dead.has(t.id)) {
      m.material[4].color = new THREE.Color(0xb4ab99);   // dim (not transparent) so it reads as ivory
    }
    rackGroup.add(m); pickables.push(m);
  });
  // exposed melds sit low in front, face up flat
  const exps = (snap.you && snap.you.exposures) || [];
  let ex = -2.4;
  exps.forEach((e) => {
    e.tiles.forEach((t) => {
      const m = makeTile(t, true); m.scale.set(0.8, 0.8, 0.8);
      m.rotation.x = -Math.PI / 2;
      m.position.set(ex, 0.16, 3.1); ex += 0.5;
    });
    ex += 0.25;
  });
}

function rowOfBacks(n, opts) {
  const g = new THREE.Group();
  const S = 0.7;
  const sp = TILE.w * S + 0.04;
  const shown = Math.min(n, 18);
  const x0 = -((shown - 1) * sp) / 2;
  for (let i = 0; i < shown; i++) {
    const m = makeTile(null, false);
    m.scale.set(S, S, S);
    if (opts.vertical) { m.rotation.z = Math.PI / 2; m.position.set(0, TILE.h * S / 2, x0 + i * sp); }
    else m.position.set(x0 + i * sp, TILE.h * S / 2, 0);
    g.add(m);
  }
  return g;
}

function layoutOpponents(snap) {
  clear(oppGroup);
  const seats = ["East", "South", "West", "North"];
  const hi = seats.indexOf(snap.you.seat);
  (snap.opponents || []).forEach((o) => {
    const off = (seats.indexOf(o.seat) - hi + 4) % 4;
    const where = off === 1 ? "right" : off === 2 ? "top" : "left";
    const backs = rowOfBacks(o.concealed_count, { vertical: where !== "top" });
    if (where === "top") { backs.position.set(0, 0, -5.9); backs.rotation.y = Math.PI; }
    if (where === "left") { backs.position.set(-5.9, 0, 0); }
    if (where === "right") { backs.position.set(5.9, 0, 0); }
    oppGroup.add(backs);
    let e = -1.2;
    (o.exposures || []).forEach((grp) => grp.tiles.forEach((t) => {
      const m = makeTile(t, true); m.rotation.x = -Math.PI / 2; m.scale.set(0.8, 0.8, 0.8);
      if (where === "top") m.position.set(e, 0.16, -4.0);
      else if (where === "left") m.position.set(-4.0, 0.16, e);
      else m.position.set(4.0, 0.16, e);
      e += 0.5; oppGroup.add(m);
    }));
  });
}

function layoutWall(snap) {
  clear(wallGroup);
  const stacks = Math.ceil((snap.wall_remaining || 0) / 2);
  const S = 0.5;                                    // wall tiles are small
  const side = 3.0, perSide = Math.ceil(stacks / 4);
  let placed = 0;
  const edges = [
    { ax: "x", z: -side, dir: 1 }, { ax: "z", x: side, dir: 1 },
    { ax: "x", z: side, dir: -1 }, { ax: "z", x: -side, dir: -1 },
  ];
  const sp = TILE.w * S + 0.02;
  edges.forEach((e) => {
    for (let i = 0; i < perSide && placed < stacks; i++, placed++) {
      const off = (i - (perSide - 1) / 2) * sp * e.dir;
      for (let h = 0; h < 2; h++) {
        const m = makeTile(null, false);
        m.scale.set(S, S, S);
        m.rotation.x = Math.PI / 2;                 // lie flat, face down
        const y = 0.1 + h * (TILE.t * S + 0.01);
        if (e.ax === "x") m.position.set(off, y, e.z);
        else { m.rotation.z = Math.PI / 2; m.position.set(e.x, y, off); }
        wallGroup.add(m);
      }
    }
  });
}

function layoutDiscards(snap) {
  clear(discardGroup);
  const d = (snap.discards || []).slice(-24);
  const cols = 8, sp = 0.56, rows = Math.ceil(d.length / cols) || 1;
  d.forEach((t, i) => {
    const r = Math.floor(i / cols), c = i % cols;
    const m = makeTile(t, true);
    m.rotation.x = -Math.PI / 2; m.scale.set(0.8, 0.8, 0.8);
    m.position.set((c - (cols - 1) / 2) * sp, 0.16, (r - (rows - 1) / 2) * sp);
    if (i === d.length - 1) animateDrop(m, 3);
    discardGroup.add(m);
  });
}

/* ---------- dice ---------- */
function pipTexture(n) {
  const c = document.createElement("canvas"); c.width = c.height = 96;
  const x = c.getContext("2d");
  x.fillStyle = "#fff"; x.fillRect(0, 0, 96, 96);
  x.fillStyle = "#b02a37";
  const P = { 1: [[48, 48]], 2: [[26, 26], [70, 70]], 3: [[26, 26], [48, 48], [70, 70]],
    4: [[26, 26], [70, 26], [26, 70], [70, 70]], 5: [[26, 26], [70, 26], [48, 48], [26, 70], [70, 70]],
    6: [[26, 24], [70, 24], [26, 48], [70, 48], [26, 72], [70, 72]] };
  (P[n] || []).forEach((p) => { x.beginPath(); x.arc(p[0], p[1], 10, 0, 7); x.fill(); });
  return new THREE.CanvasTexture(c);
}
function makeDie() {
  const mats = [1, 6, 2, 5, 3, 4].map((n) => new THREE.MeshStandardMaterial({ map: pipTexture(n), roughness: 0.4 }));
  const m = new THREE.Mesh(new THREE.BoxGeometry(0.7, 0.7, 0.7), mats);
  m.castShadow = true; return m;
}
function showDice(snap) {
  const has = !!snap.dice && snap.phase === "setup";     // only during the setup ritual
  if (!has) { clear(diceGroup); diceGroup.userData.total = null; return; }
  if (diceGroup.userData.total === snap.dice.total && diceGroup.children.length) return;
  clear(diceGroup);
  diceGroup.userData.total = snap.dice.total;
  [-0.6, 0.6].forEach((dx, k) => {
    const d = makeDie(); d.position.set(dx, 0.6, 0.6);
    diceGroup.add(d);
    anims.push({ obj: d, t: 0, dur: 0.9 + k * 0.1, kind: "die",
      from: new THREE.Euler(Math.random() * 6, Math.random() * 6, Math.random() * 6),
      to: new THREE.Euler(Math.PI * 2 * (2 + k), Math.PI * 2 * 2, Math.PI * (3 + k)) });
  });
}

/* ---------- animation ---------- */
function animateDrop(mesh, from) {
  const targetY = mesh.position.y;
  mesh.position.y = targetY + from;
  anims.push({ obj: mesh, t: 0, dur: 0.35, kind: "drop", fromY: targetY + from, toY: targetY });
}
function tick(dt) {
  for (let i = anims.length - 1; i >= 0; i--) {
    const a = anims[i]; a.t += dt;
    const p = Math.min(1, a.t / a.dur), e = 1 - Math.pow(1 - p, 3);
    if (a.kind === "drop") a.obj.position.y = a.fromY + (a.toY - a.fromY) * e;
    else if (a.kind === "die") {
      a.obj.rotation.x = a.from.x + (a.to.x - a.from.x) * e;
      a.obj.rotation.y = a.from.y + (a.to.y - a.from.y) * e;
      a.obj.rotation.z = a.from.z + (a.to.z - a.from.z) * e;
    }
    if (p >= 1) anims.splice(i, 1);
  }
}

/* ---------- camera + loop ---------- */
function applyCam() {
  const o = camOrbit;
  camera.position.set(
    o.target.x + o.r * Math.sin(o.phi) * Math.sin(o.theta),
    o.target.y + o.r * Math.cos(o.phi),
    o.target.z + o.r * Math.sin(o.phi) * Math.cos(o.theta));
  camera.lookAt(o.target);
}
let last = 0, sway = 0;
function loop(ts) {
  raf = requestAnimationFrame(loop);
  const dt = Math.min(0.05, (ts - last) / 1000 || 0); last = ts;
  tick(dt);
  if (!drag) { sway += dt * 0.25; camOrbit.theta = Math.sin(sway) * 0.05; }
  applyCam();
  renderer.render(scene, camera);
}

/* ---------- interaction ---------- */
function onDown(ev) {
  const r = renderer.domElement.getBoundingClientRect();
  pointer.x = ((ev.clientX - r.left) / r.width) * 2 - 1;
  pointer.y = -((ev.clientY - r.top) / r.height) * 2 + 1;
  drag = { x: ev.clientX, y: ev.clientY, theta: camOrbit.theta, phi: camOrbit.phi, moved: false, base: sway };
}
function onMove(ev) {
  if (!drag) return;
  const dx = ev.clientX - drag.x, dy = ev.clientY - drag.y;
  if (Math.abs(dx) + Math.abs(dy) > 4) drag.moved = true;
  camOrbit.theta = drag.theta - dx * 0.006;
  camOrbit.phi = Math.max(0.45, Math.min(1.35, drag.phi - dy * 0.005));
}
function onUp(ev) {
  const wasDrag = drag && drag.moved;
  if (drag) sway = drag.base;
  drag = null;
  if (wasDrag || !onPick) return;
  raycaster.setFromCamera(pointer, camera);
  const hit = raycaster.intersectObjects(pickables, false)[0];
  if (hit && hit.object.userData.tileId) onPick(hit.object.userData.tileId);
}

/* ---------- public API ---------- */
let currentSelected = [];
const API = {
  available() { return webglOK(); },
  init() {
    if (ready) return true;
    try {
      if (!webglOK()) { lastErr = "no-webgl"; return false; }
      renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
      renderer.setPixelRatio(Math.min(2, window.devicePixelRatio || 1));
      renderer.shadowMap.enabled = true;
      renderer.domElement.style.cssText = "width:100%;height:100%;display:block;border-radius:14px;touch-action:none";
      build();
      const el = renderer.domElement;
      el.addEventListener("pointerdown", onDown);
      window.addEventListener("pointermove", onMove);
      window.addEventListener("pointerup", onUp);
      ready = true;
      raf = requestAnimationFrame(loop);
      return true;
    } catch (e) { lastErr = String(e); ready = false; return false; }
  },
  mount(el) {
    if (!ready || !el) return;
    if (renderer.domElement.parentElement !== el) el.appendChild(renderer.domElement);
    this.resize();
  },
  resize() {
    if (!ready || !renderer.domElement.parentElement) return;
    const el = renderer.domElement.parentElement;
    const w = el.clientWidth || 640, h = el.clientHeight || 460;
    renderer.setSize(w, h, false);
    camera.aspect = w / h; camera.updateProjectionMatrix();
  },
  update(snap, opts) {
    if (!ready) return;
    try {
      currentSelected = (opts && opts.selected) || [];
      onPick = (opts && opts.onTilePick) || null;
      layoutOpponents(snap);
      layoutWall(snap);
      layoutDiscards(snap);
      layoutRack(snap);
      showDice(snap);
      this.resize();
    } catch (e) { lastErr = String(e); }
  },
  lastError() { return lastErr; },
};

window.SuitUp3D = API;
if (typeof window.__on3DReady === "function") window.__on3DReady();
