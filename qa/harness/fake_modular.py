APP="export const initializeApp=()=>({});export const getApps=()=>[];"
AUTH="""
const L=[];let cur=null;
export const getAuth=()=>({get currentUser(){return cur}});
export const onAuthStateChanged=(a,cb)=>{L.push(cb);setTimeout(()=>cb(cur),0);return()=>{}};
window.__login=(u)=>{cur=Object.assign({getIdToken:async()=>'t',reload:async()=>{},displayName:'T',photoURL:null},u);L.forEach(f=>f(cur))};
const noop=async()=>({user:cur});
export const createUserWithEmailAndPassword=noop,signInWithEmailAndPassword=noop,signInWithPopup=noop,updateProfile=async()=>{};
export const signOut=async()=>{cur=null;L.forEach(f=>f(null))};
export class GoogleAuthProvider{}
export const sendPasswordResetEmail=async()=>{},sendEmailVerification=async()=>{},setPersistence=async()=>{};
"""
FS="""
window.__DB=window.__DB||new Map();const DB=window.__DB;
export class Timestamp{constructor(ms){this.ms=ms;this.seconds=Math.floor(ms/1000);this.nanoseconds=0}toMillis(){return this.ms}toDate(){return new Date(this.ms)}static fromMillis(m){return new Timestamp(m)}static fromDate(d){return new Timestamp(d.getTime())}static now(){return new Timestamp(Date.now())}}
export const serverTimestamp=()=>Timestamp.now();
export const getFirestore=()=>({});
const norm=a=>a.filter(x=>typeof x==='string'||typeof x==='number').join('/');
export const collection=(d,...s)=>({path:norm([...s]),col:true,db:d});
export const collectionGroup=(d,id)=>({group:id,col:true,path:'*'+id});
export const doc=(d,...s)=>{if(d&&d.col&&!s.length)s=[Math.random().toString(36).slice(2,10)];return{path:norm([(d&&d.path)||'',...s].filter(Boolean)),id:(s[s.length-1]),db:d}};
const snapOf=p=>{const v=DB.get(p);return{id:p.split('/').pop(),ref:{path:p},exists:()=>v!==undefined,data:()=>v===undefined?undefined:JSON.parse(JSON.stringify(v),(k,x)=>x&&x.__ts?Timestamp.fromMillis(x.__ts):x)}};
const ser=o=>JSON.parse(JSON.stringify(o,function(k,v){return this[k] instanceof Timestamp?{__ts:this[k].ms}:v}));
export const getDoc=async r=>snapOf(r.path);
export const where=(f,op,v)=>({k:'w',f,op,v});export const orderBy=(f,d)=>({k:'o',f,d});export const limit=()=>({k:'l'});
export const query=(c,...cons)=>({...c,cons});
const rows=q=>{let out=[];for(const k of DB.keys()){let ok=false;if(q.group){const p=k.split('/');ok=p[p.length-2]===q.group}else{const pre=q.path+'/';ok=k.startsWith(pre)&&!k.slice(pre.length).includes('/')}if(ok)out.push(snapOf(k))}
 (q.cons||[]).forEach(c=>{if(c.k==='w')out=out.filter(s=>{const v=s.data()[c.f];return c.op==='=='?v===c.v:c.op==='in'?c.v.includes(v):true})});return out};
const mk=d=>({docs:d,size:d.length,empty:!d.length,forEach:f=>d.forEach(f)});
export const getDocs=async q=>mk(rows(q));
export const setDoc=async(r,d,o)=>{const cur=DB.get(r.path)||{};const dm=(a,b)=>{const o={...a};for(const k in b){o[k]=(b[k]&&typeof b[k]==='object'&&!b[k].__ts&&!Array.isArray(b[k])&&a&&typeof a[k]==='object')?dm(a[k],b[k]):b[k]}return o};DB.set(r.path,o&&o.merge?dm(cur,ser(d)):ser(d))};
export const addDoc=async(c,d)=>{const id='a'+Math.random().toString(36).slice(2,8);DB.set(c.path+'/'+id,ser(d));return{id,path:c.path+'/'+id}};
export const updateDoc=async(r,d)=>{const cur=DB.get(r.path);if(cur===undefined)throw new Error('not-found');const n=JSON.parse(JSON.stringify(cur));
 for(const [k,v] of Object.entries(ser(d))){const p=k.split('.');let o=n;for(let i=0;i<p.length-1;i++){o[p[i]]=o[p[i]]||{};o=o[p[i]]}o[p[p.length-1]]=v}DB.set(r.path,n)};
export const deleteDoc=async r=>{DB.delete(r.path)};
export const onSnapshot=(t,cb)=>{const f=()=>{if(t.col)cb(mk(rows(t)));else cb(snapOf(t.path))};setTimeout(f,0);return()=>{}};
export const arrayUnion=(...v)=>v,arrayRemove=(...v)=>v,increment=n=>n;
export const writeBatch=()=>{const ops=[];return{set:(r,d,o)=>ops.push(()=>setDoc(r,d,o)),update:(r,d)=>ops.push(()=>updateDoc(r,d)),delete:r=>ops.push(()=>deleteDoc(r)),commit:async()=>{for(const f of ops)await f()}}};
"""
import re
async def install(pg):
    async def h(r):
        u=r.request.url
        body=APP if 'firebase-app.js' in u else AUTH if 'firebase-auth.js' in u else FS if 'firebase-firestore.js' in u else ''
        await r.fulfill(body=body,content_type='application/javascript')
    await pg.route('**/www.gstatic.com/**',h)
