#!/usr/bin/env python3
"""Second half of the EN/AR parity apply: install, about, bag, articles, PVA, hubs, redirects."""
import html as H
import json
import re
import shutil
from pathlib import Path
from parity_apply import SITE, LIVE, V, read, write, replace_main, set_meta
import team_order

ROOT = SITE.parent

def deepen(html, extra='../'):
    """Add one ../ to root-relative asset and page links that already start with ../"""
    return html.replace('href="../', 'href="../' + extra).replace('src="../', 'src="../' + extra)

def clone_shell(src, dest, depth_add=0):
    s = read(src)
    if depth_add:
        s = deepen(s)
    write(dest, s)
    return dest

# ---------------------------------------------------------------- install
INSTALL_EN = {
 'راهنمای نصب مخازن': 'Canister installation',
 'نحوه نصب بر روی پایه پرتابل': 'Installation on a portable stand',
 'نحوه نصب بر روی کنسول': 'Installation on a console',
 'نحوه نصب بر روی پایه ترولی': 'Installation on a trolley stand',
 'توضیحات': 'Notes',
 'مرحله 1': 'Step 1', 'مرحله 2': 'Step 2', 'مرحله 3': 'Step 3', 'مرحله 4': 'Step 4', 'مرحله 5': 'Step 5',
 'برای نصب بر روی دستگاه پرتابل به نوع و مدل دستگاه باید توجه شود غالب دستگاه های استفاده شده در مراکز درمانی دستگاه های مدلا و صا ایران می باشد که دارای یک پروفیل در زیر قسمت موتور دستگاه ها می باشد . شرکت مخازن طبی آبادیس برای نصب مخازن های ساکشن یک نوع گیره پرتابل طراحی نموده که بر روی پروفیل این نوع دستگاه ها نصب می شود و نحوه نصب آن مرحله به مرحله توضیح داده شده است.':
  'The model of the portable unit matters. Most units in healthcare centres (Medela and Sa Iran) have a rail under the motor. Abadis Medical Reservoirs designed one portable bracket that mounts on that rail. The steps below show how.',
 'گیره پرتابل از دو قسمت تشکیل شده که با دو پیچ سایز M4 به هم متصل می شود.':
  'The portable bracket is two parts, joined by two M4 screws.',
 'پروفیل دستگاه های پرتابل مابین این دو قسمت قرار می گیرد و با سفت کردن پیچ ها گیره بر روی پروفیل دستگاه پرتابل فیکس می شود.':
  'The portable unit’s rail sits between the two parts. Tightening the screws fixes the bracket to the rail.',
 'سپس بر روی مخزن های دو و سه لیتری اتصال T و کانکشن را متصل میکنیم.':
  'On the 2-litre and 3-litre canisters, fit the T connector and the connection.',
 'در این مرحله از خروجی دستگاه پرتابل تا اتصال T شکل در مخزن های دو و سه و کانکتور وکیوم در مخزن های یک سایز می کنیم و شلنگ سیلیکونی سایز 13*7 را برش زده یک سمت شلنگ را به خروجی دستگاه ساکشن پرتابل و سمت دیگر را به اتصال T شکل در مخزن های دو و سه و کانکتور وکیوم در مخزن های یک وصل می کنیم.':
  'Measure from the portable unit outlet to the T connector on 2- and 3-litre canisters, or to the vacuum connector on 1-litre canisters. Cut 13×7 silicone tubing. Connect one end to the portable suction outlet and the other to the T connector or the vacuum connector.',
 'برای تست عدم نشتی وکیوم خروجی دستگاه ساکشن پرتابل را کین می کنیم تا حداکثر میزان فشار منحنی را بسنجیم سپس با بستن مسیر وکیوم مخزن ( سوراخ داخل مخزن و کانکتور وکیوم) اگر به میزان حداکثر فشار وکیوم دستگاه ساکشن پرتابل پر شود در اتصالات نصب شده هیچ گونه نشتی وجود ندارد.':
  'To check for leaks, close the portable unit outlet and read the maximum vacuum. Then close the canister vacuum path (the hole inside the canister and the vacuum connector). If the gauge still reaches the unit’s maximum vacuum, the joints do not leak.',
 'بر روی کنسول فلزی ابتدا گیره دیواری را در قسمت مناسب قرار داده تا زمانی که مخزن را روی گیره سوار می کنیم فضای کافی برای تعویض کیسه ها داشته باشد.':
  'On a metal console, place the wall bracket where the canister will still leave enough room to change bags.',
 'بعد از پیدا کردن قسمت مناسب گیره دیواری سوراخ های داخل گیره ها را با یک مارکر علامت می زنیم برای سوراخ کردن کنسول فلزی که غالبا از جنس آلومینیوم است از پیچ سر مته ۱۵ میلی متر استفاده می کنیم که اگر لوله های مسی سیالات پشت کنسول از قسمت نا مناسب رد شده بود سوراخ نشود و همچنین باعث نشتی نگردد.':
  'Mark the bracket holes. Consoles are usually aluminium; use a 15 mm self-drilling screw so you do not pierce copper fluid lines behind the console or cause a leak.',
 'بعد از نصب گیره اگر مخزن دو و سه لیتری نصب می شود اتصال Tو کانکشن را روی مخزن سوار میکنیم.':
  'After the bracket is fixed, fit the T connector and the connection if you are mounting a 2- or 3-litre canister.',
 'مرحله بعد مخزن ها را روی گیره به صورت کشویی از قسمت بالا روی گیره سوار میکنیم.':
  'Slide the canisters onto the bracket from the top.',
 'بعد از نصب، از خروجی وکیوم ( غالبا از رگولاتور استفاده می شود) تا مخزن ساکشن را سایز میکنیم و شلنگ سیلیکونی سایز 13*7 را برش زده از یک سمت به خروجی وکیوم و طرف دیگر شلنگ را در صورت نصب مخزن دو و سه لیتری به اتصال T شکل و در صورت نصب مخزن یک لیتری به کانکشن وکیوم آبادیس وصل میکنیم.':
  'Measure from the vacuum outlet (usually a regulator) to the canister. Cut 13×7 silicone tubing. One end goes to the vacuum outlet. The other goes to the T connector on a 2- or 3-litre canister, or to the Abadis vacuum connection on a 1-litre canister.',
 'ابتدا محل حدودی قرار بگیری پایه ترولی در اتاق عمل را تعیین می کنیم و از خروجی وکیوم تا پایه ترولی را سایز کرده و شلنگ سیلیکونی ۱۳*۷ را برش می زنیم.':
  'Decide where the trolley will stand in the operating room. Measure from the vacuum outlet to the trolley and cut 13×7 silicone tubing.',
 'یک قسمت شلنگ به خروجی وکیوم و سمت دیگر را به ورودی رگولاتور یا شیر نصب شده بر روی پایه ترولی نصب می کنیم .':
  'Connect one end of the tubing to the vacuum outlet and the other to the regulator or valve on the trolley.',
 'بر روی مخزن های دو و سه لیتری اتصال T و کانکشن را متصل می کنیم از خروجی رگولاتور تا اتصال T شکل در مخزن های دو و سه لیتری و کانکشن وکیوم درمخزن های یک لیتری سایز میکنیم .':
  'Fit the T connector and the connection on 2- and 3-litre canisters. Measure from the regulator outlet to the T connector, or to the vacuum connection on a 1-litre canister.',
 'شلنگ سیلیکونی سایز13*7 را برش زده یک سمت شلنگ را به خروجی رگولاتور یا شیر و سمت دیگر را به اتصال T شکل درمخزن های دو و سه لیتری و کانکشن وکیوم در مخزن های یک لیتری وصل می کنیم .':
  'Cut 13×7 silicone tubing. One end goes to the regulator or valve outlet. The other goes to the T connector on 2- and 3-litre canisters, or to the vacuum connection on a 1-litre canister.',
 'برای تست عدم نشتی وکیوم خروجی رگولاتور مسیر وکیوم را کین می کنیم تا حداکثر میزان فشار منفی را بسنجیم ، سپس با بستن مسیر وکیوم مخزن ( سوراخ داخل مخزن و کانکشن وکیوم ) اگر به میزان حداکثر فشار وکیوم رگولاتور برسد در اتصالات نصب شده هیچگونه نشتی وجود ندارد.':
  'Close the regulator outlet and read the maximum negative pressure. Then close the canister vacuum path (the hole inside the canister and the vacuum connection). If the gauge still reaches the regulator’s maximum vacuum, the joints do not leak.',
 'خانه': 'Home',
 'راهنمای نصب': 'Installation guide',
 '› راهنمای نصب مخازن': 'Canister installation',
}
INSTALL_AR = {
 'راهنمای نصب مخازن': 'تركيب الخزانات',
 'نحوه نصب بر روی پایه پرتابل': 'التركيب على قاعدة محمولة',
 'نحوه نصب بر روی کنسول': 'التركيب على الكونسول',
 'نحوه نصب بر روی پایه ترولی': 'التركيب على قاعدة الترولي',
 'توضیحات': 'ملاحظات',
 'مرحله 1': 'الخطوة ١', 'مرحله 2': 'الخطوة ٢', 'مرحله 3': 'الخطوة ٣', 'مرحله 4': 'الخطوة ٤', 'مرحله 5': 'الخطوة ٥',
 'خانه': 'الرئيسية',
 'راهنمای نصب': 'دليل التركيب',
}

