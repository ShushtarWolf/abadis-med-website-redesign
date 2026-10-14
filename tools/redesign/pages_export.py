"""Export page + export quote request form (fa /export/, en /en/export/, ar /arabic/export/).
Facts only from abadis-med.com / repo; unknown trade data is a visible placeholder (class .ph-data)."""
from lib import esc
from layout import page, page_hero

EMAIL = 'info@abadis-med.com'   # contact page (verbatim)
TEL = '+982192001017'
WA = 'https://wa.me/989100145809'

T = {
  'fa': dict(root='', title='صادرات و همکاری بین‌المللی', crumb='صادرات',
    lead='اطلاعات تجاری برای خریداران و توزیع‌کنندگان خارج از ایران و فرم درخواست قیمت.',
    facts_h='اطلاعات تجاری', ph='[در انتظار اطلاعات از شرکت]',
    rows=[('ظرفیت تولید', 'ظرفیت تولید سالانه ۵ میلیون کیسه ساکشن یکبارمصرف (سایت فعلی آبادیس)'), ('بسته‌بندی', 'در هر کارتن کیسه‌های ساکشن یکبار مصرف برای هر سه سایز معمولاً ۴۵ عدد است (فیلتر مکانیکی: ۳۰ عدد در کارتن). ابعاد کارتن ۱ و ۲ لیتری: ۵۷.۵ × ۴۲.۵ × ۴۴ cm؛ ۳ لیتری: ۴۹ × ۴۹ × ۴۹ cm.'),
          ('حداقل سفارش (MOQ)', None), ('زمان تحویل', None), ('شرایط تحویل (Incoterms)', None),
          ('گواهی‌ها', 'IMED، ISO، CE'), ('مستندات', 'کاتالوگ‌ها در مرکز دانلود؛ IFU انگلیسی و عربی: [در انتظار فایل از شرکت]')],
    contact_h='تماس با واحد صادرات', contact_note='ایمیل و تلفن عمومی شرکت؛ ایمیل/مسئول اختصاصی صادرات: [در انتظار اطلاعات از شرکت]',
    form_h='درخواست قیمت / همکاری صادراتی', subject='درخواست قیمت صادراتی',
    f=[('name','نام و نام خانوادگی','text',True),('company','شرکت / مرکز','text',True),('country','کشور','text',True),
       ('email','ایمیل','email',True),('phone','تلفن / واتس‌اپ','tel',False),('product','محصول','select',True),
       ('qty','تعداد تقریبی (عدد یا کارتن)','text',False),('msg','توضیحات','textarea',False)],
    products=['کیسه ساکشن ۱ لیتری','کیسه ساکشن ۲ لیتری','کیسه ساکشن ۳ لیتری','فیلترها','مخزن','پایه و نگهدارنده','اتصالات','ساکشن تیوب','سایر محصولات'],
    send='ارسال درخواست', note='با ارسال، برنامهٔ ایمیل شما با متن آماده باز می‌شود.', done='اگر برنامهٔ ایمیل باز نشد، مستقیم به این آدرس بنویسید: ',
    dl='مرکز دانلود', dl_href='downloads/'),
  'en': dict(root='en/', title='Export & International Partnership', crumb='Export',
    lead='Trade information for buyers and distributors outside Iran, and a quote request form.',
    facts_h='Trade information', ph='[Pending data from the company]',
    rows=[('Production capacity', 'Annual capacity of 5 million disposable suction bags (per abadis-med.com)'), ('Packaging', 'Disposable suction bags are usually packed 45 per carton for all three sizes (mechanical filter: 30 per carton). Carton size, 1 L and 2 L: 57.5 × 42.5 × 44 cm; 3 L: 49 × 49 × 49 cm.'),
          ('Minimum order (MOQ)', None), ('Delivery time', None), ('Delivery terms (Incoterms)', None),
          ('Certificates', 'IMED, ISO, CE'), ('Documents', 'Catalogues in the Download Center; English/Arabic IFU: [Pending file from the company]')],
    contact_h='Export contact', contact_note='General company email and phone; dedicated export contact: [Pending data from the company]',
    form_h='Request a quote / export partnership', subject='Export quote request',
    f=[('name','Full name','text',True),('company','Company / facility','text',True),('country','Country','text',True),
       ('email','Email','email',True),('phone','Phone / WhatsApp','tel',False),('product','Product','select',True),
       ('qty','Approx. quantity (pcs or cartons)','text',False),('msg','Message','textarea',False)],
    products=['Suction bag 1 L','Suction bag 2 L','Suction bag 3 L','Filters','Canisters','Base & holder','Connections','Suction tube','Other products'],
    send='Send request', note='Sending opens your email app with the message ready.', done='If your email app did not open, write to: ',
    dl='Download Center', dl_href='en/center-download/'),
  'ar': dict(root='arabic/', title='التصدير والتعاون الدولي', crumb='التصدير',
    lead='معلومات تجارية للمشترين والموزعين خارج إيران، ونموذج طلب عرض سعر.',
    facts_h='المعلومات التجارية', ph='[بانتظار البيانات من الشركة]',
    rows=[('الطاقة الإنتاجية', 'طاقة إنتاجية سنوية تبلغ ٥ ملايين كيس شفط للاستخدام الواحد (وفق موقع آباديس)'), ('التغليف', 'تُعبّأ أكياس الشفط ذات الاستخدام الواحد عادةً ٤٥ قطعة في الكرتون لجميع المقاسات الثلاثة (الفلتر الميكانيكي: ٣٠ قطعة). أبعاد الكرتون لـ ١ و٢ لتر: ‎57.5 × 42.5 × 44 cm؛ ٣ لتر: ‎49 × 49 × 49 cm.'),
          ('الحد الأدنى للطلب (MOQ)', None), ('مدة التسليم', None), ('شروط التسليم (Incoterms)', None),
          ('الشهادات', 'IMED، ISO، CE'), ('المستندات', 'الكتالوجات في مركز التنزيل؛ تعليمات الاستخدام IFU بالإنجليزية والعربية: [بانتظار الملف من الشركة]')],
    contact_h='التواصل مع قسم التصدير', contact_note='البريد والهاتف العامّان للشركة؛ مسؤول التصدير المباشر: [بانتظار البيانات من الشركة]',
    form_h='طلب عرض سعر / تعاون تصديري', subject='Export quote request (AR)',
    f=[('name','الاسم الكامل','text',True),('company','الشركة / المركز','text',True),('country','الدولة','text',True),
       ('email','البريد الإلكتروني','email',True),('phone','الهاتف / واتساب','tel',False),('product','المنتج','select',True),
       ('qty','الكمية التقريبية (قطعة أو كرتون)','text',False),('msg','ملاحظات','textarea',False)],
    products=['كيس الشفط ١ لتر','كيس الشفط ٢ لتر','كيس الشفط ٣ لتر','الفلاتر','الخزانات','الحامل والقاعدة','الوصلات','أنبوب الشفط','منتجات أخرى'],
    send='إرسال الطلب', note='عند الإرسال يُفتح تطبيق البريد لديك مع الرسالة جاهزة.', done='إذا لم يُفتح تطبيق البريد، راسلنا على: ',
    dl='مركز التنزيل', dl_href='arabic/مركز-التنزيل/'),
}


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
        rows = ''.join(
            f'<tr><th scope="row">{esc(k)}</th><td>{esc(v) if v else f"<span class=ph-data>{esc(L["ph"])}</span>"}</td></tr>'
            for k, v in L['rows'])
        main = f'''{page_hero(p, [(L['crumb'], None)], esc(L['title']), esc(L['lead']), lang=lang)}
  <section class="section"><div class="wrap export-grid">
    <div class="reveal">
      <h2>{esc(L['facts_h'])}</h2>
      <table class="spec-table export-facts"><tbody>{rows}</tbody></table>
      <p style="margin-top:14px"><a class="more-link" href="{p}{L['dl_href']}">{esc(L['dl'])} ←</a></p>
      <h2 style="margin-top:28px">{esc(L['contact_h'])}</h2>
      <div class="cta-actions export-contact">
        <a class="btn btn-ghost" href="mailto:{EMAIL}" dir="ltr">{EMAIL}</a>
        <a class="btn btn-ghost" href="tel:{TEL}" dir="ltr">+98 21 9200 1017</a>
        <a class="btn btn-ghost" href="{WA}" target="_blank" rel="noopener">WhatsApp</a>
      </div>
      <p class="qf-note"><span class="ph-data">{esc(L['contact_note'])}</span></p>
    </div>
    <div class="reveal">{form_html(L, lang)}</div>
  </div></section>'''
        if lang == 'en':
            main = main.replace('←', '→')
        html = page(p, 'contact', L['title'], L['lead'], main, lang=lang,
                    fa_path='export/' if lang == 'fa' else '', canonical_path=L['root'] + 'export/',
                    scripts=f'<script src="{p}assets/js/quote-form.js" defer></script>\n')
        write(rel, html)
