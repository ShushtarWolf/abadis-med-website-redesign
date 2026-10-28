"""Approved W2-2 orbit for homepage #why and About memberships.

Geometry and the Persian dataset come from site/why-abadis-options/option-2.html.
Active-centre counts use 1,284. English and Arabic are faithful translations.
"""
import json
import re
from pathlib import Path

from lib import esc, SITE

_PROTO = SITE / 'why-abadis-options' / 'option-2.html'
_I18N = Path(__file__).resolve().parent / 'data' / 'w2_i18n.json'

_HUB = {
    'home': {
        'fa': ('چرا آبادیس؟', ''),
        'en': ('Why Abadis?', ''),
        'ar': ('لماذا آباديس؟', ''),
    },
    'about': {
        'fa': ('آبادیس مد', 'عضویت‌ها و مجوزها'),
        'en': ('Abadis Med', 'Memberships & Credentials'),
        'ar': ('آباديس مد', 'العضويات والتراخيص'),
    },
}

_UI = {
    'fa': {
        'strip': 'انتخاب سریع گره‌ها',
        'replay': 'پخش مجدد انیمیشن',
        'stems': {
            'long': 'شاخه بلند · رشد شعاعی از مرکز',
            'medium': 'شاخه متوسط · رشد شعاعی از مرکز',
            'short': 'شاخه کوتاه (ماهواره آماری) · رشد از مرکز',
        },
    },
    'en': {
        'strip': 'Quick select',
        'replay': 'Replay animation',
        'stems': {
            'long': 'Long stem · radial growth from the hub',
            'medium': 'Medium stem · radial growth from the hub',
            'short': 'Short stem · stat satellite, growth from the hub',
        },
    },
    'ar': {
        'strip': 'اختيار سريع',
        'replay': 'إعادة تشغيل الحركة',
        'stems': {
            'long': 'فرع طويل · نمو شعاعي من المركز',
            'medium': 'فرع متوسط · نمو شعاعي من المركز',
            'short': 'فرع قصير · قمر إحصائي، نمو من المركز',
        },
    },
}


def assets(prefix=''):
    return (
        f'<link rel="stylesheet" href="{prefix}assets/css/w2-orbit.css?v=20261028m">\n'
        f'<script src="{prefix}assets/js/w2-orbit.js?v=20261028m" defer></script>\n'
    )


def _extract_object(src, marker):
    i = src.find(marker)
    if i < 0:
        raise RuntimeError('W2-2 prototype is missing ' + marker)
    i = src.find('{', i)
    depth = 0
    for j in range(i, len(src)):
        ch = src[j]
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                return json.loads(src[i:j + 1])
    raise RuntimeError('unclosed ' + marker)


def _patch_counts(text):
    return (text.replace('۱٬۲۴۲', '۱٬۲۸۴')
                .replace('۱٬۲۵۲', '۱٬۲۸۴'))


def _patch_node(node):
    out = {}
    for key, val in node.items():
        if isinstance(val, str):
            out[key] = _patch_counts(val)
        elif isinstance(val, list) and val and isinstance(val[0], list):
            out[key] = [[_patch_counts(a), _patch_counts(b)] for a, b in val]
        else:
            out[key] = val
    return out


def _load():
    html = _PROTO.read_text(encoding='utf-8')
    svg = re.search(r'<svg viewBox="0 0 640 610" class="orb-svg"[\s\S]*?</svg>', html)
    q2 = re.search(r'<div class="orb-hub-q2">([\s\S]*?)</div>', html)
    hub_style = re.search(r'<div class="orb-hub" style="([^"]+)">', html)
    if not svg or not q2 or not hub_style:
        raise RuntimeError('W2-2 prototype markup could not be read')
    specs = []
    for m in re.finditer(
        r'<button type="button" class="(orb-node[^"]*)"\s+style="([^"]+)"\s+'
        r'data-idx="(\d+)" data-stem="([^"]+)"',
        html,
    ):
        specs.append((m.group(1), m.group(2), int(m.group(3)), m.group(4)))
    if len(specs) != 8:
        raise RuntimeError('expected 8 W2-2 nodes, found %s' % len(specs))
    fa = {
        'home': {'nodes': [_patch_node(n) for n in _extract_object(html, '\n  home:')['nodes']]},
        'about': {'nodes': [_patch_node(n) for n in _extract_object(html, '\n  about:')['nodes']]},
    }
    i18n = json.loads(_I18N.read_text(encoding='utf-8'))
    return {
        'svg': svg.group(0),
        'q2': q2.group(1),
        'hub_style': hub_style.group(1),
        'specs': specs,
        'copy': {'fa': fa, 'en': i18n['en'], 'ar': i18n['ar']},
    }