def _apply_map(text, mp):
    for a, b in sorted(mp.items(), key=lambda x: -len(x[0])):
        text = text.replace(a, b)
    return text

def _videos(lang):
    labels = {
        'en': [('Portable', 'LiEf2'), ('Single', 'Nc7hg'), ('Series', 'Yp2bl')],
        'ar': [('محمول', 'LiEf2'), ('مفرد', 'Nc7hg'), ('متسلسل', 'Yp2bl')],
    }[lang]
    note = {
        'en': 'Videos are loaded from the Abadis Aparat channel.',
        'ar': 'تُحمَّل الفيديوهات من قناة آباديس على Aparat.',
    }[lang]
    cards = ''.join(
        f'<div class="reveal"><h2 style="font-size:1.3rem;margin-bottom:12px">{lab}</h2>'
        f'<div class="video-frame"><iframe src="https://www.aparat.com/video/video/embed/videohash/{code}/vt/frame" '
        f'title="{H.escape(lab)}" loading="lazy" allowfullscreen referrerpolicy="no-referrer-when-downgrade"></iframe></div></div>'
        for lab, code in labels)
    return f'<section class="section"><div class="wrap grid g-3" style="gap:20px">{cards}</div><div class="wrap"><p class="note" style="margin-top:18px">{note}</p></div></section>'

def patch_install():
    # EN hub: point the two self-links at the new subpages, in order
    hub = SITE / 'en/installation-manual/index.html'
    s = read(hub)
    s = s.replace('href="../../en/installation-manual/" role="button"',
                  'href="canister-installation/" role="button"', 1)
    s = s.replace('href="../../en/installation-manual/" role="button"',
                  'href="user-manuals/" role="button"', 1)
    s = s.replace('Canister Installation Manual User Manuals Manual',
                  'Canister installation and end-user manuals for Abadis suction canisters.')
    write(hub, s)
    # build subpages from the hub shell, one level deeper
    for slug, title, desc, body in (
        ('canister-installation', 'Canister installation — Abadis Medical Reservoirs',
         'How to install Abadis suction canisters on a portable stand, a console, and a trolley.', None),
        ('user-manuals', 'End-user manuals — Abadis Medical Reservoirs',
         'End-user videos for Abadis suction bags: portable, single, and series.', _videos('en')),
    ):
        dest = SITE / 'en/installation-manual' / slug / 'index.html'
        clone_shell(hub, dest, depth_add=1)
        if body is None:
            src = read(SITE / 'راهنمای-نصب/راهنمای-نصب-مخازن/index.html')
            main = re.search(r'<main\b[^>]*>.*?</main>', src, re.S).group(0)
            main = _apply_map(main, INSTALL_EN)
            main = deepen(main)
            # crumbs home link
            main = main.replace('href="../../../"', 'href="../../../en/"')
            main = main.replace('href="../../"', 'href="../"')
        else:
            main = f'<main id="main"><section class="page-hero"><div class="wrap"><p class="crumbs"><a href="../../../en/">Home</a> › <a href="../">Installation guide</a> › End-user manuals</p><h1>End-user manuals</h1></div></section>{body}</main>'
        replace_main(dest, main)
        set_meta(dest, title, desc)
        t = read(dest)
        t = t.replace('https://abadis-med.com/en/installation-manual/"',
                      f'https://abadis-med.com/en/installation-manual/{slug}/"')
        write(dest, t)
    # AR subpages
    ar_hub = SITE / 'arabic/دليل-التركيب/index.html'
    # fix doubled على and the Persian دلیل if present, and stop inlining by linking out
    a = read(ar_hub)
    a = a.replace('دلیل الترکیب', 'دليل التركيب').replace('على على', 'على')
    write(ar_hub, a)
    for slug, title, desc, body, h1 in (
        ('تركيب-الخزانات', 'تركيب الخزانات — خزانات طبي آباديس',
         'كيفية تركيب خزانات الشفط آباديس على قاعدة محمولة وكونسول وقاعدة ترولي.', None, 'تركيب الخزانات'),
        ('دليل-المستخدم', 'دليل المستخدم النهائي — خزانات طبي آباديس',
         'فيديوهات استخدام كيس الشفط آباديس: محمول، ومفرد، ومتسلسل.', _videos('ar'), 'دليل المستخدم النهائي'),
    ):
        dest = SITE / 'arabic/دليل-التركيب' / slug / 'index.html'
        clone_shell(ar_hub, dest, depth_add=1)
        if body is None:
            src = read(SITE / 'راهنمای-نصب/راهنمای-نصب-مخازن/index.html')
            main = re.search(r'<main\b[^>]*>.*?</main>', src, re.S).group(0)
            # English map first for the long sentences, then Arabic headings
            main = _apply_map(main, INSTALL_EN)
            # overlay Arabic headings
            overlay = {
                'Canister installation': 'تركيب الخزانات',
                'Installation on a portable stand': 'التركيب على قاعدة محمولة',
                'Installation on a console': 'التركيب على الكونسول',
                'Installation on a trolley stand': 'التركيب على قاعدة الترولي',
                'Notes': 'ملاحظات',
                'Step 1': 'الخطوة ١', 'Step 2': 'الخطوة ٢', 'Step 3': 'الخطوة ٣', 'Step 4': 'الخطوة ٤', 'Step 5': 'الخطوة ٥',
                'Home': 'الرئيسية',
                'Installation guide': 'دليل التركيب',
            }
            # The long sentences are already English from INSTALL_EN. Translate those keys' values into Arabic by a second map.
            main = _apply_map(main, overlay)
            main = _apply_map(main, AR_LONG)
            main = deepen(main)
        else:
            main = f'<main id="main"><section class="page-hero"><div class="wrap"><p class="crumbs"><a href="../../../arabic/">الرئيسية</a> › <a href="../">دليل التركيب</a> › {h1}</p><h1>{h1}</h1></div></section>{body}</main>'
        replace_main(dest, main)
        set_meta(dest, title, desc)
    print('install ok')

