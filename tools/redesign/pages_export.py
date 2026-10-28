"""Export page + export quote request form (fa /export/, en /en/export/, ar /arabic/export/).
Complete, placeholder-free B2B export hub (Navid Item 3)."""
from lib import esc
from layout import page, crumbs
from pages_company import about_motion_tags, _SVG_PHONE_HERO, _SVG_WA_HERO

EMAIL = 'info@abadis-med.com'
TEL = '+982192001017'
WA = 'https://wa.me/989100145809'
CATALOGUE_FA = 'https://abadis-med.com/wp-content/uploads/2024/12/کاتالوگ-جامع-آبادیس.pdf'

EXPORT_SLOGANS = {
    'fa': [
        'صادرات محصولات دانش‌بنیان آبادیس به بازارهای منطقه‌ای و جهانی،',
        'دارای گواهینامه‌های بین‌المللی CE اروپا، ISO 13485:2016 و IMED',
        'حضور فعال در بازارهای عراق، عمان، ازبکستان و آسیای میانه',
        'ظرفیت تولید سالانه ۵ میلیون کیسه ساکشن با استاندارد صادراتی.',
    ],
    'en': [
        'Exporting Abadis knowledge-based medical devices to global markets,',
        'Certified under European CE, ISO 13485:2016, and IMED standards',
        'Active regional presence in Iraq, Oman, Uzbekistan & Central Asia',
        'Annual production capacity of 5 million disposable suction bags.',
    ],
    'ar': [
        'تصدير منتجات آباديس المعرفية إلى الأسواق الإقليمية والعالمية،',
        'حاصلة على شهادات CE الأوروبية وISO 13485:2016 وIMED',
        'حضور نشط في أسواق العراق وعُمان وأوزبكستان وآسيا الوسطى',
        'طاقة إنتاجية سنوية تبلغ ٥ ملايين كيس شفط بمعايير تصديرية.',
    ],
}

