(function(){
"use strict";

var GRADE_ORDER = { platinum: 0, gold: 1, silver: 2, bronze: 3 };
var GRADE_LABEL = { platinum: "Platinum", gold: "Gold", silver: "Silver", bronze: "Bronze" };
var GRADE_COLOR = { platinum: "#e5e7eb", gold: "#fbbf24", silver: "#94a3b8", bronze: "#e08a3c" };

var state = {
  trophies: [],
  earned: new Set(),
  query: "",
  grade: "all",
  hideEarned: false,
  sort: "default"
};

function trophySvg(color){
  return '<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true">' +
    '<path d="M7 4h10v5a5 5 0 0 1-10 0V4z" fill="none" stroke="' + color + '" stroke-width="1.8"/>' +
    '<path d="M7 5H4a3 3 0 0 0 3 3M17 5h3a3 3 0 0 1-3 3" fill="none" stroke="' + color + '" stroke-width="1.8" stroke-linecap="round"/>' +
    '<path d="M12 14v3M8.5 20h7M10 17h4v3h-4z" fill="none" stroke="' + color + '" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>' +
    '</svg>';
}

function stars(n){
  var d = Math.max(1, Math.min(5, Number(n) || 1));
  var s = "";
  for (var i = 1; i <= 5; i++) s += (i <= d ? "★" : "☆");
  return s;
}

function isMissable(t){
  var m = t.missable;
  if (m === true) return true;
  if (typeof m === "string") return /^\s*yes\b/i.test(m);
  return false;
}

function esc(s){
  return String(s == null ? "" : s)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
}

function defaultEarned(list){
  // A sensible lived-in default so the guide opens looking alive: 14 earned (25%).
  var byGrade = { platinum: [], gold: [], silver: [], bronze: [] };
  list.forEach(function(t){ if (byGrade[t.grade]) byGrade[t.grade].push(t.id); });
  // Spread across bronze/silver/gold — a Platinum in the first 14 would look fake.
  var picks = [].concat(byGrade.bronze.slice(0, 8), byGrade.silver.slice(0, 4), byGrade.gold.slice(0, 2));
  return new Set(picks.slice(0, 14));
}

function updateStats(){
  var total = state.trophies.length;
  var earnedCount = state.earned.size;
  var pct = total ? Math.round((earnedCount / total) * 100) : 0;
  document.getElementById("pctLabel").textContent = pct + "%";
  document.getElementById("countLabel").textContent = earnedCount + " / " + total + " earned";
  var circ = 326.7;
  document.getElementById("ringProgress").setAttribute("stroke-dashoffset", String(circ - (circ * pct / 100)));

  var host = document.getElementById("gradeStats");
  host.innerHTML = "";
  ["platinum", "gold", "silver", "bronze"].forEach(function(g){
    var inGrade = state.trophies.filter(function(t){ return t.grade === g; });
    var got = inGrade.filter(function(t){ return state.earned.has(t.id); }).length;
    var p = inGrade.length ? Math.round((got / inGrade.length) * 100) : 0;
    var div = document.createElement("div");
    div.className = "grade-stat";
    div.innerHTML =
      '<div class="g-name" style="color:' + GRADE_COLOR[g] + '">' + GRADE_LABEL[g] + '</div>' +
      '<div class="g-count">' + got + ' <span class="g-sub">/ ' + inGrade.length + '</span></div>' +
      '<div class="bar"><i style="width:' + p + '%;background:' + GRADE_COLOR[g] + '"></i></div>';
    host.appendChild(div);
  });
}

function filtered(){
  var q = state.query.trim().toLowerCase();
  var out = state.trophies.filter(function(t){
    if (state.grade !== "all" && t.grade !== state.grade) return false;
    if (state.hideEarned && state.earned.has(t.id)) return false;
    if (!q) return true;
    var hay = (t.name + " " + t.description + " " + t.guide + " " + (t.tips || "")).toLowerCase();
    return hay.indexOf(q) !== -1;
  });
  if (state.sort === "name") out.sort(function(a, b){ return a.name.localeCompare(b.name); });
  else if (state.sort === "grade") out.sort(function(a, b){ return (GRADE_ORDER[a.grade] - GRADE_ORDER[b.grade]) || (a.id - b.id); });
  else if (state.sort === "difficulty") out.sort(function(a, b){ return ((a.difficulty || 1) - (b.difficulty || 1)) || (a.id - b.id); });
  else out.sort(function(a, b){ return a.id - b.id; });
  return out;
}

function render(){
  updateStats();
  var list = filtered();
  var grid = document.getElementById("trophyGrid");
  var empty = document.getElementById("emptyState");
  document.getElementById("resultLine").textContent =
    "Showing " + list.length + " of " + state.trophies.length + " trophies" +
    (state.query ? ' for "' + state.query + '"' : "") +
    (state.grade !== "all" ? " · " + GRADE_LABEL[state.grade] : "") +
    (state.hideEarned ? " · earned hidden" : "");
  grid.innerHTML = "";
  empty.hidden = list.length !== 0;
  list.forEach(function(t){
    var isEarned = state.earned.has(t.id);
    var card = document.createElement("article");
    card.className = "card" + (isEarned ? " earned" : "");
    card.tabIndex = 0;
    card.setAttribute("role", "button");
    card.setAttribute("aria-label", t.name);
    card.innerHTML =
      '<div class="card-top">' +
        '<div class="trophy-icon">' + trophySvg(GRADE_COLOR[t.grade] || "#e5e7eb") + '</div>' +
        '<div><h3>' + esc(t.name) + '</h3><p class="desc">' + esc(t.description) + '</p></div>' +
      '</div>' +
      '<div class="meta-row">' +
        '<span class="grade-pill" style="color:' + (GRADE_COLOR[t.grade] || "#e5e7eb") + '">' + esc(GRADE_LABEL[t.grade] || t.grade) + '</span>' +
        '<span class="diff" title="Difficulty">' + stars(t.difficulty) + '</span>' +
        '<span class="time">' + esc(t.time || "") + '</span>' +
        (isMissable(t) ? '<span class="missable-flag">Missable</span>' : '') +
        '<label class="earn"><input type="checkbox" data-earn="' + t.id + '"' + (isEarned ? " checked" : "") + '> Earned</label>' +
      '</div>';
    card.addEventListener("click", function(ev){
      if (ev.target && ev.target.closest && ev.target.closest(".earn")) return;
      openModal(t);
    });
    card.addEventListener("keydown", function(ev){
      if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); openModal(t); }
    });
    grid.appendChild(card);
  });
  grid.querySelectorAll("[data-earn]").forEach(function(box){
    box.addEventListener("change", function(){
      var id = Number(box.getAttribute("data-earn"));
      if (box.checked) state.earned.add(id); else state.earned.delete(id);
      render();
    });
    box.addEventListener("click", function(ev){ ev.stopPropagation(); });
  });
}