_CACHE = None


def _parts():
    global _CACHE
    if _CACHE is None:
        _CACHE = _load()
    return _CACHE


def widget(lang, mode, prefix=''):
    """Two-column W2-2. mode is 'home' or 'about'. Starts un-animated for the scroll trigger."""
    lang = lang if lang in _UI else 'fa'
    mode = mode if mode in ('home', 'about') else 'home'
    parts = _parts()
    data = parts['copy'][lang][mode]
    nodes = data['nodes']
    if len(nodes) != 8:
        raise RuntimeError('W2-2 %s/%s needs 8 nodes' % (lang, mode))
    ui = _UI[lang]
    hub_title, hub_sub = _HUB[mode][lang]
    first = nodes[0]
    buttons = []
    for cls, style, idx, stem in parts['specs']:
        nd = nodes[idx]
        active = ' is-active' if idx == 0 else ''
        # Drop a baked is-active from the prototype class string, then set it for node 0 only.
        cls = cls.replace(' is-active', '')
        buttons.append(
            f'<button type="button" class="{cls}{active}" style="{style}" '
            f'data-idx="{idx}" data-stem="{stem}" aria-label="{esc(nd["title"])}">'
            f'<span class="orb-node-halo"></span><span class="orb-node-inner">'
            f'<span class="orb-node-num">{esc(nd["num"])}</span>'
            f'<strong class="orb-node-title">{esc(nd["title"])}</strong>'
            f'<span class="orb-node-stat">{esc(nd["stat"])}</span>'
            f'</span></button>'
        )
    pills = ''.join(
        f'<button type="button" class="strip-pill{" is-active" if i == 0 else ""}" '
        f'data-idx="{i}" aria-label="{esc(nodes[i]["title"])}">{esc(nodes[i]["num"])}</button>'
        for i in range(8)
    )
    kpis = ''.join(
        f'<div class="w2-kpi"><b>{esc(a)}</b><span>{esc(b)}</span></div>'
        for a, b in first['kpis']
    )
    payload = {'nodes': nodes, 'stems': ui['stems']}
    blob = json.dumps(payload, ensure_ascii=False).replace('<', '\\u003c')
    stem0 = ui['stems'].get('long', '')
    return f'''<div class="w2-live" data-w2="{mode}">
<script type="application/json" class="w2-data">{blob}</script>
<div class="w2-grid">
<div class="w2-stage-fit">
<div class="orb-stage orb-stage--w2" data-stage="w2" style="width:640px;height:610px;">
{parts["svg"]}
<div class="orb-hub" style="{parts["hub_style"]}">
<span class="orb-hub-pulse"></span>
<div class="orb-hub-q2">{parts["q2"]}</div>
<div class="orb-hub-title">{esc(hub_title)}</div>{f'\n<div class="orb-hub-sub">{esc(hub_sub)}</div>' if hub_sub else ''}
</div>
{''.join(buttons)}
</div>
</div>
<div class="w2-detail-panel" data-panel="w2">
<div class="w2-panel-top">
<span class="w2-active-tag" data-role="tag">{esc(first["tag"])}</span>
<span class="w2-stem-pill" data-role="stem-pill">{esc(stem0)}</span>
</div>
<h3 data-role="h3">{esc(first["h3"])}</h3>
<p data-role="p">{esc(first["p"])}</p>
<div class="w2-kpi-grid" data-role="kpis">{kpis}</div>
<div class="w2-compare">
<div class="w2-bar-row">
<div class="w2-bar-head"><b data-role="bar-a-label">{esc(first["bar_a_label"])}</b><span class="w2-bar-val" data-role="bar-a-val">{esc(first["bar_a_val"])}</span></div>
<div class="w2-bar-track"><div class="w2-bar-fill" data-role="bar-a-fill" style="width:{int(first["bar_a_pct"])}%"></div></div>
</div>
<div class="w2-bar-row">
<div class="w2-bar-head"><span data-role="bar-b-label">{esc(first["bar_b_label"])}</span><span class="w2-bar-val muted" data-role="bar-b-val">{esc(first["bar_b_val"])}</span></div>
<div class="w2-bar-track"><div class="w2-bar-fill secondary" data-role="bar-b-fill" style="width:{int(first["bar_b_pct"])}%"></div></div>
</div>
</div>
<div class="w2-node-Strip">
<span class="strip-hint">{esc(ui["strip"])}</span>
<div class="strip-pills">{pills}<button type="button" class="replay-btn" data-w2-replay aria-label="{esc(ui["replay"])}">↻</button></div>
</div>
</div>
</div>
</div>'''