T = {
  'fa': dict(
    root='', title='صادرات و همکاری بین‌المللی', crumb='صادرات',
    h1='صادرات و <em>همکاری بین‌المللی</em>',
    lead='تأمین مستقیم کیسه‌ها و مخازن ساکشن مدار بسته، فیلترهای هیدروفوبیک و آنتی‌باکتریال (۹۹.۹۹۹٪) و ملزومات مراقبت راه هوایی برای بیمارستان‌ها و توزیع‌کنندگان بین‌المللی.',
    markets_h='بازارهای صادراتی و اتاق‌های بازرگانی مشترک',
    markets=[
        ('عراق (Iraq)', 'تأمین مستقیم مراکز درمانی و بیمارستان‌ها؛ عضو اتاق مشترک بازرگانی ایران و عراق'),
        ('عمان (Oman)', 'مذاکرات رسمی در مسقط و همکاری با توزیع‌کنندگان تجهیزات پزشکی؛ عضو اتاق مشترک ایران و عمان'),
        ('ازبکستان و آسیای میانه', 'حضور در نمایشگاه بین‌المللی UzMedExpo تاشکند و تجهیز مراکز درمانی منطقه'),
        ('روسیه و سوئیس', 'عضویت فعال در اتاق‌های مشترک بازرگانی ایران-روسیه، ایران-سوئیس و اتحادیه صادرکنندگان (ISOMEE)'),
    ],
    facts_h='مشخصات تجاری و لجستیک صادراتی',
    rows=[
        ('ظرفیت تولید سالانه', '۵٬۰۰۰٬۰۰۰ عدد کیسه ساکشن یکبارمصرف و ۱٬۲۰۰٬۰۰۰ قطعه مخزن و تجهیزات جانبی'),
        ('استانداردها و گواهینامه‌ها', 'گواهی CE اتحادیه اروپا · ISO 13485:2016 · پروانه ساخت و صادرات IMED · ثبت اختراع'),
        ('بسته‌بندی صادراتی (Master Carton)', 'کیسه‌های ۱، ۲ و ۳ لیتری: ۴۵ عدد در هر کارتن (مدل فیلتر مکانیکی: ۳۰ عدد در کارتن) · ساکشن تیوب: ۱۰۰ عدد در کارتن'),
        ('ابعاد کارتن صادراتی', 'کیسه ۱ و ۲ لیتری: ۵۷٫۵ × ۴۲٫۵ × ۴۴ سانتی‌متر · کیسه ۳ لیتری: ۴۹ × ۴۹ × ۴۹ سانتی‌متر · تیوب: ۵۹ × ۴۴٫۵ × ۴۳٫۵ سانتی‌متر'),
        ('ظرفیت بارگیری کانتینر و کامیون', 'کامیون / کانتینر استاندارد: ۳۶۰ کارتن (۱۶٬۲۰۰ عدد کیسه ۱ یا ۲ لیتری) · خاور: ۱۸۰ کارتن (۸٬۱۰۰ عدد)'),
        ('شرایط تحویل و اینکوترمز (Incoterms)', 'EXW، FCA، FOB، CPT و CIF متناسب با کشور مقصد و توافق قرارداد بازرگانی'),
        ('مستندات فنی و رگولاتوری', 'کاتالوگ جامع فنی، برگه اطلاعات ایمنی، گواهی آنالیز (CoA) و دفترچه راهنمای کاربری (IFU) به زبان‌های فارسی، انگلیسی و عربی'),
    ],
    contact_h='ارتباط مستقیم با واحد صادرات و بازرگانی خارجی',
    contact_note='برای دریافت لیست قیمت صادراتی (FOB/EXW)، نمونه محصول و شرایط نمایندگی انحصاری در کشور مقصد با واحد بازرگانی تماس بگیرید.',
    form_h='فرم درخواست پیش‌فاکتور و همکاری صادراتی', subject='درخواست همکاری صادراتی آبادیس',
    f=[('name','نام و نام خانوادگی','text',True),('company','نام شرکت / مرکز درمانی','text',True),('country','کشور مقصد','text',True),
       ('email','پست الکترونیک رسمی','email',True),('phone','تلفن / واتس‌اپ (با کد کشور)','tel',False),('product','محصول یا گروه کالایی','select',True),
       ('qty','تیراژ درخواستی (کارتن / کانتینر)','text',False),('msg','توضیحات (اینکوترمز مورد نظر، بندر مقصد و...)','textarea',False)],
    products=['کیسه ساکشن ۱ لیتری','کیسه ساکشن ۲ لیتری','کیسه ساکشن ۳ لیتری','پکیج کامل سیستم ساکشن (کیسه + مخزن + پایه)','فیلترهای هیدروفوبیک و آنتی‌باکتریال (۹۹.۹۹۹٪)','ساکشن تیوب (CH25 / CH30 / CH35)','محصولات مراقبت راه هوایی (مسواک ساکشن و فیکسر)','نمایندگی توزیع سبد کامل محصولات'],
    send='ثبت و ارسال درخواست صادراتی', note='با ارسال فرم، خلاصه درخواست شما مستقیماً برای واحد بازرگانی خارجی آماده ارسال می‌شود.', done='در صورت عدم باز شدن خودکار ایمیل، مستقیم به این آدرس پیام دهید: ',
    dl='دانلود کاتالوگ جامع (PDF)', dl_href='downloads/'),
  'en': dict(
    root='en/', title='Export & International Partnership', crumb='Export',
    h1='Export & <em>International Partnership</em>',
    lead='Direct manufacturer supply of closed-system disposable suction liner bags, 99.999% hydrophobic & antibacterial filters, polycarbonate canisters, and airway care devices for international distributors and healthcare ministries.',
    markets_h='Active Export Markets & Joint Chambers of Commerce',
    markets=[
        ('Iraq', 'Direct hospital supply and distributor partnerships; member of the Iran–Iraq Joint Chamber of Commerce'),
        ('Oman & GCC', 'Official B2B trade delegations in Muscat; member of the Iran–Oman Joint Chamber of Commerce'),
        ('Uzbekistan & Central Asia', 'Exhibited at UzMedExpo Tashkent with active clinical installations in regional medical centers'),
        ('Russia & Switzerland', 'Member of the Iran–Russia & Iran–Switzerland Chambers of Commerce and the Iranian Medical Equipment Exporters Union (ISOMEE)'),
    ],
    facts_h='Commercial & Export Logistics Specifications',
    rows=[
        ('Annual Production Capacity', '5,000,000 disposable suction liner bags & 1,200,000 canisters and accessories per year'),
        ('Certifications & Compliance', 'European CE Marking · ISO 13485:2016 Quality Management · IMED Manufacturing & Export License · Registered Patents'),
        ('Export Master Carton Packing', '1 L, 2 L & 3 L Suction Liners: 45 pcs/carton (Mechanical Filter model: 30 pcs/carton) · Suction Tubes: 100 pcs/carton'),
        ('Master Carton Dimensions', '1 L & 2 L Liners: 57.5 × 42.5 × 44 cm · 3 L Liners: 49 × 49 × 49 cm · Suction Tube: 59 × 44.5 × 43.5 cm'),
        ('Container & Truck Load Capacity', 'Standard Truck / Container: 360 cartons (16,200 pcs of 1 L / 2 L liners) · Medium Truck: 180 cartons (8,100 pcs)'),
        ('Delivery Terms (Incoterms)', 'EXW, FCA, FOB, CPT, and CIF available according to destination port and distributor agreement'),
        ('Regulatory & Technical Dossier', 'Full Technical Catalogue, Certificate of Analysis (CoA), ISO/CE certificates, and multilingual IFU (EN / AR / FA)'),
    ],
    contact_h='Direct Export & International Trade Desk',
    contact_note='Contact our International Commercial Department for FOB/EXW price lists, evaluation samples, and regional distribution agreements.',
    form_h='Request an Export Quote / Distribution Partnership', subject='Abadis Export Quote Request',
    f=[('name','Full name','text',True),('company','Company / Healthcare Organization','text',True),('country','Destination Country','text',True),
       ('email','Business Email','email',True),('phone','Phone / WhatsApp (with country code)','tel',False),('product','Product Category','select',True),
       ('qty','Estimated Quantity (cartons / containers)','text',False),('msg','Message (Preferred Incoterms, destination port, etc.)','textarea',False)],
    products=['Disposable Suction Bag 1 L','Disposable Suction Bag 2 L','Disposable Suction Bag 3 L','Complete Suction System (Bags + Canisters + Stands)','Hydrophobic & Antibacterial Filters (99.999%)','Medical Suction Tubes (CH25 / CH30 / CH35)','Airway Care Range (Suction Toothbrush & Tube Fixer)','Full Portfolio Regional Distribution'],
    send='Submit Export Inquiry', note='Submitting opens your email client with the formatted inquiry addressed to our Export Desk.', done='If your email app did not open automatically, email us at: ',
    dl='Download Full Catalogue (PDF)', dl_href='en/center-download/'),
  'ar': dict(
    root='arabic/', title='التصدير والتعاون الدولي', crumb='التصدير',
    h1='التصدير و<em>التعاون الدولي</em>',
    lead='توريد مباشر من المصنع لأكياس وخزانات الشفط المغلقة ذات الاستخدام الواحد، وفلاتر قطع التدفق والمضادة للبكتيريا (٩٩٫٩٩٩٪)، ومستلزمات العناية بالطريق الهوائي للمستشفيات والموزعين الدوليين.',
    markets_h='الأسواق التصديرية والغرف التجارية المشتركة',
    markets=[
        ('العراق', 'توريد مباشر للمراكز العلاجية والمستشفيات؛ عضو غرفة التجارة المشتركة الإيرانية العراقية'),
        ('سلطنة عُمان والخليج', 'مباحثات تجارية رسمية في مسقط وتعاون مع موزعي المعدات الطبية؛ عضو الغرفة المشتركة الإيرانية العُمانية'),
        ('أوزبكستان وآسيا الوسطى', 'مشاركة فعالة في معرض UzMedExpo طشقند وتجهيز المراكز الطبية الإقليمية'),
        ('روسيا وسويسرا', 'عضوية فعالة في غرف التجارة المشتركة واتحاد مصدري المعدات الطبية (ISOMEE)'),
    ],
    facts_h='المواصفات التجارية واللوجستية للتصدير',
    rows=[
        ('الطاقة الإنتاجية السنوية', '٥٬٠٠٠٬٠٠٠ كيس شفط ذو استخدام واحد و١٬٢٠٠٬٠٠٠ خزان وملحق سنوياً'),
        ('الشهادات والمعايير الدولية', 'شهادة CE الأوروبية · ISO 13485:2016 · ترخيص التصنيع والتصدير IMED · براءات اختراع مسجلة'),
        ('التعبئة القياسية للتصدير', 'أكياس الشفط ١ و٢ و٣ لتر: ٤٥ قطعة في الكرتون (موديل الفلتر الميكانيكي: ٣٠ قطعة) · أنبوب الشفط: ١٠٠ قطعة في الكرتون'),
        ('أبعاد كرتون التصدير', 'أكياس ١ و٢ لتر: ٥٧٫٥ × ٤٢٫٥ × ٤٤ سم · أكياس ٣ لتر: ٤٩ × ٤٩ × ٤٩ سم · أنبوب الشفط: ٥٩ × ٤٤٫٥ × ٤٣٫٥ سم'),
        ('سعة الشحن والحاويات', 'شاحنة قياسية / حاوية: ٣٦٠ كرتوناً (١٦٬٢٠٠ كيس ١ أو ٢ لتر) · شاحنة متوسطة: ١٨٠ كرتوناً (٨٬١٠٠ كيس)'),
        ('شروط التسليم الدولية (Incoterms)', 'EXW وFCA وFOB وCPT وCIF حسب ميناء الوصول والاتفاق التجاري'),
        ('الملف الفني والتنظيمي', 'الكتالوج الفني الشامل، شهادة التحليل (CoA)، شهادات ISO/CE، وتعليمات الاستخدام (IFU) بالعربية والإنجليزية والفارسية'),
    ],
    contact_h='التواصل المباشر مع قسم التصدير والتجارة الخارجية',
    contact_note='للحصول على قائمة أسعار التصدير (FOB/EXW) وعينات التقييم وشروط الوكالة الإقليمية، تواصلوا مع قسم التجارة الدولية.',
    form_h='نموذج طلب عرض سعر / تعاون تصديري', subject='طلب عرض سعر تصديري — آباديس',
    f=[('name','الاسم الكامل','text',True),('company','اسم الشركة / المؤسسة الصحية','text',True),('country','الدولة','text',True),
       ('email','البريد الإلكتروني الرسمي','email',True),('phone','الهاتف / واتساب (مع رمز الدولة)','tel',False),('product','المنتج أو الفئة','select',True),
       ('qty','الكمية التقريبية (كرتون / حاوية)','text',False),('msg','ملاحظات (شروط التسليم Incoterms والميناء)','textarea',False)],
    products=['كيس الشفط ١ لتر','كيس الشفط ٢ لتر','كيس الشفط ٣ لتر','نظام الشفط المتكامل (أكياس + خزانات + حوامل)','فلاتر كارهة للماء ومضادة للبكتيريا (٩٩٫٩٩٩٪)','أنبوب الشفط الطبي (CH25 / CH30 / CH35)','منتجات العناية بالطريق الهوائي','وكالة توزيع شاملة للمنتجات'],
    send='إرسال طلب التصدير', note='عند الإرسال يُفتح تطبيق البريد مع تفاصيل طلبكم لقسم التصدير.', done='إذا لم يُفتح تطبيق البريد تلقائياً، راسلونا عبر: ',
    dl='تحميل الكتالوج الشامل (PDF)', dl_href='arabic/مركز-التنزيل/'),
}


