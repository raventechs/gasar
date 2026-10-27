module.exports = {
'firebase-app.js': `export const initializeApp=c=>({c});export const getApps=()=>[];`,
'firebase-auth.js': `
let cb=null; const A={currentUser:null};
const load=()=>{try{return JSON.parse(sessionStorage.getItem('fake_user')||'null')}catch(e){return null}};
const fire=u=>{A.currentUser=u;cb&&setTimeout(()=>cb(u),0)};
export const getAuth=()=>A;
export const onAuthStateChanged=(a,f)=>{cb=f;setTimeout(()=>fire(load()),0);return()=>{}};
const sess=u=>{sessionStorage.setItem('fake_user',JSON.stringify(u));fire(u)};
const E=c=>{const e=new Error(c);e.code=c;return e};
export const signInWithEmailAndPassword=async(a,email,pass)=>{const r=await window.__fs(null,'signin',{email,pass});if(r.err)throw E(r.err);sess(r);return{user:r}};
export const createUserWithEmailAndPassword=async(a,email,pass)=>{const r=await window.__fs(null,'signup',{email,pass});if(r.err)throw E(r.err);A.currentUser=r;sessionStorage.setItem('fake_user',JSON.stringify(r));/* el alta de usuarios la hace la app y dispara onAuthStateChanged */ fire(r);return{user:r}};
export const signOut=async()=>{sessionStorage.removeItem('fake_user');fire(null)};
export class GoogleAuthProvider{}; export const signInWithPopup=async()=>{throw E('auth/popup-blocked')};
`,
'firebase-firestore.js': `
const me=()=>{try{return JSON.parse(sessionStorage.getItem('fake_user')||'null')}catch(e){return null}};
class Timestamp{constructor(ms){this._ms=ms;this.seconds=Math.floor(ms/1000);this.nanoseconds=(ms%1000)*1e6}
 toDate(){return new Date(this._ms)} toMillis(){return this._ms} static fromDate(d){return new Timestamp(d.getTime())} static now(){return new Timestamp(Date.now())} static fromMillis(m){return new Timestamp(m)}}
export {Timestamp};
export const serverTimestamp=()=>({__sv:true});
const enc=v=>{if(v instanceof Timestamp)return{__ts:v._ms};if(v instanceof Date)return{__ts:v.getTime()};if(Array.isArray(v))return v.map(enc);if(v&&typeof v==='object'&&!('__sv' in v)){const o={};for(const k of Object.keys(v))if(v[k]!==undefined)o[k]=enc(v[k]);return o}return v};
const dec=v=>{if(v&&typeof v==='object'){if('__ts' in v)return new Timestamp(v.__ts);if(Array.isArray(v))return v.map(dec);const o={};for(const k of Object.keys(v))o[k]=dec(v[k]);return o}return v};
const call=async(op,a)=>{const r=await window.__fs(me(),op,a);if(r&&r.err){const e=new Error(r.err);e.code=r.err;throw e}return r};
export const getFirestore=()=>({__db:true});
const joinp=(b,s)=>b+(b&&s.length?'/':'')+s.join('/');
export const collection=(b,...s)=>({type:'col',path:b.__db?s.join('/'):joinp(b.path,s)});
let aid=0;
export const doc=(b,...s)=>{if(b.type==='col'){const id=s[0]||('c'+Date.now()+(++aid));return{type:'doc',id,path:b.path+'/'+id}}const p=b.__db?s.join('/'):joinp(b.path,s);return{type:'doc',id:p.split('/').pop(),path:p}};
export const where=(f,op,v)=>({k:'where',f,op,v:enc(v)}); export const orderBy=(f,d)=>({k:'order',f,d:d||'asc'}); export const limit=n=>({k:'limit',n});
export const query=(c,...cs)=>({type:'query',path:c.path,where:cs.filter(x=>x.k==='where').map(x=>[x.f,x.op,x.v]),order:cs.filter(x=>x.k==='order').map(x=>[x.f,x.d]),limit:(cs.find(x=>x.k==='limit')||{}).n});
const mkSnap=(path,id,data)=>({id,ref:{type:'doc',id,path},exists:()=>data!==undefined,data:()=>data===undefined?undefined:dec(data)});
const mkQ=(r)=>({docs:r.docs.map(d=>mkSnap(r.path+'/'+d.id,d.id,d.data)),get empty(){return this.docs.length===0},get size(){return this.docs.length},forEach(f){this.docs.forEach(f)},docChanges:()=>[]});
const qArgs=q=>({path:q.path,where:q.where||[],order:q.order||[],limit:q.limit});
export const getDoc=async r=>{const x=await call('get',{path:r.path});return mkSnap(r.path,r.id,x.exists?x.data:undefined)};
export const getDocs=async q=>mkQ({path:q.path,docs:(await call('list',qArgs(q))).docs});
export const addDoc=async(c,d)=>{const r=await call('add',{path:c.path,data:enc(d)});return{id:r.path.split('/').pop(),path:r.path}};
export const setDoc=async(r,d,o)=>{await call('set',{path:r.path,data:enc(d),merge:!!(o&&o.merge)})};
export const updateDoc=async(r,d)=>{await call('update',{path:r.path,data:enc(d)})};
export const deleteDoc=async r=>{await call('delete',{path:r.path})};
export const onSnapshot=(t,ok,err)=>{let last=null,stop=false;const run=async()=>{if(stop)return;try{let out;if(t.type==='doc'){const x=await call('get',{path:t.path});out=mkSnap(t.path,t.id,x.exists?x.data:undefined);var key=JSON.stringify(x)}else{const x=await call('list',qArgs(t));out=mkQ({path:t.path,docs:x.docs});key=JSON.stringify(x)}
 if(key!==last){last=key;ok(out)}}catch(e){err&&err(e)}if(!stop)setTimeout(run,300)};run();return()=>{stop=true}};
`};
