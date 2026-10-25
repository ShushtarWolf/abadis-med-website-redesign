"""EN / AR home in the same Alireza order (1-10) as the FA home, with live abadis-med.com/en + /arabic text (re-read 2026-10-15)."""
from lib import esc, load, SITE
from layout import page, section_mark
from render import picture
import pages_home as H

AR_D = str.maketrans('0123456789', '٠١٢٣٤٥٦٧٨٩')

T = {
 'en': dict(
  root='en/', title='About us',
  desc='Abadis Med, a knowledge-based company: disposable suction liner bags and solutions for managing hospital fluid and infectious waste.',
  kicker='Abadis Med · a knowledge-based group', h1='About us',
  sub='Finally, after years of planning, dynamics and changes in the management system, in 2017, we established the Makhazen Tebi Abadis Company to start the production of Abadis disposable suction liner bags and to achieve our goals in the field of hospital infection control and medical equipment.',
  cat='Download catalogue', quote='Request a quote / export cooperation', quote_href='export/#quote',
  bag_alt='Abadis 1 L and 2 L disposable suction liner bags',
  about_eb='About us', about_h='Find out more on Abadis Med; a knowledge-based group',
  about='Abadis Med, a knowledge-based company, leverages cutting-edge technology and innovative solutions for managing hospital fluid waste and infectious waste. With a strong commitment to infection control and sustainable development, we strive to make a real impact on healthcare facilities and environmental protection.',
  goals_h='Our Goals', goals=['Optimized Management of Infectious and Hospital Liquid Waste', 'Reducing and Controlling Infections Caused by Hospital Waste and Fluids', 'Promoting Awareness and Maximizing the Use of Our Solutions in Hospitals and Healthcare Centers'],
  more='Read more →', about_href='about-us/', video_alt='Abadis Med knowledge-based factory', video_cap='Placeholder for the Abadis introduction video (video file pending)',
  slogan=['We affect as much as a fingertip', 'To You', 'To Nature', 'To World'],
  imp_eb='Abadis impact, right now', imp_unit='litres of water saved since 21 March 2026 (estimate)',
  why_eb='Why Abadis?', why_h='The added value obtained from the production of disposable suction liner bags',
  values=[('Cost Reduction', 'Reduce costs related to cleanser, water consumption, electricity and manpower'), ('Hospital and Infectious Waste Management', 'Better collection of liquid and infectious waste'), ('Recycling', 'Reduces medical waste and preserves the environment'), ('Easy To Use', 'Eliminating activities related to tank cleaning and convenient use for collecting waste during surgery')],
  factory='Established in 2018, the Abadis Medical Equipment Knowledge-Based Factory operates with state-of-the-art machinery and highly skilled experts. With an annual production capacity of 5 million disposable suction bags, Abadis is recognized as the largest manufacturer of these products in the Middle East.',
  checks=['Product Warranty and Guarantee', 'Quality Assurance', 'Provide high quality products', 'Communication of Sales and Technical Team with Medical Centers and Hospital', 'Delivery Products in the Shortest Time'],
  prod_eb='Products', prod_h='Abadis products', prod_all='All products →', prod_href='products/',
  products=[('Suction Bag', 'products/suction-bag/', 'assets/img/p/p2-main.webp'), ('Base and Holder', 'products/base-and-holder/', 'assets/img/p/p1-g3-t.webp'), ('Filters', 'products/filters/', 'assets/img/filters/anti-1-t.webp'), ('Suction Tube', 'suction-tube/', 'assets/img/p/p1-g4-t.webp'), ('Canisters', 'products/canisters/', None), ('Connections', 'products/connections/', None), ('Other Products', 'products/other-products/', None)],
  calc='Savings calculator', calc_href='calculator/', zag='Save Zagros', zag_href='~csr/',
  news_eb='News', news_h='The Latest News Company', news_href='latest-news/', view='View all →', read='View news',
  art_eb='Articles', art_h='The Latest Blogs', art_href='blog/', art_read='Find out more',
  mem_eb='Memberships', mem_h='Memberships', mem_alt='Abadis membership',
  cust_eb='Customers', cust_h='Customers', cust_btn='See the customer list', cust_href='our-customers/', prev='Previous', next='Next', cust_aria='Sample customers'),
 'ar': dict(
  root='arabic/', title='اعرف المزيد عنا',
  desc='شركة مخازن طبية آباديس المعرفية: أكياس الشفط ذات الاستعمال الواحد وحلول إدارة السوائل والنفايات المعدية في المستشفيات.',
  kicker='شركة مخازن طبية آباديس المعرفية', h1='اعرف المزيد عنا',
  sub='بعد سنوات من التخطيط واستمرار الحركة التي تم انطلاقها، ومع العمل بالنشاط وإجراء التغييرات في نظام الإدارة، أنشأنا شركة آباديس القائمة على المعرفة في عام 2017، لكي نبدأ بإنتاج أكياس شفط آباديس ذات الاستعمال الواحد، وأيضاً نخطو خطوات أكبر في تحقيق أهدافنا التي تتمثل في مكافحة عدوى المستشفيات والمعدات الطبية؛ فأدركنا بأننا مستعدون لإحداث التأثير، التأثير في مكافحة عدوى المستشفيات.',
  cat='تحميل الكتالوج', quote='طلب سعر / تعاون تصديري', quote_href='export/#quote',
  bag_alt='أكياس الشفط آباديس ذات الاستعمال الواحد ١ و٢ لتر',
  about_eb='من نحن', about_h='اعرف أكثر عن مجموعة آباديس المعرفية',
  about='شركة مخازن طبية آباديس المعرفية تعتمد على المعرفة الحديثة وتقديم منتجات وحلول مبتكرة في إدارة السوائل والنفايات العفنية في المستشفيات، وقد اتخذت خطوات فعّالة في السيطرة على العدوى المستشفوية وتحقيق التنمية المستدامة. هدفنا هو تحقيق تأثير حقيقي في تحسين صحة المراكز الصحية وحماية البيئة.',
  goals_h='أهدافنا', goals=['إدارة مثلى للنفايات العفنية والسوائل المستشفوية', 'تقليل والسيطرة على العدوى الناتجة عن النفايات والسوائل المستشفوية', 'نشر ثقافة الاستخدام الأمثل لحلولنا ومنتجاتنا في المراكز الصحية والمستشفيات'],
  more='اقرأ أكثر ←', about_href='من-نحن/', video_alt='مصنع آباديس المعرفي', video_cap='مكان فيديو التعريف بآباديس (ملف الفيديو قيد الانتظار)',
  slogan=['نحن نؤثر بقدر طرف إصبع', 'عليك', 'على الطبيعة', 'على العالم'],
  imp_eb='أثر آباديس، الآن', imp_unit='لتر من الماء تم توفيره منذ ٢١ مارس ٢٠٢٦ (تقديري)',
  why_eb='لماذا آباديس؟', why_h='القيم المضافة لأكياس الشفط ذات الاستعمال الواحد',
  values=[('تقليص التكاليف', 'تقليص التكاليف المتعلقة بالمنظّفات واستهلاك المياه والكهرباء واستخدام الموارد البشرية'), ('إدارة مخلفات المستشفيات والنفايات المعدية', 'تؤدي إلى تجميع النفايات السائلة والمعدية بشكل أفضل'), ('قابلة لإعادة التدوير', 'تؤدي إلى تقليل كميّة مخلفات المستشفيات والحفاظ على البيئة'), ('الاستخدام البسيط', 'التخلص من عملية غسيل الخزانات والاستخدام المريح لتجميع النفايات أثناء العمل')],
  factory='تأسست شركة مخازن طبية آباديس المعرفية في عام 2018 باستخدام أحدث المعدات والآلات وبالتعاون مع القوى المتخصصة. تُعدّ هذه الشركة أكبر منتج للحقائب السائلة ذات الاستخدام الواحد في منطقة الشرق الأوسط، بطاقة إنتاجية سنوية تصل إلى 5 مليون حقيبة سحب.',
  checks=['الضمان والكفالة', 'ضمان الجودة', 'التواصل المستمر بين قسم المبيعات والفريق الفني مع المراكز الطبية', 'التوصيل السريع للمنتج'],
  prod_eb='منتجات', prod_h='منتجات آباديس', prod_all='كل المنتجات ←', prod_href='منتجات/',
  products=[('كيس الشفط', 'كيس-الشفط/', 'assets/img/p/p2-main.webp'), ('تثبيت', 'تثبیت/', 'assets/img/p/p1-g3-t.webp'), ('الفلتر', 'الفلتر/', 'assets/img/filters/anti-1-t.webp'), ('أنبوب الشفط', 'أنبوب-الشفط/', 'assets/img/p/p1-g4-t.webp'), ('خزانات', 'خزانات/', None), ('الوصلات', 'الوصلات/', None), ('منتجات أخرى', 'منتجات-اخری/', None)],
  calc='حاسبة التوفير', calc_href='الحوسبة/', zag='إنقاذ زاغروس', zag_href='~csr/',
  news_eb='الاخبار', news_h='أحدث أخبار الشركة', news_href='الاخبار/', view='عرض الكل ←', read='مشاهده خبر',
  art_eb='المقالات', art_h='المقالات', art_href='~articles/', art_read='',
  mem_eb='الأعضاء', mem_h='الأعضاء', mem_alt='عضوية آباديس',
  cust_eb='عملاؤنا', cust_h='عملاؤنا', cust_btn='قائمة العملاء', cust_href='customers/', prev='السابق', next='التالي', cust_aria='نماذج من العملاء'),
}