# Arabic versions of the long install sentences (applied after the English pass + heading overlay)
AR_LONG = {}

def _fill_ar_long():
    # values of INSTALL_EN that are the long English sentences, paired with Arabic
    pairs = [
        ('The model of the portable unit matters. Most units in healthcare centres (Medela and Sa Iran) have a rail under the motor. Abadis Medical Reservoirs designed one portable bracket that mounts on that rail. The steps below show how.',
         'يُراعى نوع جهاز الشفط المحمول وطرازه. أغلب الأجهزة في المراكز العلاجية (Medela وصا إيران) لها سكة تحت المحرك. صممت خزانات آباديس الطبية قفيصاً محمولاً واحداً يُثبَّت على هذه السكة، وتوضح الخطوات التالية طريقة التركيب.'),
        ('The portable bracket is two parts, joined by two M4 screws.',
         'يتكوّن القفيص المحمول من قطعتين تُربطان ببرغيين مقاس M4.'),
        ('The portable unit’s rail sits between the two parts. Tightening the screws fixes the bracket to the rail.',
         'توضع سكة الجهاز المحمول بين القطعتين، وبشدّ البراغي يُثبَّت القفيص على السكة.'),
        ('On the 2-litre and 3-litre canisters, fit the T connector and the connection.',
         'على خزانات ٢ و٣ لتر نركّب وصلة T والكونكشن.'),
        ('Measure from the portable unit outlet to the T connector on 2- and 3-litre canisters, or to the vacuum connector on 1-litre canisters. Cut 13×7 silicone tubing. Connect one end to the portable suction outlet and the other to the T connector or the vacuum connector.',
         'في هذه الخطوة نقيس من مخرج الجهاز المحمول إلى وصلة T في خزانات ٢ و٣ لتر، أو إلى موصل التفريغ في خزان ١ لتر. نقص خرطوم السيليكون مقاس 13×7. نصل طرفاً بمخرج جهاز الشفط المحمول والطرف الآخر بوصلة T أو بموصل التفريغ.'),
        ('To check for leaks, close the portable unit outlet and read the maximum vacuum. Then close the canister vacuum path (the hole inside the canister and the vacuum connector). If the gauge still reaches the unit’s maximum vacuum, the joints do not leak.',
         'لاختبار عدم التسرّب نغلق مخرج الجهاز المحمول ونقرأ أقصى ضغط تفريغ. ثم نغلق مسار تفريغ الخزان (الفتحة داخل الخزان وموصل التفريغ). إذا بلغ المؤشر أقصى تفريغ الجهاز فلا يوجد تسرّب في الوصلات.'),
        ('On a metal console, place the wall bracket where the canister will still leave enough room to change bags.',
         'على الكونسول المعدني نضع القفيص الجداري في موضع يُبقي مسافة كافية لتبديل الأكياس بعد تركيب الخزان.'),
        ('Mark the bracket holes. Consoles are usually aluminium; use a 15 mm self-drilling screw so you do not pierce copper fluid lines behind the console or cause a leak.',
         'بعد تحديد الموضع نعلّم ثقوب القفيص. الكونسول غالباً من الألومنيوم؛ نستخدم برغي رأس مثقاب ١٥ مم حتى لا نثقب أنابيب النحاس خلف الكونسول ولا نُحدث تسرّباً.'),
        ('After the bracket is fixed, fit the T connector and the connection if you are mounting a 2- or 3-litre canister.',
         'بعد تثبيت القفيص، إذا كان الخزان ٢ أو ٣ لتر نركّب وصلة T والكونكشن على الخزان.'),
        ('Slide the canisters onto the bracket from the top.',
         'ثم نُدخل الخزانات على القفيص انزلاقاً من الأعلى.'),
        ('Measure from the vacuum outlet (usually a regulator) to the canister. Cut 13×7 silicone tubing. One end goes to the vacuum outlet. The other goes to the T connector on a 2- or 3-litre canister, or to the Abadis vacuum connection on a 1-litre canister.',
         'بعد التركيب نقيس من مخرج التفريغ (غالباً عبر منظّم) إلى خزان الشفط. نقص خرطوم سيليكون 13×7. طرف إلى مخرج التفريغ، والطرف الآخر إلى وصلة T لخزان ٢ أو ٣ لتر، أو إلى وصلة تفريغ آباديس لخزان ١ لتر.'),
        ('Decide where the trolley will stand in the operating room. Measure from the vacuum outlet to the trolley and cut 13×7 silicone tubing.',
         'نحدد أولاً موضع قاعدة الترولي التقريبي في غرفة العمليات، ونقيس من مخرج التفريغ إلى القاعدة، ونقص خرطوم السيليكون ١٣×٧.'),
        ('Connect one end of the tubing to the vacuum outlet and the other to the regulator or valve on the trolley.',
         'نصل طرف الخرطوم بمخرج التفريغ والطرف الآخر بمدخل المنظّم أو الصمام المثبَّت على قاعدة الترولي.'),
        ('Fit the T connector and the connection on 2- and 3-litre canisters. Measure from the regulator outlet to the T connector, or to the vacuum connection on a 1-litre canister.',
         'على خزانات ٢ و٣ لتر نركّب وصلة T والكونكشن، ونقيس من مخرج المنظّم إلى وصلة T أو إلى وصلة التفريغ في خزان ١ لتر.'),
        ('Cut 13×7 silicone tubing. One end goes to the regulator or valve outlet. The other goes to the T connector on 2- and 3-litre canisters, or to the vacuum connection on a 1-litre canister.',
         'نقص خرطوم السيليكون 13×7. طرف إلى مخرج المنظّم أو الصمام، والطرف الآخر إلى وصلة T في خزانات ٢ و٣ لتر أو إلى وصلة التفريغ في خزان ١ لتر.'),
        ('Close the regulator outlet and read the maximum negative pressure. Then close the canister vacuum path (the hole inside the canister and the vacuum connection). If the gauge still reaches the regulator’s maximum vacuum, the joints do not leak.',
         'لاختبار عدم التسرّب نغلق مخرج المنظّم ونقرأ أقصى ضغط سالب. ثم نغلق مسار تفريغ الخزان (الفتحة داخل الخزان ووصلة التفريغ). إذا بلغ المؤشر أقصى تفريغ المنظّم فلا يوجد تسرّب في الوصلات.'),
    ]
    AR_LONG.update(dict(pairs))

