// verify-boutique.mjs — measure what boutique.html actually builds, with no browser.
//
//     node tools/verify-boutique.mjs
//
// This Mac's PSN-069 guard routinely blocks a preview server (8GB RAM, several
// Claude sessions resident), and `file://` in the preview pane renders a static
// snapshot with NO JavaScript — it reports zero slides and zero tiles on a page
// that builds both from script, which reads exactly like a broken page.
//
// So this runs the REAL script.js under node:vm against a recording DOM shim and
// prints what it built. That is a measurement, not a code read.
//
// ⚠️ IT DOES NOT RUN TO COMPLETION, BY DESIGN. The shim stops around script.js
// line 391 on a `window.addEventListener` gap. Every boutique code path lives in
// lines 26-278, so the readings below are complete before it stops — `scriptError`
// is expected to be non-null. If that error ever moves EARLIER than line 278, the
// readings are no longer trustworthy: widen the shim, do not ignore it.
//
// ⚠️ IT MEASURES CONTENT AND WIRING, NEVER LAYOUT. Nothing here can tell you how
// five stacked rails read at 390px. That still needs a real browser.
import fs from 'node:fs';
import vm from 'node:vm';
const DIR = "/Users/kushjain/Developer/voiding szn 1/Freelance/Henna By Neena/website";
const html = fs.readFileSync(`${DIR}/boutique.html`, 'utf8');

let idc = 0;
const mk = (tag, attrs = {}) => {
  const el = {
    tagName: tag, _id: ++idc, children: [], attrs, dataset: {}, style: {},
    className: '', textContent: '', _innerHTML: '', hidden: false,
    get innerHTML() { return this._innerHTML; },
    set innerHTML(v) { this._innerHTML = v; },
    appendChild(c) { this.children.push(c); return c; },
    setAttribute(k, v) { this.attrs[k] = v; },
    getAttribute(k) { return this.attrs[k] ?? null; },
    removeAttribute(k) { delete this.attrs[k]; },
    addEventListener() {}, removeEventListener() {},
    replaceWith() { this._replaced = true; },
    querySelector(sel) { return find([this], sel)[0] ?? null; },
    querySelectorAll(sel) { return find([this], sel); },
    classList: { add() {}, remove() {}, toggle() {}, contains: () => false },
    getBoundingClientRect: () => ({ top:0,left:0,width:0,height:0,bottom:0,right:0 }),
    closest: () => null, focus() {}, matches: () => false,
  };
  return el;
};
function walk(el, out = []) { out.push(el); el.children.forEach(c => walk(c, out)); return out; }
function find(roots, sel) {
  const all = roots.flatMap(r => walk(r)).slice();
  const m = sel.match(/^\.?([\w-]+)?(?:\[data-([\w-]+)="([^"]+)"\])?$/);
  return all.filter(el => {
    if (sel.startsWith('.')) {
      const cls = sel.slice(1).split('[')[0];
      if (!String(el.className).split(/\s+/).includes(cls)) return false;
    }
    const dm = sel.match(/\[data-([\w-]+)="([^"]+)"\]/);
    if (dm) { const key = dm[1].replace(/-(\w)/g,(_,c)=>c.toUpperCase()); if (el.dataset[key] !== dm[2]) return false; }
    const am = sel.match(/^\[data-([\w-]+)\]$/);
    if (am) { const key = am[1].replace(/-(\w)/g,(_,c)=>c.toUpperCase()); if (!(key in el.dataset)) return false; }
    return true;
  });
}

// Build a real tree from boutique.html's rail + grid structure.
const root = mk('body');
const byId = {};
for (const m of html.matchAll(/<div class="gallery-collection" data-collection="([\w-]+)">/g)) {
  const block = mk('div'); block.className = 'gallery-collection'; block.dataset.collection = m[1];
  const wrap = mk('div'); wrap.className = 'swiper-wrapper gallery-wrapper';
  block.appendChild(wrap); root.appendChild(block);
}
for (const id of ['boutiqueGrid','boutiqueTabs']) { const e = mk('div'); byId[id] = e; root.appendChild(e); }
for (const c of ['clothing','jewelry','accessories']) {
  const img = mk('img'); img.dataset.boutiqueCover = c; img.className=''; root.appendChild(img);
}

const doc = {
  querySelector: s => find([root], s)[0] ?? null,
  querySelectorAll: s => find([root], s),
  getElementById: id => byId[id] ?? null,
  createElement: mk, addEventListener(){}, documentElement: mk('html'),
  body: root, head: mk('head'), hidden:false, visibilityState:'visible',
};
const ctx = vm.createContext({
  document: doc, window: {}, console,
  Swiper: class { constructor(){ this.slides=[]; this.on=()=>{}; } },
  IntersectionObserver: class { observe(){} unobserve(){} disconnect(){} },
  ResizeObserver: class { observe(){} disconnect(){} },
  matchMedia: () => ({ matches:false, addEventListener(){}, addListener(){} }),
  requestAnimationFrame: cb => cb(0), setTimeout, clearTimeout, setInterval, clearInterval,
  WeakSet, Set, Map, Math, JSON, Date, Array, Object, String, Number, Boolean,
});
ctx.window = ctx; ctx.globalThis = ctx;

let err = null;
try {
  vm.runInContext(fs.readFileSync(`${DIR}/boutique-data.js`,'utf8'), ctx);
  vm.runInContext(fs.readFileSync(`${DIR}/script.js`,'utf8'), ctx);
} catch (e) { err = `${e.name}: ${e.message}`; }

const rails = find([root],'.gallery-collection').map(b => ({
  id: b.dataset.collection, hidden: b.hidden,
  slides: (b.querySelector('.gallery-wrapper')?.children.length) ?? 0,
}));
const gridHTML = byId.boutiqueGrid.innerHTML;
const tileNames = [...gridHTML.matchAll(/<h3>([^<]+)<\/h3>/g)].map(m=>m[1]);
const tileSrcs  = [...gridHTML.matchAll(/<img src="([^"]+)" alt="([^"]*)"/g)].map(m=>({src:m[1],alt:m[2]}));
const covers = find([root],'[data-boutique-cover]').map(i=>({
  cover:i.dataset.boutiqueCover, src:i.attrs.src ?? i.src ?? null, cls:i.className, replaced:!!i._replaced}));
console.log(JSON.stringify({ scriptError: err, rails,
  tabs: byId.boutiqueTabs.children.map(b=>b.textContent),
  tileCount: tileNames.length, tileNames, tileSrcs, covers,
  placeholderTilesRendered: (gridHTML.match(/placeholders\//g)||[]).length,
  comingSoonFallbacks: (gridHTML.match(/Photo coming soon/g)||[]).length,
}, null, 1));
