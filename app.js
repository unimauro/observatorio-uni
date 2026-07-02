// Observatorio UNI — carga data/*.json y renderiza. Sin build, vanilla + Chart.js.
const CFG = window.OBS_UNI_CONFIG || {};
const GRANATE = '#9e1020', GRANATE2 = '#7a0019', ORO = '#c9962e', TEAL = '#0e7c86';
const fmtM = v => 'S/ ' + (v / 1e6).toLocaleString('es-PE', { maximumFractionDigits: 1 }) + ' M';
const fmtN = v => (v || 0).toLocaleString('es-PE');
const isDark = () => document.documentElement.getAttribute('data-theme') === 'dark';
const ink = () => isDark() ? '#c3a9a2' : '#6b5f5a';
const grid = () => isDark() ? 'rgba(255,255,255,.06)' : 'rgba(0,0,0,.06)';
Chart.defaults.font.family = getComputedStyle(document.body).fontFamily;
Chart.defaults.color = ink();

// ---- tema ----
function toggleTheme() {
  const d = isDark();
  document.documentElement.setAttribute('data-theme', d ? 'light' : 'dark');
  localStorage.setItem('obsuni_theme', d ? 'light' : 'dark');
  document.getElementById('tglBtn').textContent = d ? '🌙 Tema' : '☀️ Tema';
  Chart.defaults.color = ink();
  Object.values(Chart.instances).forEach(c => c.destroy());
  render(); // redraw with new theme
}
(function initTheme() {
  const t = localStorage.getItem('obsuni_theme');
  if (t) document.documentElement.setAttribute('data-theme', t);
  if (isDark()) document.getElementById('tglBtn').textContent = '☀️ Tema';
})();

// ---- scrollspy ----
const navA = [...document.querySelectorAll('nav.links a')];
window.addEventListener('scroll', () => {
  let cur = '';
  document.querySelectorAll('section').forEach(s => { if (window.scrollY >= s.offsetTop - 120) cur = s.id; });
  navA.forEach(a => a.classList.toggle('on', a.getAttribute('href') === '#' + cur));
});
navA.forEach(a => a.addEventListener('click', () => document.getElementById('nav').classList.remove('show')));

// ---- data ----
let DATA = {};
async function load(name) { try { const r = await fetch('data/' + name + '?v=' + Date.now()); return r.ok ? await r.json() : null; } catch { return null; } }

async function boot() {
  DATA.presu = await load('presupuesto-uni.json');
  DATA.biblio = await load('bibliometria.json');
  DATA.adm = await load('admision-uni.json');
  DATA.prov = await load('proveedores-uni.json');
  DATA.plan = await load('planilla-uni.json');
  render();
}

function opts(extra = {}) {
  return Object.assign({
    responsive: true, maintainAspectRatio: false,
    plugins: { legend: { labels: { boxWidth: 12 } } },
    scales: { x: { grid: { color: grid() } }, y: { grid: { color: grid() }, beginAtZero: true } }
  }, extra);
}

function render() {
  renderKpis(); renderPresu(); renderGasto(); renderProv(); renderInv(); renderAdm(); renderPlan();
}

// ---- KPIs ----
function renderKpis() {
  const el = document.getElementById('kpis'); if (!el) return;
  const k = [];
  const s = DATA.presu?.serie;
  if (s && s.length) {
    const last = s[s.length - 1];
    k.push(['PIM ' + last.year, fmtM(last.pim), 'Presupuesto modificado']);
    k.push(['Devengado ' + last.year, fmtM(last.dev), last.ejec_pct + '% de ejecución']);
  } else {
    k.push(['PIM 2025', 'S/ 370.6 M', 'Pliego 514 (MEF)']);
    k.push(['Devengado 2025', 'S/ 338.3 M', '91.3% de ejecución']);
  }
  const b = DATA.biblio?.uni;
  if (b) { k.push(['Publicaciones', fmtN(b.works), 'histórico (OpenAlex)']); k.push(['Citas · h-index', fmtN(b.cited) + ' · ' + b.h_index, 'impacto científico']); }
  if (DATA.adm?._meta) k.push(['Ingresantes', fmtN(DATA.adm._meta.total_ingresantes), 'de ' + fmtN(DATA.adm._meta.total_postulantes) + ' postulantes']);
  const d = DATA.biblio?.docentes;
  if (d) k.push(['Docentes', fmtN(d.total), d.posgrado_pct + '% con posgrado (' + d.anio + ')']);
  el.innerHTML = k.map(x => `<div class="kpi"><div class="v">${x[1]}</div><div class="l">${x[0]}</div><div class="s">${x[2] || ''}</div></div>`).join('');
}