# ---------------------------------------------------------------- bag glance
def patch_bag():
    import sys
    sys.path.insert(0, str(ROOT / 'tools/redesign'))
    from build_suction_bag_page import glance_i18n
    for lang, path, nav_from, nav_to in (
        ('en', SITE / 'en/products/suction-bag/index.html',
         '<a href="#benefits">Benefits</a>',
         '<a href="#benefits">Benefits</a><a href="#specs">At a glance</a>'),
        ('ar', SITE / 'arabic/كيس-الشفط/index.html',
         '<a href="#benefits">الأثر</a>',
         '<a href="#benefits">الأثر</a><a href="#specs">لمحة</a>'),
    ):
        s = read(path)
        block = glance_i18n(lang, '')
        if 'id="specs"' not in s:
            s = s.replace('<section class="bag-block bag-sizes"', block + '<section class="bag-block bag-sizes"', 1)
        if nav_from in s and '#specs' not in s.split('bag-sub', 1)[-1][:800]:
            s = s.replace(nav_from, nav_to, 1)
        if lang == 'ar':
            s = s.replace('مخازن طبی آباديس', 'خزانات طبي آباديس')
            s = s.replace('<title>كيس الشفط — مخازن طبی آباديس</title>',
                          '<title>كيس الشفط — خزانات طبي آباديس</title>')
        write(path, s)
    set_meta(SITE / 'arabic/كيس-الشفط/index.html', 'كيس الشفط — خزانات طبي آباديس')
    print('bag glance ok')

# ---------------------------------------------------------------- about videos + anchors
VIDEO = {
    'alireza': ('../../assets/team-videos/alireza/team-member-poster.webp',
                '../../assets/team-videos/alireza/team-member.webm',
                '../../assets/team-videos/alireza/team-member.mp4'),
    'navid': ('../../assets/team-videos/navid/team-member-navid-poster.webp',
              '../../assets/team-videos/navid/team-member-navid.webm',
              '../../assets/team-videos/navid/team-member-navid.mp4'),
}

def _clip(label, key):
    poster, webm, mp4 = VIDEO[key]
    return (f'<video class="team-clip" autoplay muted loop playsinline webkit-playsinline '
            f'disablepictureinpicture disableremoteplayback preload="metadata" tabindex="-1" '
            f'poster="{poster}" aria-label="{H.escape(label)}">'
            f'<source src="{webm}" type="video/webm"><source src="{mp4}" type="video/mp4"></video>')

def _swap_photo(html, name, clip_html):
    pat = re.compile(
        r'(<div class="bdt-member-photo">\s*<div>\s*)<img\b[^>]*>(\s*</div>\s*</div>(?:(?!</div>\s*</div>).){0,900}?bdt-member-name">'
        + re.escape(name) + ')',
        re.S)
    html2, n = pat.subn(r'\1' + clip_html + r'\2', html)
    return html2, n

def patch_about():
    en = SITE / 'en/about-us/index.html'
    s = read(en)
    # Team: photo cards in the live WP order, no videos (Hamid, 2026-11-17). See team_order.py.
    s = team_order.rebuild_i18n_team(s, 'en'); n1 = n2 = 0
    if 'id="history"' not in s:
        s = s.replace('<h3>History and Background of Abadis Knowledge-Based Group</h3>',
                      '<h3 id="history">History and Background of Abadis Knowledge-Based Group</h3>', 1)
    if 'id="team"' not in s:
        s = s.replace('<h2>Our Team</h2>', '<h2 id="team">Our Team</h2>', 1)
    if 'class="anchors"' not in s:
        nav = ('<nav class="anchors" aria-label="On this page"><div class="wrap">'
               '<a href="#plant">Factory</a><a href="#intro">About us</a><a href="#history">History</a>'
               '<a href="#why">Why Abadis?</a><a href="#memberships">Memberships</a>'
               '<a href="#certs-imed">Certificates</a><a href="#partners">Partners</a><a href="#team">Team</a>'
               '</div></nav>')
        s = s.replace('<main id="main">', '<main id="main">\n' + nav, 1)
    write(en, s)
    print('about EN videos', n1, n2)

    ar = SITE / 'arabic/من-نحن/index.html'
    s = read(ar)
    s = team_order.rebuild_i18n_team(s, 'ar'); n1 = n2 = 0
    if 'id="team"' not in s:
        s = s.replace('التعرف على الفريق التنفيذي', 'التعرف على الفريق التنفيذي', 1)
        s = re.sub(r'(<h2[^>]*>)(\s*التعرف على الفريق التنفيذي)', r'\1<span id="team"></span>\2', s, count=1)
    if 'class="anchors"' not in s:
        nav = ('<nav class="anchors" aria-label="أقسام الصفحة"><div class="wrap">'
               '<a href="#plant">المصنع</a><a href="#intro">من نحن</a><a href="#why">لماذا آباديس؟</a>'
               '<a href="#memberships">العضويات</a><a href="#partners">الشركاء</a><a href="#team">الفريق</a>'
               '</div></nav>')
        s = s.replace('<main id="main">', '<main id="main">\n' + nav, 1)
    # give intro an id if the first section lacks one
    if 'id="intro"' not in s:
        s = s.replace('<section class="section"', '<section class="section" id="intro"', 1)
    write(ar, s)
    print('about AR videos', n1, n2)

