"""Import Alireza's returned category sheets (Nov 2026) into data/category_overrides.json.

Per-item explicit overrides (FA post id -> categories / content type / formats) so the
final choices do not depend on keyword matching. EN/AR posts are mapped to their FA
counterpart by id (EN_TO_FA / AR_TO_FA); unmapped EN/AR posts keep keyword values.

Usage: python3 import_category_overrides.py ARTICLES.xlsx NEWS.xlsx
"""
import json, re, sys
from pathlib import Path
import openpyxl

HERE = Path(__file__).parent
ART_CATS = {'محصولات آبادیس': 'abadis_products', 'کنترل عفونت و ایمنی بیمار': 'infection_safety',
            'تجهیزات و ملزومات پزشکی': 'medical_equipment', 'کیفیت و استانداردها': 'quality_standards',
            'محیط زیست و توسعه پایدار': 'env_sustainability', 'مدیریت صنعت سلامت': 'health_management',
            'مدیریت و فناوری صنعت سلامت': 'health_management'}
ART_CTYPES = {'آموزشی': 'educational', 'پژوهشی': 'research', 'راهنمای خرید': 'buying_guide'}
NEWS_CATS = {'اخبار شرکت': 'company', 'نمایشگاه‌ها و رویدادها': 'events', 'محصولات و نوآوری': 'product',
             'محصولات': 'product',  # Alireza's shorthand
             'افتخارات': 'honor', 'همکاری‌ها و توسعه بازار': 'partnerships', 'مسئولیت اجتماعی': 'csr',
             'صنعت و تشکل‌ها': 'industry', 'آموزش و پژوهش': 'education'}
NEWS_FORMATS = {'مصاحبه': 'interview', 'گزارش': 'report', 'ویدئو': 'video', 'ویدیو': 'video', 'اطلاعیه': 'announcement'}

# EN/AR WordPress post id -> FA post id (same story). Low legacy ids that equal the FA id map implicitly.
EN_TO_FA = {11013: 19716, 11008: 19701, 11003: 19696, 10998: 19689, 10782: 18814, 10773: 18824, 10798: 18793,
            10769: 18772, 10765: 18768, 10761: 18761, 10758: 18758, 10693: 18681, 10688: 18609, 10684: 18597,
            10703: 18699, 10669: 18529, 10620: 18409, 10611: 18410, 10468: 18140, 10465: 17760, 10447: 18112,
            10452: 18088, 10492: 17992, 10305: 17949, 10298: 17936, 10290: 17929, 10149: 17781, 10162: 17796,
            10495: 17588, 10443: 18195, 10438: 17605, 10498: 17431, 10506: 17305, 10033: 16714, 9990: 16437,
            9950: 16208, 10531: 15884, 9842: 15884, 9967: 15833, 10017: 16445, 10012: 16744, 9830: 15088,
            9795: 15495, 9997: 15300, 9393: 15123, 9206: 15027, 9126: 14956, 9122: 14923, 10026: 15774,
            10021: 15757, 9981: 13840, 9529: 11467, 7138: 10187, 7071: 10719, 6919: 9354, 5948: 6708,
            4405: 3704, 4385: 3524, 1128: 14895, 9977: 16162}
AR_TO_FA = {1014: 535, 1009: 994, 991: 1001, 985: 1022, 981: 1029, 977: 1036, 970: 1056, 941: 1122,
            937: 14895, 933: 1162, 929: 3524, 923: 3704, 917: 4968, 910: 5985, 905: 6708, 894: 8008,
            882: 9013, 878: 9036, 803: 9354, 801: 10182, 782: 10187}


def split(v):
    return [s.strip() for s in re.split(r'[،,]', (v or '').replace('\u200c ', '\u200c')) if s.strip()]


def norm(s):
    return s.replace('\u200c', '').replace(' ', '')


def lookup(table, label):
    t = {norm(k): v for k, v in table.items()}
    return t.get(norm(label))


def pid(url):
    m = re.search(r'/(\d+)/?$', url or '')
    return int(m.group(1)) if m else None


def main(art_path, news_path):
    out = {'articles': {}, 'news': {}, 'en_to_fa': EN_TO_FA, 'ar_to_fa': AR_TO_FA, 'ambiguous': []}
    ws = openpyxl.load_workbook(art_path)['articles']
    hdr = [c.value for c in ws[1]]
    ci, ti = hdr.index('نهایی شده'), hdr.index('نوع محتوا')
    for r in ws.iter_rows(min_row=2, values_only=True):
        if not r[1]:
            continue
        i = pid(r[1])
        cats, bad = [], []
        for lbl in split(r[ci]):
            k = lookup(ART_CATS, lbl)
            (cats.append(k) if k and k not in cats else (bad.append(lbl) if not k else None))
        ctype = lookup(ART_CTYPES, (r[ti] or '').strip())
        if not cats or bad or not ctype:
            out['ambiguous'].append({'sheet': 'articles', 'id': i, 'title': r[0], 'cats': r[ci], 'ctype': r[ti]})
        out['articles'][str(i)] = {'cats': cats or None, 'ctype': ctype}
    ws = openpyxl.load_workbook(news_path)['news']
    hdr = [c.value for c in ws[1]]
    ci, fi = hdr.index('نوع محتوا'), hdr.index('برچسب')
    for n, r in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        if not r[1]:
            if any(r):
                out['ambiguous'].append({'sheet': 'news', 'row': n, 'note': 'stray row without a news item', 'values': [x for x in r if x]})
            continue
        i = pid(r[1])
        cats, bad, fmts = [], [], []
        for lbl in split(r[ci]):
            k = lookup(NEWS_CATS, lbl)
            (cats.append(k) if k and k not in cats else (bad.append(lbl) if not k else None))
        for lbl in split(r[fi]):
            k = lookup(NEWS_FORMATS, lbl)
            if k and k not in fmts:
                fmts.append(k)
            elif not k:
                bad.append(lbl)
        if not cats or not fmts or bad:
            out['ambiguous'].append({'sheet': 'news', 'id': i, 'title': r[0], 'cats': r[ci], 'formats': r[fi]})
        out['news'][str(i)] = {'cats': cats or None, 'formats': fmts or None}
    (HERE / 'data/category_overrides.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
    print(len(out['articles']), 'articles', len(out['news']), 'news; ambiguous:', json.dumps(out['ambiguous'], ensure_ascii=False))


if __name__ == '__main__':
    main(*sys.argv[1:3])
