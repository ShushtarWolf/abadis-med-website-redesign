/**
 * Filters preview cinematic — same studio, lighting, environment, scroll-scrub
 * easing, caption beats, still fallback and reduced-motion contract as the
 * suction-bag v12 hero (p02-cinematic-page.js). Loaded only from the filters
 * preview via data-cin-module; the bag page keeps p02-cinematic-page.js.
 *
 * Sequence: antibacterial disc (p11) → flow-stop inline (p12) → porous
 * sintered filter (p16, finished part only). No path or hose.
 */
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {RoomEnvironment} from 'three/addons/environments/RoomEnvironment.js';
import {mergeVertices} from 'three/addons/utils/BufferGeometryUtils.js';
import {applySinteredGrain} from '../../3d-sketches/p16-cinematic/sintered-grain.js';

export function mount(root){
const url=(rel)=>new URL(rel, import.meta.url).href;
const floorMode = root.getAttribute('data-cin-floors') || (root.hasAttribute('data-cin-root') ? 'hero' : 'studio');
const stillCapture = root.getAttribute('data-cin-capture') === 'still';
const mob=stillCapture?false:matchMedia('(max-width:700px),(pointer:coarse)').matches;
const cv=root.querySelector('canvas'),stage=cv.parentElement;
cv.style.touchAction='pan-y';
const R=new THREE.WebGLRenderer({canvas:cv,antialias:true,alpha:true,preserveDrawingBuffer:stillCapture,powerPreference:'high-performance',logarithmicDepthBuffer:true});
R.setClearColor(0x000000, 0);
R.setPixelRatio(Math.min(devicePixelRatio,mob?1.75:2));R.toneMapping=THREE.ACESFilmicToneMapping;R.toneMappingExposure=1.02;
R.shadowMap.enabled=!mob;R.shadowMap.type=THREE.PCFSoftShadowMap;
const S=new THREE.Scene();
const pm=new THREE.PMREMGenerator(R);S.environment=pm.fromScene(new RoomEnvironment(),.05).texture;S.environmentIntensity=.42;
const C=new THREE.PerspectiveCamera(mob?32:26,1,2,3000);
const key=new THREE.DirectionalLight(0xfff2ea,1.35);key.position.set(-140,480,260);key.castShadow=true;key.shadow.mapSize.set(2048,2048);
Object.assign(key.shadow.camera,{left:-200,right:200,top:200,bottom:-200,near:60,far:1400});key.shadow.radius=18;key.shadow.bias=-.00035;S.add(key);
const fillL=new THREE.DirectionalLight(0xfff8f2,1.35);fillL.position.set(100,220,200);S.add(fillL);
const fill2=new THREE.DirectionalLight(0xdde8ea,.55);fill2.position.set(-80,-40,120);S.add(fill2);
const rim=new THREE.DirectionalLight(0x7ecad4,.95);rim.position.set(240,140,-320);S.add(rim);
const hemi=new THREE.HemisphereLight(0xf0f6f7,0x1a1814,.85);S.add(hemi);
const under=new THREE.PointLight(0xfff8f2,.45,750,1.9);under.position.set(20,-30,140);S.add(under);
function radTex(stops){const c=document.createElement('canvas');c.width=c.height=256;const x=c.getContext('2d');const g=x.createRadialGradient(128,128,0,128,128,128);stops.forEach(s=>g.addColorStop(...s));x.fillStyle=g;x.fillRect(0,0,256,256);return new THREE.CanvasTexture(c);}
function floorPlane(sz,tex,y){const m=new THREE.Mesh(new THREE.PlaneGeometry(sz,sz),new THREE.MeshBasicMaterial({map:tex,transparent:true,depthWrite:false}));m.rotation.x=-Math.PI/2;m.position.y=y;S.add(m);return m;}
let floorTeal=null;
if(floorMode==='hero' || floorMode==='studio'){
 floorTeal=floorPlane(1100,radTex([[0,'rgba(46,127,150,.28)'],[.55,'rgba(46,127,150,.08)'],[1,'rgba(46,127,150,0)']]),-80);
}
function syncPageTone(){
 /* Hero film is a dark studio in every theme — same contract as the bag v12. */
 R.toneMappingExposure=1.02;
 S.environmentIntensity=.42;
 hemi.color.setHex(0xf0f6f7);
 hemi.groundColor.setHex(0x1a1814);
 hemi.intensity=.85;
 key.intensity=1.35;
 fillL.intensity=1.35;
 S.background=null;
}
syncPageTone();
if(!stillCapture)document.addEventListener('themechange',syncPageTone);

const glass=new THREE.MeshPhysicalMaterial({
  color:0xe7f1f8,roughness:.08,metalness:0,transparent:true,opacity:.38,
  depthWrite:false,thickness:2.2,ior:1.49,attenuationColor:0xd9eef0,attenuationDistance:80,side:THREE.DoubleSide
});
const ribMat=new THREE.MeshPhysicalMaterial({
  color:0x6f97b8,roughness:.28,metalness:0,transparent:true,opacity:.85,depthWrite:false,side:THREE.DoubleSide
});
const p12Glass=new THREE.MeshPhysicalMaterial({
  color:0xf4f8f7,roughness:.06,metalness:0,transparent:true,opacity:.36,
  depthWrite:false,thickness:2.4,ior:1.49,side:THREE.DoubleSide
});
const cartMat=new THREE.MeshStandardMaterial({color:0xf4f0e6,roughness:.9,metalness:0,envMapIntensity:.28,side:THREE.DoubleSide});
const porousMat=applySinteredGrain(new THREE.MeshPhysicalMaterial({
  color:0xf1f1f1,roughness:.90,metalness:0,envMapIntensity:0.14,side:THREE.DoubleSide
}),{mobile:mob});

function matFor(kind,name){
  const n=(name||'').toLowerCase();
  if(kind==='porous') return porousMat;
  if(kind==='inline') return n.includes('cartridge')?cartMat:p12Glass;
  return n.includes('rib')?ribMat:glass;
}

function posePart(group,kind){
  group.updateMatrixWorld(true);
  const box=new THREE.Box3().setFromObject(group);
  const size=box.getSize(new THREE.Vector3());
  const axes=[['x',size.x],['y',size.y],['z',size.z]].sort((a,b)=>a[1]-b[1]);
  const shortest=axes[0][0], longest=axes[2][0];
  /* Disc: nozzles on the unique short axis, stand them on Y. Inline: long axis along X. Porous: tall on Y. */
  if(kind==='disc' && shortest!=='y'){
    if(shortest==='x') group.rotateZ(-Math.PI/2);
    else if(shortest==='z') group.rotateX(Math.PI/2);
  }else if(kind==='inline' && longest!=='x'){
    if(longest==='y') group.rotateZ(-Math.PI/2);
    else if(longest==='z') group.rotateY(Math.PI/2);
  }else if(kind==='porous' && longest!=='y'){
    if(longest==='x') group.rotateZ(Math.PI/2);
    else if(longest==='z') group.rotateX(-Math.PI/2);
  }
  group.updateMatrixWorld(true);
  const box2=new THREE.Box3().setFromObject(group);
  const c=box2.getCenter(new THREE.Vector3());
  group.position.sub(c);
  group.updateMatrixWorld(true);
  const box3=new THREE.Box3().setFromObject(group);
  const c3=box3.getCenter(new THREE.Vector3());
  const rad=Math.max(box3.getBoundingSphere(new THREE.Sphere()).radius,.001);
  /* A gentle three-quarter yaw so ribs / ports read clearly. */
  if(kind==='disc') group.rotation.y+=.55;
  else if(kind==='inline') group.rotation.y+=.35;
  else group.rotation.y+=.45;
  group.updateMatrixWorld(true);
  return {center:c3,radius:rad,minY:box3.min.y};
}

const PRODUCTS=[
  {id:'p11',kind:'disc',src:url('../../3d-sketches/p11-cinematic/p11-disc-filter.glb')},
  {id:'p12',kind:'inline',src:url('../../3d-sketches/p12-cinematic/p12-inline-filter.glb')},
  {id:'p16',kind:'porous',src:url('../../3d-sketches/p16-cinematic/p16-porous-filter.glb?v=20261112c')}
];

const parts=[];
const loader=new GLTFLoader();
let loaded=0,ready=false;

function loadOne(spec){
  return new Promise((resolve,reject)=>{
    loader.load(spec.src,g=>{
      const group=new THREE.Group();group.name=spec.id;
      g.scene.updateMatrixWorld(true);
      g.scene.traverse(o=>{
        if(!o.isMesh)return;
        let geo=o.geometry.clone().applyMatrix4(o.matrixWorld);
        geo=mergeVertices(geo,1e-5);geo.computeVertexNormals();
        const mat=matFor(spec.kind,o.name||'').clone();
        const m=new THREE.Mesh(geo,mat);
        m.name=o.name||'part';
        m.castShadow=true;m.receiveShadow=!mob;
        m.userData.baseOpacity=mat.opacity;
        m.userData.baseTransparent=!!mat.transparent;
        group.add(m);
      });
      const info=posePart(group,spec.kind);
      group.visible=false;
      S.add(group);
      const rec={...spec,group,...info};
      resolve(rec);
    },undefined,reject);
  });
}

function setOpacity(rec,o){
  const vis=o>0.012;
  rec.group.visible=vis;
  if(!vis)return;
  rec.group.traverse(m=>{
    if(!m.isMesh)return;
    const base=m.userData.baseOpacity??1;
    m.material.opacity=base*o;
    m.material.transparent=m.userData.baseTransparent||o<0.999;
    m.material.depthWrite=!m.material.transparent && o>0.8;
  });
}

/* Cross-fade windows: p11 hold, blend to p12, p12 hold, blend to p16, p16 hold. */
function weights(t){
  const clx=x=>Math.min(1,Math.max(0,x));
  const w11=1-clx((t-.26)/.10);
  const w16=clx((t-.58)/.10);
  const w12=Math.max(0,1-w11-w16);
  return [w11,w12,w16];
}

Promise.all(PRODUCTS.map(loadOne)).then(list=>{
  parts.push(...list);
  ready=true;
  if(floorTeal){
    const minY=Math.min(...list.map(p=>p.minY));
    const rad=Math.max(...list.map(p=>p.radius));
    floorTeal.position.y=minY-rad*0.04;
    const span=Math.max(400,rad*14);
    floorTeal.scale.setScalar(span/1100);
  }
  if(stillCapture){
    T=0;requestAnimationFrame((now)=>{frame(now);root.dispatchEvent(new CustomEvent('cin-still-ready',{bubbles:true}));});
  }
  window.__filters_cin={ready:true,parts:list.map(p=>({id:p.id,radius:p.radius,minY:p.minY}))};
},e=>{console.error(e);window.__filters_cin={ready:'error',error:String(e)};});

function size(){const w=stage.clientWidth,h=stage.clientHeight;R.setSize(w,h,false);C.aspect=w/h;C.updateProjectionMatrix();}
new ResizeObserver(size).observe(stage);size();
const cl=x=>Math.min(1,Math.max(0,x)),ease=x=>{x=cl(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2;};
const beats=[...root.querySelectorAll('.beat')].map(e=>({e,a:+e.dataset.a,b:+e.dataset.b}));
const bar=root.querySelector('.cin-bar'),hint=root.querySelector('.cin-hint');
const qp=new URLSearchParams(location.search);
const V=(x,y,z)=>new THREE.Vector3(x,y,z);

/* Polar keyframes [t, azDeg, elDeg, distMul, lookYMul] — gentle orbit, no path clutter. */
const KF=[
  [0.00, -22, 10, 3.55, 0],
  [0.10, -16, 12, 3.45, 0],
  [0.22,   8, 16, 3.25, 0],
  [0.28,  14, 14, 3.40, 0],
  [0.36, -32, 14, 3.55, 0],
  [0.46, -18, 11, 3.25, 0],
  [0.56,  22, 13, 3.40, 0],
  [0.62,  26, 12, 3.50, 0],
  [0.70,  16, 20, 3.55, 0],
  [0.82, -12, 22, 3.30, 0],
  [0.92,  18, 16, 3.45, 0],
  [1.00,  14, 18, 3.55, 0]
];

let T=0,lastN=0;
const cp=new THREE.Vector3(),ct=new THREE.Vector3();
let trackH=1,trackTop=0,onScreen=true,rafId=0,looping=false,measureQueued=false;
const cinStage=root.querySelector('.cin-stage')||stage;
function measureTrack(){
  const stageH=(cinStage&&cinStage.offsetHeight)||innerHeight||1;
  trackH=Math.max(1,root.offsetHeight-stageH);
  trackTop=root.getBoundingClientRect().top+scrollY;
}
function requestMeasure(){
  if(measureQueued)return;
  measureQueued=true;
  requestAnimationFrame(()=>{measureQueued=false;measureTrack();});
}
measureTrack();
addEventListener('resize',requestMeasure,{passive:true});
if(window.visualViewport){
  visualViewport.addEventListener('resize',requestMeasure,{passive:true});
}
if('IntersectionObserver' in window){
  new IntersectionObserver((ents)=>{onScreen=ents.some(e=>e.isIntersecting);if(onScreen)ensureLoop();},{root:null,threshold:0,rootMargin:'80px 0px'}).observe(root);
}
document.addEventListener('visibilitychange',()=>{if(!document.hidden)ensureLoop();});
function prog(){
  if(qp.has('t'))return cl(+qp.get('t'));
  const scrolled=Math.min(trackH,Math.max(0,scrollY-trackTop));
  return cl(scrolled/trackH);
}
function samplePolar(t){
  let a=KF[0],b=KF[KF.length-1];
  for(let n=0;n<KF.length-1;n++)if(t>=KF[n][0]&&t<=KF[n+1][0]){a=KF[n];b=KF[n+1];break;}
  const k=ease((t-a[0])/Math.max(1e-4,b[0]-a[0]));
  const mix=(i)=>a[i]+(b[i]-a[i])*k;
  return {az:THREE.MathUtils.degToRad(mix(1)),el:THREE.MathUtils.degToRad(mix(2)),distMul:mix(3),lookYMul:mix(4)};
}
let paused=false;
const pauseBtn=root.querySelector('[data-cin-pause]');
if(pauseBtn)pauseBtn.addEventListener('click',()=>{paused=!paused;pauseBtn.setAttribute('aria-pressed',paused?'true':'false');root.classList.toggle('is-paused',paused);});
function ensureLoop(){if(looping||stillCapture)return;looping=true;rafId=requestAnimationFrame(frame);}
function frame(now){
  if(!onScreen||document.hidden){if(!stillCapture){looping=false;rafId=0;return;}}
  if(!stillCapture)rafId=requestAnimationFrame(frame);
  if(paused){R.render(S,C);return;}
  const dt=Math.min(.1,(now-(lastN||now))/1000);lastN=now;
  T+=(prog()-T)*(qp.has('t')||stillCapture?1:1-Math.exp(-dt*3.2));const t=T;
  if(bar)bar.style.width=(t*100)+'%';if(hint)hint.style.opacity=1-cl(t*18);
  beats.forEach(b=>{const f=.028;const o=Math.min(cl((t-b.a)/f),cl((b.b-t)/f));b.e.style.opacity=o;b.e.style.transform=`translateY(${(1-o)*10}px)`;});
  if(ready){
    const w=weights(t);
    let rad=0,lookY=0;
    parts.forEach((p,i)=>{
      setOpacity(p,w[i]);
      rad+=p.radius*w[i];
      lookY+=p.minY*0+ p.radius*0*w[i];
    });
    if(rad<.001 && parts[0]) rad=parts[0].radius;
    const pol=samplePolar(t);
    const dist=rad*pol.distMul;
    const el=pol.el,az=pol.az;
    ct.set(0, rad*pol.lookYMul, 0);
    cp.set(
      ct.x + dist*Math.cos(el)*Math.sin(az),
      ct.y + dist*Math.sin(el),
      ct.z + dist*Math.cos(el)*Math.cos(az)
    );
    /* Same distance-fit idea as the bag v12 so phones are not zoomed in. */
    let fit = mob ? 1.85 : 1.55;
    cp.sub(ct).multiplyScalar(fit).add(ct);
    C.position.copy(cp);C.lookAt(ct);
    const d=cp.distanceTo(ct);C.near=Math.max(.5,d*.05);C.far=d+1500;C.updateProjectionMatrix();
  }
  R.render(S,C);
  if(!window.__cin_frame){window.__cin_frame=true;root.dispatchEvent(new CustomEvent('cin-frame',{bubbles:true}));}
}

if(stillCapture){
  root.classList.add('is-still');
}else{
  root.classList.remove('is-still');
  root.classList.add('is-playing');
  ensureLoop();
}
}
