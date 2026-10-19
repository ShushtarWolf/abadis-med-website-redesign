import uharfbuzz as hb, io, os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
FD='/workspace/lw/site/fonts/'
OUT='/workspace/lw/site/brand/section-logos/'
def load(n):
    f=TTFont(FD+n); b=io.BytesIO(); f.flavor=None; f.save(b); return f,hb.Font(hb.Face(b.getvalue()))
FONTS={'b':load('KalamehWeb-FaNum-Black.woff2'),'r':load('KalamehWeb-FaNum-Regular.woff2')}
def text(s,fk,size,x,y,anchor='end',ls=0):
    tt,f=FONTS[fk]; upm=tt['head'].unitsPerEm
    buf=hb.Buffer(); buf.add_str(s); buf.guess_segment_properties(); hb.shape(f,buf)
    gs=tt.getGlyphSet(); order=tt.getGlyphOrder(); sc=size/upm
    total=sum(p.x_advance for p in buf.glyph_positions)+ls*len(buf.glyph_positions)/sc
    x0=x-total*sc if anchor=='end' else (x-total*sc/2 if anchor=='middle' else x)
    pen=SVGPathPen(gs); cx=0
    for i,p in zip(buf.glyph_infos,buf.glyph_positions):
        tp=TransformPen(pen,(sc,0,0,-sc,x0+(cx+p.x_offset)*sc,y-p.y_offset*sc))
        gs[order[i.codepoint]].draw(tp); cx+=p.x_advance+ls/sc
    return pen.getCommands(), total*sc
T='#05686b'; A='#2ec4c6'
ring='<circle cx="60" cy="60" r="54" fill="none" stroke="{c}" stroke-width="2.2"/>'
S='fill="none" stroke-linecap="round" stroke-linejoin="round"'
icons={
'why':('چرا آبادیس','Why Abadis','''<path d="M44 46a16 16 0 1 1 23 14.5C62 63 60 66 60 71v5" {S} stroke="{c}" stroke-width="4.5"/><circle cx="60" cy="89" r="3.6" fill="{a}"/>'''),
'calculator':('محاسبه گر','Calculator','''<path d="M27 76a34 34 0 1 1 66 0" {S} stroke="{c}" stroke-width="4.5"/><path d="M60 30v6M38 40l4 4M82 40l-4 4" {S} stroke="{c}" stroke-width="2.5"/><path d="M60 72L80 52" {S} stroke="{a}" stroke-width="4"/><circle cx="60" cy="72" r="4.5" fill="{c}"/><path d="M44 92h32" {S} stroke="{c}" stroke-width="3.5"/>'''),
'sustainable':('توسعه پایدار','Sustainable Development','''<path d="M60 94V58" {S} stroke="{c}" stroke-width="4"/><path d="M60 62C60 40 74 28 92 28c0 22-12 34-32 34z" fill="{a}"/><path d="M60 74C60 56 48 46 30 46c0 18 12 28 30 28z" fill="{c}"/><path d="M40 96h40" {S} stroke="{c}" stroke-width="3.5"/>'''),
'zagros':('نجات زاگرس','Save Zagros','''<path d="M18 88L46 46l14 18 14-26 28 50" {S} stroke="{c}" stroke-width="4.5"/><path d="M60 92V74" {S} stroke="{c}" stroke-width="3"/><path d="M60 78c-9 0-13-6-13-12 0-7 6-10 13-16 7 6 13 9 13 16 0 6-4 12-13 12z" fill="{a}"/>'''),
'impact':('اثر گذاری','Impact','''<circle cx="60" cy="58" r="5.5" fill="{a}"/><path d="M42 60a18 18 0 0 1 36 0" {S} stroke="{c}" stroke-width="4"/><path d="M28 60a32 32 0 0 1 64 0" {S} stroke="{c}" stroke-width="4" opacity=".55"/><path d="M60 96V82M52 88l8 8 8-8" {S} stroke="{c}" stroke-width="4" transform="rotate(180 60 89)"/>'''),
}
def icon_svg(k,c,a,rc):
    return ring.format(c=rc)+icons[k][2].replace('{S}',S).replace('{c}',c).replace('{a}',a)
for k,(fa,en,_) in icons.items():
    for mode,c,a,rc,tc,ec in [('',T,A,T,T,'#5a7578'),('-dark','#e6f3f3',A,A,'#ffffff','#9dbdbf')]:
        open(OUT+f'{k}-icon{mode}.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="240" height="240">{icon_svg(k,c,a,rc)}</svg>')
        p1,w1=text(fa,'r',46,0,0); p2,w2=text(en.upper(),'r',15,0,0,anchor='start',ls=2.5)
        W=max(w1,w2)+150; tx=W-138
        p1,_=text(fa,'r',46,tx,74); p2,_=text(en.upper(),'r',15,tx-w2,104,anchor='start',ls=2.5)
        open(OUT+f'{k}-lockup{mode}.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} 130" width="{W*2:.0f}" height="260"><g transform="translate({W-125:.1f} 5)">{icon_svg(k,c,a,rc)}</g><path d="{p1}" fill="{tc}"/><path d="{p2}" fill="{ec}"/></svg>')
mk=lambda m:''.join(f'<figure><img src="{k}-lockup{m}.svg"><img class="i" src="{k}-icon{m}.svg"></figure>' for k in icons)
open(OUT+'index.html','w').write('''<!doctype html><html lang="fa" dir="rtl"><meta charset="utf-8"><title>Abadis Med – Section Logos</title><style>body{margin:0;font-family:Tahoma,sans-serif}section{display:grid;grid-template-columns:repeat(auto-fill,minmax(420px,1fr));gap:24px;padding:32px}.l{background:#f4f8f8}.d{background:#071d20}figure{margin:0;display:flex;align-items:center;gap:20px;justify-content:space-between}figure img{height:96px}figure img.i{height:72px}</style>
<section class="l">'''+mk('')+'</section><section class="d">'+mk('-dark')+'</section></html>')
