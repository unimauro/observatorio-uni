#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Drill exploration: TipoGobierno -> Sector -> Pliego para año 2024, para descubrir mecánica."""
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


def fields(soup):
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
    return d


def list_rows(soup):
    """Devuelve [(label, grp1_value)] de las filas de datos."""
    rows = []
    for tr in soup.find_all("tr"):
        radio = tr.find("input", {"name": "grp1"})
        if not radio:
            continue
        # label: primera celda con texto tipo 'X: NOMBRE'
        txt = None
        for td in tr.find_all("td"):
            t = td.get_text(" ", strip=True)
            if re.match(r"^[\wÑ]+:\s", t) or (t and ":" in t and any(c.isalpha() for c in t)):
                txt = t; break
        rows.append((txt, radio.get("value")))
    return rows


def buttons(soup):
    return [(i.get("name"), i.get("value")) for i in soup.select("input")
            if (i.get("type") or "").lower() in ("submit", "button", "image")]


def post(s, soup, action, click_name, click_val, grp1_val=None):
    d = fields(soup)
    if grp1_val is not None:
        d["grp1"] = grp1_val
    d[click_name] = click_val
    r = s.post(BASE + action, data=d,
               headers={"Referer": BASE + action}, timeout=60)
    return BeautifulSoup(r.text, "lxml")


s = new_session()
s.get(f"{BASE}default.aspx?y={YEAR}&ap=ActProy", timeout=40)
soup = BeautifulSoup(s.get(f"{BASE}Navegar.aspx?y={YEAR}&ap=ActProy", timeout=40).text, "lxml")
action = soup.find("form").get("action")
g = soup.select_one('input[name=grp1]')
grp1 = g.get("value") if g else None

# Paso 1: Nivel de Gobierno
soup = post(s, soup, action, "ctl00$CPH1$BtnTipoGobierno", "Nivel de Gobierno", grp1)
print("=== NIVEL DE GOBIERNO ===")
rows = list_rows(soup)
for lbl, val in rows:
    print("  ROW:", lbl, "||", (val or "")[:40])
print("  BTNS:", [b[1] for b in buttons(soup)])

# elegir E: GOBIERNO NACIONAL
target = next((v for l, v in rows if l and l.strip().upper().startswith("E:")), None)
print("\n>> elijo E, grp1=", (target or "")[:40])
action2 = soup.find("form").get("action")
soup = post(s, soup, action2, "ctl00$CPH1$BtnSector", "Sector", target)
print("\n=== SECTOR ===")
rows = list_rows(soup)
for lbl, val in rows:
    if lbl:
        print("  ROW:", lbl)
print("  BTNS:", [b[1] for b in buttons(soup)])