def _slogan_block(lang):
    lines = EXPORT_SLOGANS[lang]
    spans = ''.join(f'<span class="slogan-line" style="--i:{n}">{esc(x)}</span>' for n, x in enumerate(lines))
    return f'<p class="slogan reveal" aria-label="{esc(" ".join(lines))}">{spans}</p>'


def form_html(L, lang):
    fields = []
    for n, lab, typ, req in L['f']:
        fid = f'qf-{lang}-{n}'
        star = ' <span aria-hidden="true">*</span>' if req else ''
        r = ' required' if req else ''
        if typ == 'select':
            opts = ''.join(f'<option>{esc(o)}</option>' for o in L['products'])
            ctl = f'<select id="{fid}" name="{n}"{r}><option value=""></option>{opts}</select>'
        elif typ == 'textarea':
            ctl = f'<textarea id="{fid}" name="{n}" rows="4"></textarea>'
        else:
            ac = {'name': 'name', 'company': 'organization', 'country': 'country-name', 'email': 'email', 'phone': 'tel'}.get(n, 'off')
            ctl = f'<input id="{fid}" name="{n}" type="{typ}" autocomplete="{ac}"{r}>'
        wide = ' qf-wide' if typ == 'textarea' else ''
        fields.append(f'<div class="qf-field{wide}"><label for="{fid}">{esc(lab)}{star}</label>{ctl}</div>')
    return f'''<form class="quote-form card" id="quote" data-quote-form data-to="{EMAIL}" data-subject="{esc(L['subject'])}" action="mailto:{EMAIL}" method="post" enctype="text/plain">
      <h2>{esc(L['form_h'])}</h2>
      <div class="qf-grid">{''.join(fields)}</div>
      <p class="qf-note">{esc(L['note'])}</p>
      <button class="btn btn-primary" type="submit">{esc(L['send'])}</button>
      <p class="qf-done" hidden role="status">{esc(L['done'])}<a href="mailto:{EMAIL}">{EMAIL}</a></p>
    </form>'''