function openModal(t){
  var body = document.getElementById("modalBody");
  var isEarned = state.earned.has(t.id);
  body.innerHTML =
    '<h2 id="modalTitle">' + esc(t.name) + '</h2>' +
    '<p class="modal-desc">' + esc(t.description) + '</p>' +
    '<span class="grade-pill" style="color:' + (GRADE_COLOR[t.grade] || "#e5e7eb") + '">' + esc(GRADE_LABEL[t.grade] || t.grade) + ' trophy</span>' +
    '<div class="modal-section"><h4>Guide</h4><p>' + esc(t.guide) + '</p></div>' +
    (t.tips ? '<div class="modal-section"><h4>Pro tip</h4><p>' + esc(t.tips) + '</p></div>' : '') +
    '<div class="modal-grid">' +
      '<div class="fact"><div class="f-label">Difficulty</div><div class="f-value"><span class="stars">' + stars(t.difficulty) + '</span> ' + esc(t.difficulty) + '/5</div></div>' +
      '<div class="fact"><div class="f-label">Time estimate</div><div class="f-value">' + esc(t.time || "—") + '</div></div>' +
      '<div class="fact"><div class="f-label">Missable</div><div class="f-value">' + esc(typeof t.missable === "string" ? t.missable : (t.missable ? "Yes — missable." : "No — can be earned anytime.")) + '</div></div>' +
      '<div class="fact"><div class="f-label">Trophy ID</div><div class="f-value">#' + esc(t.id) + '</div></div>' +
    '</div>' +
    '<label class="earn"><input type="checkbox" id="modalEarn"' + (isEarned ? " checked" : "") + '> Mark as earned</label>';
  document.getElementById("modalBackdrop").hidden = false;
  var box = document.getElementById("modalEarn");
  box.addEventListener("change", function(){
    if (box.checked) state.earned.add(t.id); else state.earned.delete(t.id);
    render();
  });
  document.getElementById("modalClose").focus();
}

function closeModal(){
  document.getElementById("modalBackdrop").hidden = true;
}

function buildChips(){
  var host = document.getElementById("gradeChips");
  host.innerHTML = "";
  var opts = [{ key: "all", label: "All" }].concat(
    ["platinum", "gold", "silver", "bronze"].map(function(g){ return { key: g, label: GRADE_LABEL[g] }; })
  );
  opts.forEach(function(o){
    var b = document.createElement("button");
    b.type = "button";
    b.className = "chip" + (state.grade === o.key ? " active" : "");
    b.textContent = o.label;
    b.addEventListener("click", function(){
      state.grade = o.key;
      buildChips();
      render();
    });
    host.appendChild(b);
  });
}

function wire(){
  var search = document.getElementById("searchInput");
  search.addEventListener("input", function(){
    state.query = search.value;
    render();
  });
  document.getElementById("hideEarned").addEventListener("change", function(ev){
    state.hideEarned = ev.target.checked;
    render();
  });
  document.getElementById("sortSelect").addEventListener("change", function(ev){
    state.sort = ev.target.value;
    render();
  });
  document.getElementById("modalClose").addEventListener("click", closeModal);
  document.getElementById("modalBackdrop").addEventListener("click", function(ev){
    if (ev.target === ev.currentTarget) closeModal();
  });
  document.addEventListener("keydown", function(ev){
    var tag = (document.activeElement && document.activeElement.tagName) || "";
    var typing = tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT";
    if (ev.key === "Escape") { closeModal(); return; }
    if (typing) return;
    if (ev.key === "/") { ev.preventDefault(); search.focus(); search.select(); }
    if (ev.key === "e" || ev.key === "E") {
      state.hideEarned = !state.hideEarned;
      document.getElementById("hideEarned").checked = state.hideEarned;
      render();
    }
  });
}

function boot(){
  wire();
  buildChips();
  fetch("data/trophies.json")
    .then(function(r){ return r.json(); })
    .then(function(data){
      var list = Array.isArray(data) ? data : (data.trophies || []);
      state.trophies = list.slice().sort(function(a, b){ return a.id - b.id; });
      state.earned = defaultEarned(state.trophies);
      render();
    })
    .catch(function(err){
      document.getElementById("resultLine").textContent = "Could not load trophy data.";
      console.error(err);
    });
}

document.addEventListener("DOMContentLoaded", boot);
})();
