/* Firebase simulado (compat) para probar apps RavenTechs sin red. Datos en window.__DB (Map ruta -> objeto). */
(function () {
  class Timestamp {
    constructor(s, n) { this.seconds = s; this.nanoseconds = n || 0; }
    static fromDate(d) { return new Timestamp(Math.floor(d.getTime() / 1000), (d.getTime() % 1000) * 1e6); }
    static now() { return Timestamp.fromDate(new Date()); }
    static fromMillis(ms) { return Timestamp.fromDate(new Date(ms)); }
    toDate() { return new Date(this.seconds * 1000 + this.nanoseconds / 1e6); }
    toMillis() { return this.seconds * 1000 + this.nanoseconds / 1e6; }
  }
  const SERVER_TS = { __server: true };
  const DB = window.__DB = window.__DB || new Map();
  window.__WRITES = [];
  let auto = 0;
  const resolve = v => {
    if (v === SERVER_TS) return Timestamp.now();
    if (v && typeof v === 'object' && !(v instanceof Timestamp) && !Array.isArray(v)) { const o = {}; for (const k in v) o[k] = resolve(v[k]); return o; }
    return v;
  };
  const clone = o => { const c = {}; for (const k in o) c[k] = o[k]; return c; };
  const SUBS = [];
  const notify = () => SUBS.slice().forEach(f => { try { f(); } catch (e) {} });
  const parentOf = p => p.split('/').slice(0, -1).join('/');

  class DocRef {
    constructor(path) { this.path = path; this.id = path.split('/').pop(); }
    collection(n) { return new ColRef(this.path + '/' + n); }
    async get() { return snap(this.path); }
    async set(d, opt) { window.__WRITES.push(['set', this.path]); const nd = resolve(d); DB.set(this.path, opt && opt.merge ? Object.assign(clone(DB.get(this.path) || {}), nd) : nd); notify(); }
    async update(d) {
      window.__WRITES.push(['update', this.path]);
      if (!DB.has(this.path)) throw new Error('No document to update: ' + this.path);
      DB.set(this.path, Object.assign(clone(DB.get(this.path)), resolve(d))); notify();
    }
    async delete() { window.__WRITES.push(['delete', this.path]); DB.delete(this.path); notify(); }
    onSnapshot(cb) { const f = () => cb(snap(this.path)); SUBS.push(f); setTimeout(f, 0); return () => { const i = SUBS.indexOf(f); if (i >= 0) SUBS.splice(i, 1); }; }
  }
  function snap(path) {
    const ex = DB.has(path);
    return { id: path.split('/').pop(), exists: ex, ref: new DocRef(path), data: () => ex ? clone(DB.get(path)) : undefined };
  }
  class Query {
    constructor(path, filters, order, lim) { this.path = path; this.filters = filters || []; this.order = order || null; this.lim = lim || null; }
    where(f, op, v) { return new Query(this.path, this.filters.concat([[f, op, v]]), this.order, this.lim); }
    orderBy(f, dir) { return new Query(this.path, this.filters, [f, dir || 'asc'], this.lim); }
    limit(n) { return new Query(this.path, this.filters, this.order, n); }
    onSnapshot(cb) { const f = () => this.get().then(cb); SUBS.push(f); setTimeout(f, 0); return () => { const i = SUBS.indexOf(f); if (i >= 0) SUBS.splice(i, 1); }; }
    async get() {
      let docs = [];
      for (const [p, d] of DB) if (parentOf(p) === this.path) docs.push([p, d]);
      for (const [f, op, v] of this.filters) docs = docs.filter(([, d]) => op === '==' ? d[f] === v : true);
      if (this.order) {
        const [f, dir] = this.order; const val = x => (x && x.toMillis) ? x.toMillis() : x;
        docs.sort((a, b) => (val(a[1][f]) > val(b[1][f]) ? 1 : -1) * (dir === 'desc' ? -1 : 1));
      }
      if (this.lim) docs = docs.slice(0, this.lim);
      const out = docs.map(([p]) => snap(p));
      return { docs: out, empty: !out.length, size: out.length, forEach: f => out.forEach(f) };
    }
  }
  class ColRef extends Query {
    constructor(path) { super(path); }
    doc(id) { return new DocRef(this.path + '/' + (id || ('auto' + (++auto)))); }
    async add(d) { const r = this.doc(); await r.set(d); return r; }
  }
  const firestore = () => ({
    collection: n => new ColRef(n),
    batch: () => { const ops = []; return {
      set: (r, d, o) => ops.push(() => r.set(d, o)), delete: r => ops.push(() => r.delete()), update: (r, d) => ops.push(() => r.update(d)),
      commit: async () => { for (const f of ops) await f(); } }; }
  });
  firestore.FieldValue = { serverTimestamp: () => SERVER_TS };
  firestore.Timestamp = Timestamp;

  // Auth
  let current = null; const listeners = [];
  const authObj = {
    get currentUser() { return current; },
    onAuthStateChanged: cb => { listeners.push(cb); cb(current); },
    signInWithPopup: async () => { throw new Error('popup no disponible en la prueba'); },
    signInWithEmailAndPassword: async () => { throw new Error('no usado'); },
    createUserWithEmailAndPassword: async () => { throw new Error('no usado'); },
    signOut: async () => { current = null; listeners.forEach(f => f(null)); }
  };
  const auth = () => authObj;
  auth.GoogleAuthProvider = function () {};
  window.__login = u => {
    current = Object.assign({ displayName: 'Prueba', emailVerified: true, getIdToken: async () => 'TOKEN-' + u.uid }, u);
    return Promise.all(listeners.map(f => f(current)));
  };
  window.firebase = { initializeApp() {}, auth, firestore };
})();
