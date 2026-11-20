// Leonida Legend — GTA VI trophy guide & tracker.
// Loads the 55 official trophies from data/trophies.json, renders a searchable,
// filterable, sortable checklist, and tracks earned state for the session.

const GRADE_ORDER = { platinum: 0, gold: 1, silver: 2, bronze: 3 };
const GRADE_COLORS = {
  platinum: ["#eaf7ff", "#8fd8ff", "#4db8e8"],
  gold: ["#fff3b0", "#ffd23d", "#e09a00"],
  silver: ["#ffffff", "#d7dce6", "#9aa4b5"],
  bronze: ["#ffd9b8", "#e08a4c", "#a85a24"],
};

const state = {
  trophies: [],
  earned: new Set(),
  grade: "all",
  query: "",
  hideEarned: false,
  sort: "grade",
  openId: null,
};

const els = {};
for (const id of ["list", "empty", "resultCount", "search", "hideEarned", "sort", "pct", "ringFg",
  "cPlatinum", "cGold", "cSilver", "cBronze", "cTotal", "modalBackdrop", "modalClose",
  "modalIcon", "modalName", "modalDesc", "modalMeta", "modalGuide", "modalTips",
  "modalMissable", "modalDifficulty", "modalTime", "modalEarned"]) {
  els[id] = document.getElementById(id);
}

function trophyIcon(grade, size = 52) {
  const [light, mid, dark] = GRADE_COLORS[grade] || GRADE_COLORS.bronze;
  const gid = `g-${grade}-${size}`;
  return `
  <svg viewBox="0 0 64 64" width="${size}" height="${size}" aria-hidden="true">
    <defs>
      <linearGradient id="${gid}" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="${light}"/>
        <stop offset="0.55" stop-color="${mid}"/>
        <stop offset="1" stop-color="${dark}"/>
      </linearGradient>
    </defs>
    <path d="M15 5h34v15c0 10-7.6 17-17 17S15 30 15 20z" fill="url(#${gid})"/>
    <path d="M15 9H7c0 10 4.6 15.6 11 17.6M49 9h8c0 10-4.6 15.6-11 17.6" fill="none" stroke="${dark}" stroke-width="4"/>
    <rect x="28" y="37" width="8" height="8" fill="${dark}"/>
    <rect x="20" y="45" width="24" height="6" rx="2" fill="${mid}"/>
    <rect x="16" y="51" width="32" height="5" rx="2" fill="${dark}"/>
    <path d="M32 12l2.2 4.4 4.8.7-3.5 3.4.8 4.8L32 23l-4.3 2.3.8-4.8L25 17.1l4.8-.7z" fill="#fff" opacity="0.85"/>
  </svg>`;
}

function stars(n) {
  return "★".repeat(n) + "☆".repeat(Math.max(0, 5 - n));
}

function esc(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  }[c]));
}

function visibleTrophies() {
  const q = state.query.trim().toLowerCase();
  let items = state.trophies.filter((t) => {
    if (state.grade !== "all" && t.grade !== state.grade) return false;
    if (state.hideEarned && state.earned.has(t.id)) return false;
    if (q) {
      const hay = `${t.name} ${t.description} ${t.guide} ${t.tips || ""}`.toLowerCase();
      if (!hay.includes(q)) return false;
    }
    return true;
  });
  const byGrade = (a, b) => (GRADE_ORDER[a.grade] - GRADE_ORDER[b.grade]) || (a.id - b.id);
  if (state.sort === "grade") items.sort(byGrade);
  else if (state.sort === "name") items.sort((a, b) => a.name.localeCompare(b.name));
  else if (state.sort === "unearned") {
    items.sort((a, b) => (state.earned.has(a.id) - state.earned.has(b.id)) || byGrade(a, b));
  } else items.sort((a, b) => a.id - b.id);
  return items;
}

function renderProgress() {
  const total = state.trophies.length;
  const earned = state.earned.size;
  const pct = total ? Math.round((earned / total) * 100) : 0;
  els.pct.textContent = `${pct}%`;
  const circumference = 326.7;
  els.ringFg.style.strokeDashoffset = String(circumference * (1 - (total ? earned / total : 0)));
  const count = (g) => state.trophies.filter((t) => t.grade === g && state.earned.has(t.id)).length;
  const of = (g) => state.trophies.filter((t) => t.grade === g).length;
  els.cPlatinum.textContent = `${count("platinum")}/${of("platinum")}`;
  els.cGold.textContent = `${count("gold")}/${of("gold")}`;
  els.cSilver.textContent = `${count("silver")}/${of("silver")}`;
  els.cBronze.textContent = `${count("bronze")}/${of("bronze")}`;
  els.cTotal.textContent = `${earned}/${total}`;
}