# ---------------------------------------------------------------- articles
def widget_inner(html, widget_type, start=0):
    key = f'data-widget_type="{widget_type}"'
    i = html.find(key, start)
    if i < 0:
        return '', -1
    j = html.find('<div class="elementor-widget-container">', i)
    if j < 0 or j - i > 800:
        return '', -1
    depth = 0
    k = j
    while k < len(html):
        o = html.find('<div', k)
        c = html.find('</div>', k)
        if c < 0:
            break
        if o != -1 and o < c:
            depth += 1
            k = o + 4
        else:
            depth -= 1
            k = c + 6
            if depth == 0:
                inner = html[html.find('>', j) + 1:c]
                return inner, k
    return '', -1

def clean_article(fragment):
    fragment = re.sub(r'<script\b[^>]*>.*?</script>', '', fragment, flags=re.S | re.I)
    fragment = re.sub(r'<style\b[^>]*>.*?</style>', '', fragment, flags=re.S | re.I)
    fragment = re.sub(r'\sstyle="[^"]*"', '', fragment)
    fragment = re.sub(r'\sdata-[a-z0-9-]+="[^"]*"', '', fragment)
    fragment = fragment.replace('&#8217;', '’').replace('&#038;', '&').replace('&nbsp;', ' ')
    fragment = H.unescape(fragment)
    # drop a leading h1; the page hero carries the only h1
    fragment = re.sub(r'<h1\b[^>]*>.*?</h1>', '', fragment, count=1, flags=re.S)
    return fragment.strip()

def accordion_to_details(fragment):
    items = re.findall(
        r'elementor-toggle-title">([^<]*)</a>[\s\S]*?elementor-tab-content[^>]*>([\s\S]*?)</div>\s*</div>',
        fragment)
    if not items:
        items = re.findall(
            r'elementor-accordion-title[^>]*>([^<]*)</[\s\S]*?elementor-tab-content[^>]*>([\s\S]*?)</div>',
            fragment)
    if not items:
        return ''
    bits = ['<h2>FAQ</h2>']
    for q, a in items:
        q = H.unescape(re.sub(r'\s+', ' ', q)).strip()
        a = clean_article(a)
        if not q:
            continue
        bits.append(f'<details class="letter"><summary>{H.escape(q)}</summary>{a}</details>')
    return '\n'.join(bits)

def extract_article(path, lang):
    raw = Path(path).read_text(encoding='utf-8', errors='replace')
    body, end = widget_inner(raw, 'theme-post-content.default')
    body = clean_article(body)
    extra = ''
    if lang == 'fa':
        acc, _ = widget_inner(raw, 'dce-acf-repeater-v2.default')
        if acc:
            # questions live in the repeater; keep paragraph text via a simple details pass
            qs = re.findall(r'<p[^>]*>(.*?)</p>', acc, flags=re.S)
            # better: title spans
            titles = re.findall(r'elementor-accordion-title[^>]*>(.*?)</', acc)
            contents = re.findall(r'elementor-tab-content[^>]*>([\s\S]*?)</div>\s*</div>', acc)
            if titles and contents:
                bits = ['<h2>سؤالات متداول</h2>']
                for q, a in zip(titles, contents):
                    q = re.sub('<[^>]+>', '', H.unescape(q)).strip()
                    bits.append(f'<details class="letter"><summary>{H.escape(q)}</summary>{clean_article(a)}</details>')
                extra = '\n'.join(bits)
    else:
        acc, _ = widget_inner(raw, 'toggle.default', 0)
        # skip a toggle whose questions are Persian
        if acc and not re.search(r'[گچپژ]', acc):
            extra = accordion_to_details(acc).replace('<h2>FAQ</h2>', '<h2>Frequently asked questions</h2>')
    return body + ('\n' + extra if extra else '')

def article_page(shell, dest, title, desc, canonical, body, crumbs_html, back_href, back_label, hreflang=None):
    s = read(shell)
    main = (f'<main id="main"><section class="page-hero"><div class="wrap">{crumbs_html}'
            f'<h1>{H.escape(title)}</h1></div></section>'
            f'<section class="section"><div class="wrap"><article class="article prose post-v2">{body}</article>'
            f'<div class="article-foot"><a href="{back_href}">{H.escape(back_label)}</a></div>'
            f'</div></section></main>')
    s2, n = re.subn(r'<main\b[^>]*>.*?</main>', main, s, count=1, flags=re.S)
    if n != 1:
        raise SystemExit('article shell failed ' + str(dest))
    s2 = re.sub(r'<title>.*?</title>', f'<title>{H.escape(title)} — {H.escape("مخازن طبی آبادیس" if "fa" in crumbs_html or "خانه" in crumbs_html else "Abadis Medical Reservoirs")}</title>', s2, count=1, flags=re.S)
    # simpler title set after
    d = H.escape(re.sub('<[^>]+>', ' ', desc)[:180], quote=True)
    s2 = re.sub(r'(<meta name="description" content=")[^"]*"', rf'\1{d}"', s2, count=1)
    s2 = re.sub(r'(<link rel="canonical" href=")[^"]*"', rf'\1{canonical}"', s2, count=1)
    s2 = re.sub(r'(<meta property="og:title" content=")[^"]*"', rf'\1{H.escape(title, quote=True)}"', s2, count=1)
    if hreflang:
        block = '\n'.join(f'<link rel="alternate" hreflang="{hl}" href="{url}">' for hl, url in hreflang) + '\n'
        if 'hreflang=' not in s2:
            s2 = s2.replace('<link rel="canonical"', block + '<link rel="canonical"', 1)
    write(dest, s2)

ARTICLES = [
    # kind, live file, dest relative, title, shell, crumbs, back, canonical, fa pair or ''
    ('fa', 'fa-or-infection.html', 'از-اتاق-عمل-تا-کنترل-عفونت؛-نقش-کیسه-ساک',
     'از اتاق عمل تا کنترل عفونت؛ نقش کیسه ساکشن در دامپزشکی'),
    ('fa', 'fa-waste-colors.html', 'رنگبندی-کیسههای-زباله-بیمارستانی',
     'رنگ‌بندی کیسه‌های زباله بیمارستانی'),
    ('fa', 'fa-4-brands.html', '۴-برند-تولیدکننده-کیسه-ساکشن-در-جهان-که',
     '۴ برند تولیدکننده کیسه ساکشن در جهان'),
]

