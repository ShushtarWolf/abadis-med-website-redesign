// Presentation only — does not change geometry. 3D procedural sintered
// grain in object space so the outer wall, bore and rims share one
// seamless field (no UV seams, no cylindrical stretching).
export function applySinteredGrain(mat, opts={}){
  const mobile = !!opts.mobile;
  const u = {
    uAmp:  {value: opts.amp  ?? 0.050},
    uBump: {value: opts.bump ?? 0.016},
    uWarm: {value: opts.warm ?? 0.48}
  };
  mat.userData.sinteredUniforms = u;
  mat.customProgramCacheKey = () => 'p16-sintered-v2h';
  mat.onBeforeCompile = (shader) => {
    Object.assign(shader.uniforms, u);
    shader.vertexShader = shader.vertexShader
      .replace('#include <common>', `#include <common>\nvarying vec3 vObjPos;\nvarying vec3 vViewPos;`)
      .replace('#include <begin_vertex>', `#include <begin_vertex>\nvObjPos = position;`)
      .replace('#include <project_vertex>', `#include <project_vertex>\nvViewPos = mvPosition.xyz;`);
    shader.fragmentShader = shader.fragmentShader
      .replace('#include <common>', `#include <common>
varying vec3 vObjPos;
varying vec3 vViewPos;
uniform float uAmp;
uniform float uBump;
uniform float uWarm;
float shash(vec3 p){
  p = fract(p * 0.3183099 + vec3(0.11, 0.23, 0.37));
  p += dot(p, p.yzx + 19.19);
  return fract((p.x + p.y) * p.z);
}
float svnoise(vec3 x){
  vec3 i = floor(x);
  vec3 f = fract(x);
  f = f * f * (3.0 - 2.0 * f);
  float n000 = shash(i);
  float n100 = shash(i + vec3(1.0, 0.0, 0.0));
  float n010 = shash(i + vec3(0.0, 1.0, 0.0));
  float n110 = shash(i + vec3(1.0, 1.0, 0.0));
  float n001 = shash(i + vec3(0.0, 0.0, 1.0));
  float n101 = shash(i + vec3(1.0, 0.0, 1.0));
  float n011 = shash(i + vec3(0.0, 1.0, 1.0));
  float n111 = shash(i + vec3(1.0, 1.0, 1.0));
  float n00 = mix(n000, n100, f.x);
  float n10 = mix(n010, n110, f.x);
  float n01 = mix(n001, n101, f.x);
  float n11 = mix(n011, n111, f.x);
  float n0 = mix(n00, n10, f.y);
  float n1 = mix(n01, n11, f.y);
  return mix(n0, n1, f.z);
}
// Soft cloudy mottle (~1.2 mm and ~0.45 mm) plus sparse pore pits (~0.2 mm).
// Returns 0 at pits / dark speckles, 1 at highlights. p is millimetres.
float sgrain(vec3 p){
  // Light domain warp so the mottle is not a regular cell field.
  vec3 w = vec3(svnoise(p * 0.37), svnoise(p * 0.37 + 5.1), svnoise(p * 0.37 + 9.4));
  p += 0.55 * (w - 0.5);
  float m = svnoise(p * 0.85);
  m = 0.62 * m + 0.38 * svnoise(p * 2.15 + 7.3);
  ${mobile ? '' : 'm = 0.82 * m + 0.18 * svnoise(p * 4.4 + 13.1);'}
  // Continuous fine grain only — no thresholded pits, which read as droplets.
  m = 0.80 * m + 0.20 * svnoise(p * 5.6 + 19.7);
  return clamp(m, 0.0, 1.0);
}
`)
      .replace('#include <normal_fragment_begin>', `#include <normal_fragment_begin>
#ifdef STANDARD
{
  float h = sgrain(vObjPos);
  vec2 dHdxy = vec2(dFdx(h), dFdy(h)) * uBump;
  vec3 vSigmaX = dFdx(vViewPos);
  vec3 vSigmaY = dFdy(vViewPos);
  vec3 R1 = cross(vSigmaY, normal);
  vec3 R2 = cross(normal, vSigmaX);
  float fDet = dot(vSigmaX, R1);
  vec3 vGrad = sign(fDet) * (dHdxy.x * R1 + dHdxy.y * R2);
  normal = normalize(abs(fDet) * normal - vGrad);
}
#endif
`)
      .replace('#include <map_fragment>', `#include <map_fragment>
{
  float h = sgrain(vObjPos);
  float k = (0.5 - h) * uAmp;
  diffuseColor.rgb *= 1.0 - k;
  // Pits pick up a touch of warm beige, like the official sintered PE.
  vec3 warm = vec3(1.0, 0.985, 0.96);
  diffuseColor.rgb = mix(diffuseColor.rgb, diffuseColor.rgb * warm, (1.0 - h) * uWarm);
}
`)
      .replace('#include <roughnessmap_fragment>', `#include <roughnessmap_fragment>
  roughnessFactor = clamp(roughnessFactor + 0.05 * (1.0 - sgrain(vObjPos)), 0.0, 1.0);
`);
  };
  mat.needsUpdate = true;
  return mat;
}
