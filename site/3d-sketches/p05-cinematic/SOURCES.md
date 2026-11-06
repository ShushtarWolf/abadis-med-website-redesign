# P05 — actual 1 L reusable suction canister

## Geometry, no substitutes
Source: `/workspace/boss-orders/partlens/extracted/Abadis/1L pit.partlens`.
Source archive SHA256: `aadfde16e0bdf26db94ff6bcd80a9dbf3be496cdce938aca020c5850edca33e6`.
Exact HIGH mesh fingerprint: `423c00c3e4a32abcb09f98e22c418f9409ab448e25f61c3748956489c8704c98`.

All 1,094 original CAD triangles are retained: vessel 542; upper collar/rear mounting structure 552. Coordinate conversion (x,y,z) -> (x,z,-y), millimetres. No scaling, vertex smoothing, shape deformation, subdivision, clipping or invented rigid parts. Crease-aware normals change shading only.

Full assembly mesh bounds: 129 × 183 × 150.2338 mm in Three.js x/y/z, including mounting structure; vessel body approximately 123 mm wide. These are approximate tessellated CAD extents, not manufacturer nominal dimensions. No dimensions appear in the cinematic.

The open top is intentional and is the actual CAD. No lid, mouth ports, bag liner, filter, sachet, fluid or additional hose barb is added. The mounting piece remains attached in its original pose throughout. No exploded assembly or invented moving mechanism.

## Verified manufacturer reference
https://www.abadis-med.com/en/products/canisters/
Opened during this work: reusable transparent polycarbonate 1 L canister, product code 0402011. The page's 12.2 × 18 cm figures are explicitly individual package dimensions; not product dimensions and not used as such.

Manufacturer photo inspected: `site/assets/img/c/49d95f95cd78-900.webp` (three actual clear canisters). Used for clear polycarbonate appearance only. Branding/printed graduation decals are not reproduced because the CAD contains no print and a calibrated 1 L decal source has not been established. This does not claim print-free appearance of the sold product.

## Presentation
Approved P02 typography, vendor dependencies, antialiasing, 1800vh scroll track and exp(-dt*3.2) camera damping. New canister-specific story: full product, open rim, rear mount, transparent wall, base, final hero. No autonomous product/camera drift. Soft studio environment and contact shadow are presentation assets, not product geometry. Optical appearance uses edge-weighted alpha for readable clear walls and the original rear mounting geometry. This is approximate real-time rendering, not physically calibrated refraction or laboratory-validated material optics.

QA scripts/screenshots/report live outside repository: `/workspace/_qa_p05/v1/`. P01 and P02 are unchanged. No other sizes or products are included.