EN_ARTICLES = [
    ('en-vet-liners.html', 'from-the-operating-room-to-infection-control-the-role-of-suction-liners-in-veterinary-medicine',
     'From the Operating Room to Infection Control: The Role of Suction Liners in Veterinary Medicine',
     'از-اتاق-عمل-تا-کنترل-عفونت؛-نقش-کیسه-ساک'),
    ('en-bi.html', 'business-intelligence-bi-transforming-the-medical-device-industry',
     'Business Intelligence: Transforming the Medical Device Industry',
     'هوش-تجاری-bi؛-تحول-هوشمند-صنعت-تجهیزات-پ'),
    ('en-oral-hygiene-art.html', 'oral-hygiene-in-hospitals-from-essential-patient-care-to-specialized-medical-equipment',
     'Oral Hygiene in Hospitals: From Essential Patient Care to Specialized Medical Equipment',
     'بهداشت-دهان-در-بیمارستان؛-از-اهمیت-مرا'),
    ('en-chest-bottle.html', 'what-is-a-chest-bottle-types-applications-and-how-chest-drainage-systems-work',
     'What Is a Chest Bottle? Types, Applications, and How Chest Drainage Systems Work',
     'چست-باتل-چیست؟-آشنایی-با-انواع،-کاربرد'),
    ('en-microdrip.html', 'what-is-a-microdrip-set-uses-components-differences-from-macrodrip-sets',
     'What Is a Microdrip Set? Uses, Components, and Differences from Macrodrip Sets',
     'میکروست-چیست؟-کاربرد،-اجزا-و-تفاوت-با-م'),
    ('en-iv-set.html', 'what-is-an-iv-infusion-set-a-comprehensive-guide-to-types-components-applications-and-safety-standards',
     'What Is an IV Infusion Set? Types, Components, Applications, and Safety Standards',
     'ست-سرم-چیست؟-راهنمای-جامع-انواع،-اجزا،'),
    ('en-un-sdgs-art.html', 'un-sdgs-and-infection-control',
     'UN SDGs and Infection Control', ''),
]

def patch_articles():
    fa_shell = SITE / 'چست-تیوب-چیست؟/index.html'
    en_shell = SITE / 'en/what-is-a-chest-tube/index.html'
    for kind, live, slug, title in ARTICLES:
        body = extract_article(LIVE / live, 'fa')
        if len(body) < 500:
            raise SystemExit('short FA article ' + live + ' ' + str(len(body)))
        dest = SITE / slug / 'index.html'
        crumbs = f'<p class="crumbs"><a href="../">خانه</a> › <a href="../مقالات/">مقالات</a></p>'
        plain = re.sub('<[^>]+>', ' ', body)[:160]
        article_page(fa_shell, dest, title, plain, f'https://abadis-med.com/{slug}/', body,
                     crumbs, '../مقالات/', 'بازگشت به مقالات')
        print('FA', slug, len(body))
    for live, slug, title, fa_slug in EN_ARTICLES:
        body = extract_article(LIVE / live, 'en')
        if len(body) < 500:
            raise SystemExit('short EN article ' + live + ' ' + str(len(body)))
        dest = SITE / 'en' / slug / 'index.html'
        crumbs = '<p class="crumbs"><a href="../../en/">Home</a> › <a href="../blog/">Articles</a></p>'
        plain = re.sub('<[^>]+>', ' ', body)[:160]
        hl = [('en', f'https://abadis-med.com/en/{slug}/')]
        if fa_slug:
            hl.insert(0, ('fa-IR', f'https://abadis-med.com/{fa_slug}/'))
            hl.append(('x-default', f'https://abadis-med.com/{fa_slug}/'))
        article_page(en_shell, dest, title, plain, f'https://abadis-med.com/en/{slug}/', body,
                     crumbs, '../blog/', 'Back to articles', hl)
        # point the existing FA page's lang switch EN link at this article when it still points at the hub
        if fa_slug:
            fp = SITE / fa_slug / 'index.html'
            if fp.is_file():
                fs = read(fp)
                fs2 = fs.replace('href="../en/blog/"', f'href="../en/{slug}/"', 1)
                if 'hreflang="en"' not in fs2:
                    fs2 = fs2.replace('<link rel="canonical"',
                                      f'<link rel="alternate" hreflang="en" href="https://abadis-med.com/en/{slug}/">\n<link rel="canonical"', 1)
                write(fp, fs2)
        print('EN', slug, len(body))