// ---- Presupuesto ----
function renderPresu() {
  const s = DATA.presu?.serie;
  if (!s || !s.length) { document.getElementById('presupNote').textContent = 'Cargando serie histórica del MEF…'; return; }
  new Chart(cSerie, {
    type: 'bar',
    data: {
      labels: s.map(x => x.year),
      datasets: [
        { label: 'PIM', data: s.map(x => x.pim / 1e6), backgroundColor: ORO },
        { label: 'Devengado', data: s.map(x => x.dev / 1e6), backgroundColor: GRANATE },
      ]
    }, options: opts({ plugins: { legend: { labels: { boxWidth: 12 } }, tooltip: { callbacks: { label: c => c.dataset.label + ': S/ ' + c.raw.toFixed(1) + ' M' } } } })
  });
  new Chart(cEjec, {
    type: 'line',
    data: { labels: s.map(x => x.year), datasets: [{ label: '% ejecución', data: s.map(x => x.ejec_pct), borderColor: GRANATE, backgroundColor: 'rgba(158,16,32,.12)', fill: true, tension: .3 }] },
    options: opts({ scales: { x: { grid: { color: grid() } }, y: { grid: { color: grid() }, min: 60, max: 100 } } })
  });
  const first = s[0], last = s[s.length - 1];
  document.getElementById('presupNote').textContent = `Serie ${first.year}–${last.year}. Fuente: ${DATA.presu._meta.fuente}. ${DATA.presu._meta.pliego}.`;
}

// ---- En qué se gasta ----
function donut(ctx, rows, valueKey = 'dev', top = 8) {
  const r = [...rows].sort((a, b) => b[valueKey] - a[valueKey]);
  const head = r.slice(0, top), rest = r.slice(top).reduce((s, x) => s + x[valueKey], 0);
  const labels = head.map(x => (x.nombre || '—').replace(/^\d+[:.\-]?\s*/, '').slice(0, 32));
  const vals = head.map(x => x[valueKey] / 1e6);
  if (rest > 0) { labels.push('Otros'); vals.push(rest / 1e6); }
  const cols = ['#9e1020', '#c9962e', '#7a0019', '#0e7c86', '#5c0013', '#d98c3a', '#a8324a', '#3a7d6f', '#8a6d1f', '#b5495f'];
  new Chart(ctx, {
    type: 'doughnut', data: { labels, datasets: [{ data: vals, backgroundColor: cols }] },
    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'right', labels: { boxWidth: 12, font: { size: 11 } } }, tooltip: { callbacks: { label: c => c.label + ': S/ ' + c.raw.toFixed(1) + ' M' } } } }
  });
}
function renderGasto() {
  const d = DATA.presu?.detalle_ultimo_anio;
  if (!d) return;
  const gen = d.por_categoria?.length ? d.por_categoria : d.por_generica;
  if (gen?.length) donut(cGen, gen);
  if (d.por_unidad?.length) donut(cUni, d.por_unidad);
  const tb = document.querySelector('#tFun tbody');
  if (tb && d.por_funcion?.length) {
    tb.innerHTML = d.por_funcion.map(x => `<tr><td>${(x.nombre || '—').replace(/^\d+[:.\-]?\s*/, '')}</td><td class="n">${fmtN(Math.round(x.pim))}</td><td class="n">${fmtN(Math.round(x.dev))}</td><td class="n">${x.pim ? Math.round(100 * x.dev / x.pim) + '%' : '—'}</td></tr>`).join('');
  }
}

