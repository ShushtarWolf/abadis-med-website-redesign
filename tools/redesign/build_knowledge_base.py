"""Build the Core Abadis Knowledge Base (Markdown + JSON).

Sources, in order:
- live abadis-med.com snapshots in tools/redesign/data/ (About, FAQ, products)
- approved redesign copy (about_copy.json, solutions_philosophy.py, dial-practical formulas)
Facts that are not on those sources are marked absent. Nothing is invented.
"""
from __future__ import annotations

import json
import re
import sys
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import solutions_philosophy as phil  # noqa: E402

DATA = Path(__file__).resolve().parent / 'data'
SITE = ROOT / 'site'
OUT_JSON = [
    SITE / 'assets/data/abadis-knowledge-base.json',
    ROOT / 'docs/knowledge-base/abadis-knowledge-base.json',
]
OUT_MD = ROOT / 'docs/knowledge-base/abadis-core-knowledge-base.md'
OUT_FALLBACK = SITE / 'assets/chatbot/kb-fallback.js'

# EN/AR mirrors of the short live FAQ items. Key = exact Persian question.
# The two long published tables (vehicle loads, product codes) stay Persian-only.
FAQ_I18N = {
    'آیا باید بعد از هر بار مصرف مخازن ساکشن آبادیس را عوض کرد ؟': (
        'Do Abadis suction canisters have to be replaced after every use?',
        'No. The rigid canisters do not need to be replaced after every use.',
        'هل يجب استبدال خزانات الشفط من آباديس بعد كل استخدام؟',
        'لا. الخزانات الثابتة لا تحتاج إلى استبدال بعد كل استخدام.',
    ),
    'کیسه های ساکشن یکبار مصرف از چه موادی ساخته شده اند؟': (
        'What are the disposable suction liners made of?',
        'The liner is polyethylene (PE). The rigid canister is polycarbonate.',
        'ممّ تُصنع أكياس الشفط ذات الاستعمال الواحد؟',
        'الكيس من البولي إيثيلين (PE) والخزان الثابت من البولي كربونات.',
    ),
    'فیلتر قطع کننده کیسه ساکشن آبادیس چه وظیفه ای دارد؟': (
        'What does the shutoff filter on the Abadis suction liner do?',
        'It stops suctioned fluid from overflowing into the surroundings.',
        'ما وظيفة فلتر قطع التدفق في كيس الشفط؟',
        'يمنع طفح السوائل المسحوبة إلى المحيط.',
    ),
    'آیا فیلترهای قطع کننده تولید داخل ایران می باشند؟': (
        'Are the shutoff filters made in Iran?',
        'Abadis Medical is the first manufacturer of these filters in Iran.',
        'هل فلاتر قطع التدفق مصنّعة في إيران؟',
        'شركة خزانات آباديس الطبية هي أول منتج لهذه الفلاتر في إيران.',
    ),
    'پودر جاذب (جامدکننده) در کیسه های ساکشن آبادیس چیست؟': (
        'What is the absorbent (solidifying) powder in Abadis liners?',
        'It gels the liquid inside the liner so the bag is easier to carry, and if the liner overflows or tears the fluid is contained better. International sources report that absorbent powder can cut hospital-waste disposal costs by up to three times.',
        'ما هو المسحوق الماص (المُصلِّب) في أكياس آباديس؟',
        'يحوّل السائل داخل الكيس إلى هلام فيسهل الحمل، وإذا طفح الكيس أو تمزق يُجمع السائل بصورة أفضل. تفيد مصادر دولية أن المسحوق الماص يخفض كلفة التخلص من نفايات المستشفى حتى ثلاثة أضعاف.',
    ),
    'زمانی که کیسه های ساکشن شروع به استفاده می گردد، بعد از چه مدتی باید آن ها را تعویض کرد؟': (
        'Once a liner is in use, when should it be changed?',
        'Change it when it is full. Do not move one patient’s liner to another patient.',
        'متى يُستبدل كيس الشفط بعد بدء الاستخدام؟',
        'يمكن استبداله بعد امتلائه. لا يُنقل كيس مريض إلى مريض آخر.',
    ),
    'در چه صورتی کیسه ساکشن آبادیس از گارانتی خارج می گردد؟': (
        'When does an Abadis suction liner leave warranty?',
        '1) The liner does not match the canister size. 2) A liner in use is not changed at least every 24 hours. 3) A liner is used more than once. Use outside these rules voids the warranty.',
        'متى يخرج كيس الشفط من الضمان؟',
        '١) عدم استخدام كيس يناسب حجم الخزان. ٢) عدم استبدال الكيس المستخدم مرة كل ٢٤ ساعة على الأقل. ٣) استخدام الكيس أكثر من مرة. خلاف ذلك يُسقط الضمان.',
    ),
    'شیوه صحیح شست و شوی مخازن ساکشن آبادیس چگونه است ؟': (
        'How should Abadis suction canisters be washed?',
        '1) Disinfectant to water, 1:10. 2) Roll the canister in that solution for 10 minutes — not longer, or the canister can be damaged. 3) Dry it on a clean towel. 4) Autoclave washing is possible up to 120°C. 5) Replace a cracked or broken canister. Any other wash voids the warranty. Wash only when the canister is contaminated.',
        'ما الطريقة الصحيحة لغسل خزانات الشفط؟',
        '١) مطهّر إلى ماء بنسبة ١ إلى ١٠. ٢) دحرجة الخزان في المحلول ١٠ دقائق لا أكثر. ٣) التجفيف على منشفة نظيفة. ٤) يمكن الغسل في الأوتوكلاف حتى ١٢٠ درجة. ٥) يُستبدل الخزان إذا تشقق أو انكسر. أي غسل آخر يُسقط الضمان. الغسل فقط عند وجود تلوث.',
    ),
    'طول عمر فیلتر آنتی باکتریال چقدر است؟': (
        'How long does the antibacterial filter last?',
        'Replace it when the paper inside changes colour. Replacing it every 6 months gives the best performance.',
        'ما عمر الفلتر المضاد للبكتيريا؟',
        'يُستبدل عندما يتغير لون الورق داخله. الاستبدال كل ٦ أشهر يعطي أفضل أداء.',
    ),
    'طول عمر فیلتر قطع کننده جریان چقدر است ؟': (
        'How long does the flow-stopper filter last?',
        'Replace it when liquid reaches its surface or suction pressure drops. For correct operation, replace it every month.',
        'ما عمر فلتر قطع التدفق؟',
        'يُستبدل عندما يصل السائل إلى سطحه أو ينخفض ضغط الشفط. والأفضل استبداله كل شهر.',
    ),
    'آیا گیره مخزن دیواری و پرتابل قابل شست و شو است؟': (
        'Can the wall and portable canister clamps be washed?',
        'Yes. Both the metal and plastic versions can be washed up to 95°C.',
        'هل يمكن غسل مشبك الخزان الجداري والمحمول؟',
        'نعم. النوعان المعدني والبلاستيكي يُغسلان حتى ٩٥ درجة كحد أقصى.',
    ),
    'در چه صورتی پایه ساکشن پرتابل از گارانتی خارج می گردد؟': (
        'When does the portable suction base leave warranty?',
        'A heavy impact voids the warranty.',
        'متى تخرج قاعدة الشفط المحمولة من الضمان؟',
        'إذا تلقت ضربة شديدة.',
    ),
    'در چه صورتی مخازن ساکشن آبادیس از گارانتی خارج می گردد؟': (
        'When does an Abadis canister leave warranty?',
        'If it is damaged or struck.',
        'متى يخرج خزان الشفط من الضمان؟',
        'إذا تضرر أو تعرّض لضربة.',
    ),
    'در چه صورتی رگولاتور آبادیس از گارانتی خارج می گردد؟': (
        'When does an Abadis regulator leave warranty?',
        'If it is struck and the device is damaged.',
        'متى يخرج المنظّم من الضمان؟',
        'إذا تعرّض لضربة وتضرر الجهاز.',
    ),
    'وارانتی محصولات شرکت مخازن طبی آبادیس به چه صورت می باشد؟': (
        'What is the Abadis product warranty?',
        'Suction liner: free replacement up to 1 year after the sale date if there is a fault. Suction canister: the same, 1 year. Portable base: free replacement for 6 months, then free repair up to 1 year, then paid repair. Wall clamp and portable clamp: free replacement for 3 years. T connector and connector: lifetime free replacement. Regulator and wall suction: free replacement for 6 months, free repair up to 1 year, then paid.',
        'كيف يكون ضمان منتجات آباديس؟',
        'كيس الشفط والخزان: استبدال مجاني حتى سنة من تاريخ البيع عند وجود عيب. القاعدة المحمولة: استبدال مجاني ٦ أشهر ثم إصلاح مجاني حتى سنة ثم إصلاح مدفوع. مشبك الجدار والمشبك المحمول: استبدال مجاني ٣ سنوات. وصلة T والوصلة: استبدال مجاني مدى الحياة. المنظّم والشفط الجداري: استبدال ٦ أشهر ثم إصلاح مجاني حتى سنة ثم مدفوع.',
    ),
    'ساکشن تیوب آبادیس چند نوع است؟': (
        'How many Abadis suction-tube sizes are there?',
        'Three: CH25, CH30 and CH35.',
        'كم نوعًا لأنبوب الشفط؟',
        'ثلاثة: CH25 وCH30 وCH35.',
    ),
    'تعداد کیسه ساکشن یکبار مصرف آبادیس در هر کارتن چند عدد است؟': (
        'How many liners are in a carton?',
        '45 liners per carton for each of the three sizes. A liner with a mechanical filter is packed 30 per carton.',
        'كم كيس شفط في الكرتون؟',
        '٤٥ كيسًا لكل سعة من السعات الثلاث. الكيس بفلتر ميكانيكي: ٣٠ في الكرتون.',
    ),
    'سایز کیسه ساکشن های یکبار مصرف آبادیس چند لیتر است؟': (
        'Which volumes do Abadis disposable liners come in?',
        '1 litre, 2 litres and 3 litres.',
        'ما سعات أكياس الشفط؟',
        '١ لتر و٢ لتر و٣ لترات.',
    ),
    'ابعاد کارتن های محصولات آبادیس چقدر است؟': (
        'What are the carton dimensions?',
        '1 L and 2 L liners: 57.5 × 42.5 × 44 cm. 3 L: 49 × 49 × 49 cm. Suction tube: 59 × 44.5 × 43.5 cm.',
        'ما أبعاد الكراتين؟',
        '١ و٢ لتر: ٥٧٫٥ × ٤٢٫٥ × ٤٤ سم. ٣ لتر: ٤٩ × ٤٩ × ٤٩ سم. أنبوب الشفط: ٥٩ × ٤٤٫٥ × ٤٣٫٥ سم.',
    ),
    'تعداد ساکشن تیوب آبادیس در هر کارتن چند عدد است؟': (
        'How many suction tubes are in a carton?',
        '100 suction tubes per carton.',
        'كم أنبوب شفط في الكرتون؟',
        '١٠٠ أنبوب في الكرتون.',
    ),
    'برای درخواست نمونه از محصولات شرکت مخازن طبی آبادیس چه مراحلی باید طی شود؟': (
        'How do I request a product sample?',
        'Send the contact form, or call the installation and commissioning unit.',
        'كيف أطلب عيّنة من المنتجات؟',
        'عبر نموذج اتصل بنا، أو بالاتصال بوحدة التركيب والتشغيل.',
    ),
    'مراحل خرید محصولات شرکت مخازن طبی آبادیس چگونه است؟': (
        'What are the steps to buy Abadis products?',
        '1) Contact form or a call to sales, and the request is registered. 2) The customer confirms the proforma. 3) Payment. 4) Dispatch.',
        'ما خطوات شراء منتجات آباديس؟',
        '١) نموذج الاتصال أو الاتصال بمندوبي المبيعات وتسجيل الطلب. ٢) اعتماد الفاتورة الأولية. ٣) الدفع. ٤) الشحن.',
    ),
    'آیا شرکت مخازن طبی آبادیس در دیگر استان های کشور دارای نمایندگی است؟': (
        'Does Abadis have distributors in other provinces?',
        'Yes. The distributor list is on the representatives page.',
        'هل لآباديس ممثلون في المحافظات؟',
        'نعم. قائمة الممثلين في صفحة الممثلين.',
    ),
    'نحوه نصب کیسه های ساکشن یکبار مصرف آبادیس چگونه است؟': (
        'How is a disposable liner installed?',
        '1) Connect the silicone tube from the regulator or suction unit to the T connector on the canister. 2) From the other side of the T, connect silicone tube to the connector and seat that connector on the vacuum port of the lid. 3) Connect the suction tube to the patient port and suction through that tube.',
        'كيف يُركَّب كيس الشفط؟',
        '١) وصل الخرطوم السيليكوني من المنظّم أو جهاز الشفط إلى وصلة T على الخزان. ٢) من الجهة الأخرى لوصلة T إلى الوصلة ثم إلى منفذ الفراغ على الغطاء. ٣) وصل أنبوب الشفط بمنفذ المريض والشفط عبره.',
    ),
    'در حین نصب کیسه های ساکشن آبادیس به چه نکاتی برای جلوگیری از افت فشار و نشتی باید توجه کرد ؟': (
        'What should be checked during installation to avoid pressure loss and leaks?',
        'Check: 1) the T clamp on the canister, 2) the silicone hoses between the suction unit and the T clamp, with no leak, 3) the suction tube connection to the patient.',
        'ما الذي يُفحص عند التركيب لتفادي هبوط الضغط والتسرب؟',
        '١) مشبك T على الخزان. ٢) خراطيم السيليكون بين الجهاز ومشبك T من دون تسرب. ٣) وصل أنبوب الشفط بالمريض.',
    ),
    'آیا کیسه های ساکشن یکبار مصرف آبادیس با یکدیگر سری می شوند؟': (
        'Can Abadis liners be connected in series?',
        'Yes. Connect the regulator to the T on the first (pre) canister, then from that T to the next canister which holds the final liner and the shutoff filter, then from that T to the vacuum port on the lid, then from the patient port of that canister back to the vacuum of the previous one, and the suction tube to the patient port.',
        'هل يمكن وصل أكياس الشفط على التسلسل؟',
        'نعم. المنظّم إلى وصلة T للخزان الأول (pre)، ثم إلى الخزان التالي الذي فيه الكيس النهائي وفلتر القطع، ثم إلى منفذ الفراغ على الغطاء، ثم من منفذ المريض في هذا الخزان إلى فراغ الخزان السابق، وأنبوب الشفط إلى منفذ المريض.',
    ),
    'چند عدد کیسه ساکشن را با هم می توان سری کرد؟': (
        'How many liners can be connected in series?',
        'Up to four disposable liners can be connected together on the trolley base.',
        'كم كيسًا يمكن وصلها معًا؟',
        'أربعة أكياس كحد أقصى على قاعدة الترولي.',
    ),
}


