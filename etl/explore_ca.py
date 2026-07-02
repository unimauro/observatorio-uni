#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Explora la Consulta Amigable: dump de botones y filas para entender el drill a pliego 514."""
import requests, re
from bs4 import BeautifulSoup

BASE = "https://apps5.mineco.gob.pe/transparencia/Navegador/"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
YEAR = 2024


def new_session():
    s = requests.Session()
    s.headers.update({"User-Agent": UA})
    s.get(BASE + "default.aspx", timeout=40)
    return s


def dump_buttons(soup, label):
    print(f"\n=== BUTTONS @ {label} ===")
    for inp in soup.select("input"):
        t = (inp.get("type") or "text").lower()
        if t in ("submit", "button", "image"):
            print("  btn:", inp.get("name"), "|", inp.get("value"))
    print("--- grp1 radios (rows) ---")
    for inp in soup.select('input[name=grp1]'):
        print("  grp1 value:", (inp.get("value") or "")[:80])


def fields(soup, click_name=None, click_val=None):
    d = {}
    for inp in soup.select("input"):
        n = inp.get("name"); t = (inp.get("type") or "text").lower()
        if not n or t in ("submit", "button", "image", "reset"):
            continue
        if t in ("radio", "checkbox"):
            if inp.has_attr("checked"):
                d[n] = inp.get("value", "on")
        else:
            d[n] = inp.get("value", "")
    for sel in soup.select("select"):
        n = sel.get("name")
        if n:
            o = sel.select_one("option[selected]") or sel.select_one("option")
            d[n] = o.get("value", "") if o else ""
    if click_name:
        d[click_name] = click_val
    return d


s = new_session()
s.get(f"{BASE}default.aspx?y={YEAR}&ap=ActProy", timeout=40)
html = s.get(f"{BASE}Navegar.aspx?y={YEAR}&ap=ActProy", timeout=40).text
soup = BeautifulSoup(html, "lxml")
sel = soup.select_one("#ctl00_CPH1_DrpYear option[selected]")
print("year fijado:", sel.get_text(strip=True) if sel else "?")
dump_buttons(soup, "Navegar inicial")
print("\naction:", soup.find("form").get("action"))