// ---- Proveedores ----
function renderProv() {
  const w = document.getElementById('provWrap');
  if (DATA.prov?.proveedores?.length) {
    const p = DATA.prov.proveedores.slice(0, 30);
    w.innerHTML = `<div class="card"><div class="scroll"><table><thead><tr><th>Proveedor</th><th>RUC</th><th class="n">Monto (S/)</th><th class="n">N.º contratos</th><th>Dueño / representante</th></tr></thead><tbody>${p.map(x => `<tr><td>${x.nombre}</td><td>${x.ruc || '—'}</td><td class="n">${fmtN(Math.round(x.monto))}</td><td class="n">${x.n || '—'}</td><td>${x.dueno || '<span class="pill">por cruzar</span>'}</td></tr>`).join('')}</tbody></table></div><p class="note">Fuente: ${DATA.prov._meta?.fuente || 'OECE/OCDS'}.</p></div>`;
  } else {
    w.innerHTML = `<div class="soon"><h3>🔎 En construcción</h3><p style="margin:0;color:var(--muted)">Estamos descargando y cruzando las contrataciones de la UNI desde la API de <strong>Contrataciones Abiertas del OECE</strong> (estándar OCDS) para listar cada proveedor, su RUC, el monto que recibió y —cuando sea posible— a sus dueños/representantes legales. Aparecerá aquí en la próxima actualización de datos.</p></div>`;
  }
}

// ---- Investigación ----
function renderInv() {
  const b = DATA.biblio?.uni; if (!b?.by_year) return;
  const y = b.by_year.filter(x => x.year <= 2025);
  new Chart(cInv, {
    data: {
      labels: y.map(x => x.year),
      datasets: [
        { type: 'bar', label: 'Publicaciones', data: y.map(x => x.works), backgroundColor: GRANATE, yAxisID: 'y' },
        { type: 'line', label: 'Citas', data: y.map(x => x.cited), borderColor: ORO, backgroundColor: 'transparent', tension: .3, yAxisID: 'y1' },
      ]
    },
    options: { responsive: true, maintainAspectRatio: false, scales: { x: { grid: { color: grid() } }, y: { position: 'left', grid: { color: grid() }, beginAtZero: true }, y1: { position: 'right', grid: { drawOnChartArea: false }, beginAtZero: true } } }
  });
  const peers = [['uni', 'UNI'], ['sanmarcos', 'San Marcos'], ['pucp', 'PUCP'], ['cayetano', 'Cayetano'], ['unalm', 'La Molina'], ['upc', 'UPC']]
    .map(([k, n]) => DATA.biblio[k] ? { n, v: DATA.biblio[k].works } : null).filter(Boolean).sort((a, b) => b.v - a.v);
  new Chart(cPares, {
    type: 'bar', data: { labels: peers.map(x => x.n), datasets: [{ label: 'Publicaciones', data: peers.map(x => x.v), backgroundColor: peers.map(x => x.n === 'UNI' ? GRANATE : ORO) }] },
    options: opts({ indexAxis: 'y', plugins: { legend: { display: false } } })
  });
  document.getElementById('invNote').textContent = `UNI: ${fmtN(b.works)} publicaciones, ${fmtN(b.cited)} citas, h-index ${b.h_index} (OpenAlex, ${DATA.biblio._meta?.extraido || '2026'}).`;
}

// ---- Admisión (SOLO agregados — nunca nombres) ----
function renderAdm() {
  const a = DATA.adm; if (!a) return;
  const esp = a.ingresantes_por_especialidad || a.por_especialidad;
  const mod = a.ingresantes_por_modalidad || a.por_modalidad;
  if (esp?.length) {
    const e = esp.slice(0, 15);
    new Chart(cEsp, { type: 'bar', data: { labels: e.map(x => x.nombre.replace('INGENIERÍA ', 'Ing. ')), datasets: [{ label: 'Ingresantes', data: e.map(x => x.n), backgroundColor: GRANATE }] }, options: opts({ indexAxis: 'y', plugins: { legend: { display: false } } }) });
  }
  if (mod?.length) {
    const m = mod.slice(0, 10);
    new Chart(cMod, { type: 'bar', data: { labels: m.map(x => x.nombre.slice(0, 26)), datasets: [{ label: 'Ingresantes', data: m.map(x => x.n), backgroundColor: ORO }] }, options: opts({ indexAxis: 'y', plugins: { legend: { display: false } } }) });
  }
  const pp = a.puntaje_postulantes, pi = a.puntaje_ingresantes;
  document.getElementById('admNote').textContent =
    `${fmtN(a._meta.total_ingresantes)} ingresantes de ${fmtN(a._meta.total_postulantes)} postulantes` +
    (pi?.prom ? `. Puntaje final promedio: ingresantes ${pi.prom} vs. postulantes ${pp?.prom}` : '') +
    `. Solo datos agregados: este portal no publica nombres de estudiantes.`;
}

