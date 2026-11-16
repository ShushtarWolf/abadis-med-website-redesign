"""Self-hosted diagrams for the live FAQ answers (FA, EN, AR).

The crawl stored those answers as text, and the EN/AR pages still hotlink the
small PNGs. Live alt text and captions are empty, so alt comes from the
diagram labels and the answer they sit in, in that page's language.

Files follow lib.img(): sha1(URL path)[:12]-1000.webp under site/assets/img/c/.
The WebP is already built, so a later rebuild does not need the raw cache.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / 'site'

# Live pages have no <figcaption> on these answers.
_IMG = re.compile(r'<img\b[^>]*>', re.I)

FA_INSTALL = {
    'src': 'assets/img/c/c7dd2844a840-1000.webp',
    'w': 768, 'h': 994,
    'alt': 'نمودار نصب کیسه ساکشن آبادیس: بیمار، رگولاتور، ساکشن مرکزی، مخزن شماره ۱، مخزن شماره ۲ و فیلتر قطع‌کننده',
}
FA_SERIES = {
    'src': 'assets/img/c/962821efe4cd-1000.webp',
    'w': 705, 'h': 468,
    'alt': 'نمودار سری کردن کیسه‌های ساکشن یکبارمصرف آبادیس: مخزن شماره ۱، مخزن شماره ۲، رگولاتور و فیلتر قطع‌کننده',
}
EN_INSTALL = {
    'src': 'assets/img/c/4081a0dd9334-1000.webp',
    'w': 1000, 'h': 437,
    'alt': 'Diagram of installing an Abadis suction bag: patient, regulator, central suction, canister 1, canister 2 and the filter breaker',
}
EN_SERIES = {
    'src': 'assets/img/c/4081a0dd9334-1000.webp',
    'w': 1000, 'h': 437,
    'alt': 'Diagram of connecting Abadis suction bags in series: patient, regulator, central suction, canister 1, canister 2 and the filter breaker',
}
AR_INSTALL = {
    'src': 'assets/img/c/ce2f8a7578fb-1000.webp',
    'w': 768, 'h': 994,
    'alt': 'مخطط تركيب كيس شفط آباديس: المريض والمنظم والشفط المركزي والخزان ١ والخزان ٢ وفلتر القطع',
}
AR_SERIES = {
    'src': 'assets/img/c/0f5f4e6cd05e-1000.webp',
    'w': 705, 'h': 468,
    'alt': 'مخطط توصيل أكياس شفط آباديس ذات الاستعمال الواحد على التوالي: الخزان ١ والخزان ٢ والمنظم وفلتر القطع',
}


def _tag(prefix: str, spec: dict) -> str:
    alt = (spec['alt']
           .replace('&', '&amp;')
           .replace('"', '&quot;')
           .replace('<', '&lt;'))
    return (f'<img class="faq-answer-img" src="{prefix}{spec["src"]}" '
            f'width="{spec["w"]}" height="{spec["h"]}" loading="lazy" decoding="async" '
            f'alt="{alt}">')


def _insert_after(html: str, prefix: str, marker: str, spec: dict) -> str:
    """Put the diagram in its own paragraph just after `marker` (live position)."""
    n = html.count(marker)
    if n != 1:
        raise SystemExit(f'FAQ image marker found {n} times: {marker[:48]}')
    tag = _tag(prefix, spec)
    i = html.find(marker)
    window = html[i:i + len(marker) + 500]
    if spec['src'] in window:
        return html
    return html.replace(marker, marker + f'<p>{tag}</p>', 1)


def _replace_first_remote(html: str, prefix: str, needle: str, spec: dict) -> str:
    """Swap the first still-hotlinked <img> whose tag contains `needle`."""
    tag = _tag(prefix, spec)
    done = False

    def sub(m):
        nonlocal done
        if done or needle not in m.group(0):
            return m.group(0)
        done = True
        return tag

    return _IMG.sub(sub, html)


def inject_faq_html(html: str, prefix: str, lang: str) -> str:
    """Insert or relink FAQ answer diagrams. Idempotent."""
    if lang == 'fa':
        # Install diagram sits at the end of step 3; series diagram after step 5.
        html = _insert_after(html, prefix, 'عملیات ساکشن را انجام می دهد.</p>', FA_INSTALL)
        html = _insert_after(html, prefix, 'عملیات ساکشن را انجام می دهیم</p>', FA_SERIES)
    elif lang == 'en':
        # Same live file in both answers. Install image is first in the page.
        html = _replace_first_remote(html, prefix, '/wp-content/uploads/2022/01/12', EN_INSTALL)
        html = _replace_first_remote(html, prefix, '/wp-content/uploads/2022/01/12', EN_SERIES)
    elif lang == 'ar':
        html = _replace_first_remote(html, prefix, '11-1-768x994-1', AR_INSTALL)
        html = _replace_first_remote(html, prefix, '11-705x468-1', AR_SERIES)
    else:
        raise SystemExit(f'unknown FAQ lang {lang}')
    return html


def _prefix(rel: Path) -> str:
    depth = len(rel.relative_to(SITE).parent.parts)
    return '../' * depth


def apply_site() -> None:
    pages = [
        (SITE / 'پرسش-های-متداول' / 'index.html', 'fa'),
        (SITE / 'en' / 'faqs' / 'index.html', 'en'),
        (SITE / 'arabic' / 'پرسش-های-متداول' / 'index.html', 'ar'),
    ]
    for path, lang in pages:
        html = path.read_text(encoding='utf-8')
        new = inject_faq_html(html, _prefix(path), lang)
        if new.count('faq-answer-img') < 2:
            raise SystemExit(f'{path} expected 2 FAQ diagrams, got {new.count("faq-answer-img")}')
        if 'wp-content/uploads' in new:
            raise SystemExit(f'{path} still hotlinks an upload')
        path.write_text(new, encoding='utf-8')
        print('patched', path.relative_to(ROOT), 'imgs', new.count('faq-answer-img'))


if __name__ == '__main__':
    apply_site()
