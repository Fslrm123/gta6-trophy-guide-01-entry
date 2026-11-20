// Leonida Legend — offline GTA VI trophy guide & tracker.
// Loads app/data/trophies.json (same origin only), renders the checklist,
// filters, search and detail modal. Earned state persists in localStorage;
// a first visit seeds a starter set so the progress header is alive.
const KEY = 'leonida-legend-earned-v1';
// Starter earned set (14 of 55): both golds, 4 of 6 silvers, 8 bronzes.
const SEED = [7, 14, 15, 17, 25, 30, 2, 3, 4, 5, 6, 8, 9, 10];
const GRADES = ['platinum', 'gold', 'silver', 'bronze'];
const GRADE_LABEL = { platinum: 'Platinum', gold: 'Gold', silver: 'Silver', bronze: 'Bronze' };
const GRADE_COLOR = { platinum: '#d9e6ff', gold: '#f5c451', silver: '#c3cad9', bronze: '#d08a4e' };
const RING_C = 326.7; // 2 * pi * 52

const $ = (id) => document.getElementById(id);
const els = {
  grid: $('grid'), empty: $('empty'), resultLine: $('resultLine'),
  search: $('search'), chips: $('chips'), hideEarned: $('hideEarned'), sort: $('sort'),
  ringFill: $('ringFill'), ringPct: $('ringPct'), ringCount: $('ringCount'),
  gradeCards: $('gradeCards'),
  backdrop: $('modalBackdrop'), modalClose: $('modalClose'), modalIcon: $('modalIcon'),
  modalTitle: $('modalTitle'), modalDesc: $('modalDesc'), modalGrade: $('modalGrade'),
  factGrid: $('factGrid'), modalGuide: $('modalGuide'), modalTip: $('modalTip'),
  modalEarned: $('modalEarned'),
};

let trophies = [];
let earned = loadEarned();
let gradeFilter = 'all';
let query = '';
let hideEarned = false;
let sortMode = 'default';
let openId = null;

function loadEarned() {
  try {
    const raw = localStorage.getItem(KEY);
    if (raw) return new Set(JSON.parse(raw));
  } catch { /* storage unavailable: fall through to the seed */ }
  return new Set(SEED);
}
function save() {
  try { localStorage.setItem(KEY, JSON.stringify([...earned])); } catch { /* offline/private mode */ }
}

function trophySvg(grade) {
  const c = GRADE_COLOR[grade];
  return `<svg viewBox="0 0 48 48" aria-hidden="true"><path fill="${c}" d="M14 6h20v4h6c0 7-3.6 11.4-9 12.4A10 10 0 0 1 27 27.6V32h5v4H16v-4h5v-4.4A10 10 0 0 1 17 22.4C11.6 21.4 8 17 8 10h6V6zm-3.2 7c.6 3 2 5 4 6.2A12 12 0 0 1 14 13h-3.2zm26.4 0H34a12 12 0 0 1-.8 6.2c2-1.2 3.4-3.2 4-6.2zM20 38h8v3h-8v-3z"/></svg>`;
}
function stars(n) {
  let s = '';
  for (let i = 1; i <= 5; i++) s += i <= n ? '★' : '<span class="off">★</span>';
  return `<span class="stars" role="img" aria-label="Difficulty ${n} of 5">${s}</span>`;
}
function matches(t) {
  if (gradeFilter !== 'all' && t.grade !== gradeFilter) return false;
  if (hideEarned && earned.has(t.id)) return false;
  if (query) {
    const hay = `${t.name} ${t.description} ${t.guide}`.toLowerCase();
    if (!hay.includes(query)) return false;
  }
  return true;
}
function sorted(list) {
  const out = [...list];
  if (sortMode === 'name') out.sort((a, b) => a.name.localeCompare(b.name));
  else if (sortMode === 'difficulty') out.sort((a, b) => a.difficulty - b.difficulty || a.id - b.id);
  else if (sortMode === 'time') out.sort((a, b) => (a.timeMin ?? 9999) - (b.timeMin ?? 9999) || a.id - b.id);
  else out.sort((a, b) => a.id - b.id);
  return out;
}

function renderHeader() {
  const total = trophies.length;
  const got = trophies.filter((t) => earned.has(t.id)).length;
  const pct = total ? Math.round((got / total) * 100) : 0;
  els.ringPct.textContent = `${pct}%`;
  els.ringCount.textContent = `${got} / ${total}`;
  els.ringFill.style.strokeDashoffset = String(RING_C * (1 - (total ? got / total : 0)));
  els.gradeCards.replaceChildren();
  for (const g of GRADES) {
    const all = trophies.filter((t) => t.grade === g);
    const has = all.filter((t) => earned.has(t.id)).length;
    const card = document.createElement('div');
    card.className = `grade-card g-${g}`;
    const w = all.length ? Math.round((has / all.length) * 100) : 0;
    card.innerHTML = `<div class="g-name">${GRADE_LABEL[g]}</div><div class="g-count">${has} <small>/ ${all.length} earned</small></div><div class="bar"><i style="width:${w}%"></i></div>`;
    els.gradeCards.append(card);
  }
}