// ---- Planilla ----
function renderPlan() {
  const w = document.getElementById('planWrap');
  if (DATA.plan?.personas?.length) {
    const p = DATA.plan.personas.slice(0, 40);
    w.innerHTML = `<div class="card"><div class="scroll"><table><thead><tr><th>Nombre</th><th>Cargo / categoría</th><th>Régimen</th><th class="n">Remuneración (S/)</th></tr></thead><tbody>${p.map(x => `<tr><td>${x.nombre}</td><td>${x.cargo || '—'}</td><td>${x.regimen || '—'}</td><td class="n">${x.remun ? fmtN(Math.round(x.remun)) : '—'}</td></tr>`).join('')}</tbody></table></div><p class="note">Fuente: ${DATA.plan._meta?.fuente || 'datos nominales del sector público'}. Solo docentes, funcionarios y personal (no estudiantes).</p></div>`;
  } else {
    w.innerHTML = `<div class="soon"><h3>🔎 En construcción</h3><p style="margin:0;color:var(--muted)">Estamos cruzando la planilla nominal de la UNI (docentes, funcionarios y planas mayores, con sus remuneraciones) a partir de datos públicos del Estado (AIRHSP / portal de transparencia). Por diseño, este portal <strong>solo muestra personal — nunca nombres de estudiantes</strong>.</p></div>`;
  }
}

// ---- Asistente IA ----
async function sendChat() {
  const inp = document.getElementById('chatIn'), box = document.getElementById('msgs');
  const q = inp.value.trim(); if (!q) return;
  inp.value = '';
  box.insertAdjacentHTML('beforeend', `<div class="m u">${q.replace(/</g, '&lt;')}</div>`);
  const wait = document.createElement('div'); wait.className = 'm a'; wait.textContent = '…'; box.appendChild(wait); box.scrollTop = box.scrollHeight;
  const ctx = buildCtx();
  try {
    const r = await fetch(CFG.AI_ENDPOINT, {
      method: 'POST', headers: { 'Content-Type': 'application/json', 'X-Client-Token': CFG.AI_TOKEN },
      body: JSON.stringify({ project: CFG.AI_PROJECT, messages: [{ role: 'system', content: ctx }, { role: 'user', content: q }] })
    });
    const j = await r.json();
    wait.textContent = j.reply || j.message || 'No pude responder ahora, intenta de nuevo.';
  } catch { wait.textContent = 'Servicio no disponible por ahora.'; }
  box.scrollTop = box.scrollHeight;
}
function buildCtx() {
  const s = DATA.presu?.serie, b = DATA.biblio?.uni;
  let c = 'Eres el asistente del Observatorio UNI, un portal ciudadano de transparencia de la Universidad Nacional de Ingeniería del Perú, con datos públicos (MEF, OECE, OpenAlex). Responde corto, en español, solo sobre la UNI y sus datos. No inventes cifras.';
  if (s?.length) { const l = s[s.length - 1]; c += ` Presupuesto ${l.year}: PIM S/${(l.pim / 1e6).toFixed(1)}M, devengado S/${(l.dev / 1e6).toFixed(1)}M (${l.ejec_pct}%).`; }
  if (b) c += ` Investigación: ${b.works} publicaciones, ${b.cited} citas, h-index ${b.h_index}.`;
  if (DATA.adm?._meta) c += ` Ingresantes: ${DATA.adm._meta.total_ingresantes}.`;
  return c;
}

boot();
