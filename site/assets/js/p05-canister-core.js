/**
 * Shared P05 canister loading for the canister product page: genuine CAD GLBs,
 * the genuine size-specific official photo print, the approved clear-PC
 * material, and the photo-derived hose set (0402102 / 0402103) materials.
 * Same shader and mapping as the approved P05 cinematics.
 */
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {mergeVertices, toCreasedNormals} from 'three/addons/utils/BufferGeometryUtils.js';

const base = new URL('../../3d-sketches/', import.meta.url);
const u = rel => new URL(rel, base).href;
export const CANISTERS = {
  'p05-1l': {glb: u('p05-cinematic/p05-1l-canister-cad.glb'), ink: u('p05-cinematic/tex/official-1l-print.png?v=photo-refinement-2'), ph: 183, H: 183},
  'p05-2l': {glb: u('p05-2l-cinematic/p05-2l-canister-cad.glb'), ink: u('p05-2l-cinematic/tex/official-2l-print.png?v=2l-photo-1'), ph: 270, H: 270},
  'p05-3l': {glb: u('p05-3l-cinematic/p05-3l-canister-cad.glb'), ink: u('p05-3l-cinematic/tex/official-3l-print.png?v=3l-photo-1'), ph: 420, H: 420},
  'p05-2l-set': {glb: u('p05-2l-set-cinematic/p05-2l-set.glb?v=set-1'), ink: u('p05-2l-cinematic/tex/official-2l-print.png?v=2l-photo-1'), ph: 270, H: 270, set: true},
  'p05-3l-set': {glb: u('p05-3l-set-cinematic/p05-3l-set.glb?v=set-1'), ink: u('p05-3l-cinematic/tex/official-3l-print.png?v=3l-photo-1'), ph: 420, H: 420, set: true}
};

export function kitMaterials() {
  // Photo-derived hose set 050103; colours sampled from the official photos (est.).
  return {
    'silicone-hose': new THREE.MeshPhysicalMaterial({color: 0x2f6200, roughness: .55, metalness: 0, clearcoat: .1, clearcoatRoughness: .5, envMapIntensity: .22}),
    'pe-yellow': new THREE.MeshPhysicalMaterial({color: 0x9e8a00, roughness: .55, metalness: 0, envMapIntensity: .12}),
    'pom-white': new THREE.MeshPhysicalMaterial({color: 0xe4e8e6, roughness: .34, metalness: 0, clearcoat: .15, clearcoatRoughness: .35, envMapIntensity: .6})
  };
}

function pcMaterials(R, cfg, onInk, tone) {
  const light = tone === 'light';
  const pc = new THREE.MeshPhysicalMaterial({color: light ? 0xe9f1f4 : 0xf3f8fa, roughness: .075, metalness: 0, transmission: 0, transparent: true, opacity: light ? .55 : .48, depthWrite: false, thickness: 2.4, ior: 1.586, attenuationColor: 0xd9eef0, attenuationDistance: 650, clearcoat: .5, clearcoatRoughness: .12, envMapIntensity: .95, side: THREE.DoubleSide});
  const mountPC = pc.clone(); mountPC.roughness = .16; mountPC.opacity = light ? .62 : .56; mountPC.thickness = 3.4;
  const ink = new THREE.TextureLoader().load(cfg.ink, onInk, undefined, onInk);
  ink.colorSpace = THREE.SRGBColorSpace; ink.anisotropy = Math.min(16, R.capabilities.getMaxAnisotropy());
  const ph = cfg.ph.toFixed(1);
  for (const m of [pc, mountPC]) {
    m.onBeforeCompile = shader => {
      const glassAlpha = 'diffuseColor.a *= .18 + .82 * pow(1. - abs(dot(normal, normalize(vViewPosition))), 2.2);';
      if (m === pc) {
        shader.uniforms.uOfficialInk = {value: ink};
        shader.vertexShader = shader.vertexShader.replace('#include <common>', '#include <common>\nattribute float printOuter; varying vec3 vInkPos; varying vec3 vInkWorld; varying float vInkOuter;').replace('#include <begin_vertex>', '#include <begin_vertex>\nvInkPos=position;vInkWorld=(modelMatrix*vec4(position,1.)).xyz;vInkOuter=printOuter;');
        shader.fragmentShader = shader.fragmentShader.replace('#include <common>', '#include <common>\nuniform sampler2D uOfficialInk;varying vec3 vInkPos;varying vec3 vInkWorld;varying float vInkOuter;');
        shader.fragmentShader = shader.fragmentShader.replace('#include <opaque_fragment>', glassAlpha + '\n#include <opaque_fragment>');
        shader.fragmentShader = shader.fragmentShader.replace('#include <colorspace_fragment>', `#include <colorspace_fragment>
   vec2 inkUV=vec2(.5+atan(vInkPos.x,vInkPos.z)/6.28318530718,1.+vInkPos.y/${ph});
   vec4 ink=texture2D(uOfficialInk,inkUV);
   float exteriorFacing=step(.02,dot(normalize(vec3(vInkPos.x,0.,vInkPos.z)),normalize(cameraPosition-vInkWorld)));
   float inkA=ink.a*vInkOuter*exteriorFacing;
   if(inkA>0.){
    float printedAlpha=inkA+(1.-inkA)*gl_FragColor.a;
    vec3 inkColor=linearToOutputTexel(vec4(ink.rgb,1.)).rgb;
    gl_FragColor.rgb=(gl_FragColor.rgb*gl_FragColor.a*(1.-inkA)+inkColor*inkA)/max(printedAlpha,.00001);
    gl_FragColor.a=printedAlpha;
   }
  `);
      } else shader.fragmentShader = shader.fragmentShader.replace('#include <opaque_fragment>', glassAlpha + '\n#include <opaque_fragment>');
    };
    m.customProgramCacheKey = () => (m === pc ? 'p05-page-ink-' + ph : 'p05-page-edge') + (light ? '-l' : '-d');
  }
  return {pc, mountPC, ink};
}