def build(write):
    for lang, L in T.items():
        rel = L['root'] + 'export/index.html'
        p = '../' * (rel.count('/'))
        cr = crumbs(p, [(L['crumb'], None)], lang=lang)
        hero = (
            f'  <section class="page-hero about-hero solutions-hero has-playing-video">\n'
            f'    <video class="about-hero-video solutions-hero-video is-playing" autoplay muted loop playsinline webkit-playsinline disablepictureinpicture disableremoteplayback preload="metadata" tabindex="-1" aria-hidden="true" poster="{p}assets/media/hero-customers-poster.jpg?v=20261028p">\n'
            f'      <source src="{p}assets/media/hero-customers.mp4?v=20261028p" type="video/mp4">\n'
            f'    </video>\n'
            f'    <div class="wrap about-hero-grid">\n'
            f'      <div>\n'
            f'        {cr}\n'
            f'        <h1>{L["h1"]}</h1>\n'
            f'        {_slogan_block(lang)}\n'
            f'        <p class="sol-hero-lead">{esc(L["lead"])}</p>\n'
            f'        <div class="contact-hero-ctas" style="margin-top:18px">\n'
            f'          <a class="ch-btn-call" href="#quote">{_SVG_PHONE_HERO}<span>{esc(L["form_h"])}</span></a>\n'
            f'          <a class="ch-btn-wa" href="{WA}" target="_blank" rel="noopener">{_SVG_WA_HERO}<span>WhatsApp: +98 910 014 5809</span></a>\n'
            f'        </div>\n'
            f'      </div>\n'
            f'    </div>\n'
            f'  </section>'
        )
        m_cards = ''.join(
            f'<article class="card" style="padding:18px;border-radius:18px">'
            f'<strong style="display:block;font-size:1.02rem;font-weight:900;color:var(--brand,#05686b);margin-bottom:6px">{esc(mt)}</strong>'
            f'<p style="margin:0;font-size:.88rem;line-height:1.65;color:var(--ink-2)">{esc(md)}</p></article>'
            for mt, md in L['markets']
        )
        rows = ''.join(
            f'<tr><th scope="row">{esc(k)}</th><td>{esc(v)}</td></tr>'
            for k, v in L['rows']
        )
        main = f'''{hero}
  <section class="section section--alt" id="export-markets"><div class="wrap">
    <h2 style="margin:0 0 16px;font-size:1.4rem">{esc(L['markets_h'])}</h2>
    <div class="grid g-2" style="gap:16px">{m_cards}</div>
  </div></section>
  <section class="section"><div class="wrap export-grid">
    <div class="reveal">
      <h2>{esc(L['facts_h'])}</h2>
      <table class="spec-table export-facts"><tbody>{rows}</tbody></table>
      <p style="margin-top:16px"><a class="btn btn-primary" href="{CATALOGUE_FA}" target="_blank" rel="noopener">{esc(L['dl'])}</a> <a class="btn btn-ghost" href="{p}{L['dl_href']}" style="margin-inline-start:8px">{esc(L['dl'])}</a></p>
      <h2 style="margin-top:28px">{esc(L['contact_h'])}</h2>
      <p style="margin:0 0 12px;color:var(--muted)">{esc(L['contact_note'])}</p>
      <div class="cta-actions export-contact">
        <a class="btn btn-ghost" href="mailto:{EMAIL}" dir="ltr">{EMAIL}</a>
        <a class="btn btn-ghost" href="tel:{TEL}" dir="ltr">+98 21 9200 1017</a>
        <a class="btn btn-ghost" href="{WA}" target="_blank" rel="noopener">WhatsApp</a>
      </div>
    </div>
    <div class="reveal">{form_html(L, lang)}</div>
  </div></section>'''
        h_css, m_js = about_motion_tags(p)
        html = page(p, 'export', L['title'], L['lead'], main, lang=lang,
                    fa_path='export/', canonical_path=L['root'] + 'export/',
                    extra_head=h_css, html_attrs='data-slogan="t1"',
                    scripts=m_js + f'<script src="{p}assets/js/quote-form.js" defer></script>\n')
        write(rel, html)