def _h(t, p, href):
    """Link relative to the language root, or to the site root with '~'."""
    return p + href[1:] if href.startswith('~') else p + t['root'] + href


def build_home(write, lang):
    t = T[lang]; p = '../'
    live = load('home_live_i18n.json')[lang]
    img = lambda n: f'{p}assets/img/live/{n}.webp'
    hero = f'''  <section class="hx" data-tone="dark" id="intro" aria-label="{esc(t['bag_alt'])}">
    <div class="hx-bg" aria-hidden="true"><span class="hx-grid"></span><span class="hx-ring hx-ring--a"></span><span class="hx-ring hx-ring--b"></span><span class="hx-scan"></span></div>
    <div class="wrap hx-inner">
      <div class="hx-copy">
        <p class="hx-kicker">{esc(t['kicker'])}</p>
        <h1>{esc(t['h1'])}</h1>
        <p class="hx-sub">{esc(t['sub'])}</p>
        <div class="hero-actions">
          <a class="btn btn-primary" href="{esc(H.CATALOGUE)}" target="_blank" rel="noopener" data-track="catalogue_download" data-track-label="home_hero_catalogue_{lang}">{esc(t['cat'])}</a>
          <a class="btn btn-ghost" href="{_h(t, p, t['quote_href'])}" data-track="contact_click" data-track-label="home_hero_quote_{lang}">{esc(t['quote'])}</a>
        </div>
      </div>
      <figure class="hx-product"><span class="hx-glow" aria-hidden="true"></span>
        <img src="{p}assets/img/p/hero-bags.webp" alt="{esc(t['bag_alt'])}" width="555" height="554" decoding="async" fetchpriority="high"></figure>
    </div>
  </section>'''
    goals = ''.join(f'<li>{esc(g)}</li>' for g in t['goals'])
    about = f'''  <section class="section" id="about"><div class="wrap split">
      <div class="reveal"><p class="eyebrow">{esc(t['about_eb'])}</p><h2>{esc(t['about_h'])}</h2>
        <p style="margin-top:12px;text-align:justify">{esc(t['about'])}</p>
        <h3 style="font-weight:900;font-size:1.1rem;margin-top:18px">{esc(t['goals_h'])}</h3><ul class="goals">{goals}</ul>
        <p style="margin-top:18px"><a class="more-link" href="{_h(t, p, t['about_href'])}">{esc(t['more'])}</a></p></div>
      <figure class="video-slot reveal" data-video-slot="home-about"><img src="{img('86201b7b17')}" alt="{esc(t['video_alt'])}" width="1024" height="576" loading="lazy" decoding="async"><figcaption>{esc(t['video_cap'])}</figcaption></figure>
    </div></section>'''
    lines = ''.join(f'<span class="slogan-line" style="--i:{i}">{esc(s)}</span>' for i, s in enumerate(t['slogan']))
    zero = '0' if lang == 'en' else '٠'
    impact = f'''  <section class="section deep impact" id="impact"><div class="wrap">
      <div class="impact-inner">
      <div class="impact-slogan reveal">{H.IMPACT_MARK}
        <p class="slogan" aria-label="{esc(' '.join(t['slogan']))}">{lines}</p></div>
      <div class="impact-counter reveal" data-impact-counter data-counter="m2" data-locale="{'en-US' if lang == 'en' else 'ar-EG'}">
        {section_mark(p, 'impact', 'sec-mark--lg')}
        <p class="eyebrow">{esc(t['imp_eb'])}</p><strong class="impact-num" aria-live="off">{zero}</strong>
        <span class="impact-unit">{esc(t['imp_unit'])}</span></div>
      </div>
      {H.impact_stats(lang)}
    </div></section>'''
    vals = ''.join(f'<div class="card value reveal"><h3>{esc(a)}</h3><p>{esc(b)}</p></div>' for a, b in t['values'])
    checks = ''.join(f'<li>{esc(c)}</li>' for c in t['checks'])
    why = f'''  <section class="section section--alt" id="why"><div class="wrap">
      <div class="section-head reveal has-mark">{section_mark(p, 'why')}<div><p class="eyebrow">{esc(t['why_eb'])}</p><h2>{esc(t['why_h'])}</h2></div></div>
      <div class="grid g-4 values">{vals}</div>
      <div class="split" style="margin-top:28px"><div class="reveal"><p>{esc(t['factory'])}</p></div><ul class="checks reveal">{checks}</ul></div>
    </div></section>'''
    import solutions_arch
    products = solutions_arch.home_section(p, lang)
    quick = f'''  <section class="section quick" id="quick" style="padding-block:28px"><div class="wrap quick-row">
      <a class="quick-btn" href="{_h(t, p, t['calc_href'])}">{section_mark(p, 'calculator', 'sec-mark--sm')}{esc(t['calc'])}</a>
      <a class="quick-btn" href="{_h(t, p, t['zag_href'])}">{section_mark(p, 'zagros', 'sec-mark--sm')}{esc(t['zag'])}</a>
    </div></section>'''
    def pc(x, label, tag):
        href = x['href'].split('abadis-med.com/', 1)[1]
        return (f'<a class="post-card reveal" href="{p}{esc(href)}"><div class="ph"><img src="{img(x["local"])}" alt="{esc(x["t"])}" loading="lazy" decoding="async"></div>'
                f'<div class="body"><span class="tag">{esc(tag)}</span><h3>{esc(x["t"])}</h3><span class="go">{esc(label)}</span></div></a>')
    import solutions_arch as S
    if lang == 'en':
        news_items, art_items = live[:6], live[6:]
        art_go = t['art_read']
    else:
        # No Arabic articles on the live site: the next live news items fill the articles tab.
        news_items, art_items = live[:3], live[3:]
        art_go = t['read']
    news_rail = S.carousel(''.join(pc(x, t['read'], t['news_eb']) for x in news_items), len(news_items), t['prev'], t['next'], t['news_eb'])
    art_rail = S.carousel(''.join(pc(x, art_go, t['art_eb']) for x in art_items), len(art_items), t['prev'], t['next'], t['art_eb'])
    box_h = 'Articles & News' if lang == 'en' else 'المقالات والأخبار'
    news_all = 'View all news →' if lang == 'en' else 'عرض كل الأخبار ←'
    art_all = 'View all articles →' if lang == 'en' else 'عرض كل المقالات ←'
    stories = f'''  <section class="section" id="stories"><div class="wrap">
      <div class="section-head reveal"><h2>{esc(box_h)}</h2></div>
      <div class="h-box ps-root" data-ps data-ps-home data-ps-default="news">
        <div class="ps-tabs" role="tablist" aria-orientation="horizontal" aria-label="{esc(box_h)}">
          <a role="tab" id="tab-home-news" href="#news" data-ps-tab="news" aria-selected="true" aria-controls="news">{esc(t['news_eb'])}</a>
          <a role="tab" id="tab-home-articles" href="#articles" data-ps-tab="articles" aria-selected="false" aria-controls="articles">{esc(t['art_eb'])}</a>
        </div>
        <div class="ps-panel is-default" id="news" role="tabpanel" aria-labelledby="tab-home-news" data-ps-panel="news">{news_rail}</div>
        <div class="ps-panel" id="articles" role="tabpanel" aria-labelledby="tab-home-articles" data-ps-panel="articles" hidden>{art_rail}</div>
        <p class="h-all">
          <a class="btn btn-ghost" href="{_h(t, p, t['news_href'])}">{esc(news_all)}</a>
          <a class="btn btn-ghost" href="{_h(t, p, t['art_href'])}">{esc(art_all)}</a>
        </p>
      </div>
    </div></section>'''
    logos = ''.join(f'<li><img src="{img(n)}" alt="{esc(t["mem_alt"])}" loading="lazy" decoding="async"></li>' for n in H.MEMBERSHIPS if (SITE / H._live(n)).exists())
    mem = f'''  <section class="section" id="memberships"><div class="wrap"><div class="section-head reveal"><p class="eyebrow">{esc(t['mem_eb'])}</p><h2>{esc(t['mem_h'])}</h2></div><ul class="member-logos reveal">{logos}</ul></div></section>'''
    bl = H._B('/مشتریان-ما/'); lg = []
    for it in bl[1]['items']:
        if len(lg) >= H.LOGO_STRIP_N: break
        im = next((x for x in it['blocks'] if x['t'] == 'img'), None); name = next((x['text'] for x in it['blocks'] if x['t'] == 'h'), '')
        pic = picture(p, im['src'], im.get('alt') or name, 300) if im else ''
        if pic: lg.append(f'<div class="home-logo" role="group" aria-label="{esc(name)}" title="{esc(name)}" lang="fa">{pic}</div>')
    cust = f'''  <section class="section" id="customers"><div class="wrap">
      <div class="section-head reveal"><p class="eyebrow">{esc(t['cust_eb'])}</p><h2>{esc(t['cust_h'])}</h2><p>{esc(H.customers_lead(lang))}</p></div>
      <div class="logo-carousel reveal" data-logo-carousel><button type="button" class="logo-carousel-btn logo-carousel-prev" aria-label="{esc(t['prev'])}">‹</button>
        <div class="logo-carousel-track" tabindex="0" aria-label="{esc(t['cust_aria'])}">{''.join(lg)}</div>
        <button type="button" class="logo-carousel-btn logo-carousel-next" aria-label="{esc(t['next'])}">›</button></div>
      <p class="home-logo-cta reveal"><a class="btn btn-ghost" href="{_h(t, p, t['cust_href'])}">{esc(t['cust_btn'])}</a></p>
    </div></section>'''
    main = '\n'.join([hero, about, impact, why, products, quick, stories, mem, cust])
    if lang == 'en': main = main.replace('←', '→')
    extra_head = f'<link rel="preload" as="image" href="{p}assets/img/p/hero-bags.webp" type="image/webp">\n<link rel="stylesheet" href="{p}assets/css/home.css">\n{H.logo_scroll_css(p)}\n{H.counter_options_css(p)}'
    html = page(p, None, t['title'], t['desc'], main, lang=lang, fa_path='', canonical_path=t['root'],
                extra_head=extra_head, scripts=H.logo_scroll_scripts(p) + H.counter_options_script(p), main_class='home-page', body_class='home', lightbox=True,
                html_attrs='data-slogan="t1"')
    write(t['root'] + 'index.html', html)
    return t['root'] + 'index.html'
