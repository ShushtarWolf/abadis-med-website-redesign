#!/usr/bin/env python3
"""Generate Persian Phase 1 management report PDF (RTL, real tables)."""
from __future__ import annotations

import re
from pathlib import Path

import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    HRFlowable,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

FONT_DIR = Path(
    "/Users/siamakghodsi/.claude/skills/persian-writing/assets/fonts"
)
OUT = Path(__file__).resolve().parent / "ABADIS-PHASE-1-MANAGEMENT-REPORT-FA.pdf"

pdfmetrics.registerFont(TTFont("Vazir", str(FONT_DIR / "Vazirmatn-Regular.ttf")))
pdfmetrics.registerFont(TTFont("Vazir-Bold", str(FONT_DIR / "Vazirmatn-Bold.ttf")))

# Wrap WHOLE ranges / Latin / digits as one LTR span so endpoints keep order.
# Use LRE…PDF — python-bidi rejects LRI in resolve_implicit_levels.
_LTR_RE = re.compile(
    r"(?:"
    r"\$?\d[\d,]*(?:\.\d+)?(?:\s*(?:[–\-]|تا)\s*\$?\d[\d,]*(?:\.\d+)?)?%?"
    r"|[A-Za-z][A-Za-z0-9._+\-/]*"
    r"|[۰-۹]+(?:[٬،.][۰-۹]+)*(?:\s*(?:[–\-]|تا)\s*[۰-۹]+(?:[٬،.][۰-۹]+)*)?"
    r")"
)


def reshape(text: str) -> str:
    if text is None:
        return ""
    s = str(text)

    def _wrap(m: re.Match[str]) -> str:
        return "\u202A" + m.group(0) + "\u202C"  # LRE … PDF

    protected = _LTR_RE.sub(_wrap, s)
    return get_display(arabic_reshaper.reshape(protected))


def P(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(reshape(text).replace("\n", "<br/>"), style)


styles = {
    "title": ParagraphStyle(
        "t",
        fontName="Vazir-Bold",
        fontSize=13,
        leading=20,
        alignment=TA_CENTER,
        spaceAfter=3,
    ),
    "sub": ParagraphStyle(
        "s",
        fontName="Vazir",
        fontSize=9,
        leading=13,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#444444"),
        spaceAfter=4,
    ),
    "h1": ParagraphStyle(
        "h1",
        fontName="Vazir-Bold",
        fontSize=11.5,
        leading=17,
        alignment=TA_RIGHT,
        spaceBefore=8,
        spaceAfter=5,
    ),
    "h2": ParagraphStyle(
        "h2",
        fontName="Vazir-Bold",
        fontSize=10,
        leading=14,
        alignment=TA_RIGHT,
        spaceBefore=6,
        spaceAfter=3,
    ),
    "body": ParagraphStyle(
        "b",
        fontName="Vazir",
        fontSize=9.5,
        leading=14.5,
        alignment=TA_RIGHT,
        spaceAfter=2.5,
    ),
    "small": ParagraphStyle(
        "sm",
        fontName="Vazir",
        fontSize=8.5,
        leading=12.5,
        alignment=TA_RIGHT,
        textColor=colors.HexColor("#333333"),
        spaceAfter=2,
    ),
    "cell": ParagraphStyle(
        "c", fontName="Vazir", fontSize=7.8, leading=11.2, alignment=TA_RIGHT
    ),
    "cellb": ParagraphStyle(
        "cb", fontName="Vazir-Bold", fontSize=7.8, leading=11.2, alignment=TA_RIGHT
    ),
    "note": ParagraphStyle(
        "n",
        fontName="Vazir",
        fontSize=8.5,
        leading=12.5,
        alignment=TA_RIGHT,
        backColor=colors.HexColor("#FFF8E6"),
        borderPadding=5,
        spaceAfter=4,
    ),
    "label_ok": ParagraphStyle(
        "lok",
        fontName="Vazir-Bold",
        fontSize=8.5,
        leading=12,
        alignment=TA_RIGHT,
        textColor=colors.HexColor("#1a4d2e"),
        spaceAfter=2,
    ),
}

LAND = landscape(A4)
PW = A4[0] - 28 * mm
LW = LAND[0] - 28 * mm

HDR_BG = colors.HexColor("#E8E8E8")
GRID = colors.HexColor("#AAAAAA")
ALT = colors.HexColor("#F7F7F7")


def make_table(headers, rows, col_widths, font_size=None):
    cell_style = styles["cell"]
    head_style = styles["cellb"]
    if font_size:
        cell_style = ParagraphStyle(
            f"c{font_size}",
            fontName="Vazir",
            fontSize=font_size,
            leading=font_size + 3.2,
            alignment=TA_RIGHT,
        )
        head_style = ParagraphStyle(
            f"cb{font_size}",
            fontName="Vazir-Bold",
            fontSize=font_size,
            leading=font_size + 3.2,
            alignment=TA_RIGHT,
        )
    headers_r = list(reversed(headers))
    widths_r = list(reversed(col_widths))
    data = [[P(h, head_style) for h in headers_r]]
    for row in rows:
        data.append([P(c, cell_style) for c in reversed(row)])
    t = Table(data, colWidths=widths_r, repeatRows=1)
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), HDR_BG),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#111111")),
                ("ALIGN", (0, 0), (-1, -1), "RIGHT"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("GRID", (0, 0), (-1, -1), 0.4, GRID),
                ("LEFTPADDING", (0, 0), (-1, -1), 3.2),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3.2),
                ("TOPPADDING", (0, 0), (-1, -1), 3.2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, ALT]),
            ]
        )
    )
    return t