function render() {
  renderHeader();
  const visible = sorted(trophies.filter(matches));
  els.grid.replaceChildren();
  for (const t of visible) {
    const isEarned = earned.has(t.id);
    const card = document.createElement('article');
    card.className = `card${isEarned ? ' is-earned' : ''}`;
    card.dataset.id = String(t.id);
    card.innerHTML = `
      <div class="trophy-icon">${trophySvg(t.grade)}</div>
      <div class="card-body">
        <div class="card-top">
          <h3></h3>
          ${isEarned ? '<span class="earned-pill">Earned</span>' : ''}
        </div>
        <p class="desc"></p>
        <div class="card-meta">
          <span class="grade-tag ${t.grade}">${GRADE_LABEL[t.grade]}</span>
          ${stars(t.difficulty)}
          <span>${t.time}</span>
        </div>
        <label class="card-check">
          <input type="checkbox" ${isEarned ? 'checked' : ''} aria-label="Mark ${t.name} as earned">
          <span>${isEarned ? 'Earned' : 'Mark earned'}</span>
        </label>
      </div>`;
    card.querySelector('h3').textContent = t.name;
    card.querySelector('.desc').textContent = t.description;
    const box = card.querySelector('input[type="checkbox"]');
    box.addEventListener('click', (e) => e.stopPropagation());
    box.addEventListener('change', () => {
      if (box.checked) earned.add(t.id); else earned.delete(t.id);
      save();
      render();
    });
    card.addEventListener('click', () => openModal(t.id));
    els.grid.append(card);
  }
  els.empty.hidden = visible.length > 0;
  const bits = [`Showing ${visible.length} of ${trophies.length} trophies`];
  if (gradeFilter !== 'all') bits.push(GRADE_LABEL[gradeFilter]);
  if (query) bits.push(`matching “${query}”`);
  if (hideEarned) bits.push('earned hidden');
  els.resultLine.textContent = bits.join(' · ');
}

function openModal(id) {
  const t = trophies.find((x) => x.id === id);
  if (!t) return;
  openId = id;
  els.modalIcon.innerHTML = trophySvg(t.grade);
  els.modalTitle.textContent = t.name;
  els.modalDesc.textContent = t.description;
  els.modalGrade.textContent = `${GRADE_LABEL[t.grade]} trophy`;
  els.modalGrade.style.color = GRADE_COLOR[t.grade];
  els.factGrid.innerHTML = `
    <div class="fact"><div class="f-label">Difficulty</div><div class="f-value">${stars(t.difficulty)}</div></div>
    <div class="fact"><div class="f-label">Time estimate</div><div class="f-value">${t.time}</div></div>
    <div class="fact"><div class="f-label">Missable</div><div class="f-value"></div></div>
    <div class="fact"><div class="f-label">Trophy ID</div><div class="f-value">#${t.id} of 55</div></div>`;
  els.factGrid.querySelectorAll('.f-value')[2].textContent = t.missable;
  els.modalGuide.textContent = t.guide;
  els.modalTip.textContent = t.tips;
  els.modalEarned.checked = earned.has(t.id);
  els.backdrop.hidden = false;
  els.modalClose.focus();
}
function closeModal() {
  els.backdrop.hidden = true;
  openId = null;
}

els.modalEarned.addEventListener('change', () => {
  if (openId === null) return;
  if (els.modalEarned.checked) earned.add(openId); else earned.delete(openId);
  save();
  render();
});
els.modalClose.addEventListener('click', closeModal);
els.backdrop.addEventListener('click', (e) => { if (e.target === els.backdrop) closeModal(); });

els.search.addEventListener('input', () => {
  query = els.search.value.trim().toLowerCase();
  render();
});
els.chips.addEventListener('click', (e) => {
  const btn = e.target.closest('.chip');
  if (!btn) return;
  gradeFilter = btn.dataset.grade;
  for (const c of els.chips.querySelectorAll('.chip')) c.classList.toggle('is-active', c === btn);
  render();
});
els.hideEarned.addEventListener('change', () => {
  hideEarned = els.hideEarned.checked;
  render();
});
els.sort.addEventListener('change', () => {
  sortMode = els.sort.value;
  render();
});
document.addEventListener('keydown', (e) => {
  const typing = /^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement?.tagName ?? '');
  if (e.key === 'Escape' && !els.backdrop.hidden) { closeModal(); return; }
  if (typing) return;
  if (e.key === '/') { e.preventDefault(); els.search.focus(); }
  else if (e.key.toLowerCase() === 'e') {
    hideEarned = !hideEarned;
    els.hideEarned.checked = hideEarned;
    render();
  }
});

function applyUrlState() {
  const p = new URLSearchParams(location.search);
  const q = p.get('q');
  if (q) { query = q.toLowerCase(); els.search.value = q; }
  const g = p.get('grade');
  if (g && GRADES.includes(g)) {
    gradeFilter = g;
    for (const c of els.chips.querySelectorAll('.chip')) c.classList.toggle('is-active', c.dataset.grade === g);
  }
  const s = p.get('sort');
  if (s && ['default', 'name', 'difficulty', 'time'].includes(s)) { sortMode = s; els.sort.value = s; }
  if (p.get('hide') === '1') { hideEarned = true; els.hideEarned.checked = true; }
  return p.get('trophy');
}

const doc = await (await fetch('data/trophies.json')).json();
trophies = doc.trophies;
const openParam = applyUrlState();
render();
if (openParam) {
  const byName = trophies.find((t) => t.name.toLowerCase() === openParam.toLowerCase());
  const byId = trophies.find((t) => String(t.id) === openParam);
  const target = byName ?? byId;
  if (target) openModal(target.id);
}