function renderList() {
  const items = visibleTrophies();
  els.resultCount.textContent = items.length === state.trophies.length
    ? `Showing all ${items.length} trophies — click any card for the full guide.`
    : `Showing ${items.length} of ${state.trophies.length} trophies.`;
  els.empty.hidden = items.length > 0;
  els.list.innerHTML = items.map((t) => `
    <button class="card${state.earned.has(t.id) ? " earned" : ""}" data-id="${t.id}" type="button">
      <span class="card-icon">${trophyIcon(t.grade)}</span>
      <span class="card-body">
        <span class="card-name">${esc(t.name)}</span>
        <span class="card-desc">${esc(t.description)}</span>
        <span class="card-meta">
          <span class="badge badge-${t.grade}">${t.grade}</span>
          <span class="meta-chip">Difficulty ${stars(t.difficulty || 1)}</span>
          <span class="meta-chip">${esc(t.time || "")}</span>
        </span>
      </span>
      <span class="card-check"><input type="checkbox" data-check="${t.id}" ${state.earned.has(t.id) ? "checked" : ""} aria-label="Mark ${esc(t.name)} as earned"></span>
    </button>`).join("");
}

function render() {
  renderProgress();
  renderList();
}

function openModal(id) {
  const t = state.trophies.find((x) => x.id === id);
  if (!t) return;
  state.openId = id;
  els.modalIcon.innerHTML = trophyIcon(t.grade, 84);
  els.modalName.textContent = t.name;
  els.modalDesc.textContent = t.description;
  els.modalMeta.innerHTML = `<span class="badge badge-${t.grade}">${t.grade}</span>
    <span class="meta-chip">Trophy #${t.id} of 55</span>`;
  els.modalGuide.textContent = t.guide;
  els.modalTips.textContent = t.tips || "—";
  els.modalMissable.textContent = t.missable || "—";
  els.modalDifficulty.innerHTML = `<span class="stars">${stars(t.difficulty || 1)}</span> ${t.difficulty || 1}/5`;
  els.modalTime.textContent = t.time || "—";
  els.modalEarned.checked = state.earned.has(t.id);
  els.modalBackdrop.hidden = false;
  els.modalClose.focus();
}

function closeModal() {
  state.openId = null;
  els.modalBackdrop.hidden = true;
}

function setEarned(id, on) {
  if (on) state.earned.add(id); else state.earned.delete(id);
  render();
}

els.list.addEventListener("click", (event) => {
  const check = event.target.closest("[data-check]");
  if (check) {
    event.stopPropagation();
    setEarned(Number(check.dataset.check), check.checked);
    return;
  }
  const card = event.target.closest(".card");
  if (card) openModal(Number(card.dataset.id));
});

document.querySelectorAll(".chip").forEach((chip) => {
  chip.addEventListener("click", () => {
    document.querySelectorAll(".chip").forEach((c) => c.classList.remove("active"));
    chip.classList.add("active");
    state.grade = chip.dataset.grade;
    renderList();
  });
});

els.search.addEventListener("input", () => { state.query = els.search.value; renderList(); });
els.hideEarned.addEventListener("change", () => { state.hideEarned = els.hideEarned.checked; renderList(); });
els.sort.addEventListener("change", () => { state.sort = els.sort.value; renderList(); });
els.modalClose.addEventListener("click", closeModal);
els.modalBackdrop.addEventListener("click", (event) => { if (event.target === els.modalBackdrop) closeModal(); });
document.addEventListener("keydown", (event) => { if (event.key === "Escape") closeModal(); });
els.modalEarned.addEventListener("change", () => {
  if (state.openId != null) setEarned(state.openId, els.modalEarned.checked);
});

// Press "/" anywhere to jump to the search box; "e" toggles hide-earned.
document.addEventListener("keydown", (event) => {
  const typing = /^(INPUT|SELECT|TEXTAREA)$/.test(document.activeElement?.tagName || "");
  if (typing || event.metaKey || event.ctrlKey) return;
  if (event.key === "/") { event.preventDefault(); els.search.focus(); }
  if (event.key === "e") {
    els.hideEarned.checked = !els.hideEarned.checked;
    state.hideEarned = els.hideEarned.checked;
    renderList();
  }
});

async function boot() {
  const res = await fetch("./data/trophies.json");
  const data = await res.json();
  state.trophies = data.trophies;
  render();
}

boot();
