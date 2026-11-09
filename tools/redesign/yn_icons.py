"""Shared yes/no icons — single-stroke SVG check and dash (suction-bag approved)."""
from __future__ import annotations

import html as html_mod

_CHECK_SVG = (
    '<svg class="yn-ico" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
    '<path d="M5.5 12.5 L9.5 16.5 L18.5 7.5" fill="none" stroke="currentColor" '
    'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
)
_DASH_SVG = (
    '<svg class="yn-ico" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
    '<path d="M6 12h12" fill="none" stroke="currentColor" stroke-width="2.2" '
    'stroke-linecap="round"/></svg>'
)

# Data-URI masks (stroke black; color comes from background-color)
_CHECK_MASK = (
    "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' "
    "viewBox='0 0 24 24'%3E%3Cpath d='M5.5 12.5 L9.5 16.5 L18.5 7.5' fill='none' "
    "stroke='%23000' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'/%3E"
    "%3C/svg%3E\")"
)
_DASH_MASK = (
    "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' "
    "viewBox='0 0 24 24'%3E%3Cpath d='M6 12h12' fill='none' stroke='%23000' "
    "stroke-width='2.2' stroke-linecap='round'/%3E%3C/svg%3E\")"
)


def svg_check() -> str:
    return _CHECK_SVG


def svg_dash() -> str:
    return _DASH_SVG


def yn_yes(label: str) -> str:
    la = html_mod.escape(label, quote=True)
    return f'<span class="yn yn-yes" role="img" aria-label="{la}">{_CHECK_SVG}</span>'


def yn_no(label: str) -> str:
    la = html_mod.escape(label, quote=True)
    return f'<span class="yn yn-no" role="img" aria-label="{la}">{_DASH_SVG}</span>'


def yn_flag(flag: str, yes_label: str, no_label: str = '') -> str:
    if flag in ('yes', 'y', True):
        return yn_yes(yes_label)
    if flag in ('no', 'n', False, '×', 'x'):
        return yn_no(no_label or yes_label)
    return yn_no(no_label or yes_label)
