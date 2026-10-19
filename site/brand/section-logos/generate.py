import base64
exec(open('/workspace/section-logos/round3.py').read().split("os.makedirs('r3'")[0])
D='/workspace/lw/site/brand/section-logos/'
b64=base64.b64encode(open(D+'impact-sign.png','rb').read()).decode()
IMG=f'<image href="data:image/png;base64,{b64}" x="0" y="0" width="120" height="120" style="image-rendering:auto"/>'
sets={'why':('چرا آبادیس','Why Abadis',O['W2']),'calculator':('محاسبه گر','Calculator',O['C']),
'sustainable':('توسعه پایدار','Sustainable Development',O['S1']),'zagros':('نجات زاگرس','Save Zagros',O['Z1']),'impact':('اثرگذاری','Impact',IMG)}
def dark(k,v):
    if k in('sustainable','impact'): return v
    return v.replace(f'stroke="{T}" stroke-width="2.2"',f'stroke="{A}" stroke-width="2.2"').replace(T,'#e6f3f3')
import glob,os
for f in glob.glob(D+'*.svg'): os.remove(f)
for k,(fa,en,v) in sets.items():
    for m,vv,tc,ec in [('',v,T,'#5a7578'),('-dark',dark(k,v),'#ffffff','#9dbdbf')]:
        open(D+f'{k}-icon{m}.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="240" height="240">{vv}</svg>')
        _,w1=text(fa,'r',46,0,0); _,w2=text(en.upper(),'r',15,0,0,anchor='start',ls=2.5)
        W=max(w1,w2)+150; tx=W-138
        p1,_=text(fa,'r',46,tx,74); p2,_=text(en.upper(),'r',15,tx-w2,104,anchor='start',ls=2.5)
        open(D+f'{k}-lockup{m}.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} 130" width="{W*2:.0f}" height="260"><g transform="translate({W-125:.1f} 5)">{vv}</g><path d="{p1}" fill="{tc}"/><path d="{p2}" fill="{ec}"/></svg>')
mk=lambda m:''.join(f'<figure><img src="{k}-lockup{m}.svg"><img class="i" src="{k}-icon{m}.svg"></figure>' for k in sets)
note='''<p class="n">توسعه پایدار: چرخ رنگی اهداف توسعه پایدار سازمان ملل فقط به‌صورت بدون تغییر و برای اطلاع‌رسانی استفاده شود، همراه با جمله «آبادیس از اهداف توسعه پایدار حمایت می‌کند». ادغام آن با لوگوی آبادیس مجاز نیست.</p><p class="n" dir="ltr" style="text-align:left">SDG colour wheel: use unaltered, informational only, with “Abadis Med supports the Sustainable Development Goals”; must not be merged into our logo or imply UN endorsement; link the <a href="https://www.un.org/sustainabledevelopment/news/communications-material/">UN SDG guidelines</a> on any web page that shows it.</span> · Impact sign: original Abadis artwork, unmodified (impact-sign.png / impact-sign-full.webp).</p>'''
open(D+'index.html','w').write('''<!doctype html><html lang="fa" dir="rtl"><meta charset="utf-8"><title>Abadis Med – Section Logos</title><style>body{margin:0;font-family:Tahoma,sans-serif}section{display:grid;grid-template-columns:repeat(auto-fill,minmax(420px,1fr));gap:24px;padding:32px}.l{background:#f4f8f8}.d{background:#071d20}figure{margin:0;display:flex;align-items:center;gap:20px;justify-content:space-between}figure img{height:96px}figure img.i{height:72px}.n{margin:0;padding:16px 32px;font-size:13px;line-height:1.8;color:#5a7578;background:#fff}.f{background:#fff;padding:16px 32px}</style>
<section class="l">'''+mk('')+'</section><section class="d">'+mk('-dark')+'</section><div class="f"><img src="impact-sign-full.webp" height="100"></div>'+note+'</html>')