/** Load one canister (or set). Resolves to {group, cfg, bounds}. */
export function loadCanister(R, id, {tone = 'dark'} = {}) {
  const cfg = CANISTERS[id];
  return new Promise((resolve, reject) => {
    let inkDone = false, glb = null;
    const mats = pcMaterials(R, cfg, () => { inkDone = true; done(); }, tone);
    const kit = kitMaterials();
    function done() {
      if (!inkDone || !glb) return;
      const group = new THREE.Group();
      glb.scene.updateMatrixWorld(true);
      glb.scene.traverse(o => {
        if (!o.isMesh) return;
        const km = kit[o.material && o.material.name];
        let geo = o.geometry;
        if (!km) {
          // Normals only: vertices and silhouette untouched.
          geo = o.geometry.clone(); geo.deleteAttribute('normal'); geo = mergeVertices(geo, 1e-5); geo = toCreasedNormals(geo, Math.PI / 3);
        }
        if (o.name === 'vessel') {
          const pos = geo.attributes.position, outer = new Float32Array(pos.count);
          const a = new THREE.Vector3(), b = new THREE.Vector3(), c = new THREE.Vector3();
          for (let i = 0; i < pos.count; i += 3) {
            a.fromBufferAttribute(pos, i); b.fromBufferAttribute(pos, i + 1); c.fromBufferAttribute(pos, i + 2);
            const n = b.clone().sub(a).cross(c.clone().sub(a)).normalize();
            const radial = a.clone().add(b).add(c); radial.y = 0; radial.normalize();
            if (n.dot(radial) > .95 && Math.abs(n.y) < .2) outer.fill(1, i, i + 3);
          }
          geo.setAttribute('printOuter', new THREE.BufferAttribute(outer, 1));
        }
        const m = new THREE.Mesh(geo, km || (o.name === 'vessel' ? mats.pc : mats.mountPC));
        m.name = o.name;
        group.add(m);
      });
      resolve({group, cfg, bounds: new THREE.Box3().setFromObject(group)});
    }
    new GLTFLoader().load(cfg.glb, g => { glb = g; done(); }, undefined, reject);
  });
}

export function contactShadow(size) {
  const sc = document.createElement('canvas'); sc.width = sc.height = 256;
  const sx = sc.getContext('2d'); const sg = sx.createRadialGradient(128, 128, 10, 128, 128, 128);
  sg.addColorStop(0, 'rgba(0,0,0,.6)'); sg.addColorStop(.48, 'rgba(0,0,0,.2)'); sg.addColorStop(1, 'rgba(0,0,0,0)');
  sx.fillStyle = sg; sx.fillRect(0, 0, 256, 256);
  const m = new THREE.Mesh(new THREE.PlaneGeometry(size, size), new THREE.MeshBasicMaterial({map: new THREE.CanvasTexture(sc), transparent: true, depthWrite: false}));
  m.rotation.x = -Math.PI / 2;
  return m;
}
