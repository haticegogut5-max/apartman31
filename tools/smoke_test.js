// Headless smoke test WITHOUT a browser: loads the game scripts in Node with a Proxy-stubbed THREE/DOM
// and runs a few frames + the main state functions. It only catches load-time/TDZ/TypeError bugs, NOT visual bugs.
// Usage (from project root): node tools/smoke_test.js
const fs=require('fs'),vm=require('vm'),path=require('path');
function mk(){const f=function(){};return new Proxy(f,{get(t,k){if(k===Symbol.toPrimitive)return()=>0;if(k==='then')return undefined;if(k==='length')return()=>0;if(k===Symbol.iterator)return function*(){};return mk()},set(){return true},apply(){return mk()},construct(){return mk()}})}
const ctx={Image:function(){},atob:x=>Buffer.from(x,'base64').toString('binary'),THREE:mk(),document:mk(),window:{},innerWidth:800,innerHeight:600,devicePixelRatio:1,performance:{now:()=>0},navigator:{},
setTimeout:f=>{try{f()}catch(e){console.log('timeout cb error',e.message)}return 0},clearTimeout(){},setInterval:()=>0,clearInterval(){},requestAnimationFrame(){},addEventListener(){},console,Math,Date,Set,Object,Array,JSON,Float32Array,parseInt,isNaN,Number,String};
ctx.window=ctx;
const root=path.join(__dirname,'..');
const src=['js/models_chars.js','js/model_galina.js','js/game.js'].map(f=>fs.readFileSync(path.join(root,f),'utf8')).join('\n')+
`\n;window.__t=(st,n)=>{S.playing=true;S.paused=false;S.stage=st;S.talk=S.talk||new Set();S.got=S.got||new Set();for(let i=0;i<n;i++)frame(i*16)};window.__x=()=>{talk('a');freeTalk('b');emerge('c',['x'],()=>{});scare();fearIn();fearOut();silAt(0,0);startN2();startN3();startN4();startN5();startN6();startN7()}`;
try{vm.runInNewContext(src,ctx,{timeout:15000});for(const st of [0,10,20,22,31,41,50,61,63,44])ctx.__t(st,5);ctx.__x();for(const st of [0,20,63])ctx.__t(st,5);console.log('SMOKE TEST OK (load + frames + state functions)')}catch(e){console.log('SMOKE TEST FAILED:',e.name,e.message);console.log((e.stack||'').split('\n').slice(0,6).join('\n'));process.exit(1)}