def patch_pva():
    img = 'https://abadis-media.storage.iran.liara.site/wp-content/uploads/2026/10/Premium-medical-laundry-bag-showcase.png'
    def page(lang):
        if lang == 'fa':
            return dict(
                h1='کیسه زباله PVA',
                lead='کیسه محلول در آب برای جمع‌آوری و انتقال لباس، ملحفه و منسوجات قابل شست‌وشو.',
                p='کیسه زباله PVA برای جمع‌آوری و انتقال لباس، ملحفه و منسوجات قابل شست‌وشو طراحی می‌شود. این نوع کیسه، در صورت سازگاری با فرایند شست‌وشو، همراه محتویات وارد ماشین لباس‌شویی می‌شود و در شرایط تعیین‌شده حل می‌گردد؛ در نتیجه نیاز به بازکردن کیسه و تخلیه دستی لباس‌ها کاهش می‌یابد.',
                h2='مزایا و کاربردها',
                items=['جمع‌آوری و انتقال لباس و ملحفه قابل شست‌وشو.',
                       'کاهش نیاز به بازکردن کیسه پیش از شست‌وشو.',
                       'کمک به کاهش تماس مستقیم کارکنان با منسوجات مصرف‌شده.',
                       'تسهیل گردش کار از محل جمع‌آوری تا رخت‌شوی‌خانه.',
                       'کاربرد در بیمارستان‌ها، مراکز مراقبتی و رخت‌شوی‌خانه‌های مجهز به فرایند سازگار.'],
                name_h='نام محصول', code_h='کد محصول', name='کیسه محلول در آب PVA',
                crumbs='<p class="crumbs"><a href="../../">خانه</a> › <a href="../">محصولات</a> › کیسه زباله PVA</p>',
                alt='کیسه زباله PVA آبادیس',
            )
        if lang == 'en':
            return dict(
                h1='PVA waste bag',
                lead='A water-soluble bag for collecting and transporting washable clothing, bed linen, and textiles.',
                p='The PVA waste bag is designed for collecting and transporting washable clothing, bed linen, and textiles. When compatible with the laundry process, the bag can be placed in the washing machine together with its contents and dissolves under specified conditions, reducing the need to open the bag and manually unload the items.',
                h2='Benefits and applications',
                items=['Collection and transport of washable clothing and bed linen.',
                       'Reduced need to open the bag before washing.',
                       'Helps reduce staff contact with used textiles.',
                       'Streamlines handling from the collection point to the laundry.',
                       'Suitable for hospitals, care facilities, and laundries with compatible washing processes.'],
                name_h='Product name', code_h='Product code', name='PVA waste bag',
                crumbs='<p class="crumbs"><a href="../../../en/">Home</a> › <a href="../">Products</a> › PVA waste bag</p>',
                alt='Abadis PVA waste bag',
            )
        return dict(
            h1='كيس نفايات PVA',
            lead='كيس يذوب في الماء لجمع الملابس والملاءات والمنسوجات القابلة للغسل ونقلها.',
            p='صُمم كيس نفايات PVA لجمع الملابس والملاءات والمنسوجات القابلة للغسل ونقلها. عندما يكون متوافقاً مع عملية الغسيل، يُدخل الكيس مع محتوياته إلى الغسالة ويذوب في الشروط المحددة، فيقلّ الاحتياج إلى فتح الكيس وتفريغ الملابس يدوياً.',
            h2='المزايا والاستخدامات',
            items=['جمع الملابس والملاءات القابلة للغسل ونقلها.',
                   'تقليل الحاجة إلى فتح الكيس قبل الغسيل.',
                   'المساعدة على تقليل تماس الموظفين مع المنسوجات المستعملة.',
                   'تيسير المسار من نقطة الجمع إلى المغسلة.',
                   'مناسب للمستشفيات ومراكز الرعاية والمغاسل ذات عملية غسيل متوافقة.'],
            name_h='اسم المنتج', code_h='رمز المنتج', name='كيس PVA القابل للذوبان في الماء',
            crumbs='<p class="crumbs"><a href="../../arabic/">الرئيسية</a> › <a href="../منتجات/">منتجات</a> › كيس نفايات PVA</p>',
            alt='كيس نفايات PVA من آباديس',
        )
    def html_for(d):
        lis = ''.join(f'<li>{H.escape(x)}</li>' for x in d['items'])
        return (f'<main id="main"><section class="page-hero"><div class="wrap">{d["crumbs"]}'
                f'<h1>{H.escape(d["h1"])}</h1><p class="lead">{H.escape(d["lead"])}</p></div></section>'
                f'<section class="section"><div class="wrap" style="display:grid;grid-template-columns:minmax(0,280px) 1fr;gap:28px;align-items:start">'
                f'<figure class="media-frame reveal" style="margin:0;border-radius:20px;overflow:hidden;background:#fff">'
                f'<img src="{img}" width="600" height="486" alt="{H.escape(d["alt"])}" loading="lazy" decoding="async"></figure>'
                f'<div class="prose reveal"><p>{H.escape(d["p"])}</p><h2>{H.escape(d["h2"])}</h2><ul>{lis}</ul>'
                f'<table class="pack-table glance-table"><thead><tr><th scope="col">{H.escape(d["name_h"])}</th>'
                f'<th scope="col">{H.escape(d["code_h"])}</th></tr></thead><tbody><tr>'
                f'<td>{H.escape(d["name"])}</td><td><bdi dir="ltr">—</bdi></td></tr></tbody></table>'
                f'</div></div></section></main>')
    # shells
    jobs = [
        ('fa', SITE / 'محصولات/فیلترها/index.html', SITE / 'محصولات/کیسه-های-تخصصی-و-مدیریت-پسماند-2/index.html',
         'کیسه زباله PVA — مخازن طبی آبادیس', 'https://abadis-med.com/محصولات/کیسه-های-تخصصی-و-مدیریت-پسماند-2/'),
        ('en', SITE / 'en/products/filters/index.html', SITE / 'en/products/specialized-bags-waste-management/index.html',
         'PVA waste bag — Abadis Medical Reservoirs', 'https://abadis-med.com/en/products/specialized-bags-waste-management/'),
        ('ar', SITE / 'arabic/الفلتر/index.html', SITE / 'arabic/كيس-نفايات-pva/index.html',
         'كيس نفايات PVA — خزانات طبي آباديس', 'https://abadis-med.com/arabic/كيس-نفايات-pva/'),
    ]
    for lang, shell, dest, title, can in jobs:
        if not shell.is_file():
            raise SystemExit('missing shell ' + str(shell))
        s = read(shell)
        body = html_for(page(lang))
        # drop the accidental empty note
        s2, n = re.subn(r'<main\b[^>]*>.*?</main>', body, s, count=1, flags=re.S)
        if n != 1:
            raise SystemExit('pva shell ' + str(dest))
        s2 = re.sub(r'<title>.*?</title>', f'<title>{H.escape(title)}</title>', s2, count=1, flags=re.S)
        s2 = re.sub(r'(<link rel="canonical" href=")[^"]*"', rf'\1{can}"', s2, count=1)
        hl = (
            '<link rel="alternate" hreflang="fa-IR" href="https://abadis-med.com/محصولات/کیسه-های-تخصصی-و-مدیریت-پسماند-2/">\n'
            '<link rel="alternate" hreflang="en" href="https://abadis-med.com/en/products/specialized-bags-waste-management/">\n'
            '<link rel="alternate" hreflang="ar" href="https://abadis-med.com/arabic/كيس-نفايات-pva/">\n'
            '<link rel="alternate" hreflang="x-default" href="https://abadis-med.com/محصولات/کیسه-های-تخصصی-و-مدیریت-پسماند-2/">\n'
        )
        if 'كيس-نفايات-pva' not in s2 and 'specialized-bags-waste' not in s2:
            s2 = s2.replace('<link rel="canonical"', hl + '<link rel="canonical"', 1)
        write(dest, s2)
        print('pva', lang, dest.stat().st_size)
    # responsive stack
    css = '<style>@media(max-width:700px){#main .wrap[style*="grid-template-columns"]{grid-template-columns:1fr!important}}</style>\n'
    for _, _, dest, _, _ in jobs:
        s = read(dest)
        if 'grid-template-columns:1fr' not in s:
            s = s.replace('</head>', css + '</head>', 1)
            write(dest, s)

def drop_redirect_lines(text, needles):
    out = []
    for line in text.splitlines(True):
        if any(n in line for n in needles):
            continue
        out.append(line)
    return ''.join(out)