def clean_html(html: str) -> str:
    html = html or ''
    html = re.sub(r'<br\s*/?>', '\n', html, flags=re.I)
    html = re.sub(r'</(p|li|tr|h\d|div)>', '\n', html, flags=re.I)
    html = re.sub(r'<li[^>]*>', '• ', html, flags=re.I)
    html = re.sub(r'<[^>]+>', '', html)
    text = unescape(html).replace('\xa0', ' ').replace('\u200c', '\u200c')
    text = re.sub(r'[ \t]+\n', '\n', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def tri(fa, en, ar):
    return {'fa': fa, 'en': en, 'ar': ar}


def load_faq(pages):
    items = []
    group = ''
    for block in pages['/پرسش-های-متداول/']['blocks']:
        if block.get('t') == 'h' and block.get('lvl') == 2:
            group = block.get('text') or group
        if block.get('t') != 'faq':
            continue
        for it in block['items']:
            q = re.sub(r'\s+', ' ', it['q']).strip()
            a = clean_html(it['a'])
            pair = FAQ_I18N.get(q)
            if pair:
                q_en, a_en, q_ar, a_ar = pair
                status = 'translated-from-fa-faq'
            elif len(a) > 800:
                q_en = 'Published table on the Persian FAQ (not retyped)'
                a_en = 'The full table is stored verbatim in answer.fa and on /faq/. Digits are the live-site figures.'
                q_ar = 'جدول منشور في الأسئلة الشائعة بالفارسية'
                a_ar = 'الجدول الكامل محفوظ حرفيًا في answer.fa وعلى /faq/.'
                status = 'fa-table-verbatim'
            else:
                q_en = a_en = q_ar = a_ar = ''
                status = 'fa-only'
            items.append({
                'id': f'faq-{len(items)+1:02d}',
                'group': group,
                'question': tri(q, q_en, q_ar),
                'answer': tri(a, a_en, a_ar),
                'translation': status,
                'source': 'http://abadis-med.com/پرسش-های-متداول/',
                'url': {'fa': '/faq/', 'en': '/en/faqs/', 'ar': '/arabic/پرسش-های-متداول/'},
            })
    return items


def load_products(pages):
    families = [
        ('liners', '/محصولات/کیسه-ساکشن/', tri('کیسه ساکشن یکبارمصرف', 'Disposable suction liner', 'كيس الشفط ذو الاستعمال الواحد'),
         {'fa': '/products/suction-bag/', 'en': '/en/products/suction-bag/', 'ar': '/arabic/كيس-الشفط/'}),
        ('canisters', '/محصولات/مخزن/', tri('مخزن ساکشن', 'Suction canister', 'خزان الشفط'),
         {'fa': '/products/canister/', 'en': '/en/products/canisters/', 'ar': '/arabic/خزانات/'}),
        ('tubes', '/محصولات/ساکشن-تیوب/', tri('ساکشن تیوب', 'Suction tube', 'أنبوب الشفط'),
         {'fa': '/products/suction-tube/', 'en': '/en/suction-tube/', 'ar': '/arabic/أنبوب-الشفط/'}),
        ('filters', '/محصولات/فیلترها/', tri('فیلتر', 'Filter', 'الفلتر'),
         {'fa': '/products/filters/', 'en': '/en/products/filters/', 'ar': '/arabic/الفلتر/'}),
        ('stands', '/محصولات/پایه/', tri('پایه و نگهدارنده', 'Stand and holder', 'القاعدة والحامل'),
         {'fa': '/products/stand/', 'en': '/en/products/base-and-holder/', 'ar': '/arabic/تثبیت/'}),
        ('connectors', '/محصولات/اتصالات/', tri('اتصالات', 'Connectors', 'الوصلات'),
         {'fa': '/products/connectors/', 'en': '/en/products/connections/', 'ar': '/arabic/الوصلات/'}),
        ('other', '/محصولات/سایر-محصولات/', tri('سایر محصولات', 'Other products', 'منتجات أخرى'),
         {'fa': '/products/other/', 'en': '/en/products/other-products/', 'ar': '/arabic/منتجات-اخری/'}),
    ]
    out = []
    for key, path, title, urls in families:
        sections = []
        current = None
        for block in pages[path]['blocks']:
            if block.get('t') == 'h' and block.get('lvl') in (1, 2):
                current = {'heading': block.get('text') or '', 'body': ''}
                sections.append(current)
                continue
            if current is None:
                continue
            if block.get('t') == 'html':
                text = clean_html(block.get('html') or '')
            elif block.get('t') == 'table':
                rows = block.get('rows') or []
                text = '\n'.join(' | '.join(clean_html(c) for c in row) for row in rows)
            else:
                text = ''
            if text:
                current['body'] = (current['body'] + '\n' + text).strip()
        # Drop empty image-only headings and cap very long bodies.
        kept = []
        for sec in sections:
            body = sec['body'][:4000]
            if not body and sec['heading'] in ('',):
                continue
            kept.append({'heading': sec['heading'], 'body': body})
        out.append({'id': key, 'title': title, 'url': urls, 'source': 'http://abadis-med.com' + path, 'sections': kept})
    return out


def t_list(items):
    return [tri(x['fa'], x['en'], x['ar']) if isinstance(x, dict) else x for x in items]


def solutions_block():
    def pack(node):
        if isinstance(node, dict) and set(node) <= {'fa', 'en', 'ar'}:
            return node
        if isinstance(node, dict):
            return {k: pack(v) for k, v in node.items()}
        if isinstance(node, list):
            return [pack(v) for v in node]
        if isinstance(node, tuple) and len(node) == 2 and isinstance(node[0], dict):
            return {'label': node[0], 'text': node[1]}
        return node

    pages = []
    for slug, name in phil.PAGE_NAME.items():
        folder = {'fa': '/solutions/', 'en': '/en/solutions/', 'ar': '/arabic/الحلول/'}
        pages.append({'slug': slug, 'title': name, 'url': {k: folder[k] + slug + '/' for k in folder}})
    return {
        'architecture': 'dual-path',
        'paths': {
            'heading': phil.PATHS_H,
            'columns': phil.PATHS_HEAD,
            'rows': [{'aspect': a, 'products': b, 'solutions': c} for a, b, c in phil.PATHS],
        },
        'pillars': [
            {'title': phil.PILLARS[i], 'question': phil.PILLAR_TEXT[i]}
            for i in range(4)
        ],
        'intro': {'title': phil.INTRO_H, 'subtitle': phil.INTRO_SUB, 'paragraphs': phil.INTRO},
        'themes': [
            {
                'key': theme['key'],
                'title': theme['title'],
                'products': theme['products'],
                'pages': phil.THEME_PAGES.get(theme['key'], []),
            }
            for theme in phil.THEMES
        ],
        'areas': [
            pack(phil.FLUID) | {'id': 'fluid', 'pages': ['fluid-management']},
            pack(phil.AIRWAY) | {'id': 'airway', 'pages': ['airway-care']},
            pack(phil.WASTE) | {'id': 'infection-waste', 'pages': ['waste-management-pva']},
        ],
        'application_contexts_without_own_page': [
            {
                'id': 'or-efficiency',
                'title': tri('کارایی اتاق عمل', 'OR efficiency', 'كفاءة غرفة العمليات'),
                'note': tri(
                    'اتاق عمل در کاربردهای کیسه ۳ لیتری و در محاسبه‌گر تخت‌ها آمده است. صفحه راهکار جداگانه‌ای برای «OR Efficiency» در سایت نیست؛ زیر مدیریت مایعات خوانده می‌شود.',
                    'The operating room is a published use of the 3 L liner and an input of the bed calculator. There is no separate “OR Efficiency” solution page; it is read under fluid management.',
                    'غرفة العمليات استخدام منشور لكيس ٣ لتر ومدخل في حاسبة الأسرّة. لا صفحة حل مستقلة لها؛ تُقرأ تحت إدارة السوائل.',
                ),
                'url': {'fa': '/solutions/fluid-management/', 'en': '/en/solutions/fluid-management/', 'ar': '/arabic/الحلول/fluid-management/'},
            },
            {
                'id': 'icu-care',
                'title': tri('مراقبت ICU', 'ICU care', 'رعاية ICU'),
                'note': tri(
                    'CCU/ICU از کاربردهای کیسه ۲ لیتری است و تخت ICU در محاسبه‌گر هست. صفحه راهکار جداگانه ندارد.',
                    'CCU/ICU is a published use of the 2 L liner, and ICU beds are a calculator input. There is no separate ICU solution page.',
                    'CCU/ICU استخدام منشور لكيس ٢ لتر، وأسرّة ICU مدخل في الحاسبة. لا صفحة حل مستقلة.',
                ),
                'url': {'fa': '/solutions/fluid-management/', 'en': '/en/solutions/fluid-management/', 'ar': '/arabic/الحلول/fluid-management/'},
            },
        ],
        'pages': pages,
        'source': 'tools/redesign/solutions_philosophy.py (Alireza, Oct 2026) on the three solution pages',
    }


def categories(products):
    by_id = {p['id']: p for p in products}
    def fam(*ids):
        return [by_id[i]['url'] for i in ids]

    return [
        {
            'id': 'canisters-liners',
            'title': tri('مخازن و کیسه‌های ساکشن', 'Suction canisters and liners', 'خزانات وأكياس الشفط'),
            'status': 'in_current_catalog',
            'volumes': ['1 L', '2 L', '3 L'],
            'summary': tri(
                'کیسه یکبارمصرف در ۱، ۲ و ۳ لیتر داخل مخزن پلی‌کربنات. ۲ لیتر تا ۸ لیتر تک‌ردیف و ۱۶ لیتر دو ردیف؛ ۳ لیتر تا ۱۲ لیتر سری. کارتن معمولاً ۴۵ عدد (فیلتر مکانیکی ۳۰). ابعاد کیسه از صفحه محصول: ۱ لیتر Ø۱۱×۱۵٫۵، ۲ لیتر Ø۱۱×۲۴٫۵، ۳ لیتر Ø۱۱×۳۹ سانتی‌متر.',
                'Disposable liner in 1, 2 and 3 L inside a polycarbonate canister. 2 L up to 8 L single-row / 16 L double-row; 3 L up to 12 L in series. Carton usually 45 (mechanical filter 30). Bag size on the product page: 1 L Ø11×15.5, 2 L Ø11×24.5, 3 L Ø11×39 cm.',
                'كيس استعمال واحد ١ و٢ و٣ لتر داخل خزان بولي كربونات. ٢ لتر حتى ٨ لتر صفًا واحدًا / ١٦ لتر صفين؛ ٣ لتر حتى ١٢ لترًا بالتسلسل. الكرتون عادة ٤٥ (الفلتر الميكانيكي ٣٠).',
            ),
            'applications': tri(
                '۱ لیتر: آمبولانس، عفونی، دندانپزشکی، چشم، کودکان. ۲ لیتر: ریه و آندوسکوپی، گوارش، CCU/ICU، عفونی، بخش مردان و زنان، NICU/PICU، اورژانس، ECT. ۳ لیتر: عفونی، اتاق عمل، قلب، بخش مردان و زنان، لیپوساکشن، جراحی، گوارش، ICU.',
                '1 L: ambulance, infectious, dentistry, ophthalmology, paediatrics. 2 L: lung and endoscopy, gastroenterology, CCU/ICU, infectious, men’s and women’s wards, NICU/PICU, emergency, ECT. 3 L: infectious, operating room, cardiology, men’s and women’s wards, liposuction, surgery, gastroenterology, ICU.',
                '١ لتر: إسعاف، عدوى، أسنان، عيون، أطفال. ٢ لتر: رئة وتنظير، جهاز هضمي، CCU/ICU، عدوى، جناحا الرجال والنساء، NICU/PICU، طوارئ، ECT. ٣ لتر: عدوى، عمليات، قلب، جناحا الرجال والنساء، شفط دهون، جراحة، جهاز هضمي، ICU.',
            ),
            'links': fam('liners', 'canisters'),
            'family_ids': ['liners', 'canisters'],
        },
        {
            'id': 'suction-instruments',
            'title': tri('ابزار ساکشن (تیوب و فینگرتیپ)', 'Suction instruments (tube and fingertip)', 'أدوات الشفط (الأنبوب وطرف الإصبع)'),
            'status': 'in_current_catalog',
            'volumes': ['CH25', 'CH30', 'CH35'],
            'summary': tri(
                'ساکشن تیوب شفاف و شیاردار در CH25 و CH30 و CH35، با یا بدون فینگرتیپ. Yankauer به‌عنوان محصول آبادیس در کاتالوگ زنده نیست؛ در مقاله تاریخی ساکشن به مخترع آن اشاره شده است.',
                'Clear and ribbed suction tube in CH25, CH30 and CH35, with or without a fingertip. Yankauer is not an Abadis SKU in the live catalog; an article only names Yankauer as the historical inventor of an early suction device.',
                'أنبوب شفط شفاف ومضلّع بمقاسات CH25 وCH30 وCH35، مع طرف الإصبع أو من دونه. Yankauer ليس رمز منتج لآباديس في الكتالوج الحالي.',
            ),
            'applications': tri(
                'اتصال مدار بیمار به کیسه و مخزن در اتاق عمل، مراقبت ویژه و سایر بخش‌هایی که ساکشن نیاز دارند.',
                'Connects the patient circuit to the liner and canister in the operating room, intensive care and other departments that need suction.',
                'يوصل دارة المريض بالكيس والخزان في العمليات والعناية المركزة وسائر الأقسام التي تحتاج إلى شفط.',
            ),
            'links': fam('tubes'),
            'family_ids': ['tubes'],
        },
        {
            'id': 'airway',
            'title': tri('مراقبت تنفسی و راه هوایی', 'Respiratory and airway care', 'العناية التنفسية والطريق الهوائي'),
            'status': 'in_current_catalog',
            'volumes': [],
            'summary': tri(
                'مسواک ساکشن، سواب دهانی و فیکسر لوله تراشه روی صفحه بهداشت دهان. سواب دهانی صفحه مشخصات جدا ندارد و متناسب با وضعیت توسعه و عرضه معرفی شده است.',
                'The suction toothbrush, oral swab and endotracheal-tube fixer are on the oral-hygiene page. The swab has no separate specification page; it is named according to its stage of development and supply.',
                'فرشاة الشفط والمسحة الفموية ومثبّت أنبوب القصبة في صفحة نظافة الفم. المسحة بلا صفحة مواصفات مستقلة، وتُذكر بحسب مرحلة التطوير والعرض.',
            ),
            'applications': tri(
                'مراقبت دهان و بیماران دارای لوله تراشه، مطابق دستورالعمل هر محصول.',
                'Oral care and patients with an endotracheal tube, following each product’s instructions.',
                'عناية الفم والمرضى ذوو أنبوب القصبة، وفق تعليمات كل منتج.',
            ),
            'links': [tri('/products/oral-hygiene/', '/en/products/oral-hygiene/', '/arabic/نظافة-الفم/')],
            'family_ids': ['oral'],
        },
        {
            'id': 'urology',
            'title': tri('اورولوژی و درناژ', 'Urology and drainage', 'المسالك البولية والتصريف'),
            'status': 'not_a_separate_catalog_line',
            'volumes': [],
            'summary': tri(
                'خط محصول جداگانه‌ای با این نام در abadis-med.com نیست. کیسه ساکشن در بخش مردان استفاده می‌شود و محفظه نمونه‌گیری برای جمع‌آوری ذرات از مایع ساکشن است.',
                'abadis-med.com has no separate product line under this name. Suction liners are used on the men’s ward, and the collection cup gathers particles from suctioned fluid.',
                'لا خط منتجات مستقل بهذا الاسم في abadis-med.com. تُستخدم أكياس الشفط في جناح الرجال، وكوب العينة يجمع الجسيمات من سائل الشفط.',
            ),
            'applications': tri('بخش مردان؛ نمونه‌گیری از مایع ساکشن.', 'Men’s ward; sampling suctioned fluid.', 'جناح الرجال؛ أخذ عينة من سائل الشفط.'),
            'links': fam('liners', 'canisters'),
            'family_ids': ['liners', 'canisters'],
        },
        {
            'id': 'gastroenterology',
            'title': tri('گوارش', 'Gastroenterology', 'الجهاز الهضمي'),
            'status': 'use_site_not_a_separate_catalog_line',
            'volumes': ['2 L', '3 L'],
            'summary': tri(
                'گوارش کاربرد منتشرشده کیسه ۲ و ۳ لیتری است، نه خانواده محصول جدا.',
                'Gastroenterology is a published use of the 2 L and 3 L liners, not a separate product family.',
                'الجهاز الهضمي استخدام منشور لكيسي ٢ و٣ لتر، وليس عائلة منتجات مستقلة.',
            ),
            'applications': tri('ریه و آندوسکوپی و گوارش، طبق صفحه کیسه ساکشن.', 'Lung, endoscopy and gastroenterology, as on the liner page.', 'الرئة والتنظير والجهاز الهضمي، كما في صفحة الكيس.'),
            'links': fam('liners'),
            'family_ids': ['liners'],
        },
        {
            'id': 'gynecology',
            'title': tri('زنان', 'Gynecology', 'النساء'),
            'status': 'use_site_not_a_separate_catalog_line',
            'volumes': ['2 L', '3 L'],
            'summary': tri(
                'بخش زنان کاربرد منتشرشده کیسه ۲ و ۳ لیتری است. محصول زنان و زایمان جداگانه‌ای در کاتالوگ نیست.',
                'The women’s ward is a published use of the 2 L and 3 L liners. The catalog has no separate obstetrics and gynecology range.',
                'جناح النساء استخدام منشور لكيسي ٢ و٣ لتر. لا مجموعة مستقلة لطب النساء في الكتالوج.',
            ),
            'applications': tri('بخش زنان.', 'Women’s ward.', 'جناح النساء.'),
            'links': fam('liners'),
            'family_ids': ['liners'],
        },
        {
            'id': 'anesthesia-icu',
            'title': tri('ملزومات بیهوشی و ICU', 'Anesthesia and ICU consumables', 'مستهلكات التخدير وICU'),
            'status': 'in_current_catalog',
            'volumes': ['2 L'],
            'summary': tri(
                'کیسه ۲ لیتری برای CCU/ICU، رگولاتور بزرگسال VR-A1 و کودکان VR-B1، فیلتر آنتی‌باکتریال و قطع‌کننده جریان، نگهدارنده لوله تراشه.',
                '2 L liner for CCU/ICU, adult regulator VR-A1 and paediatric VR-B1, antibacterial and flow-stopper filters, endotracheal-tube holder.',
                'كيس ٢ لتر لـ CCU/ICU، منظّم الكبار VR-A1 والأطفال VR-B1، الفلتر المضاد للبكتيريا وقاطع التدفق، وحامل أنبوب القصبة.',
            ),
            'applications': tri('CCU/ICU، اتاق عمل، مدار وکیوم.', 'CCU/ICU, operating room, vacuum circuit.', 'CCU/ICU وغرفة العمليات ودارة الفراغ.'),
            'links': fam('liners', 'filters', 'other'),
            'family_ids': ['liners', 'filters', 'other'],
        },
        {
            'id': 'general-consumables',
            'title': tri('ملزومات عمومی', 'General consumables', 'مستهلكات عامة'),
            'status': 'in_current_catalog',
            'volumes': ['600 ml'],
            'summary': tri(
                'رسیور یکبارمصرف ۶۰۰ میلی‌لیتر (پلی‌پروپیلن)، اتصال T، کانکتور، شلنگ سیلیکونی، شیر ON/OFF، گیره مخزن. Splash-Vac روی سایر محصولات است.',
                '600 ml disposable kidney dish (polypropylene), T connector, connector, silicone hose, ON/OFF valve, canister clamp. Splash-Vac is on the other-products page.',
                'وعاء كلوي ٦٠٠ مل (بولي بروبيلين)، وصلة T، وصلة، خرطوم سيليكون، صمام تشغيل/إيقاف، مشبك الخزان. Splash-Vac في صفحة المنتجات الأخرى.',
            ),
            'applications': tri('جمع‌آوری اولیه، اتصالات مدار ساکشن، شمارش ابزار.', 'First collection, suction-circuit connectors, instrument counting.', 'الجمع الأولي، وصلات دارة الشفط، عدّ الأدوات.'),
            'links': fam('connectors', 'other', 'stands'),
            'family_ids': ['connectors', 'other', 'stands'],
        },
    ]


def chunks_from(kb):
    rows = []

    def add(id_, section, url, fa, en='', ar='', keywords=''):
        rows.append({
            'id': id_,
            'section': section,
            'url': url if isinstance(url, str) else url,
            'text': tri(fa, en or fa, ar or en or fa),
            'keywords': keywords,
        })

    c = kb['company']
    add('company-profile', 'company', {'fa': '/about/', 'en': '/en/about-us/', 'ar': '/arabic/من-نحن/'},
        c['about_fa_lead'], c['about_en_lead'], c['about_ar_lead'],
        'about mission vision 2017 1396 founding تاسیس درباره آبادیس')
    add('company-slogan', 'company', {'fa': '/about/', 'en': '/en/about-us/', 'ar': '/arabic/من-نحن/'},
        c['slogan']['fa'], c['slogan']['en'], c['slogan']['ar'],
        'slogan سرانگشت fingertip mission اثر')
    add('contact', 'company', {'fa': '/contact/', 'en': '/en/contact-us/', 'ar': '/arabic/اتصل-بنا/'},
        c['contact_blurb']['fa'], c['contact_blurb']['en'], c['contact_blurb']['ar'],
        'phone email address تماس دفتر کارخانه whatsapp')
    fnd = c['founding']['authoritative']
    add('founding', 'company', {'fa': '/about/', 'en': '/en/about-us/', 'ar': '/arabic/من-نحن/'},
        f'شرکت مخازن طبی آبادیس در سال {fnd["company_established_gregorian"]} میلادی برابر {fnd["company_established_jalali"]} تأسیس شد. {fnd["source"]} {c["founding"]["not_used"]}',
        f'Abadis Medical was established in {fnd["company_established_gregorian"]} ({fnd["company_established_jalali"]}). {fnd["source"]} {c["founding"]["not_used"]}',
        f'تأسست خزانات آباديس الطبية عام {fnd["company_established_gregorian"]} الموافق {fnd["company_established_jalali"]}. {c["founding"]["not_used"]}',
        'founded established 2017 1396 تأسیس تاسیس founding')
    add('company-impact-stats', 'company', {'fa': '/about/', 'en': '/en/about-us/', 'ar': '/arabic/من-نحن/'},
        'آمار و دستاوردهای آبادیس در یک نگاه (سال ۱۴۰۵):\n• ۱٬۲۸۴ مرکز درمانی فعال (شمارنده صفحه نخست data-impact-stat برابر ۱۲۸۴، نه ۶۱۲)\n• ۱۱٬۱۱۲ کاربر کادر درمان\n• ۹۸.۹۹٪ رضایت مشتریان\n• ۰.۰۰۱۸٪ نرخ خرابی محصول\n• صرفه‌جویی سالانه بیش از ۱۲ میلیون لیتر آب (صفحه توسعه پایدار؛ ارقام ۱۱٫۲۵ میلیون و ۲۸ میلیون معیار فعلی نیستند)\n• ظرفیت تولید سالانه ۵ میلیون کیسه ساکشن (کارخانه از سال ۱۳۹۷)\n• پوشش حدود ۹۰٪ سهم بازار داخلی کیسه ساکشن و ۱٬۲۸۴ مرکز روی نقشه خانواده سبز در ۳۱ استان.',
        'Abadis Impact & Key Metrics (1405 / 2026):\n• 1,284 active healthcare centres (homepage data-impact-stat="1284", not 612)\n• 11,112 active clinical users\n• 98.99% customer satisfaction rate\n• 0.0018% product failure rate\n• Annual water savings of more than 12 million litres (SDGs page; 11.25 million and 28 million are not the current figure)\n• 5,000,000 annual disposable liner production capacity (factory operating since 1397 / 2018)\n• About 90% domestic market share, with 1,284 centres on the green-family map across 31 provinces.',
        'إحصائيات وإنجازات آباديس (۱۴۰۵):\n• ١٬٢٨٤ مركزًا علاجيًا (عداد الصفحة الرئيسية data-impact-stat = 1284 وليس 612)\n• ١١٬١١٢ مستخدمًا من الكوادر الطبية\n• ٩٨٫٩٩٪ نسبة رضا العملاء\n• ٠٫٠٠١٨٪ معدل عطل المنتج\n• توفير سنوي يزيد على ١٢ مليون لتر من الماء (صفحة أهداف التنمية؛ ١١٫٢٥ مليون و٢٨ مليون ليستا الرقم الحالي)\n• طاقة إنتاجية سنوية تبلغ ٥ ملايين كيس شفط، و١٬٢٨٤ مركزًا على خريطة العائلة الخضراء في ٣١ محافظة.',
        'stats impact metrics مراکز درمانی بیمارستان رضایت آمار تعداد کاربر ظرفیت تولید سهم بازار خرابی 1232 612 11112 98.99 0.0018 satisfaction centers centres hospitals users capacity failure rate إحصائيات رضا مراكز مستشفيات')
    add('solutions-philosophy', 'solutions', {'fa': '/solutions/#philosophy', 'en': '/en/solutions/#philosophy', 'ar': '/arabic/الحلول/#philosophy'},
        'فلسفه راهکارهای بالینی آبادیس:\nآبادیس نمایش محصولات را از دو مسیر مکمل ارائه می‌دهد: ۱) «بر اساس محصول» و ۲) «بر اساس راهکار بالینی».\nسه راهکار زنده سایت: ۱) مدیریت مایعات و ترشحات بیمارستانی، ۲) ایمنی و مراقبت از راه هوایی، ۳) کنترل آلودگی و مدیریت پسماند. اتاق عمل و ICU کاربرد کیسه ساکشن داخل راهکار مایعات هستند، نه راهکار جدا.',
        'Abadis Clinical Solutions Philosophy:\nThe live catalogue is organised by product and by clinical solution.\nThree live solutions: (1) Hospital fluid and secretion management, (2) Airway safety and care, (3) Contamination control and waste management. Operating-room and ICU use are applications of the fluid solution, not separate solutions.',
        'فلسفة الحلول السريرية في آباديس:\nثلاثة حلول حية: ١) إدارة السوائل والإفرازات، ٢) سلامة الطريق الهوائي والعناية به، ٣) السيطرة على التلوث وإدارة النفايات. غرفة العمليات والعناية المركزة تطبيقان لحل السوائل، وليسا حلين منفصلين.',
        'فلسفه راهکار راهکارها ستون معماری بالینی دوگانه philosophy solutions pillars dual path clinical approach فلسفة الحلول الأركان')
    add('closed-vs-glass-suction', 'solutions', {'fa': '/solutions/hospital-suction-systems/', 'en': '/en/solutions/hospital-suction-systems/', 'ar': '/arabic/الحلول/hospital-suction-systems/'},
        'چرا سیستم ساکشن مدار بسته یکبارمصرف آبادیس بهتر از شیشه‌های سنتی و مخازن چندبارمصرف است؟\n۱. کنترل عفونت و ایمنی کادر درمان: حذف کامل تماس پرستار با ترشحات عفونی، خون و آئروسل‌ها هنگام تخلیه و شست‌وشوی دستی شیشه‌های ساکشن.\n۲. فیلتر قطع‌کننده جریان (هیدروفوبیک) و آنتی‌باکتریال: جلوگیری از سرریز مایعات و ورود آلودگی به دستگاه ساکشن مرکزی یا پرتابل.\n۳. پودر جاذب (ژله‌ای‌کننده): تبدیل مایعات عفونی به ژل برای امحای ایمن و کاهش تا ۳ برابری هزینه امحای پسماند بیمارستانی.\n۴. صرفه‌جویی اقتصادی و زمانی: حذف مصرف هزاران لیتر آب، مواد ضدعفونی‌کننده و ساعت‌ها زمان شست‌وشو و اتوکلاو شیشه‌های سنتی، به همراه سبکی و نشکن بودن مخازن پلی‌کربنات.',
        'Why Closed-System Disposable Suction Liners Beat Traditional Glass / Reusable Bottles:\n1. Infection Control & Staff Safety: Eliminates nurse exposure to splashes, aerosols, and infectious fluids during manual emptying and washing of glass bottles.\n2. Shutoff (Hydrophobic) & Antibacterial Filters: Prevents fluid overflow and protects central vacuum lines and portable suction units from contamination.\n3. Absorbent Solidifying Powder: Turns infectious liquids into gel, preventing spills and cutting hospital waste disposal costs up to 3x.\n4. Water, Cost & Time Savings: Eliminates thousands of litres of washing water, chemical disinfectants, autoclave cycles, and staff hours, while unbreakable polycarbonate canisters replace heavy breakable glass.',
        'لماذا يتفوق نظام الشفط المغلق ذو الاستعمال الواحد من آباديس على القوارير الزجاجية التقليدية؟\n١. مكافحة العدوى وسلامة الطاقم: منع تعرض التمريض للسوائل المعدية والرذاذ أثناء التفريغ والغسل اليدوي.\n٢. فلتر قطع التدفق والمضاد للبكتيريا: يمنع طفح السوائل ويحمي جهاز الشفط والمنظومة المركزية.\n٣. المسحوق الماص (المُصلِّب): يحول السائل إلى هلام ويخفض كلفة التخلص من النفايات حتى ٣ أضعاف.\n٤. توفير الماء والوقت والتكلفة: إلغاء غسل وتعقيم القوارير الزجاجية الثقيلة والقابلة للكسر.',
        'مدار بسته شیشه شیشه‌ای شیشه ای سنتی چندبارمصرف مقایسه مزیت برتری چرا بهتر closed system glass bottle reusable traditional vs advantages comparison مقارنه زجاجي تقليدي مغلق لماذا أفضل')
    add('pricing-and-ordering', 'support', {'fa': '/articles/18786/', 'en': '/en/contact-us/', 'ar': '/arabic/اتصل-بنا/'},
        'قیمت، حجم‌ها و نحوه خرید و استعلام پیش‌فاکتور کیسه ساکشن آبادیس:\n• حجم‌های کیسه ساکشن یکبارمصرف: ۱ لیتر (آمبولانس، دندانپزشکی، چشم، اطفال)، ۲ لیتر (ICU/CCU، آندوسکوپی، گوارش، اورژانس) و ۳ لیتر (اتاق عمل، جراحی، لیپوساکشن؛ قابلیت اتصال سری تا ۴ مخزن / ۱۲ لیتر).\n• بسته‌بندی کارتن: ۴۵ عدد در هر کارتن برای کیسه‌های ۱، ۲ و ۳ لیتری معمولی (۳۰ عدد برای کیسه با فیلتر مکانیکی).\n• استعلام قیمت روز و پیش‌فاکتور (مناقصه و خرید مستقیم مراکز درمانی و نمایندگان): به دلیل فروش سازمانی و بیمارستانی، قیمت روز از طریق واحد فروش و صدور پیش‌فاکتور رسمی اعلام می‌شود. با شماره ۰۲۱-۹۲۰۰۱۰۱۷ (داخلی ۱۱ فروش) یا واتس‌اپ +۹۸۹۱۰۰۱۴۵۸۰۹ تماس بگیرید و راهنمای خرید و قیمت را در /articles/18786/ ببینید.',
        'Suction Liner Pricing, Volumes, Carton Counts & How to Order (Proforma Quote):\n• Volumes: 1 L (ambulance, dental, ophthalmic, pediatric), 2 L (ICU/CCU, endoscopy, GI, emergency), and 3 L (operating room, high-volume surgery; connectable in series up to 4 canisters / 12 L).\n• Carton packaging: 45 liners per carton for standard 1 L, 2 L, and 3 L liners (30 per carton with mechanical filter).\n• Pricing & Proforma Invoice: Institutional & hospital pricing is issued via official proforma invoice. Contact Abadis Sales at +98-21-92001017 (Ext. 11) or WhatsApp +989100145809, or read the procurement guide at /articles/18786/.',
        'أسعار وسعات أكياس الشفط وكيفية الشراء وطلب الفاتورة الأولية:\n• السعات المتوفرة: ١ لتر، ٢ لتر (للعناية المركزة والتنظير)، و٣ لتر (لغرف العمليات مع إمكانية الربط المتسلسل حتى ٤ خزانات / ١٢ لترًا).\n• التعبئة: ٤٥ كيسًا في الكرتون للمقاسات القياسية (٣٠ كيسًا للفلتر الميكانيكي).\n• الأسعار وطلب عرض السعر: تُصدر الأسعار الرسمية للمستشفيات والموزعين عبر فاتورة أولية من قسم المبيعات على الرقم 02192001017 (تحويلة 11) أو واتساب +989100145809.',
        'قیمت خرید هزینه تعرفه لیست قیمت حجم حجم‌ها سایز پیش فاکتور پیش‌فاکتور فروش چنده price pricing cost quote proforma order volumes sizes how much سعر أسعار شراء تكلفة سعات')
    add('nin-intranet-engine', 'support', {'fa': '/chatbot-demo/', 'en': '/chatbot-demo/', 'ar': '/chatbot-demo/'},
        'پایداری چت‌بات در شبکه ملی اطلاعات (اینترنت ملی و قطع اینترنت بین‌الملل):\nبله؛ موتور اصلی مشاور فروش و آکادمی آبادیس ۱۰۰٪ بومی و در هسته خود وب‌سایت تعبیه شده است:\n۱. لایه ۱ (پیش‌فرض — موتور بومی داخل هسته سایت): جستجوی هوشمند BM25، فرهنگ مترادف‌های تخصصی فارسی/انگلیسی/عربی و پیکربند فروش و محاسبه‌گر کاملاً روی فایل‌های داخلی سایت (abadis-knowledge-base.json و نسخه پشتیبان kb-fallback.js) اجرا می‌شوند و هیچ وابستگی به اینترنت بین‌الملل، فونت خارجی یا CDN خارجی ندارند.\n۲. لایه ۲ (مدل هوش مصنوعی داخلی): امکان اتصال به سرور هوش مصنوعی داخل ایران (مثلاً روی سرورهای داخلی آبادیس یا لیارا).\n۳. لایه ۳ (API بین‌المللی با بازگشت خودکار): در صورت قطع یا فیلترینگ اینترنت بین‌الملل، در کسری از ثانیه بدون توقف به موتور بومی هسته سایت برمی‌گردد.',
        'Iran Intranet (National Information Network) Resilience & Offline Core Engine:\nYes — the Abadis Sales & Academy Chatbot works 100% on Iran’s domestic intranet even if international internet is completely cut off or filtered:\n1. Tier 1 (Default On-Site Core Engine): Runs entirely inside the website’s own files (abadis-knowledge-base.json + embedded kb-fallback.js) using an in-core BM25 & synonym engine in FA/EN/AR with zero foreign CDN, font, or API dependencies.\n2. Tier 2 (Optional Domestic LLM): Connects to a self-hosted model inside Iran (e.g., on abadis-med.com or Liara) with automatic fallback.\n3. Tier 3 (Optional International API): Uses a 2.5s timeout and falls back immediately to the on-site core engine if international access is blocked.',
        'عمل المساعد الذكي على الشبكة الوطنية الإيرانية وعند انقطاع الإنترنت الدولي:\nنعم؛ يعمل مساعد مبيعات وأكاديمية آباديس بالكامل داخل نواة الموقع دون الحاجة إلى إنترنت دولي:\n١. الطبقة ١ (المحرك المحلي الافتراضي): يعمل بالكامل من ملفات الموقع المحلية (abadis-knowledge-base.json و kb-fallback.js) بلا أي اعتماد على خطوط أو خوادم خارجية.\n٢. الطبقة ٢ (نموذج داخلي داخل إيران) والطبقة ٣ (واجهة دولية مع رجوع فوري تلقائي إلى المحرك المحلي عند الحجب أو الانقطاع).',
        'اینترنت فیلترینگ شبکه ملی اطلاعات اینترنت ملی داخلی آفلاین چت بات چت‌بات intranet iran filtering offline national network domestic انقطاع الإنترنت حجب الشبكة الوطنية')
    cert = kb['certificates']
    add('certificates', 'certificates', cert['url'],
        'گواهینامه‌ها و مجوزهای آبادیس (ترتیب مصوب): ۱) IMED (اداره کل تجهیزات پزشکی)، ۲) گواهی‌های ثبت اختراع، ۳) پروانه بهره‌برداری و استانداردهای ISO 13485:2016 و GMP، ۴) جوایز، افتخارات و مقالات علمی. نوار پاورقی: CE · ISO 13485:2016 · IMED.',
        'Abadis Certificates, Licences & Approvals (Approved Order): (1) IMED, (2) Patents, (3) Operating Licences and ISO 13485:2016 / GMP, (4) Awards and scientific publications. Footer strip: CE · ISO 13485:2016 · IMED.',
        'شهادات وتراخيص آباديس (الترتيب المعتمد): ١) IMED، ٢) براءات الاختراع، ٣) رخصة التشغيل و ISO 13485:2016 / GMP، ٤) الجوائز والمقالات العلمية. شريط التذييل: CE · ISO 13485:2016 · IMED.',
        'iso 13485 imed ce gmp certificate certificates license licences گواهینامه گواهینامه‌ها مجوز مجوزها گواهی پتنت ثبت اختراع پروانه استاندارد ایزو شهادات تراخيص المعتمدة')
    for cat in kb['catalog']:
        add('cat-' + cat['id'], 'catalog', cat['links'][0],
            cat['title']['fa'] + '\n' + cat['summary']['fa'] + '\n' + cat['applications']['fa'],
            cat['title']['en'] + '\n' + cat['summary']['en'] + '\n' + cat['applications']['en'],
            cat['title']['ar'] + '\n' + cat['summary']['ar'] + '\n' + cat['applications']['ar'],
            cat['id'] + ' ' + ' '.join(cat.get('volumes') or []))
    for area in kb['solutions']['areas']:
        body_fa = area['title']['fa'] + '\n' + area['lead']['fa'] + '\n' + '\n'.join(p['fa'] for p in area['body'])
        body_en = area['title']['en'] + '\n' + area['lead']['en'] + '\n' + '\n'.join(p['en'] for p in area['body'])
        body_ar = area['title']['ar'] + '\n' + area['lead']['ar'] + '\n' + '\n'.join(p['ar'] for p in area['body'])
        url = kb['solutions']['pages']
        page_url = next(p['url'] for p in kb['solutions']['pages'] if p['slug'] in area['pages'])
        add('sol-' + area['id'], 'solutions', page_url, body_fa, body_en, body_ar, area['id'] + ' solution راهکار')
    calc = kb['calculator']
    add('calculator', 'calculator', {'fa': '/dial-practical/', 'en': '/en/calculator/', 'ar': '/arabic/الحوسبة/'},
        calc['summary']['fa'], calc['summary']['en'], calc['summary']['ar'],
        'calculator water cost hours 15000 co2 dial-practical صرفه')
    csr = kb['csr']
    add('csr', 'csr', {'fa': '/csr/', 'en': '/en/csr/', 'ar': '/arabic/csr/'},
        csr['summary']['fa'], csr['summary']['en'], csr['summary']['ar'],
        'zagros oak tree csr نجات زاگرس بلوط')
    for item in kb['faq']:
        add(item['id'], 'faq', item['url'],
            item['question']['fa'] + '\n' + item['answer']['fa'],
            (item['question']['en'] + '\n' + item['answer']['en']) if item['answer']['en'] else '',
            (item['question']['ar'] + '\n' + item['answer']['ar']) if item['answer']['ar'] else '',
            item['group'])
    for flow in kb['support']['flows']:
        add(flow['id'], 'support', flow['url'],
            flow['question']['fa'] + '\n' + flow['answer']['fa'],
            flow['question']['en'] + '\n' + flow['answer']['en'],
            flow['question']['ar'] + '\n' + flow['answer']['ar'],
            ' '.join(flow.get('keywords') or []))
    return rows


def build():
    pages = json.loads((DATA / 'pages.json').read_text(encoding='utf-8'))
    about = json.loads((DATA / 'about_copy.json').read_text(encoding='utf-8'))
    names = json.loads((SITE / 'zagros-names/names.json').read_text(encoding='utf-8'))
    centres = len({n.strip() for n in names if isinstance(n, str) and n.strip()})
    products = load_products(pages)
    faq = load_faq(pages)
    posts = json.loads((DATA / 'posts.json').read_text(encoding='utf-8'))
    articles = []
    for post in sorted(posts, key=lambda p: p.get('date') or '', reverse=True):
        title = post.get('title') or ''
        if 'استخدام' in title:
            continue
        local = SITE / 'articles' / str(post.get('id')) / 'index.html'
        articles.append({
            'id': post.get('id'),
            'title': title,
            'description': (post.get('desc') or '')[:280],
            'date': post.get('date'),
            'url': f"/articles/{post.get('id')}/" if local.exists() else post.get('url'),
        })
        if len(articles) >= 24:
            break

    company = {
        'legal_name': tri('شرکت دانش‌بنیان مخازن طبی آبادیس', 'Abadis Medical (knowledge-based company)', 'شركة خزانات آباديس الطبية المعرفية'),
        'founding': {
            'authoritative': {
                'company_established_gregorian': 2017,
                'company_established_jalali': 1396,
                'source': 'Live About page (about_copy.json, modified 2026-10-20) and the homepage: the company was established in 2017. Factory lead: factory started in 1397.',
            },
            'earlier_context_on_the_same_about_page': 'Disposable liners have been used in developed countries since the 1990s. In Iran, culture-building began in 2010 through Abzar Darman Persia.',
            'not_used': '1387 / 2008 is not the founding year on the current abadis-med.com About page. This knowledge base does not treat it as a fact.',
        },
        'slogan': {
            'fa': 'ما به اندازه یک سرانگشت اثر می‌گذاریم، به شما، به طبیعت، به جهان',
            'en': 'We make a difference as small as a fingertip — for you, for nature, for the world.',
            'ar': 'نُحدِث أثرًا بقدر رأس إصبع — لك، وللطبيعة، وللعالم.',
            'source': 'Live About hero, SLOGAN_ABOUT in pages_company.py. The CSR page uses the same line.',
        },
        'about_fa_lead': about['fa']['intro'][0],
        'about_en_lead': about['en']['intro'][0],
        'about_ar_lead': about['ar']['intro'][0],
        'about': about,
        'stats': {
            'active_centres_redesign_list': centres,
            'active_centres_note': 'Homepage impact counter is data-impact-stat="1284". 612 is not the current homepage figure.',
            'users': 11112,
            'satisfaction_percent': 98.99,
            'failure_percent': 0.0018,
            'annual_liner_capacity': '5 million',
            'domestic_liner_share_about_page': 'about 90 percent',
            'provinces_about_page': 28,
            'customers_about_page': 'more than 1000',
            'source': 'Homepage impact counters and the 2026-10-20 About page. The figures are not interchangeable.',
        },
        'contact': {
            'phones': ['02192001017', '02122671845', '02122205502', '02122215503', '02122218910'],
            'fax': '02141425555 | داخلی 28544',
            'extensions': {'management': '12', 'sales': '11', 'finance': '32'},
            'email': 'info@abadis-med.com',
            'whatsapp': 'https://wa.me/989100145809',
            'hq': {
                'fa': 'ایران، تهران، قیطریه، خیابان اندرزگو، پلاک 104، واحد2',
                'en': 'Iran, Tehran, Qeytarieh, Andarzgoo St., No. 104, Unit 2',
                'postal': '1935839683',
                'neshan': 'https://neshan.org/maps/places/9399a4513b6974a287127c06bd9269b9',
                'google_maps': 'https://www.google.com/maps/search/?api=1&query=35.79866,51.44826',
            },
            'factory': {
                'fa': 'ایران،تهران،شهرک صنعتی شمس آباد، بلوار گلستان، کوچه گلشن ۱۹،پلاک۱۷',
                'en': 'Iran, Tehran, Shamsabad Industrial Town, Golestan Blvd, Golshan 19, No. 17',
                'postal': '1834165776',
            },
        },
        'contact_blurb': tri(
            'مرکز تماس ۰۲۱۹۲۰۰۱۰۱۷، فروش داخلی ۱۱، واتس‌اپ +۹۸۹۱۰۰۱۴۵۸۰۹، info@abadis-med.com. دفتر: قیطریه، اندرزگو، پلاک ۱۰۴، واحد ۲. کارخانه: شمس‌آباد، گلستان، گلشن ۱۹، پلاک ۱۷.',
            'Call centre 02192001017, sales extension 11, WhatsApp +989100145809, info@abadis-med.com. Office: Qeytarieh, Andarzgoo, No. 104, Unit 2. Factory: Shamsabad, Golestan, Golshan 19, No. 17.',
            'مركز الاتصال 02192001017، المبيعات التحويلة 11، واتساب +989100145809، info@abadis-med.com. المكتب: قيطريه، أندرزغو، رقم 104، وحدة 2. المصنع: شمس آباد، گلستان، گلشن 19، رقم 17.',
        ),
    }

    kb = {
        'meta': {
            'title': 'Core Abadis Knowledge Base',
            'version': '2026-10-26',
            'source_of_truth': 'https://abadis-med.com for pages that already exist (About, products, certificates, contact). Approved redesign specs fill new sections and are labelled.',
            'languages': ['fa', 'en', 'ar'],
        },
        'company': company,
        'catalog': categories(products),
        'product_pages': products,
        'solutions': solutions_block(),
        'calculator': {
            'id': 'dial-practical',
            'url': {'fa': '/dial-practical/', 'en': '/en/calculator/', 'ar': '/arabic/الحوسبة/'},
            'cap_surgeries': 15000,
            'includes_co2': False,
            'co2_decision': 'Alireza: the calculator does not report CO₂.',
            'outputs': ['water_litres', 'wash_and_disinfectant_cost_toman', 'staff_hours'],
            'not_numeric': [
                'CO₂',
                'plastic mass',
                'infectious-waste volume — named in the homepage teaser, not a dial-practical output',
            ],
            'usd_toman_fallback': 269500,
            'usd_source': 'https://api.tgju.org/v1/market/indicator/today-table-data/price_dollar_rl',
            'formulas': {
                'surgery': {
                    'inputs': {'n': 'surgeries per year, step 100, max 15000'},
                    'water_litres': 'n * 1.6 * 9.971',
                    'cost_toman': 'n * 2.5 * usd_toman',
                    'staff_hours': 'n * 1.6 * 2.2 * 7.1 / 60',
                },
                'beds': {
                    'inputs': {'a': 'OR beds, max 700', 'b': 'ICU beds, max 700'},
                    'water_litres': '((a * 254) + (b * 67)) * 1.6 * 9.971',
                    'cost_toman': '((a * 254) + (b * 65)) * 2.5 * usd_toman',
                    'staff_hours': '((a * 254) + (b * 67)) * 1.7 * 2.2 * 7.1 / 60',
                },
            },
            'constants_note': 'Comment in site/assets/dial/abadis-common.js: water × 9.971; surgery staff 1.6; beds cost OR 254 / ICU 65; beds staff 1.7.',
            'summary': tri(
                'محاسبه‌گر دایال عملی تا ۱۵٬۰۰۰ عمل در سال. خروجی: لیتر آب، تومان هزینه شست‌وشو و ضدعفونی، ساعت کادر درمان. بدون CO₂ و بدون کیلوگرم پلاستیک.',
                'The dial-practical calculator caps at 15,000 surgeries a year. Outputs: litres of water, toman of wash and disinfectant cost, staff hours. No CO₂ and no plastic kilograms.',
                'حاسبة dial-practical حتى ١٥٬٠٠٠ عملية في السنة. المخرجات: لترات الماء، وكلفة الغسل والتعقيم بالتومان، وساعات الطاقم. بلا CO₂ وبلا كيلوغرامات بلاستيك.',
            ),
        },
        'csr': {
            'name': tri('نجات زاگرس', 'Save Zagros', 'إنقاذ زاغروس'),
            'summary': tri(
                'در ۱۳۹۵ بیش از ۷۵ آتش‌سوزی حدود ۹۵۰ هکتار از جنگل زاگرس را از بین برد. آبادیس با ایده‌پردازان نواندیش فردا (Dpaper) به ازای هر عضو خانواده مراکز درمانی (آن زمان بیش از ۴۰۰ مرکز) یک نهال بلوط کاشت و هدف ۱۰۰۰ نهال تا اردیبهشت ۱۴۰۳ بود. ۱۵ اسفند ۱۴۰۲ همایش نجات زاگرس با حدود ۸۰۰ شرکت‌کننده. ۳۰ تیر ۱۴۰۳ کارزار درخواست نجات زاگرس. دیوار افتخار بیمارستان‌ها: /zagros-names/4-mix/. گونه بلوط ایرانی در صفحه زنده نام برده نشده است.',
                'In 1395 more than 75 fires destroyed about 950 hectares of Zagros forest. With Dpaper, Abadis planted one oak per member of its family of care centres (then 400+) and aimed at 1,000 saplings by Ordibehesht 1403. The 15 Esfand 1402 conference had about 800 participants. On 30 Tir 1403 Abadis signed the Save Zagros campaign. Hospital wall of honour: /zagros-names/4-mix/. The live page does not name Quercus brantii.',
                'في ١٣٩٥ دمّر أكثر من ٧٥ حريقًا نحو ٩٥٠ هكتارًا من غابات زاغروس. زرعت آباديس مع Dpaper بلوطة عن كل مركز في عائلتها (أكثر من ٤٠٠ حينها) بهدف ١٠٠٠ غرسة حتى أرديبهشت ١٤٠٣. مؤتمر ١٥ اسفند ١٤٠٢ بنحو ٨٠٠ مشارك. جدار التكريم: /zagros-names/4-mix/.',
            ),
            'wall_of_honor': '/zagros-names/4-mix/',
            'url': {'fa': '/csr/', 'en': '/en/csr/', 'ar': '/arabic/csr/'},
            'source': 'https://abadis-med.com/نجات-زاگرس،مسئولیت-اجتماعی-آبادیس/ and docs/abadis/redesign-context/ZAGROS-CSR.md',
        },
        'certificates': {
            'order': [
                {'id': 'imed', 'title': tri('IMED', 'IMED', 'IMED')},
                {'id': 'patent', 'title': tri('ثبت اختراع', 'Patents', 'براءات الاختراع')},
                {'id': 'operate', 'title': tri('پروانه بهره‌برداری و ISO 13485 / GMP', 'Operating licences and ISO 13485 / GMP', 'رخصة التشغيل و ISO 13485 / GMP')},
                {'id': 'awards', 'title': tri('جوایز و مقالات', 'Awards and publications', 'الجوائز والمقالات')},
            ],
            'footer_strip': 'CE · ISO 13485:2016 · IMED',
            'note': 'Display order on About is IMED, patents, operating licence, awards (pages_company.CERT_GROUPS). The filename router currently files ISO*, CE, export and IMED images into the IMED bucket and operating-licence filenames into operate. ISO 13485 is named on the footer strip. Do not invent certificate numbers.',
            'url': {'fa': '/about/#certs', 'en': '/en/about-us/', 'ar': '/arabic/من-نحن/'},
        },
        'academy': {
            'status': 'mock-shell-plus-live-articles',
            'note': tri(
                'پوسته آکادمی در /academy/ نمونه رابط است و دوره واقعی ندارد. آموزش منتشرشده، مقالات و راهنمای نصب و پرسش‌های متداول است.',
                'The /academy/ shell is a mock interface and has no live course. Published education is the articles archive, the install guide and the FAQ.',
                'واجهة /academy/ نموذج تجريبي بلا دورة فعلية. التعليم المنشور هو المقالات ودليل التركيب والأسئلة الشائعة.',
            ),
            'url': {'fa': '/articles/', 'en': '/en/blog/', 'ar': '/arabic/'},
            'articles': articles,
        },
        'faq': faq,
        'support': {
            'flows': [
                {
                    'id': 'flow-tender',
                    'keywords': ['tender', 'مناقصه', 'procurement', 'خرید', 'proforma'],
                    'question': tri('برای مناقصه و خرید بیمارستانی از کجا شروع کنیم؟', 'Where does a hospital tender or purchase start?', 'من أين يبدأ شراء المستشفى أو المناقصة؟'),
                    'answer': tri(
                        '۱) فرم ارتباط با ما یا تماس با فروش، داخلی ۱۱، شماره ۰۲۱۹۲۰۰۱۰۱۷. ۲) تأیید پیش‌فاکتور. ۳) واریز. ۴) ارسال. کاتالوگ در مرکز دانلود است. کد کالاها در پرسش‌های متداول جدول شده‌اند.',
                        '1) Contact form or sales, extension 11, 02192001017. 2) Confirm the proforma. 3) Pay. 4) Dispatch. Catalogues are in Downloads. Product codes are tabulated on the FAQ.',
                        '١) نموذج الاتصال أو المبيعات، التحويلة 11، الرقم 02192001017. ٢) اعتماد الفاتورة الأولية. ٣) الدفع. ٤) الشحن. الكتالوجات في مركز التنزيل. رموز المنتجات في الأسئلة الشائعة.',
                    ),
                    'url': {'fa': '/contact/', 'en': '/en/contact-us/', 'ar': '/arabic/اتصل-بنا/'},
                },
                {
                    'id': 'flow-distributor',
                    'keywords': ['distributor', 'نماینده', 'نمایندگی', 'dealer'],
                    'question': tri('چطور نماینده یا پوشش استانی را پیدا کنیم؟', 'How do I find a distributor?', 'كيف أجد الممثل؟'),
                    'answer': tri(
                        'لیست نمایندگان در /dealers/ است. برای استان بدون نماینده، با شرکت تماس بگیرید.',
                        'The distributor list is at /en/representatives/. For a province without a distributor, call the company.',
                        'قائمة الممثلين في صفحة الممثلين. للمحافظة بلا ممثل، اتصلوا بالشركة.',
                    ),
                    'url': {'fa': '/dealers/', 'en': '/en/representatives/', 'ar': '/arabic/قائمة-الممثلين/'},
                },
                {
                    'id': 'flow-sample',
                    'keywords': ['sample', 'نمونه', 'demo'],
                    'question': tri('درخواست نمونه چطور ثبت می‌شود؟', 'How do I request a sample?', 'كيف أطلب عيّنة؟'),
                    'answer': tri(
                        'فرم ارتباط با ما، یا تماس با واحد نصب و راه‌اندازی. این عین متن پرسش متداول سایت است.',
                        'Use the contact form, or call the installation and commissioning unit. That is the live FAQ wording.',
                        'عبر نموذج اتصل بنا أو بالاتصال بوحدة التركيب والتشغيل. هذا نص الأسئلة الشائعة.',
                    ),
                    'url': {'fa': '/contact/', 'en': '/en/contact-us/', 'ar': '/arabic/اتصل-بنا/'},
                },
                {
                    'id': 'flow-sizing',
                    'keywords': ['size', '1l', '2l', '3l', 'حجم', 'لیتر', 'sizing'],
                    'question': tri('کدام حجم کیسه را انتخاب کنیم؟', 'Which liner volume should we choose?', 'أي سعة كيس نختار؟'),
                    'answer': tri(
                        '۱ لیتر برای آمبولانس، دندانپزشکی، چشم و کودکان. ۲ لیتر برای آندوسکوپی، گوارش، ICU و اورژانس. ۳ لیتر برای اتاق عمل و جراحی‌های با حجم مایع بیشتر. کیسه باید با سایز مخزن یکی باشد وگرنه از گارانتی خارج می‌شود.',
                        '1 L for ambulance, dentistry, eyes and children. 2 L for endoscopy, gastroenterology, ICU and emergency. 3 L for the operating room and higher fluid volumes. The liner must match the canister size or the warranty is void.',
                        '١ لتر للإسعاف والأسنان والعيون والأطفال. ٢ لتر للتنظير والجهاز الهضمي وICU والطوارئ. ٣ لتر للعمليات والحجوم الأكبر. يجب أن يطابق الكيس حجم الخزان وإلا سقط الضمان.',
                    ),
                    'url': {'fa': '/products/suction-bag/', 'en': '/en/products/suction-bag/', 'ar': '/arabic/كيس-الشفط/'},
                },
            ],
            'ctas': {
                'quote': {'fa': '/contact/', 'en': '/en/contact-us/', 'ar': '/arabic/اتصل-بنا/'},
                'catalogue': {'fa': '/downloads/', 'en': '/en/center-download/', 'ar': '/arabic/مركز-التنزيل/'},
                'phone': 'tel:+982192001017',
                'whatsapp': 'https://wa.me/989100145809',
            },
        },
        'social': {
            'instagram_homepage_footer': 'https://www.instagram.com/abadis.med/',
            'instagram_contact_pages_and_redesign_footer': 'https://www.instagram.com/abadismedical.co',
            'linkedin': 'https://www.linkedin.com/company/abadis-medical-co/',
            'facebook_short': 'https://fb.com/AbadisMedCo',
            'facebook_canonical_also_on_homepage': 'https://www.facebook.com/AbadisMedCo/',
            'pinterest': None,
            'pinterest_note': 'No profile URL in the live FA, EN or AR HTML fetched 2026-10-26. Placeholder only.',
        },
    }
    kb['chunks'] = chunks_from(kb)
    return kb


def md_escape(text):
    return (text or '').replace('\r', '')


def render_md(kb):
    lines = []
    w = lines.append
    w('# Core Abadis Knowledge Base')
    w('')
    w('Version **2026-10-26**. Machine-readable twin: `site/assets/data/abadis-knowledge-base.json` (same file also at `docs/knowledge-base/abadis-knowledge-base.json`). The chatbot also keeps `site/assets/chatbot/kb-fallback.js`, the same JSON on `window.ABADIS_KB`, for `file://` and a cache that cannot fetch the JSON. Section 8 is the Iran intranet engine.')
    w('')
    w('**Source of truth.** For pages that already exist — About, products, certificates, contact — [abadis-med.com](https://abadis-med.com) wins. New sections use the approved redesign (solutions philosophy, dial-practical calculator, Zagros CSR) and are labelled. Figures below are copied, not improved.')
    w('')
    w('## 1. Company profile and About')
    w('')
    c = kb['company']
    w(f"- **Name:** {c['legal_name']['fa']} / {c['legal_name']['en']}")
    w(f"- **Established:** {c['founding']['authoritative']['company_established_gregorian']} / {c['founding']['authoritative']['company_established_jalali']}. {c['founding']['authoritative']['source']}")
    w(f"- **Not used as a founding date:** {c['founding']['not_used']}")
    w(f"- **Earlier context on the same About page:** {c['founding']['earlier_context_on_the_same_about_page']}")
    w(f"- **Slogan (live About hero):** {c['slogan']['fa']}")
    w(f"- **EN gloss:** {c['slogan']['en']}")
    w(f"- **AR gloss:** {c['slogan']['ar']}")
    w('')
    w(c['about_fa_lead'])
    w('')
    w(c['about_en_lead'])
    w('')
    w('### Mission, vision, history')
    w('')
    w('The full FA / EN / AR About text approved on 2026-10-20 is embedded in the JSON under `company.about` (mission, vision, three strategic pillars, achievements, three history phases, commitment, goals). It is not shortened here.')
    w('')
    s = c['stats']
    w('### Stats (do not merge these rows)')
    w('')
    w(f"| Figure | Value | Source |")
    w(f"| --- | --- | --- |")
    w(f"| Active centres on the redesign customers list | {s['active_centres_redesign_list']} | zagros-names/names.json |")
    w(f"| Live homepage counter on 2026-10-24 | 612 | {s['active_centres_note']} |")
    w(f"| Users | {s['users']} | homepage impact row |")
    w(f"| Satisfaction | {s['satisfaction_percent']}% | homepage impact row |")
    w(f"| Product failure | {s['failure_percent']}% | homepage impact row |")
    w(f"| Annual liner capacity | {s['annual_liner_capacity']} | homepage factory lead, factory year 1397 |")
    w(f"| Domestic liner share | {s['domestic_liner_share_about_page']} | About page 2026-10-20 |")
    w(f"| Provinces | {s['provinces_about_page']} | About page |")
    w(f"| Customers on the About page | {s['customers_about_page']} | About page |")
    w('')
    contact = c['contact']
    w('### Contact')
    w('')
    w(f"- Phones: {', '.join(contact['phones'])}")
    w(f"- Fax: {contact['fax']}")
    w(f"- Extensions: management {contact['extensions']['management']}, sales {contact['extensions']['sales']}, finance {contact['extensions']['finance']}")
    w(f"- Email: {contact['email']}")
    w(f"- WhatsApp: {contact['whatsapp']}")
    w(f"- Tehran office: {contact['hq']['fa']} — postal {contact['hq']['postal']}")
    w(f"- Neshan: {contact['hq']['neshan']}")
    w(f"- Google Maps: {contact['hq']['google_maps']}")
    w(f"- Factory: {contact['factory']['fa']} — postal {contact['factory']['postal']}")
    w('')
    w('## 2. Product categories and catalog')
    w('')
    w('Eight headings for the meeting. A heading is a catalog line only when `status` says so. Urology, gynecology and gastroenterology are published **use sites** of the suction liner, not extra SKUs.')
    w('')
    for cat in kb['catalog']:
        w(f"### {cat['title']['en']} — {cat['title']['fa']}")
        w('')
        w(f"- Status: `{cat['status']}`")
        if cat['volumes']:
            w(f"- Volumes / sizes: {', '.join(cat['volumes'])}")
        w(f"- FA: {cat['summary']['fa']}")
        w(f"- EN: {cat['summary']['en']}")
        w(f"- AR: {cat['summary']['ar']}")
        w(f"- Applications: {cat['applications']['en']}")
        links = ', '.join(f"{item['fa']}" for item in cat['links'])
        w(f"- Links (FA): {links}")
        w('')
    w('Full Persian product-page text (headings, tables, uses) is in JSON `product_pages`, taken from the live page snapshots.')
    w('')
    w('## 3. Clinical solutions')
    w('')
    w('Dual path: **by product** (specs, real photos, enquiry) and **by solution** (problem, technology, advantage, result). Four pillars: Products, Solutions, Applications, Innovation.')
    w('')
    sol = kb['solutions']
    for pillar in sol['pillars']:
        w(f"- **{pillar['title']['en']} / {pillar['title']['fa']}.** {pillar['question']['en']}")
    w('')
    for area in sol['areas']:
        w(f"### {area['title']['en']}")
        w('')
        w(area['lead']['en'])
        w('')
        for p in area['body']:
            w(p['en'])
            w('')
        w(f"FA title: {area['title']['fa']}. AR title: {area['title']['ar']}.")
        w('')
    w('OR efficiency and ICU care are application contexts of fluid management (see JSON `application_contexts_without_own_page`). They do not have their own solution URL.')
    w('')
    w('## 4. Savings calculator and Save Zagros')
    w('')
    calc = kb['calculator']
    w(calc['summary']['en'])
    w('')
    w(f"- Surgery cap: **{calc['cap_surgeries']}**.")
    w(f"- CO₂: **not included.** {calc['co2_decision']}")
    w('- Plastic mass and infectious-waste volume are **not** numeric outputs. The homepage teaser mentions infectious-waste savings; dial-practical does not compute them.')
    w(f"- Surgery water (litres): `{calc['formulas']['surgery']['water_litres']}`")
    w(f"- Surgery cost (toman): `{calc['formulas']['surgery']['cost_toman']}`")
    w(f"- Surgery staff hours: `{calc['formulas']['surgery']['staff_hours']}`")
    w(f"- Beds water: `{calc['formulas']['beds']['water_litres']}`")
    w(f"- Beds cost: `{calc['formulas']['beds']['cost_toman']}`")
    w(f"- Beds hours: `{calc['formulas']['beds']['staff_hours']}`")
    w(f"- USD fallback: {calc['usd_toman_fallback']} toman, then TGJU.")
    w(f"- Page: {calc['url']['fa']}")
    w('')
    w('### Save Zagros')
    w('')
    w(kb['csr']['summary']['en'])
    w('')
    w(f"Wall of honour: `{kb['csr']['wall_of_honor']}`")
    w('')
    w('## 5. Certificates, licences and awards')
    w('')
    w('Approved order:')
    w('')
    for i, group in enumerate(kb['certificates']['order'], 1):
        w(f"{i}. {group['title']['fa']} / {group['title']['en']}")
    w('')
    w(f"Footer strip only: {kb['certificates']['footer_strip']}.")
    w('')
    w(kb['certificates']['note'])
    w('')
    w('## 6. Abadis Academy and news')
    w('')
    w(kb['academy']['note']['en'])
    w('')
    w('Recent article titles (redesign archive, titles verbatim):')
    w('')
    for art in kb['academy']['articles']:
        w(f"- [{art['title']}]({art['url']})")
    w('')
    w('## 7. FAQ, sales configurator and support')
    w('')
    w(f"Live FAQ: **{len(kb['faq'])}** pairs from the Persian FAQ page. EN/AR on the short answers are translations of that Persian text (`translation: translated-from-fa-faq`). The vehicle-load table and the product-code table stay verbatim in Persian.")
    w('')
    for item in kb['faq']:
        if item['translation'] == 'fa-table-verbatim':
            w(f"### {item['question']['fa']}")
            w('')
            w('Long published table — see JSON `faq` and `/faq/`.')
            w('')
            continue
        w(f"### {item['question']['fa']}")
        w('')
        w(item['answer']['fa'])
        w('')
        if item['answer']['en']:
            w(f"**EN.** {item['question']['en']} {item['answer']['en']}")
            w('')
            w(f"**AR.** {item['question']['ar']} {item['answer']['ar']}")
            w('')
    w('### Support flows')
    w('')
    for flow in kb['support']['flows']:
        w(f"- **{flow['question']['en']}** {flow['answer']['en']}")
    w('')
    w('CTAs: contact form, downloads (catalogue), `tel:+982192001017`, WhatsApp `https://wa.me/989100145809`.')
    w('')
    w('## 8. Iran intranet engine (شبکه ملی اطلاعات)')
    w('')
    w('Hamid’s requirement: if filtering leaves only Iran’s National Information Network, the sales and academy chatbot must still answer. The engine is part of the site core. It does not load Google Fonts, jsDelivr, unpkg, Cloudflare, or any other foreign script or stylesheet. Kalameh is the set already in `site/assets/fonts/`. Icons in the widget are inline SVG.')
    w('')
    w('Files:')
    w('')
    w('- `site/assets/chatbot/chatbot.js` — widget, BM25 retrieval, synonym expansion, sales intent, and answer synthesis.')
    w('- `site/assets/data/abadis-knowledge-base.json` — same-origin knowledge base. This is the copy the widget fetches first.')
    w('- `site/assets/chatbot/kb-fallback.js` — that same JSON assigned to `window.ABADIS_KB`. The widget loads this sibling file only when the JSON fetch fails.')
    w('- `site/chatbot-demo/index.html` — meeting page, with the badge, the tier switch, and the international-cut-off toggle.')
    w('')
    w('Three tiers. Tier 1 is the default and does not leave the site.')
    w('')
    w('1. **Tier 1 — موتور بومی داخل هسته سایت.** BM25 over the chunks, plus synonym groups (Persian, English, Arabic) and the sales intent rules (solution, product, volume, savings). The answer is synthesized from the winning chunk and cites the on-site page. No API key and no foreign host.')
    w('2. **Tier 2 — optional domestic model.** A URL the hospital or Abadis hosts inside Iran, for example `/api/chat` on Liara, on abadis-med.com, or an on-prem Ollama or vLLM. The call uses a 2.5 second timeout. If it fails, the Tier 1 answer stays on screen.')
    w('3. **Tier 3 — optional international model.** An OpenAI-style chat-completions URL and a session key. Same 2.5 second timeout. If the request is blocked, times out, or the demo toggle «شبیه‌سازی قطع اینترنت بین‌الملل» is on, the widget does not wait on that host: the Tier 1 answer is already shown, and the foreign request is skipped while the toggle is on.')
    w('')
    w('The widget header and `/chatbot-demo/` show this badge: **موتور داخلی هسته سایت (فعال در شبکه ملی اطلاعات / بدون نیاز به اینترنت بین‌الملل)** — Core On-Site Engine, 100% Iran intranet resilient.')
    w('')
    return '\n'.join(lines) + '\n'


def main():
    kb = build()
    raw = json.dumps(kb, ensure_ascii=False, indent=2)
    for path in OUT_JSON:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(raw, encoding='utf-8')
        print(path, len(raw))
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text(render_md(kb), encoding='utf-8')
    print(OUT_MD, 'faq', len(kb['faq']), 'chunks', len(kb['chunks']))
    OUT_FALLBACK.parent.mkdir(parents=True, exist_ok=True)
    # JSON is valid JS except U+2028/U+2029, which would break a script.
    literal = raw.replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
    OUT_FALLBACK.write_text(
        '/* Same-origin copy of the knowledge base. The chatbot loads this file only when '
        'fetch of abadis-knowledge-base.json fails (file:// or a strict cache). Not a CDN. */\n'
        'window.ABADIS_KB = ' + literal + ';\n',
        encoding='utf-8',
    )
    print(OUT_FALLBACK, OUT_FALLBACK.stat().st_size)


if __name__ == '__main__':
    main()
