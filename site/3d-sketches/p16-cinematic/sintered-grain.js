// Presentation only — does not change geometry. 3D procedural sintered
// grain in object space so the outer wall, bore and rims share one
// seamless field (no UV seams, no cylindrical stretching).
export function applySinteredGrain(mat, opts={}){
  const mobile = !!opts.mobile;
  const u = {
    uAmp:  {value: opts.amp  ?? 0.11},
    uBump: {value: opts.bump ?? 0.020},
    uPore: {value: opts.pore ?? 0.08}
  };
  mat.userData.sinteredUniforms = u;
  mat.customProgramCacheKey = () => 'p16-sintered-v3d';
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
uniform float uPore;
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
// Pixel size in millimetres — used to fade fine pores so they do not
// alias or shimmer when the tube is small on screen.
float grainPx(){
  return max(length(dFdx(vObjPos)), length(dFdy(vObjPos)));
}
// Soft sandstone mottle plus irregular micro-pores.
// Returns vec3: x = albedo height, y = bump height (mid mottle only, no
// high-frequency pores — those cause droplet / ripple highlights), z = pores.
vec3 sgrain(vec3 p){
  float px = grainPx();
  float fadeFine = 1.0 - smoothstep(0.10, 0.38, px);
  float fadeMed  = 1.0 - smoothstep(0.28, 0.90, px);
  // Domain warp so the field is not a regular cell grid.
  vec3 w = vec3(svnoise(p * 0.37), svnoise(p * 0.37 + 5.1), svnoise(p * 0.37 + 9.4));
  p += 0.55 * (w - 0.5);
  float m = svnoise(p * 0.85);
  m = 0.62 * m + 0.38 * svnoise(p * 2.15 + 7.3);
  ${mobile ? '' : 'if (fadeMed > 0.01) m = mix(m, 0.78 * m + 0.22 * svnoise(p * 4.4 + 13.1), fadeMed);'}
  // Continuous fine sugar / sandstone grain — no hard pore threshold,
  // which reads as water droplets in close-up. Fine octaves fade with pixel size.
  float fadeTiny = 1.0 - smoothstep(0.055, 0.20, px);
  float fine = 0.5;
  float pores = 0.0;
  if (fadeFine > 0.01){
    vec3 q = p + 0.45 * (vec3(svnoise(p * 1.6 + 2.0), svnoise(p * 1.6 + 8.2), svnoise(p * 1.6 + 14.7)) - 0.5);
    fine = svnoise(q * 6.8);
    fine = 0.58 * fine + 0.42 * svnoise(q * 11.4 + 17.4);
    if (fadeTiny > 0.01) fine = mix(fine, 0.72 * fine + 0.28 * svnoise(q * 16.8 + 23.0), fadeTiny);
    // Remap for readable contrast without clipping into islands.
    fine = smoothstep(0.18, 0.84, fine);
    pores = (1.0 - fine) * fadeFine;
  }
  float hAlbedo = mix(m, 0.38 * m + 0.62 * fine, fadeFine);
  float hBump = m; // mid-scale only
  return vec3(clamp(hAlbedo, 0.0, 1.0), clamp(hBump, 0.0, 1.0), pores);
}
`)
      .replace('#include <normal_fragment_begin>', `#include <normal_fragment_begin>
#ifdef STANDARD
{
  vec3 g = sgrain(vObjPos);
  float fadeBump = 1.0 - smoothstep(0.14, 0.70, grainPx());
  vec2 dHdxy = vec2(dFdx(g.y), dFdy(g.y)) * uBump * fadeBump;
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
  vec3 g = sgrain(vObjPos);
  float k = (0.5 - g.x) * uAmp + g.z * uPore;
  diffuseColor.rgb *= 1.0 - k;
  // Pores stay cool neutral grey, never a yellow cast.
  vec3 cool = vec3(0.965, 0.968, 0.975);
  diffuseColor.rgb = mix(diffuseColor.rgb, diffuseColor.rgb * cool, g.z * 0.55);
}
`)
      .replace('#include <roughnessmap_fragment>', `#include <roughnessmap_fragment>
{
  vec3 g = sgrain(vObjPos);
  roughnessFactor = clamp(roughnessFactor + 0.04 * (1.0 - g.x) + 0.05 * g.z, 0.0, 1.0);
}
`);
  };
  mat.needsUpdate = true;
  return mat;
}
