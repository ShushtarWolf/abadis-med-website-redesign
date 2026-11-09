/**
 * Approved P01 cinematic v12 (commit d3c5851d), embedded on the suction-bag page.
 * Geometry, materials, lid and camera match site/3d-sketches/p01-cinematic/index.html.
 * This wrapper only scopes scroll progress to the hero track, resolves asset URLs, and adds pause.
 */
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {RoomEnvironment} from 'three/addons/environments/RoomEnvironment.js';
import {mergeVertices,toCreasedNormals} from 'three/addons/utils/BufferGeometryUtils.js';

export function mount(root){
const asset=(rel)=>new URL(rel, new URL('../../3d-sketches/p01-cinematic/', import.meta.url)).href;
const floorMode = root.getAttribute('data-cin-floors') || (root.hasAttribute('data-cin-root') ? 'hero' : 'studio');
const stillCapture = root.getAttribute('data-cin-capture') === 'still';
const mob=stillCapture?false:matchMedia('(max-width:700px),(pointer:coarse)').matches;
const cv=root.querySelector('canvas'),stage=cv.parentElement;
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
let floorTeal=null,floorDark=null,sr=null;
if(floorMode==='hero'){
 floorTeal=floorPlane(1100,radTex([[0,'rgba(46,127,150,.28)'],[.55,'rgba(46,127,150,.08)'],[1,'rgba(46,127,150,0)']]),-179);
}else if(floorMode==='studio'){
 floorTeal=floorPlane(1100,radTex([[0,'rgba(46,127,150,.28)'],[.55,'rgba(46,127,150,.08)'],[1,'rgba(46,127,150,0)']]),-179);
 floorDark=floorPlane(300,radTex([[0,'rgba(0,0,0,.72)'],[.5,'rgba(0,0,0,.2)'],[1,'rgba(0,0,0,0)']]),-178.6);
 sr=new THREE.Mesh(new THREE.PlaneGeometry(650,650),new THREE.ShadowMaterial({opacity:.38}));
}else if(floorMode==='soft'){
}else{
 R.shadowMap.enabled=false;key.castShadow=false;
}
if(sr){sr.rotation.x=-Math.PI/2;sr.position.y=-178.4;sr.receiveShadow=true;S.add(sr);}
function syncPageTone(){
 const t=document.documentElement.getAttribute('data-theme')||'light';
 const light=t==='light';
 if(floorMode==='hero'){
  R.toneMappingExposure=1.02;
  S.environmentIntensity=.42;
  hemi.color.setHex(0xf0f6f7);
  hemi.groundColor.setHex(0x1a1814);
  hemi.intensity=.85;
  key.intensity=1.35;
  fillL.intensity=1.35;
  S.background=null;
  return;
 }
 const pageBg=light?0xf3fafa:t==='noir'?0x0a0a12:0x061719;
 R.toneMappingExposure=light?1.14:1.02;
 if(floorMode==='soft'||floorMode==='none'){
  S.environmentIntensity=light?.52:.34;
  hemi.color.setHex(light?0xf8fbfb:0x0b2427);
  hemi.groundColor.setHex(pageBg);
  hemi.intensity=light?.62:.42;
  S.background=null;
 }else{
  S.environmentIntensity=light?.58:.42;
 }
 key.intensity=light?1.48:1.35;
 fillL.intensity=light?1.45:1.35;
 if(sr)sr.material.opacity=light?(floorMode==='studio'?.28:.22):.22;
 if(floorDark)floorDark.visible=floorMode==='studio'?!light:true;
}
syncPageTone();
if(!stillCapture)document.addEventListener('themechange',syncPageTone);
const TL=new THREE.TextureLoader();
const filmT=TL.load(asset('tex/film-bump.jpg'));filmT.wrapS=filmT.wrapT=THREE.RepeatWrapping;filmT.repeat.set(5,4);
const weaveT=TL.load(asset('tex/sachet-weave.jpg'));weaveT.wrapS=weaveT.wrapT=THREE.RepeatWrapping;weaveT.repeat.set(3,4);
const TEAL=0x0a6176;
const ppMicro=TL.load(asset('tex/pp-micro-bump.jpg'));ppMicro.wrapS=ppMicro.wrapT=THREE.RepeatWrapping;ppMicro.repeat.set(14,14);
const filtDiff=TL.load(asset('tex/filter-diffuse.jpg'));filtDiff.wrapS=filtDiff.wrapT=THREE.ClampToEdgeWrapping;
const filtBump=TL.load(asset('tex/filter-bump.jpg'));filtBump.wrapS=filtBump.wrapT=THREE.ClampToEdgeWrapping;
const M={
 /* Satin PP outer — FrontSide so rim has real thickness with lidIn, not paper-thin DoubleSide */
 lid:new THREE.MeshPhysicalMaterial({color:TEAL,roughness:.62,metalness:.01,clearcoat:.08,clearcoatRoughness:.7,sheen:.08,sheenColor:0x4a9aa6,envMapIntensity:.45,bumpMap:ppMicro,bumpScale:mob?.45:.7,roughnessMap:ppMicro,side:THREE.FrontSide}),
 /* Opaque underside shell — never hide; slightly darker for contact AO */
 lidIn:new THREE.MeshPhysicalMaterial({color:0x085a6c,roughness:.7,metalness:.01,clearcoat:.05,clearcoatRoughness:.8,side:THREE.BackSide,envMapIntensity:.35,polygonOffset:true,polygonOffsetFactor:2,polygonOffsetUnits:2,bumpMap:ppMicro,bumpScale:.45}),
 bag:new THREE.MeshPhysicalMaterial({color:0xeef3f4,roughness:.62,metalness:0,transparent:true,opacity:.16,bumpMap:filmT,bumpScale:mob?2.8:3.6,roughnessMap:filmT,side:THREE.DoubleSide,depthWrite:false,clearcoat:.12,clearcoatRoughness:.65}),
 bagIn:new THREE.MeshPhysicalMaterial({color:0xe4ecee,roughness:.85,transparent:true,opacity:.08,side:THREE.BackSide,depthWrite:false}),
 sachet:new THREE.MeshPhysicalMaterial({color:0xf3f3ef,roughness:.85,bumpMap:weaveT,bumpScale:1.2,map:weaveT,sheen:.6,sheenColor:0xffffff}),
 /* Opaque white porous disc — photo texture, no glassiness */
 filter:new THREE.MeshStandardMaterial({color:0xffffff,roughness:.95,metalness:0,map:filtDiff,bumpMap:filtBump,bumpScale:3.2,roughnessMap:filtBump,envMapIntensity:.15,side:THREE.DoubleSide}),
};
const U={uR:{value:0},uC:{value:new THREE.Vector3(10,-165,0)}};
const fluidM=new THREE.MeshPhysicalMaterial({color:0x5a050f,roughness:.08,metalness:0,transmission:.06,transparent:true,opacity:.95,clearcoat:.85,clearcoatRoughness:.12,attenuationColor:0x2a0003,attenuationDistance:20,thickness:20,ior:1.36});
const GK='float gd=distance(vWp,uC)+6.*sin(vWp.x*.3)*sin(vWp.z*.27+vWp.y*.2);float gk=1.-smoothstep(uR-14.,uR,gd);';
fluidM.customProgramCacheKey=()=>'gelfluid2';fluidM.onBeforeCompile=sdr=>{window.__gel=1;Object.assign(sdr.uniforms,U);
 sdr.vertexShader=sdr.vertexShader.replace('#include <common>','#include <common>\nvarying vec3 vWp;').replace('#include <project_vertex>','#include <project_vertex>\nvWp=(modelMatrix*vec4(transformed,1.)).xyz;');
 sdr.fragmentShader=sdr.fragmentShader.replace('#include <common>','#include <common>\nvarying vec3 vWp;uniform float uR;uniform vec3 uC;')
  .replace('#include <color_fragment>','#include <color_fragment>\n'+GK+'float depth=smoothstep(-176.,-100.,vWp.y);diffuseColor.rgb=mix(diffuseColor.rgb*1.12,diffuseColor.rgb*.55,depth*.55);diffuseColor.rgb=mix(diffuseColor.rgb,vec3(.04,.002,.005)*(.9+.15*sin(vWp.x*.12+vWp.y*.09)),gk);diffuseColor.a=mix(diffuseColor.a,1.,gk);')
  .replace('#include <roughnessmap_fragment>','#include <roughnessmap_fragment>\nroughnessFactor=mix(roughnessFactor,.9,gk);');};
function clipFilterCavity(geo,cx,cz,rMax,y0,y1){
 /* Drop CAD triangles inside the filter pocket cylinder (vert OR centroid).
  * Outer skirt (origin r>=51) is never touched so the rim stays closed. */
 const g=geo.index?geo.toNonIndexed():geo.clone();
 const p=g.attributes.position, n=p.count, keep=[];
 const inside=(x,y,z)=>Math.hypot(x-cx,z-cz)<rMax && y>=y0 && y<=y1 && Math.hypot(x,z)<51;
 for(let i=0;i<n;i+=3){
  const ax=p.getX(i),ay=p.getY(i),az=p.getZ(i);
  const bx=p.getX(i+1),by=p.getY(i+1),bz=p.getZ(i+1);
  const cx3=p.getX(i+2),cy=p.getY(i+2),cz3=p.getZ(i+2);
  const mx=(ax+bx+cx3)/3, my=(ay+by+cy)/3, mz=(az+bz+cz3)/3;
  if(inside(ax,ay,az)||inside(bx,by,bz)||inside(cx3,cy,cz3)||inside(mx,my,mz)) continue;
  keep.push(ax,ay,az, bx,by,bz, cx3,cy,cz3);
 }
 if(!keep.length) return geo;
 let out=new THREE.BufferGeometry();
 out.setAttribute('position',new THREE.Float32BufferAttribute(keep,3));
 out=mergeVertices(out,2e-4); /* re-weld so normals stay smooth (no faceting) */
 out.computeVertexNormals();
 return out;
}
function tuckBagTop(g){
 /* Bag ends at y=-24, lid skirt bottom at -23: pull the top lip up and just
  * inside the skirt (r<=55.2) so the film disappears under the rim, no gap. */
 const p=g.attributes.position;
 for(let i=0;i<p.count;i++){const y=p.getY(i);if(y<-30)continue;
  const k=(y+30)/6; const x=p.getX(i),z=p.getZ(i),r=Math.hypot(x,z);
  const ny=y+k*7, nr=Math.min(r,55.2+ (1-k)*(r-55.2));
  if(r>1e-3){p.setX(i,x/r*nr);p.setZ(i,z/r*nr);} p.setY(i,ny);}
 p.needsUpdate=true;g.computeVertexNormals();return g;}
function clampCollar(g){
 /* CAD collar lugs (r≤60.4) poke through the lid skirt (r 55.9@y-23 → 60.4@y-13).
  * Pull collar verts just inside the skirt profile; hidden part, no visible change. */
 const p=g.attributes.position;
 for(let i=0;i<p.count;i++){const y=p.getY(i),x=p.getX(i),z=p.getZ(i),r=Math.hypot(x,z);
  const sk=55.9+cl((y+23)/10)*4.5-0.8; if(r>sk){p.setX(i,x/r*sk);p.setZ(i,z/r*sk);}}
 p.needsUpdate=true;g.computeVertexNormals();return g;}
function cleanBag(geo){let g=geo.clone();['normal','uv','uv1','tangent','color'].forEach(a=>g.deleteAttribute(a));g=mergeVertices(g,1e-3);
 const ix=g.index.array,out=[],seen=new Set();for(let i=0;i<ix.length;i+=3){const t=[ix[i],ix[i+1],ix[i+2]];if(t[0]===t[1]||t[1]===t[2]||t[0]===t[2])continue;const k=[...t].sort((a,b)=>a-b).join();if(seen.has(k))continue;seen.add(k);out.push(...t);}
 g.setIndex(out);return toCreasedNormals(g,Math.PI/2.4);}
function prepSmooth(geo){let g=geo.clone();['uv1','tangent','color'].forEach(a=>g.deleteAttribute(a));
 if(g.attributes.normal)g.deleteAttribute('normal');
 if(g.index)g=mergeVertices(g,2e-4);
 g.computeVertexNormals(); return g;}
function cylUV(g,y0,y1){const p=g.attributes.position,uv=new Float32Array(p.count*2);for(let i=0;i<p.count;i++){uv[i*2]=Math.atan2(p.getZ(i),p.getX(i))/(2*Math.PI)+.5;uv[i*2+1]=(p.getY(i)-y0)/(y1-y0);}g.setAttribute('uv',new THREE.BufferAttribute(uv,2));return g;}
function addM(parent,geo,mat){const m=new THREE.Mesh(geo,mat);m.castShadow=true;m.receiveShadow=!mob;parent.add(m);return m;}
/* ease-out with tiny overshoot for lid settle */
function easeOutBack(x){x=cl(x);const c1=1.55,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2);}
const lidG=new THREE.Group(),bagG=new THREE.Group(),rig=new THREE.Group();S.add(rig);rig.add(lidG,bagG);
let fluid,sachet,pour,capM,fG,filtLook;const fW=new THREE.Vector3();
const loader=new GLTFLoader();
loader.load(asset('../p01-exploded/p01-1l.glb'),g=>{
 g.scene.updateMatrixWorld(true);const ms=[];g.scene.traverse(o=>{if(o.isMesh)ms.push(o)});
 ms.forEach(o=>{const nm=(o.name+' '+(o.parent?.name||'')).toLowerCase();
  if(nm.includes('pit'))return; /* canister — bag-only */
  if(nm.includes('lid'))return; /* replaced by smooth CAD lid */
  if(nm.includes('cap')){
   /* ORIGINAL CAD cap (32-vert) — smooth normals, no invented geometry */
   const geo=prepSmooth(o.geometry.clone().applyMatrix4(o.matrixWorld));
   capM=new THREE.Mesh(geo,M.lid);capM.name='CadCap';capM.castShadow=true;capM.receiveShadow=!mob;lidG.add(capM);
   return;
  }
  const k=['bag','collar'].find(x=>nm.includes(x));if(!k)return;
  const geo=cleanBag(o.geometry.clone().applyMatrix4(o.matrixWorld));
  if(k==='bag'){tuckBagTop(geo);cylUV(geo,-178,-24);const m=new THREE.Mesh(geo,M.bag);m.renderOrder=5;bagG.add(m);const mi=new THREE.Mesh(geo,M.bagIn);mi.renderOrder=4;bagG.add(mi);}
  else{clampCollar(geo);const m=new THREE.Mesh(geo,M.lid);m.castShadow=true;m.receiveShadow=!mob;m.renderOrder=3;bagG.add(m);}
 });
 loader.load(asset('p01-lid-smooth.glb'),hg=>{
  hg.scene.updateMatrixWorld(true);
  hg.scene.traverse(o=>{if(!o.isMesh)return;
   let geo=prepSmooth(o.geometry.clone().applyMatrix4(o.matrixWorld));
   /* Clip ONLY faces that intrude into the VACUUM filter cavity so CAD ribs
    * never cross the white disc. Cavity from GLB analysis: axis (33,-32),
    * clear core r≲14 at y∈[-18,-6]. Keep cylindrical wall (r≳14). */
   geo=clipFilterCavity(geo,30,-28,13.5,-24,-2);
   const m=new THREE.Mesh(geo,M.lid);m.castShadow=true;m.receiveShadow=!mob;lidG.add(m);
   /* Opaque BackSide twin — gives rim real thickness; bag cannot show through */
   const inn=new THREE.Mesh(geo,M.lidIn);inn.renderOrder=1;lidG.add(inn);
  });
  /* Opaque deck plug under main lid body — fills hollow shell so hero/final
   * never reads paper-thin. Annulus leaves VACUUM cavity open for the disc. */
  (function solidDeck(){
    /* Opaque underside plate with hole ONLY at VACUUM (33,-32) — stops bag bleed */
    const sh=new THREE.Shape();
    const N=72; for(let i=0;i<=N;i++){const a=i/N*Math.PI*2;const x=Math.cos(a)*51,y=Math.sin(a)*51; if(i===0)sh.moveTo(x,y); else sh.lineTo(x,y);}
    const hole=new THREE.Path();
    for(let i=0;i<=N;i++){const a=i/N*Math.PI*2;const x=30+Math.cos(a)*12.5,y=-28+Math.sin(a)*12.5; if(i===0)hole.moveTo(x,y); else hole.lineTo(x,y);}
    sh.holes.push(hole);
    const deckGeo=new THREE.ShapeGeometry(sh,12);
    const deck=new THREE.Mesh(deckGeo,M.lid);
    deck.rotation.x=-Math.PI/2;deck.position.y=-3.0;deck.castShadow=true;lidG.add(deck);
    const deck2=new THREE.Mesh(deckGeo,M.lid);
    deck2.rotation.x=-Math.PI/2;deck2.position.y=-6.5;lidG.add(deck2);
    const deckIn=new THREE.Mesh(deckGeo,M.lidIn);
    deckIn.rotation.x=Math.PI/2;deckIn.position.y=-3.15;lidG.add(deckIn);
    /* Opaque backing just inside CAD skirt (skirt inner r≈52..56, y -23..-5):
     * nothing behind the rim can show through. No extra visible rings. */
    const seal=new THREE.Mesh(new THREE.CylinderGeometry(51.6,54.6,17,72,1,true),M.lidIn);
    seal.position.y=-14;lidG.add(seal);
  })();
  /*
   * PHOTO EXCEPTION: white porous flow-stopper disc + minimal teal seat.
   * Refs: 01M6ND806 (tear-down), 01M6NCZQ (porous). NO large basin plate.
   * Disc recessed in clear CAD cavity at (33,-14.5,-32), r≈11.5 < wall≈19.
   */
  fG=new THREE.Group();fG.name='PhotoFilter';
  /* Short recessed pocket: floor + low lip only (tall open cylinder made a chord across disc) */
  const seatFloor=new THREE.Mesh(new THREE.CylinderGeometry(11.6,11.6,1.8,48),M.lid);
  seatFloor.position.y=-2.8;seatFloor.castShadow=true;
  const seatLip=new THREE.Mesh(new THREE.TorusGeometry(10.9,1.5,12,48),M.lid);
  seatLip.rotation.x=Math.PI/2;seatLip.position.y=1.6;
  const seatWall=new THREE.Mesh(new THREE.CylinderGeometry(11.2,11.5,3.2,48,1,true),M.lid);
  seatWall.position.y=0.2;
  const ao=new THREE.Mesh(new THREE.RingGeometry(8.6,11.8,48),new THREE.MeshBasicMaterial({color:0x000000,transparent:true,opacity:.42,depthWrite:false,side:THREE.DoubleSide}));
  ao.rotation.x=-Math.PI/2;ao.position.y=-1.9;ao.renderOrder=2;
  /* Disc sits in pocket, fully inside lip, proud of floor */
  const disc=new THREE.Mesh(new THREE.CylinderGeometry(9.4,9.4,4.0,48),M.filter);
  disc.position.y=0.0;disc.castShadow=true;disc.receiveShadow=!mob;
  fG.add(seatFloor,seatWall,seatLip,ao,disc);
  fG.position.set(30,-16.0,-28);
  fG.rotation.x=Math.PI;
  lidG.add(fG);
  filtLook=new THREE.Object3D();filtLook.position.set(30,-16.0,-28);lidG.add(filtLook);
  /* CAD assembly pose: lid skirt bottom y=-23 == collar bottom -23.05 */
  lidG.position.y=0;
  const sg=new THREE.BoxGeometry(34,7,46,10,2,12);const ps=sg.attributes.position;
  for(let i=0;i<ps.count;i++){const x=ps.getX(i)/17,z=ps.getZ(i)/23;ps.setY(i,ps.getY(i)*Math.max(.12,(1-x*x)*(1-Math.pow(Math.max(0,z),6))));}
  sg.computeVertexNormals();sachet=new THREE.Group();const smh=new THREE.Mesh(sg,M.sachet);smh.castShadow=true;sachet.add(smh);
  const seal=new THREE.Mesh(new THREE.BoxGeometry(34,1,6),new THREE.MeshPhysicalMaterial({color:0xdedfdc,roughness:.5,transparent:true,opacity:.85,bumpMap:weaveT,bumpScale:2}));seal.position.z=25.5;sachet.add(seal);
  bagG.add(sachet);
  const rAt=y=>48.7+(y+178)/154*7.9-2.2;const H=82,yb=-176.5;
  const rTop=rAt(yb+H),rBot=rAt(yb);
  const fg=new THREE.CylinderGeometry(rTop*.985,rBot*.985,H,96,20);fg.translate(0,H/2,0);
  const fpos=fg.attributes.position,fBaseY=new Float32Array(fpos.count);
  for(let i=0;i<fpos.count;i++){
   fBaseY[i]=fpos.getY(i); const y=fBaseY[i],x=fpos.getX(i),z=fpos.getZ(i);
   if(y>H*.78){const rr=Math.min(1,Math.hypot(x,z)/(rTop+1e-3)),ang=Math.atan2(z,x);
    fpos.setY(i,y+Math.pow(rr,2.2)*7.2+Math.sin(ang*2)*.9*rr+Math.sin(ang*5+1.1)*.4*rr);}
  }
  fpos.needsUpdate=true;fg.computeVertexNormals();fg.userData.baseY=fBaseY;fg.userData.H=H;fg.userData.rTop=rTop;
  fluid=new THREE.Mesh(fg,fluidM);fluid.position.y=yb;fluid.renderOrder=2;bagG.add(fluid);
  const bubG=new THREE.Group();const bubM=new THREE.MeshPhysicalMaterial({color:0xffe8ea,roughness:.15,transparent:true,opacity:.3,transmission:.55,thickness:2,depthWrite:false});
  [[8,0,12],[-14,0,-6],[18,0,-10],[-6,0,16],[12,0,-18]].forEach(([x,y,z],i)=>{const b=new THREE.Mesh(new THREE.SphereGeometry(.85+i*.12,12,10),bubM.clone());b.position.set(x,H*.9+y,z);bubG.add(b);});
  fluid.add(bubG);window.__bub=bubG;
  const dropG=new THREE.Group();const dropM=new THREE.MeshPhysicalMaterial({color:0x6a0812,roughness:.08,transparent:true,opacity:.7,clearcoat:.9,clearcoatRoughness:.1,depthWrite:false});
  [[10,0,8],[-12,0,-4],[6,0,-14],[-4,0,14]].forEach(([x,y,z],i)=>{const d=new THREE.Mesh(new THREE.SphereGeometry(.55+i*.08,10,8),dropM.clone());d.position.set(x,H*.92+y,z);dropG.add(d);});
  fluid.add(dropG);window.__drops=dropG;
  /* thin tapered pour — short soft cone, high transmission so it reads liquid not a stick */
  const pourGeo=new THREE.CylinderGeometry(.35,.95,70,12);pourGeo.translate(0,-35,0);
  pour=new THREE.Mesh(pourGeo,new THREE.MeshPhysicalMaterial({color:0x8a1018,roughness:.18,transparent:true,opacity:.28,transmission:.35,thickness:3,depthWrite:false,side:THREE.DoubleSide}));
  pour.position.set(26,-40,18);pour.rotation.z=.22;pour.rotation.x=-.06;pour.visible=false;pour.renderOrder=3;bagG.add(pour);
  window.__ready=true;
  if(stillCapture){
   T=0;requestAnimationFrame((now)=>{frame(now);window.__still_capture=true;root.dispatchEvent(new CustomEvent('cin-still-ready',{bubbles:true}));});
  }
 },undefined,e=>{console.error('lid-smooth',e);window.__ready='error';});
},undefined,e=>{console.error(e);window.__ready='error';});
function size(){const w=stage.clientWidth,h=stage.clientHeight;R.setSize(w,h,false);C.aspect=w/h;C.updateProjectionMatrix();}
new ResizeObserver(size).observe(stage);size();
const cl=x=>Math.min(1,Math.max(0,x)),ease=x=>{x=cl(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2;},seg=(t,a,b)=>ease((t-a)/(b-a)),lerp=(a,b,k)=>a+(b-a)*k;
const beats=[...root.querySelectorAll('.beat')].map(e=>({e,a:+e.dataset.a,b:+e.dataset.b}));
const logo=root.querySelector('.cin-logo'),hint=root.querySelector('.cin-hint'),bar=root.querySelector('.cin-bar');
const qp=new URLSearchParams(location.search);
const V=(x,y,z)=>new THREE.Vector3(x,y,z);
/* Deliberate scroll-film block — denser keys so motion never rests flat */
const KF=[
 /* Hero: gentle orbit with wider establishing */
 [0,    V(110,28,520), V(0,-48,0)],
 [.04,  V(140,34,430), V(2,-55,4)],
 [.08,  V(160,40,350), V(0,-72,0)],
 /* PATIENT: establish then low-ish 3/4 close-up */
 [.11,  V(140,40,240), V(10,0,20)],
 [.15,  V(122,30,168), V(16,8,30)],
 [.19,  V(128,34,158), V(12,10,32)],
 [.22,  V(135,38,165), V(8,8,30)],
 /* Filter: approach then hold a tear-down-style look INTO underside basin */
 [.25,  V(140,20,280), V(0,-30,0)],
 [.28,  V(120,40,220), V(10,20,-10)],
 /* placeholders — overridden by underside-normal camera below */
 [.31,  V(80,30,160), V(30,20,-25)],
 [.34,  V(75,28,150), V(32,18,-28)],
 [.37,  V(100,25,190), V(15,15,-15)],
 [.4,   V(140,10,260), V(0,-20,0)],
 /* Sachet: mid-height 3/4 with establish */
 [.42,  V(185,20,270), V(5,-85,0)],
 [.47,  V(195,2,250),  V(0,-110,0)],
 /* Blood: side-on at fluid level */
 [.53,  V(200,-130,160), V(0,-140,0)],
 [.58,  V(188,-145,150), V(5,-148,0)],
 [.62,  V(172,-152,155), V(0,-152,5)],
 /* Gel drift */
 [.68,  V(145,-120,150), V(0,-145,8)],
 [.74,  V(118,-125,158), V(5,-142,0)],
 [.82,  V(90,-100,170),  V(0,-125,20)],
 /* Final iso hero */
 [.92,  V(72,10,470), V(0,-48,0)],
 [.97,  V(78,14,490), V(0,-45,0)],
 [1,    V(80,14,495), V(0,-45,0)]
];
let T=0,lastN=0;const cp=new THREE.Vector3(),ct=new THREE.Vector3();
function prog(){if(qp.has('t'))return +qp.get('t');const total=Math.max(1,root.offsetHeight-innerHeight);const scrolled=Math.min(total,Math.max(0,-root.getBoundingClientRect().top));return cl(scrolled/total);}
function sampleKF(t,outP,outT){
 let a=KF[0],b=KF[KF.length-1];
 for(let n=0;n<KF.length-1;n++)if(t>=KF[n][0]&&t<=KF[n+1][0]){a=KF[n];b=KF[n+1];break;}
 const k=ease((t-a[0])/Math.max(1e-4,b[0]-a[0]));
 outP.lerpVectors(a[1],b[1],k);outT.lerpVectors(a[2],b[2],k);
}
let paused=false;
const pauseBtn=root.querySelector('[data-cin-pause]');
if(pauseBtn)pauseBtn.addEventListener('click',()=>{paused=!paused;pauseBtn.setAttribute('aria-pressed',paused?'true':'false');root.classList.toggle('is-paused',paused);});
function frame(now){requestAnimationFrame(frame);
 if(paused){R.render(S,C);return;}
 const dt=Math.min(.1,(now-(lastN||now))/1000);lastN=now;T+=(prog()-T)*(qp.has('t')?1:1-Math.exp(-dt*3.2));const t=T;
 const tSec=now*.001;
 if(bar)bar.style.width=(t*100)+'%';if(hint)hint.style.opacity=1-cl(t*18);
 beats.forEach(b=>{const f=.028;const o=Math.min(cl((t-b.a)/f),cl((b.b-t)/f));b.e.style.opacity=o;b.e.style.transform=`translateY(${(1-o)*10}px)`;});
 if(logo)logo.style.opacity=cl((t-.94)/.03);
 /* v8 scroll feel: no idle sway / micro-drift — camera only follows scrubbed t */
 rig.rotation.set(0,0,0);
 if(fluid){
  /* lid lift with soft settle + tiny overshoot (easeOutBack) */
  const liftIn=easeOutBack(seg(t,.24,.31));
  const liftOut=easeOutBack(seg(t,.47,.54));
  const lift=liftIn*(1-liftOut);
  /* base settle -1.8 seats lid on collar; lift reveals underside + disc */
  lidG.position.y=lift*75;lidG.position.z=lift*24;lidG.rotation.x=-lift*.58;
  const sd=seg(t,.38,.48);sachet.visible=t>.37;sachet.position.set(10,lerp(70,-170,sd),0);sachet.rotation.set(lerp(-.9,0,sd),lerp(1.2,.3,sd),lerp(.5,0,sd));
  const fill=seg(t,.53,.64);fluid.visible=fill>.005;fluid.scale.y=Math.max(.001,fill);
  U.uR.value=lerp(0,190,seg(t,.65,.78));
  const pos=fluid.geometry.attributes.position,base=fluid.geometry.userData.baseY,HH=fluid.geometry.userData.H||82,rt=fluid.geometry.userData.rTop||54;
  if(base&&fill>.01){
   const live=(1-seg(t,.66,.78))*fill;
   /* landing splash ripple while pouring */
   const splash=seg(t,.53,.58)*(1-seg(t,.59,.65));
   for(let i=0;i<pos.count;i++){
    const y0=base[i]; if(y0<=HH*.78) continue;
    const x=pos.getX(i),z=pos.getZ(i),rr=Math.min(1,Math.hypot(x,z)/(rt+1e-3)),ang=Math.atan2(z,x);
    const men=Math.pow(rr,2.2)*7.2+(Math.sin(ang*2+tSec*1.4)*.85+Math.sin(ang*5+tSec*2.1)*.35)*rr*live;
    const rip=splash*Math.sin(ang*3-tSec*6)*.9*rr*Math.exp(-rr*1.2);
    pos.setY(i,y0+men+rip);
   }
   pos.needsUpdate=true;
  }
  const wob=(1-seg(t,.66,.76))*fill;fluid.rotation.z=Math.sin(tSec*1.6)*.01*wob;fluid.rotation.x=Math.cos(tSec*1.3)*.01*wob;
  if(pour){
   const ps=seg(t,.53,.58)*(1-seg(t,.6,.66));
   pour.visible=ps>.02;
   pour.material.opacity=.08+.22*ps;
   const wobP=Math.sin(tSec*5.5)*.055*ps;
   pour.scale.set(.7+.25*ps, Math.max(.03,ps*(.85+Math.sin(tSec*3)*.08)), .7+.25*ps);
   pour.rotation.z=.22+wobP;pour.rotation.x=-.06+Math.cos(tSec*4.2)*.04*ps;
   pour.position.x=26+Math.sin(tSec*3.8)*1.2*ps;
  }
  if(window.__bub){const bo=(1-seg(t,.66,.76))*fill;window.__bub.visible=bo>.05;window.__bub.children.forEach((b,i)=>{b.material.opacity=.1+.28*bo;b.position.y=HH*.88+Math.sin(tSec*2+i)*1.1;});}
  if(window.__drops){const dd=seg(t,.54,.62)*(1-seg(t,.66,.74));window.__drops.visible=dd>.04;window.__drops.children.forEach((d,i)=>{d.material.opacity=.15+.55*dd;d.position.y=HH*.9+Math.sin(tSec*3+i*1.7)*.8;d.scale.setScalar(.7+dd*.5);});}
 }
 sampleKF(t,cp,ct);
 /* Distance fit only — keyframes stay put.
    Phone: v12's tall-phone scale (1.36), even when the caption band
    makes the stage wider, so the opening frame is not zoomed in.
    Desktop: a slightly longer lens so the base stays inside a 16:9 frame. */
 let fit = mob ? 1.72 : 1.46;
 if (mob && t > 0.2 && t < 0.58) fit = Math.max(fit, 1.92);
 if (mob && t >= 0.58) fit = Math.max(fit, 1.78);
 cp.sub(ct).multiplyScalar(fit).add(ct);
 /* Filter stays on underside; hide only once blood fills */
 if(fG){ fG.visible=t<.52; }
 /*
  * Filter beat: 3/4 from below looking into recessed housing — disc seated
  * inside teal seat, no ribs crossing face (cavity clipped).
  */
 /* Desktop-only filter close-up; on phones keep scroll keyframes so the bag stays in frame */
 if(!mob&&filtLook&&t>.27&&t<.4){
  const w=seg(t,.28,.32)*(1-seg(t,.37,.4));
  filtLook.getWorldPosition(fW);
  const nrm=V(0,-1,0).applyQuaternion(lidG.quaternion).normalize();
  const side=V(.25,0,.15).applyQuaternion(lidG.quaternion).normalize();
  const dist=110;
  const goal=fW.clone().addScaledVector(nrm,dist).addScaledVector(side,18);
  cp.lerp(goal,w);
  ct.lerp(fW,w);
 }

 C.position.copy(cp);C.lookAt(ct);const d=cp.distanceTo(ct);C.near=Math.max(1,d*.05);C.far=d+1500;C.updateProjectionMatrix();
 R.render(S,C);
 if(window.__cin_profile_on){
  const p=performance.now();
  const prof=window.__cin_profile||{frames:[]};
  if(prof.last)prof.frames.push(p-prof.last);
  prof.last=p;window.__cin_profile=prof;
 }
 if(!window.__cin_frame){window.__cin_frame=true;root.dispatchEvent(new CustomEvent('cin-frame',{bubbles:true}));}
}


if(stillCapture){
 root.classList.add('is-still');
}else{
 root.classList.remove('is-still');
 root.classList.add('is-playing');
 requestAnimationFrame(frame);
}
}