def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont("Vazir", 8)
    txt = reshape(
        f"صفحه {canvas.getPageNumber()}  ·  گزارش وضعیت فاز اول آبادیس  ·  26 September 2026"
    )
    canvas.drawCentredString(doc.pagesize[0] / 2, 10 * mm, txt)
    canvas.restoreState()


def on_page_p(canvas, doc):
    canvas.setPageSize(A4)
    add_page_number(canvas, doc)


def on_page_l(canvas, doc):
    canvas.setPageSize(LAND)
    add_page_number(canvas, doc)


def build():
    doc = BaseDocTemplate(
        str(OUT),
        pagesize=A4,
        rightMargin=14 * mm,
        leftMargin=14 * mm,
        topMargin=12 * mm,
        bottomMargin=16 * mm,
    )
    frame_p = Frame(14 * mm, 16 * mm, A4[0] - 28 * mm, A4[1] - 28 * mm, id="p")
    frame_l = Frame(14 * mm, 16 * mm, LAND[0] - 28 * mm, LAND[1] - 28 * mm, id="l")
    doc.addPageTemplates(
        [
            PageTemplate(id="Portrait", frames=frame_p, pagesize=A4, onPage=on_page_p),
            PageTemplate(
                id="Landscape", frames=frame_l, pagesize=LAND, onPage=on_page_l
            ),
        ]
    )

    story = []

    # Title
    story.append(
        P(
            "گزارش وضعیت و برنامه اجرایی فاز اول بازطراحی و مهاجرت وب‌سایت آبادیس",
            styles["title"],
        )
    )
    story.append(
        P("Audit → Specification → Structure → Design Preparation", styles["sub"])
    )
    story.append(
        P(
            "تاریخ گزارش: 26 September 2026  ·  مخاطب: مدیریت آبادیس مدیکال",
            styles["sub"],
        )
    )
    story.append(
        HRFlowable(
            width="100%", thickness=1, color=colors.HexColor("#CCCCCC"), spaceAfter=6
        )
    )
    story.append(
        P(
            "سه برچسب در کل گزارش: "
            "«تأیید شده / Verified» · "
            "«برآورد اولیه / Estimate» · "
            "«نیازمند بررسی یا تأیید / Pending». "
            "هزینهٔ نامشخص به‌عنوان صفر نوشته نمی‌شود. "
            "بازهٔ 41–62 روز کاری تاریخ قطعی تحویل نیست. "
            "مشخصات اصلی (Master Spec) READY FOR IMPLEMENTATION نامیده نمی‌شود.",
            styles["note"],
        )
    )

    # ── 1 Status ──
    story.append(P("۱. وضعیت پروژه", styles["h1"]))
    story.append(
        P(
            "مرحلهٔ فعلی (Verified): آماده‌سازی مشخصات، ساختار صفحات / مدل محتوا، و مشخصات طراحی — "
            "پیش از طراحی بصری تأییدشده و پیش از پیاده‌سازی Nuxt تولیدی.",
            styles["body"],
        )
    )
    story.append(
        P(
            "پیاده‌سازی تولیدی Nuxt هنوز شروع نشده است. (Verified)",
            styles["body"],
        )
    )
    story.append(P("انجام‌شده (خلاصه — Verified):", styles["h2"]))
    for t in [
        "ممیزی مبتنی بر شواهد (25 September 2026) و خلاصهٔ مدیریتی ممیزی",
        "به‌روزرسانی مشخصات اصلی (Master Spec) با پاسخ‌های مدیریت — پیش‌نویس کاری، نه اعلام READY FOR IMPLEMENTATION",
        "طرح اجرایی فاز ۱ با هزینه و زمان‌بندی برآوردی",
        "ساختار صفحات و مدل محتوا — پیش‌نویس برای بررسی مدیریت",
        "مشخصات طراحی صفحهٔ اصلی و صفحهٔ محصول (بدون mockup بصری)",
    ]:
        story.append(P("• " + t, styles["body"]))
    story.append(
        P(
            "گام بعد (Pending): دریافت جهت‌دهی‌های باز طراحی و ورودی‌های باز آبادیس، سپس تولید بستهٔ بصری "
            "چهارقابی Home / Product برای مرور مدیریت.",
            styles["body"],
        )
    )

    # ── 2 Audit ──
    story.append(P("۲. خلاصهٔ ممیزی (شواهد موجود)", styles["h1"]))
    story.append(
        P(
            "منبع (Verified): ABADIS-AUDIT.json با generated_at برابر 2026-09-25T15:24:58.690Z. "
            "این ممیزی یک بررسی کامل HTML برای تک‌تک 718 نشانی نبود و آزمون کامل لینک‌های شکسته انجام نشد.",
            styles["note"],
        )
    )
    # Avoid the Persian crawl-term that mis-renders under reshape/bidi; use «بررسی کامل HTML» instead.
    story.append(
        make_table(
            ["فهرست", "کامل؟", "عدد / توضیح"],
            [
                ["فهرست URL", "بله — Verified", "718 نشانی (sitemap + ریشه‌های زبان + کشف EN/AR)"],
                ["ترکیب زبان در فهرست", "بله — Verified", "fa 540 · en 101 · ar 77"],
                ["افزودهٔ کشف EN/AR", "بله — Verified", "+177 نشانی از HTMLهای /en/ و /arabic/"],
                ["تصاویر media sitemap (image:loc)", "بله — Verified", "1053"],
                ["جمع REST وردپرس (X-WP-Total)", "بله — Verified", "جدول جداگانه زیر"],
                ["آیتم‌های REST دانلودشده در این اجرا", "خیر", "309 (سقف‌دار)"],
                ["ممیزی HTML / SEO صفحه", "خیر", "فقط 10 صفحه (maxCrawlUrls=10)"],
                ["فرم‌های مشاهده‌شده", "خیر", "6 فرم فقط روی نمونهٔ HTML"],
                ["آزمون لینک شکسته (HEAD)", "خیر", "0 در این اجرا — کامل نشده"],
            ],
            [PW * 0.28, PW * 0.18, PW * 0.54],
        )
    )
    story.append(Spacer(1, 5))
    story.append(
        P(
            "تفکیک نوع در فهرست URL (طبقه‌بندی موجودی — نه اثبات دریافت HTML هر نشانی):",
            styles["h2"],
        )
    )
    story.append(
        make_table(
            ["نوع / سطل", "تعداد"],
            [
                ["post", "208"],
                ["page", "25"],
                ["language_root", "3"],
                ["_customers", "156"],
                ["_franchise", "27"],
                ["_citynmg", "25"],
                ["post_tag", "63"],
                ["category", "8"],
                ["_joboffers", "10"],
                ["_downloadcenter", "10"],
                ["jet-menu", "3"],
                ["author", "4"],
                ["lang_discovered", "176"],
                ["جمع", "718"],
            ],
            [PW * 0.55, PW * 0.45],
        )
    )
    story.append(Spacer(1, 5))
    story.append(P("WordPress REST (جمع کل از هدرها — Verified):", styles["h2"]))
    story.append(
        make_table(
            ["کلید", "جمع کل", "نوع"],
            [
                ["post", "221", "type"],
                ["page", "26", "type"],
                ["attachment", "1727", "type"],
                ["_customers", "155", "type"],
                ["_franchise", "26", "type"],
                ["_downloadcenter", "9", "type"],
                ["_joboffers", "9", "type"],
                ["category", "8", "taxonomy"],
                ["post_tag", "76", "taxonomy"],
                ["_citynmg", "31", "taxonomy"],
            ],
            [PW * 0.40, PW * 0.30, PW * 0.30],
        )
    )
    story.append(
        P(
            "رسانه: 1053 مورد image:loc در sitemap · 1727 attachment در REST — شمارش‌اند نه تأیید یک‌به‌یک صحت فایل. "
            "نوع REST عمومی به نام product در فهرست انواع ممیزی‌شده دیده نشد.",
            styles["small"],
        )
    )
    story.append(
        P(
            "نمونهٔ HTML/SEO (10 صفحه): نقص‌هایی مانند فقدان H1 در Home FA، alt ناقص، hreflang خالی، "
            "و lang اشتباه عربی (fa-IR) در نمونه دیده شد.",
            styles["small"],
        )
    )

    # ── 3 Decisions ──
    story.append(P("۳. تصمیم‌های مدیریت (ثبت‌شده — Verified مگر خلاف آن ذکر شود)", styles["h1"]))
    for d in [
        "مرز قرارداد: فاز ۱ الان؛ فاز ۲ قرارداد جدا",
        "پورتال مشتری / سفارش پیام‌گستر = فاز ۲؛ خارج از تحویل پایهٔ فاز ۱",
        "مسیر معماری: وردپرس headless (جهت پذیرفته‌شده) + Nuxt به‌عنوان لایهٔ نمایش",
        "میزبانی: لیارا اولین گزینه برای بررسی؛ تأیید نهایی Pending (هزینه / محل / پشتیبان / بازیابی / دسترسی)",
        "مالکیت: دامنه، میزبانی، GitHub و حساب سرویس‌ها با آبادیس · دسترسی نقش‌محور",
        "Staging الزامی؛ تأیید آبادیس قبل از انتشار روی production",
        "توالی طراحی: ساختار / مدل محتوا → طراحی Home و Product برای تأیید → سپس ساخت",
        "concept-preview مرجع بصری تأییدشده نیست",
        "زبان‌ها: FA / EN / AR با فرادادهٔ زبانی صحیح",
        "حفظ URL / سئو / رسانه مگر با تأیید صریح آبادیس برای تغییر نقشه‌شده",
        "سرنخ: ذخیرهٔ پایدار قبل از اطلاع‌رسانی؛ اتصال پیام‌گستر فقط اگر API / دسترسی / هزینه / بار کاری جداگانه تأیید شود",
        "خارج از پایهٔ فاز ۱ مگر تأیید جدا: چت‌بات، تجارب ما، کمپین / بازی دهم، نمایشگر سه‌بعدی تعاملی",
        "لانچ / بازگشت / پشتیبان با آزمون بازیابی واقعی · گارانتی باگ 60 روز پس از انتشار",
        "اصول آمار رویدادها، حریم خصوصی، عملکرد و پایش الزامی است (جزئیات عددی / ابزار هنوز Pending)",
        "فی توسعه برای این همکاری: 0 USD؛ زیرساخت جدا",
    ]:
        story.append(P("• " + d, styles["body"]))

    # ── 4 Completed timeline (separate) ──
    story.append(
        P(
            "۴. زمان‌بندی کار انجام‌شده (جدا از برآورد آینده)",
            styles["h1"],
        )
    )
    story.append(
        P(
            "این بخش فقط واقعیت‌های تقویمی را نشان می‌دهد و با جدول برآورد آینده مخلوط نمی‌شود.",
            styles["small"],
        )
    )
    story.append(
        make_table(
            ["تاریخ", "رویداد (Verified)"],
            [
                [
                    "21 September 2026",
                    "شروع قابل‌اثبات پروژه / ممیزی (git + شواهد Manus)",
                ],
                ["23 September 2026", "شروع کار محلی Cursor روی پروژه"],
                [
                    "25 September 2026",
                    "n8n + بستهٔ ممیزی (ABADIS-AUDIT.json) + کار فنی / معماری",
                ],
                [
                    "25 September 2026",
                    "Master Spec و برگه‌های تصمیم مدیریت",
                ],
                [
                    "26 September 2026",
                    "ثبت تصمیم‌های مدیریت + طرح اجرایی + ساختار صفحات / مدل محتوا + مشخصات طراحی",
                ],
            ],
            [PW * 0.32, PW * 0.68],
        )
    )
    story.append(
        P(
            "حدود 5–6 روز تقویمی سپری شده؛ نفر-روز و ساعات فعال دقیق قابل اثبات نیست. "
            "(Verified برای بازهٔ تقویمی · Pending برای ساعات فعال / person-day)",
            styles["note"],
        )
    )

    # ── 5 Future time — landscape ──
    story.append(NextPageTemplate("Landscape"))
    story.append(PageBreak())
    story.append(P("۵. زمان‌بندی اجرایی فاز ۱ (آینده)", styles["h1"]))
    story.append(
        P(
            "برآورد اولیه — زمان اجرای کاری، نه تاریخ قطعی تحویل. "
            "زمان انتظار / تأیید مدیریت (Pending) فعلاً نامشخص است و به‌عنوان تلاش توسعه لحاظ نشده.",
            styles["note"],
        )
    )
    story.append(Spacer(1, 3))
    story.append(
        make_table(
            ["مرحله", "خروجی", "زمان کاری تخمینی"],
            [
                [
                    "IA / Content Matrix / Data Model",
                    "ساختار و مدل محتوا (پیش‌نویس آماده؛ تکمیل با ورودی محصول)",
                    "برآورد اولیه: 2–3 روز کاری",
                ],
                [
                    "Design System + Home + Product Desktop/Mobile",
                    "سیستم بصری + 4 قاب Home/Product",
                    "برآورد اولیه: 5–7 روز کاری",
                ],
                [
                    "Other page templates",
                    "قالب صفحات اولویت‌دار دیگر",
                    "برآورد اولیه: 5–7 روز کاری",
                ],
                [
                    "WordPress/CMS + migration mapping",
                    "نگاشت مهاجرت و آماده‌سازی CMS",
                    "برآورد اولیه: 3–5 روز کاری",
                ],
                [
                    "Nuxt frontend + WordPress integration",
                    "فرانت Nuxt متصل به headless WP",
                    "برآورد اولیه: 10–15 روز کاری",
                ],
                [
                    "Phase 1 features",
                    "فرم‌ها، سرنخ، صفحات/قابلیت‌های پایهٔ فاز ۱",
                    "برآورد اولیه: 5–8 روز کاری",
                ],
                [
                    "SEO / redirects / hreflang / media migration",
                    "سئو، ریدایرکت، hreflang، مهاجرت رسانه",
                    "برآورد اولیه: 3–5 روز کاری",
                ],
                [
                    "QA / performance / accessibility / security / reconciliation",
                    "آزمون کیفیت، عملکرد، دسترسی‌پذیری، امنیت، تطبیق",
                    "برآورد اولیه: 5–7 روز کاری",
                ],
                [
                    "Staging / UAT / launch preparation",
                    "Staging، پذیرش کاربری، آماده‌سازی لانچ",
                    "برآورد اولیه: 3–5 روز کاری",
                ],
                [
                    "جمع تقریبی",
                    "بدون زمان انتظار مدیریت و بدون تاریخ قطعی تحویل",
                    "برآورد اولیه: حدود 41–62 روز کاری",
                ],
            ],
            [LW * 0.34, LW * 0.36, LW * 0.30],
            font_size=8.2,
        )
    )
    story.append(
        P(
            "جمع بالا Estimate است. تاریخ اتمام کل پروژه اعلام نشده. "
            "زمان تأیید مدیریت جدا و نامشخص است.",
            styles["small"],
        )
    )

    # ── 6 Cost / purchases — landscape ──
    story.append(PageBreak())
    story.append(
        P("۶. هزینه‌ها و حساب‌ها / سرویس‌های موردنیاز", styles["h1"])
    )
    story.append(
        P(
            "این جدول حساب‌ها و سرویس‌هایی را نشان می‌دهد که ممکن است نیاز به خرید / پرداخت داشته باشند. "
            "هزینهٔ نامشخص به‌عنوان صفر نوشته نشده است. "
            "نرخ Cursor Pro+ در مستندات رسمی cursor.com در تاریخ گزارش حدود $60/mo بود — قبل از خرید دوباره Verify کنید.",
            styles["note"],
        )
    )
    story.append(Spacer(1, 3))
    story.append(
        make_table(
            [
                "مورد",
                "آیا نیاز به خرید/پرداخت جدید دارد؟",
                "هزینه",
                "وضعیت",
                "توضیح",
            ],
            [
                [
                    "هزینه توسعه فاز ۱",
                    "خیر",
                    "0 دلار",
                    "Confirmed / Verified",
                    "هزینه توسعه طبق توافق فعلی صفر است.",
                ],
                [
                    "Cursor Pro+",
                    "بله / در صورت نداشتن حساب سازمانی موجود",
                    "حدود 60 دلار در ماه",
                    "نیازمند Verify قیمت فعلی",
                    "ابزار توسعه؛ اگر حساب موجود تیم قابل استفاده باشد، خرید جدید لازم نیست.",
                ],
                [
                    "n8n",
                    "خیر، فعلاً",
                    "نامشخص / 0 دلار خرید جدید در این برنامه",
                    "از Instance فعلی استفاده می‌شود",
                    "hamidafghah.app.n8n.cloud موجود است؛ قیمت Plan فعلی در مستندات تأیید نشده و نباید حدس زده شود.",
                ],
                [
                    "Liara Hosting",
                    "بله، در صورت انتخاب نهایی",
                    "حداقل بودجه در نظر گرفته‌شده 4,000,000 تومان در ماه",
                    "نیازمند بررسی و تأیید نهایی",
                    "هزینه واقعی به Plan نهایی، منابع، Backup، Storage و نیازهای واقعی بستگی دارد.",
                ],
                [
                    "Database",
                    "ممکن است",
                    "نامشخص",
                    "وابسته به معماری نهایی",
                    "فقط در صورت نیاز به سرویس / منبع جداگانه.",
                ],
                [
                    "Storage / CDN",
                    "ممکن است",
                    "نامشخص",
                    "وابسته به نیاز و Plan",
                    "هزینه جداگانه فقط در صورت نیاز.",
                ],
                [
                    "Backup / Recovery",
                    "ممکن است",
                    "نامشخص",
                    "باید در بررسی نهایی Hosting مشخص شود",
                    "اصل پشتیبان و آزمون بازیابی الزامی است؛ هزینهٔ محصول هنوز Pending.",
                ],
                [
                    "Domain",
                    "خیر",
                    "Renewal در صورت سررسید",
                    "دامنه موجود است",
                    "مالکیت با آبادیس؛ تمدید جدا از فی توسعه.",
                ],
                [
                    "SSL",
                    "فعلاً پیش‌بینی نشده",
                    "نامشخص / احتمالاً وابسته به Hosting",
                    "بررسی با Hosting نهایی",
                    "عدد جداگانه اختراع نشده.",
                ],
                [
                    "GitHub",
                    "فعلاً خیر",
                    "0 دلار خرید جدید در برنامه",
                    "حساب موجود",
                    "حساب متعلق به آبادیس.",
                ],
                [
                    "Corporate Email",
                    "فعلاً خیر",
                    "نامشخص",
                    "ابتدا حساب‌های موجود بررسی شوند",
                    "برای اطلاع‌رسانی سرنخ در صورت نیاز.",
                ],
                [
                    "SMS",
                    "اختیاری",
                    "نامشخص",
                    "خارج از Base Scope مگر اینکه تأیید شود",
                    "Email + request list مسیر پایه است.",
                ],
                [
                    "Analytics",
                    "فعلاً خیر",
                    "نامشخص / ابتدا سرویس فعلی بررسی شود",
                    "نیازمند بررسی حساب موجود",
                    "اصل آمار الزامی است؛ ابزار نهایی Pending.",
                ],
                [
                    "Monitoring",
                    "فعلاً خیر",
                    "نامشخص",
                    "ابتدا ابزارهای موجود بررسی شوند",
                    "مالک / کانال پایش هنوز Pending.",
                ],
                [
                    "PayamGostar Customer Portal",
                    "Phase 1 نیست",
                    "Phase 2 — جداگانه",
                    "خارج از هزینه Phase 1",
                    "فقط آماده‌سازی آینده در فاز ۱ مجاز است.",
                ],
                [
                    "Maintenance after 60 days",
                    "جدا از گارانتی پایه",
                    "جداگانه / هنوز تعیین نشده",
                    "خارج از 60-day included bug-fix period",
                    "قرارداد نگهداری جدا در صورت نیاز.",
                ],
            ],
            [LW * 0.16, LW * 0.18, LW * 0.22, LW * 0.18, LW * 0.26],
            font_size=7.5,
        )
    )

    # ── 7 First deliverable ──
    story.append(NextPageTemplate("Portrait"))
    story.append(PageBreak())
    story.append(P("۷. اولین خروجی قابل‌مشاهده", styles["h1"]))
    story.append(
        make_table(
            ["آیتم", "وضعیت"],
            [
                [
                    "1) ساختار صفحات + مدل محتوا",
                    "پیش‌نویس برای بررسی مدیریت — تکمیل‌شده به‌عنوان خروجی اول (نه تأیید نهایی قطعی) · Pending تأیید",
                ],
                [
                    "2) طراحی صفحهٔ اصلی + صفحهٔ محصول",
                    "گام بعد پس از جهت‌دهی‌های باز · Pending",
                ],
                [
                    "بستهٔ مرور بصری",
                    "چهار قاب: Home دسکتاپ · Home موبایل · Product دسکتاپ · Product موبایل",
                ],
                [
                    "شروع طراحی بصری",
                    "فقط بعد از پاسخ جهت‌دهی‌های مدیریت (نه قبل)",
                ],
                ["concept-preview", "مرجع بصری تأییدشده نیست (Verified)"],
            ],
            [PW * 0.35, PW * 0.65],
        )
    )

    # ── 8 Open ──
    story.append(P("۸. تصمیم‌ها / ورودی‌های باز آبادیس (Pending)", styles["h1"]))
    story.append(
        P(
            "موارد زیر هنوز باز هستند و برخی شروع طراحی نهایی یا ساخت را مشروط می‌کنند:",
            styles["body"],
        )
    )
    opens = [
        "فهرست رسمی محصولات و منابع فنی مشخصات",
        "ساختار خانواده / SKU در مقابل فقط Category / Family",
        "ماتریس محتوا (بازنویسی کامل / ویرایش جزئی / فقط ظاهر)",
        "جهت بصری و محدودیت‌های قطعی Brand Book (رنگ / تایپ)",
        "حقایق و خط زمانی About (شامل دانش‌بنیان در برابر تأسیس)",
        "دامنهٔ رسمی: apex در برابر www",
        "فرمول و فرضیات محاسبه‌گر",
        "فرمول شمارندهٔ اثرگذاری (Impact) در صورت نمایش",
        "صفحات الزامی سه‌زبانه در فاز ۱",
        "مالک فروش، SLA، کانال اطلاع‌رسانی، کدام فرم‌ها سرنخ‌اند",
        "ابزار آمار و رویدادها · بودجهٔ عملکرد",
        "مالک / کانال پایش",
        "بررسی نهایی میزبانی لیارا (هزینه / محل / پشتیبان / بازیابی / دسترسی)",
        "آری / خیر برای API سرنخ پیام‌گستر در فاز ۱",
        "مالک go/no-go و مجوز بازگشت در لانچ",
        "گواهی‌ها و لوگوهای مجاز برای نمایش",
        "جهت Hero و ماژول‌های اختیاری Home (Solutions، آمار، Impact، Customers، Factory Video)",
    ]
    for i, o in enumerate(opens, 1):
        story.append(P(f"{i}. {o}", styles["body"]))

    story.append(Spacer(1, 6))
    story.append(
        HRFlowable(
            width="100%",
            thickness=0.5,
            color=colors.HexColor("#CCCCCC"),
            spaceBefore=4,
            spaceAfter=5,
        )
    )
    story.append(
        P(
            "پایان گزارش · مرجع اصلی: ABADIS-MASTER-SPECIFICATION.md · "
            "این PDF جایگزین مشخصات اصلی نیست و وضعیت را برای واتساپ / مدیریت جمع‌بندی می‌کند. "
            "Master Spec به‌عنوان READY FOR IMPLEMENTATION اعلام نشده است.",
            styles["small"],
        )
    )

    doc.build(story)
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    build()