def patch_redirects():
    drop = [
        '/en/products/specialized-bags-waste-management',
        '/en/business-intelligence-bi-transforming-the-medical-device-industry',
        '/en/from-the-operating-room-to-infection-control-the-role-of-suction-liners-in-veterinary-medicine',
        '/en/oral-hygiene-in-hospitals-from-essential-patient-care-to-specialized-medical-equipment',
        '/en/un-sdgs-and-infection-control',
        '/en/what-is-a-chest-bottle-types-applications-and-how-chest-drainage-systems-work',
        '/en/what-is-a-microdrip-set-uses-components-differences-from-macrodrip-sets',
        '/en/what-is-an-iv-infusion-set-a-comprehensive-guide-to-types-components-applications-and-safety-standards',
        'کیسه-های-تخصصی-و-مدیریت-پسماند-2',
        'از-اتاق-عمل-تا-کنترل-عفونت',
        'رنگبندی-کیسههای-زباله-بیمارستانی',
        '۴-برند-تولیدکننده-کیسه-ساکشن',
    ]
    retarget = {
        '/en/canister-installation': '/en/installation-manual/canister-installation/',
        '/en/user-manuals': '/en/installation-manual/user-manuals/',
        'کیسه-های-تخصصی-و-مدیریت-پسماند/': '/محصولات/کیسه-های-تخصصی-و-مدیریت-پسماند-2/',
        'کیسه-های-تخصصی-و-مدیریت-پسماند/?': '/محصولات/کیسه-های-تخصصی-و-مدیریت-پسماند-2/',
    }
    for rel in ('_redirects', 'liara_nginx.conf', 'redirects-nginx.conf'):
        p = SITE / rel
        s = read(p)
        s = drop_redirect_lines(s, drop)
        s = s.replace('/en/installation-manual/ 301', 'KEEPME')  # don't touch hub
        # retarget the two install aliases and the empty category (the -2 line was dropped)
        s = s.replace('https://$host/en/installation-manual/" permanent;',
                      'https://$host/en/installation-manual/" permanent;')  # noop placeholder
        if rel == '_redirects':
            s = s.replace('/en/canister-installation/ /en/installation-manual/ 301',
                          '/en/canister-installation/ /en/installation-manual/canister-installation/ 301')
            s = s.replace('/en/canister-installation /en/installation-manual/ 301',
                          '/en/canister-installation /en/installation-manual/canister-installation/ 301')
            s = s.replace('/en/user-manuals/ /en/installation-manual/ 301',
                          '/en/user-manuals/ /en/installation-manual/user-manuals/ 301')
            s = s.replace('/en/user-manuals /en/installation-manual/ 301',
                          '/en/user-manuals /en/installation-manual/user-manuals/ 301')
        else:
            s = s.replace('"$" "https://$host/en/installation-manual/" permanent;',
                          '"$" "https://$host/en/installation-manual/" permanent;')
            s = s.replace('^/en/canister-installation/?$" "https://$host/en/installation-manual/"',
                          '^/en/canister-installation/?$" "https://$host/en/installation-manual/canister-installation/"')
            s = s.replace('^/en/user-manuals/?$" "https://$host/en/installation-manual/"',
                          '^/en/user-manuals/?$" "https://$host/en/installation-manual/user-manuals/"')
        # empty category still points at the solution page
        s = s.replace('/solutions/waste-management-pva/',
                      '/محصولات/کیسه-های-تخصصی-و-مدیریت-پسماند-2/')
        # that replacement is too broad if any other rule used the solution page.
        # The specialized empty category was the one. Revert unrelated if we changed a wanted keep.
        # catalogue and reservoir must stay. They don't use waste-management.
        if 'arabic/sustainability' not in s and rel != '_redirects':
            s += '\nrewrite "^/arabic/sustainability/?$" "https://$host/arabic/sdgs/" permanent;\n'
        if rel == '_redirects' and '/arabic/sustainability/' not in s:
            s += '/arabic/sustainability/ /arabic/sdgs/ 301\n/arabic/sustainability /arabic/sdgs/ 301\n'
        s = s.replace('KEEPME', '/en/installation-manual/ 301')
        write(p, s)
        print('redirects', rel)
    # aliases json
    aj = ROOT / 'tools/redesign/data/url_aliases.json'
    data = json.loads(aj.read_text(encoding='utf-8'))
    for key in list(data):
        if any(n in key for n in drop):
            # keep the empty category (no -2) as a redirect to the product
            if key.rstrip('/').endswith('کیسه-های-تخصصی-و-مدیریت-پسماند') and not key.rstrip('/').endswith('-2'):
                data[key]['to'] = '/محصولات/کیسه-های-تخصصی-و-مدیریت-پسماند-2/'
                continue
            if key.rstrip('/').endswith('-2') or any(n in key for n in drop if 'پسماند-2' in n or n.startswith('/en/')):
                data.pop(key, None)
    for key, info in list(data.items()):
        if key in ('/en/canister-installation/', '/en/user-manuals/'):
            info['to'] = '/en/installation-manual/canister-installation/' if 'canister' in key else '/en/installation-manual/user-manuals/'
    # remove article alias keys explicitly
    for key in list(data):
        if any(x in key for x in (
            'business-intelligence-bi-transforming',
            'from-the-operating-room-to-infection-control',
            'oral-hygiene-in-hospitals-from-essential',
            'un-sdgs-and-infection-control',
            'what-is-a-chest-bottle',
            'what-is-a-microdrip',
            'what-is-an-iv-infusion-set',
            'از-اتاق-عمل-تا-کنترل-عفونت',
            'رنگبندی-کیسههای-زباله',
            '۴-برند-تولیدکننده-کیسه-ساکشن',
            'specialized-bags-waste-management',
        )):
            data.pop(key, None)
    # empty category stays
    empty = '/محصولات/کیسه-های-تخصصی-و-مدیریت-پسماند/'
    if empty in data:
        data[empty]['to'] = '/محصولات/کیسه-های-تخصصی-و-مدیریت-پسماند-2/'
    aj.write_text(json.dumps(data, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    # rewrite the empty-category stub if it exists
    stub = SITE / 'محصولات/کیسه-های-تخصصی-و-مدیریت-پسماند/index.html'
    if stub.is_file():
        write(stub, '<!DOCTYPE html><html lang="fa" dir="rtl"><head><meta charset="utf-8">'
              '<title>کیسه زباله PVA</title><meta name="robots" content="noindex,nofollow">'
              '<link rel="canonical" href="https://abadis-med.com/محصولات/کیسه-های-تخصصی-و-مدیریت-پسماند-2/">'
              '<meta http-equiv="refresh" content="0; url=../کیسه-های-تخصصی-و-مدیریت-پسماند-2/">'
              '</head><body><p><a href="../کیسه-های-تخصصی-و-مدیریت-پسماند-2/">کیسه زباله PVA</a></p>'
              '<script>location.replace("../کیسه-های-تخصصی-و-مدیریت-پسماند-2/")</script></body></html>\n')
    for rel, target in (
        ('en/canister-installation/index.html', '../installation-manual/canister-installation/'),
        ('en/user-manuals/index.html', '../installation-manual/user-manuals/'),
    ):
        write(SITE / rel, '<!DOCTYPE html><html lang="en" dir="ltr"><head><meta charset="utf-8">'
              f'<title>Installation guide</title><meta name="robots" content="noindex,nofollow">'
              f'<meta http-equiv="refresh" content="0; url={target}">'
              f'<link rel="canonical" href="https://abadis-med.com/en/installation-manual/{target.split("/")[-2]}/">'
              f'</head><body><p><a href="{target}">Installation guide</a></p>'
              f'<script>location.replace("{target}")</script></body></html>\n')
    print('aliases updated')

def main():
    _fill_ar_long()
    patch_install()
    patch_bag()
    patch_about()
    patch_articles()
    patch_pva()
    patch_redirects()
    print('rest done')

if __name__ == '__main__':
    main()
