#!/usr/bin/env python3
"""Índice por persona natural de lo que la UNI (pliego 514, RUC 20169004359, PTE id 10048) le pagó, 2021-2026.

Fuentes oficiales (todas públicas, sin CAPTCHA):
  1. PTE "Personal" (planilla nominal mensual por régimen), vía las funciones de etl/build_planilla_pte.py
     (misma URL GET; caché en etl/cache_pte/).
  2. SEACE "Reporte de registro de órdenes de compra y órdenes de servicio" (OCOS) al que enlaza el PTE
     (rubro Contrataciones > Órdenes de compra/servicio). Es una vista JSF/PrimeFaces; se pide la página
     y luego el evento AJAX de paginación con rows=10000 para traer el mes completo en 2 peticiones.
     Caché en etl/cache_pte/ocos/ (gitignorado). Se guardan solo filas cuyo RUC es de persona natural (10, 15, 17).
     El buscador no trae datos desde mayo-2025 (cambio de plataforma por la Ley 32069): queda como brecha.
  3. CONOSCE adjudicaciones 2023-2025 (agregado por proveedor ya presente en data/proveedores-uni.json).
  4. OCDS/OECE (contratacionesabiertas.oece.gob.pe) para UNI, filas persona natural ya extraídas por el
     repo hermano peru-transparente (data/contratos.csv, data/ordenes_servicio.csv), con enlace al record.

Privacidad: se guarda el RUC (dato público del proveedor) pero NUNCA el DNI, ni se deriva del RUC.

Clave de persona = norm_key(nombre): mayúsculas, sin tildes, solo letras A-Z, tokens ordenados y unidos
por un espacio. "TALLEDO CORONADO, ARTURO FERNANDO" -> "ARTURO CORONADO FERNANDO TALLEDO".
Advertencia: un mismo nombre puede corresponder a dos personas (homonimia); la planilla no trae RUC/DNI.

Uso:
    python3 etl/build_pagos_personas.py                 # 2021..año actual, usa caché y descarga lo que falte
    python3 etl/build_pagos_personas.py --no-net        # solo caché
    python3 etl/build_pagos_personas.py --desde 2023 --sin-planilla
    python3 etl/build_pagos_personas.py --refresh-ocos-recientes   # vuelve a pedir OCOS de los últimos 3 meses
Solo stdlib.
"""
from __future__ import annotations

import argparse
import csv
import html
import json
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from http.cookiejar import CookieJar
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "etl"))
import build_planilla_pte as PL  # noqa: E402  (reutiliza URL, caché y parser de la planilla PTE)

OUT = ROOT / "data" / "pagos-personas-uni.json"
OUT_FULL = ROOT / "build" / "pagos-personas-uni.full.json"
CACHE_OCOS = ROOT / "etl" / "cache_pte" / "ocos"   # bajo etl/cache_pte/ (gitignorado)
PROVEEDORES = ROOT / "data" / "proveedores-uni.json"
PT_REPO = Path.home() / "Repos" / "peru-transparente"
PT_FILES = [PT_REPO / "data" / "contratos.csv", PT_REPO / "data" / "ordenes_servicio.csv"]

RUC_UNI = "20169004359"
OCOS_BASE = "https://prod2.seace.gob.pe/seacebus-uiwd-pub/buscadorPublico/ongei/buscadorPublicoOCOS.xhtml"
PTE_OCOS_URL = ("https://www.transparencia.gob.pe/contrataciones/pte_transparencia_ordenes_compra.aspx"
                "?id_entidad=10048&id_tema=34&Ver=")
OCDS_RECORD = "https://contratacionesabiertas.oece.gob.pe/api/v1/record/{ocid}"
UA = PL.UA
DELAY = 0.4             # pausa por petición (cortesía con los portales)
MAX_BYTES = 8_000_000
PREFIJOS_NATURAL = ("10", "15", "17")


def log(*a):
    print(*a, file=sys.stderr, flush=True)


def norm_key(nombre: str) -> str:
    """Clave de búsqueda: MAYÚSCULAS, sin tildes, tokens A-Z ordenados. Úsese igual al cruzar."""
    s = unicodedata.normalize("NFKD", nombre or "").encode("ascii", "ignore").decode()
    s = re.sub(r"[^A-Za-z ]+", " ", s.upper())
    return " ".join(sorted(t for t in s.split() if t))


def money_ocos(s: str) -> tuple[float | None, str]:
    s = (s or "").strip()
    moneda = "PEN"
    if s.startswith("US$") or s.startswith("$"):
        moneda = "USD"
    elif s.startswith("€"):
        moneda = "EUR"
    v = re.sub(r"^(S/\.?|US\$|\$|€)\s*", "", s).replace(",", "").strip()
    if not re.fullmatch(r"-?\d+(\.\d+)?", v or ""):
        return None, moneda
    return round(float(v), 2), moneda


# ------------------------------------------------------------------ SEACE OCOS
def ocos_url(anio: int, mes: int) -> str:
    return f"{OCOS_BASE}?ruc_entidad={RUC_UNI}&anio={anio}&mes={mes:02d}&theme=ongei"


def ocos_fetch(anio: int, mes: int) -> str:
    """GET de la vista + POST AJAX de paginación con rows grande. Devuelve el XML parcial (o el HTML si 0 filas)."""
    jar = CookieJar()
    op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    op.addheaders = [("User-Agent", UA), ("Accept-Language", "es-PE,es;q=0.9")]
    last = None
    for i in range(PL.RETRIES):
        try:
            page = op.open(ocos_url(anio, mes), timeout=90).read().decode("utf-8", "replace")
            m = re.search(r"rowCount:(\d+)", page)
            total = int(m.group(1)) if m else 0
            if total == 0:
                return f"<!--rowCount:0-->{page}"
            act = re.search(r'<form id="formBuscador"[^>]*action="([^"]+)"', page).group(1)
            vs = re.search(r'name="javax\.faces\.ViewState"[^>]*value="([^"]+)"', page).group(1)
            data = urllib.parse.urlencode({
                "javax.faces.partial.ajax": "true", "javax.faces.source": "formBuscador:dtProcesos",
                "javax.faces.partial.execute": "formBuscador:dtProcesos",
                "javax.faces.partial.render": "formBuscador:dtProcesos",
                "formBuscador:dtProcesos": "formBuscador:dtProcesos",
                "formBuscador:dtProcesos_pagination": "true", "formBuscador:dtProcesos_first": "0",
                "formBuscador:dtProcesos_rows": str(max(total, 15) + 100),
                "formBuscador:dtProcesos_encodeFeature": "true",
                "javax.faces.behavior.event": "page", "javax.faces.partial.event": "page",
                "formBuscador": "formBuscador", "javax.faces.ViewState": vs,
            }).encode()
            time.sleep(DELAY)
            req = urllib.request.Request("https://prod2.seace.gob.pe" + html.unescape(act), data=data, headers={
                "Faces-Request": "partial/ajax", "X-Requested-With": "XMLHttpRequest",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"})
            xml = op.open(req, timeout=300).read().decode("utf-8", "replace")
            return f"<!--rowCount:{total}-->{xml}"
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(2 ** i + 1)
    raise RuntimeError(f"OCOS {anio}-{mes:02d} falló: {last}")


def ocos_get(anio: int, mes: int, no_net: bool, refresh: bool) -> str | None:
    f = CACHE_OCOS / f"{anio}_{mes:02d}.xml"
    if f.exists() and not refresh:
        return f.read_text(encoding="utf-8")
    if no_net:
        return None
    t = ocos_fetch(anio, mes)
    CACHE_OCOS.mkdir(parents=True, exist_ok=True)
    f.write_text(t, encoding="utf-8")
    time.sleep(DELAY)
    return t


def ocos_parse(raw: str) -> tuple[int, list[list[str]]]:
    total = int(re.match(r"<!--rowCount:(\d+)-->", raw).group(1))
    rows = []
    if total:
        for tr in re.findall(r'<tr data-ri="\d+"[^>]*>(.*?)</tr>', raw, flags=re.S):
            cells = [PL._strip(c) for c in re.findall(r"<td[^>]*>(.*?)</td>", tr, flags=re.S)]
            if len(cells) >= 12:
                rows.append(cells[:12])
    return total, rows


def fecha_iso(s: str) -> str:
    m = re.match(r"(\d{4}-\d{2}-\d{2})", s or "")
    return m.group(1) if m else (s or "")


# ------------------------------------------------------------------ main
def main() -> int:
    hoy = datetime.now(timezone.utc)
    ap = argparse.ArgumentParser()
    ap.add_argument("--desde", type=int, default=2021)
    ap.add_argument("--hasta", type=int, default=hoy.year)
    ap.add_argument("--no-net", action="store_true")
    ap.add_argument("--sin-planilla", action="store_true")
    ap.add_argument("--sin-ocos", action="store_true")
    ap.add_argument("--refresh-ocos-recientes", action="store_true",
                    help="vuelve a pedir los últimos 3 meses de OCOS aunque estén en caché")
    ap.add_argument("--threads", type=int, default=2)
    a = ap.parse_args()
    anios = list(range(a.desde, a.hasta + 1))
    meses_todos = [(y, m) for y in anios for m in range(1, 13) if (y, m) <= (hoy.year, hoy.month)]
    recientes = set(meses_todos[-3:])

    personas: dict[str, dict] = {}

    def P(nombre: str) -> dict:
        k = norm_key(nombre)
        if k not in personas:
            personas[k] = {"nombre_fuente": nombre.strip(), "ruc": None, "planilla": {}, "planilla_cargos": {},
                           "ordenes": [], "adjudicaciones": []}
        return personas[k]

    cobertura: dict[str, dict] = {"planilla_pte": {}, "ordenes_seace_ocos": {}, "ocds_oece": {}}

    # ---------- 1. planilla PTE
    if not a.sin_planilla:
        orig_fetch = PL.fetch

        def polite(url):
            time.sleep(DELAY)
            return orig_fetch(url)
        PL.fetch = polite
        regs = [r for r in PL.REGIMENES]  # 8 = pensionistas excluido en build_planilla_pte
        tasks = [(y, m, r) for (y, m) in meses_todos for r in regs]
        res: dict[tuple[int, int, int], list[dict]] = {}
        with ThreadPoolExecutor(max_workers=max(1, min(3, a.threads))) as ex:
            for (y, m, r), fu in zip(tasks, [ex.submit(PL.download_month_regime, y, m, r, a.no_net, 1)
                                             for (y, m, r) in tasks]):
                try:
                    res[(y, m, r)] = fu.result()[2]
                except Exception as e:  # noqa: BLE001
                    log(f"  ! planilla {y}-{m:02d} r{r}: {e}")
                    res[(y, m, r)] = []
        def completo(y: int, m: int, r: int) -> bool:
            """True si están en caché todas las páginas que anuncia la página 1 (no se publica un mes a medias)."""
            f1 = PL.CACHE / f"{y}_{m:02d}_r{r}_p1.html"
            if not f1.exists():
                return False
            t = f1.read_text(encoding="utf-8", errors="replace")
            n = PL.last_page(t)
            return all((PL.CACHE / f"{y}_{m:02d}_r{r}_p{i}.html").exists() for i in range(1, n + 1))

        incompletos = sorted({f"{y}-{m:02d}" for (y, m, r) in tasks if res.get((y, m, r)) and not completo(y, m, r)})
        if incompletos:
            log(f"  ! meses de planilla incompletos (se omiten): {incompletos}")
        cobertura["planilla_pte_incompletos"] = incompletos
        if PL.BAD_ROWS:
            log(f"  ! {len(PL.BAD_ROWS)} filas de planilla con montos no numéricos (omitidas, no se inventa 0)")
        for (y, m) in meses_todos:
            if f"{y}-{m:02d}" in incompletos:
                continue
            vistos = set()
            n = 0
            for r in regs:
                for x in res.get((y, m, r), []):
                    sig = (x["regimen_pte"], x["nombre"], x["cargo"], x["dependencia"], x["total"])
                    if sig in vistos:  # fila repetida entre páginas
                        continue
                    vistos.add(sig)
                    n += 1
                    p = P(x["nombre"])
                    ym = f"{y}-{m:02d}"
                    p["planilla"][ym] = round(p["planilla"].get(ym, 0.0) + x["total"], 2)
                    p["planilla_cargos"][ym] = x["cargo"]
            if n:
                cobertura["planilla_pte"][f"{y}-{m:02d}"] = n

    # ---------- 2. órdenes SEACE (OCOS)
    ocos_stats = {"filas_totales": 0, "filas_persona_natural": 0}
    if not a.sin_ocos:
        for (y, m) in meses_todos:
            try:
                raw = ocos_get(y, m, a.no_net, a.refresh_ocos_recientes and (y, m) in recientes)
            except Exception as e:  # noqa: BLE001
                log(f"  ! {e}")
                cobertura["ordenes_seace_ocos"][f"{y}-{m:02d}"] = "error"
                continue
            if raw is None:
                continue
            total, rows = ocos_parse(raw)
            if total and len(rows) != total:
                log(f"  ! OCOS {y}-{m:02d}: {len(rows)} filas parseadas de {total}")
            nat = 0
            for c in rows:
                _, tipo, num, tipo_contr, desc, siaf, f_emi, f_comp, estado, monto_s, ruc, razon = c
                if not ruc.startswith(PREFIJOS_NATURAL) or len(ruc) != 11:
                    continue
                # el SEACE entrega la Ñ como '¿' (p. ej. 'ACU¿A'): se restituye solo entre letras
                razon = re.sub(r"(?<=[A-Za-z])¿(?=[A-Za-z])", "Ñ", razon)
                monto, moneda = money_ocos(monto_s)
                if monto is None:
                    log(f"  ! monto no numérico OCOS {y}-{m:02d}: {razon} {monto_s!r}")
                    continue
                nat += 1
                p = P(razon)
                p["ruc"] = p["ruc"] or ruc
                p["ordenes"].append({
                    "anio": y, "tipo": "compra" if tipo.upper().startswith("O/C") else "servicio",
                    "numero": num, "monto": monto, "moneda": moneda, "estado": estado,
                    "descripcion": desc[:140], "fecha": fecha_iso(f_emi), "exp_siaf": siaf,
                    "fuente_url": ocos_url(y, m),
                })
            ocos_stats["filas_totales"] += total
            ocos_stats["filas_persona_natural"] += nat
            cobertura["ordenes_seace_ocos"][f"{y}-{m:02d}"] = {"filas": total, "persona_natural": nat}

    # ---------- 3. CONOSCE adjudicaciones 2023-2025 (agregado)
    prov_meta = {}
    if PROVEEDORES.exists():
        d = json.loads(PROVEEDORES.read_text(encoding="utf-8"))
        prov_meta = d.get("_meta", {})
        for pr in d.get("proveedores", []):
            ruc = str(pr.get("ruc") or "")
            if not ruc.startswith(PREFIJOS_NATURAL):
                continue
            p = P(pr["nombre"])
            p["ruc"] = p["ruc"] or ruc
            p["adjudicaciones"].append({
                "fuente": "CONOSCE", "periodo": prov_meta.get("periodo", "2023-2025"), "anio": None,
                "monto": pr.get("monto"), "moneda": "PEN", "n_procesos": pr.get("n"),
                "tipos": pr.get("tipos"), "objeto": pr.get("objeto"),
                "fuente_url": prov_meta.get("fuente_url"),
            })

    # ---------- 4. OCDS/OECE (filas UNI persona natural extraídas por peru-transparente)
    vistos = set()
    for f in PT_FILES:
        if not f.exists():
            continue
        with f.open(encoding="utf-8", errors="ignore", newline="") as fh:
            for r in csv.DictReader(line.replace("\x00", "") for line in fh):
                ent = (r.get("comprador") or r.get("entidad") or "").upper()
                if "UNIVERSIDAD NACIONAL DE INGENIER" not in ent:
                    continue
                ruc = r.get("proveedor_ruc") or r.get("ruc") or ""
                fecha = (r.get("fecha") or "")[:10]
                if not ruc.startswith(PREFIJOS_NATURAL) or not fecha[:4].isdigit():
                    continue
                y = int(fecha[:4])
                if y < a.desde or y > a.hasta:
                    continue
                k = (r["ocid"], ruc)
                try:
                    monto = round(float(r.get("monto") or ""), 2)
                except ValueError:
                    continue
                if k in vistos:
                    # ordenes_servicio.csv aporta la descripción que contratos.csv no tiene
                    if r.get("descripcion"):
                        for adj in P(r["proveedor"])["adjudicaciones"]:
                            if adj.get("ocid") == r["ocid"] and not adj.get("descripcion"):
                                adj["descripcion"] = r["descripcion"][:140]
                    continue
                vistos.add(k)
                p = P(r["proveedor"])
                p["ruc"] = p["ruc"] or ruc
                p["adjudicaciones"].append({
                    "fuente": "OCDS-OECE", "anio": y, "fecha": fecha, "ocid": r["ocid"],
                    "monto": monto, "moneda": r.get("moneda") or "PEN",
                    "descripcion": (r.get("descripcion") or r.get("objeto") or "")[:140],
                    "fuente_url": OCDS_RECORD.format(ocid=r["ocid"]),
                })
                cobertura["ocds_oece"][str(y)] = cobertura["ocds_oece"].get(str(y), 0) + 1

    # ---------- totales
    ult_meses = sorted(cobertura["planilla_pte"])[-12:]
    for p in personas.values():
        por_anio: dict[str, dict] = defaultdict(lambda: {"planilla": 0.0, "planilla_meses": 0,
                                                          "ordenes": 0.0, "adjudicaciones": 0.0})
        for ym, v in p["planilla"].items():
            por_anio[ym[:4]]["planilla"] += v
            por_anio[ym[:4]]["planilla_meses"] += 1
        tot_ord = 0.0
        for o in p["ordenes"]:
            if o["moneda"] == "PEN" and not o["estado"].upper().startswith("ANUL"):
                por_anio[str(o["anio"])]["ordenes"] += o["monto"]
                tot_ord += o["monto"]
        tot_adj = 0.0
        for j in p["adjudicaciones"]:
            if j.get("moneda", "PEN") == "PEN" and isinstance(j.get("monto"), (int, float)):
                tot_adj += j["monto"]
                if j.get("anio"):
                    por_anio[str(j["anio"])]["adjudicaciones"] += j["monto"]
        ult = sorted(p["planilla"])
        p["totales"] = {
            # suma de lo publicado en los últimos 12 meses con datos de planilla (ventana común a todos)
            "planilla_anual_aprox": round(sum(p["planilla"].get(ym, 0.0) for ym in ult_meses), 2) if p["planilla"] else 0.0,
            "planilla_ultimo_mes": {"mes": ult[-1], "total": p["planilla"][ult[-1]],
                                    "cargo": p["planilla_cargos"].get(ult[-1])} if ult else None,
            "ordenes": round(tot_ord, 2),
            "adjudicaciones": round(tot_adj, 2),
            "por_anio": {y: {k: (round(v, 2) if isinstance(v, float) else v) for k, v in d.items() if v}
                         for y, d in sorted(por_anio.items())},
        }
        p.pop("planilla_cargos")
        p["planilla"] = dict(sorted(p["planilla"].items()))
        p["ordenes"].sort(key=lambda o: (o["fecha"], o["numero"]))

    pl_anios = sorted({ym[:4] for ym in cobertura["planilla_pte"]})
    meta = {
        "titulo": "Pagos de la UNI a personas naturales (planilla, órdenes de compra/servicio y adjudicaciones), 2021-2026",
        "entidad": "Universidad Nacional de Ingeniería (pliego 514, RUC 20169004359, PTE id_entidad 10048)",
        "generado": hoy.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "script": "etl/build_pagos_personas.py",
        "clave": ("norm_key(nombre): MAYÚSCULAS, sin tildes ni signos, tokens A-Z ordenados y unidos por un espacio. "
                  "Ej. 'Talledo Coronado, Arturo Fernando' -> 'ARTURO CORONADO FERNANDO TALLEDO'."),
        "fuentes": {
            "planilla": {
                "nombre": "Portal de Transparencia Estándar (PTE) - Personal, planilla nominal mensual",
                "url": PL.query_url(2026, 9, 3, 1),
                "url_patron": PL.BASE + "?id_entidad=10048&in_anno_consulta={AAAA}&ch_mes_consulta={MM}&ch_tipo_regimen={1..9}&id_tema=32&pag={n}",
                "periodo": f"{min(cobertura['planilla_pte'], default='-')} a {max(cobertura['planilla_pte'], default='-')}",
                "campo": "planilla['AAAA-MM'] = suma de TOTAL INGRESOS (remuneración + honorarios + incentivo + aguinaldo + otros) de todas las filas de la persona ese mes",
            },
            "ordenes": {
                "nombre": "SEACE - Reporte de registro de órdenes de compra y de servicio (enlazado desde el PTE, rubro Contrataciones)",
                "url": PTE_OCOS_URL,
                "url_patron": OCOS_BASE + "?ruc_entidad=20169004359&anio={AAAA}&mes={MM}&theme=ongei",
                "periodo": f"{min((k for k, v in cobertura['ordenes_seace_ocos'].items() if isinstance(v, dict) and v['filas']), default='-')} a "
                           f"{max((k for k, v in cobertura['ordenes_seace_ocos'].items() if isinstance(v, dict) and v['filas']), default='-')}",
                "filtro": "solo RUC 10/15/17 (persona natural); totales excluyen estado 'Anulada' y montos en moneda extranjera",
                **ocos_stats,
            },
            "adjudicaciones_conosce": {
                "nombre": prov_meta.get("fuente", "CONOSCE adjudicaciones"),
                "url": prov_meta.get("fuente_url"), "periodo": prov_meta.get("periodo", "2023-2025"),
                "nota": "Agregado por proveedor para todo el periodo (sin desglose anual); tomado de data/proveedores-uni.json.",
            },
            "adjudicaciones_ocds": {
                "nombre": "OECE Contrataciones Abiertas (OCDS), awards a persona natural con comprador UNI",
                "url": "https://contratacionesabiertas.oece.gob.pe/",
                "nota": "Filas tomadas de peru-transparente (data/contratos.csv y data/ordenes_servicio.csv); cada fila enlaza a su record OCDS. "
                        "Cobertura parcial: depende de lo que ese repo haya barrido.",
            },
        },
        "cobertura": {
            "planilla_pte_personas_por_mes": cobertura["planilla_pte"],
            "planilla_anios": pl_anios,
            "planilla_meses_incompletos_omitidos": cobertura.get("planilla_pte_incompletos", []),
            "ordenes_seace_por_mes": cobertura["ordenes_seace_ocos"],
            "ocds_filas_por_anio": cobertura["ocds_oece"],
        },
        "notas": [
            "planilla_anual_aprox = suma de los últimos 12 meses con planilla publicada en el PTE (" +
            (f"{ult_meses[0]} a {ult_meses[-1]}" if ult_meses else "-") + "); 0 si la persona no figura en planilla.",
            "El PTE no publica nominalmente a todos los docentes (ver data/planilla-uni.json, AIRHSP); ausencia en planilla no prueba que no cobre.",
            "El buscador SEACE de órdenes (OCOS) no devuelve datos para la UNI desde mayo-2025 (migración por la Ley 32069 a la nueva plataforma); "
            "las órdenes posteriores no están cubiertas por esta fuente.",
            "Clave por nombre: posible homonimia; la planilla del PTE no trae RUC ni DNI. Verifique con cargo/fecha antes de afirmar identidad.",
            "No se publica DNI ni se deriva del RUC.",
            "En las órdenes SEACE la Ñ llega como '¿' (ACU¿A); se restituye a Ñ solo entre letras.",
            "Montos tal cual los publica la fuente; no se imputan meses faltantes.",
        ],
    }
    out = {"_meta": meta, "personas": dict(sorted(personas.items()))}
    txt = json.dumps(out, ensure_ascii=False, separators=(",", ":"))
    if len(txt.encode()) > MAX_BYTES:
        OUT_FULL.parent.mkdir(parents=True, exist_ok=True)
        OUT_FULL.write_text(txt, encoding="utf-8")
        log(f"completo ({len(txt.encode())/1e6:.1f} MB) en {OUT_FULL}; se escribe versión ligera")
        slim = {}
        for k, p in personas.items():
            q = dict(p)
            q["planilla"] = {ym: v for ym, v in p["planilla"].items() if ym.endswith("-12") or ym == max(p["planilla"])} \
                if p["planilla"] else {}
            q["ordenes"] = [{"anio": o["anio"], "tipo": o["tipo"], "monto": o["monto"], "fecha": o["fecha"],
                             "estado": o["estado"], "descripcion": o["descripcion"][:80]}
                            | ({"moneda": o["moneda"]} if o["moneda"] != "PEN" else {}) for o in p["ordenes"]]
            slim[k] = q
        meta["version_ligera"] = ("planilla solo diciembre de cada año + último mes (los totales anuales completos están en totales.por_anio); "
                                  "órdenes sin número/SIAF/url (url_patron por año-mes en _meta.fuentes.ordenes), descripción a 80 caracteres, moneda solo si no es PEN. "
                                  "Versión completa: build/pagos-personas-uni.full.json")
        txt = json.dumps({"_meta": meta, "personas": slim}, ensure_ascii=False, separators=(",", ":"))
    OUT.write_text(txt, encoding="utf-8")
    n_pl = sum(1 for p in personas.values() if p["planilla"])
    n_or = sum(1 for p in personas.values() if p["ordenes"])
    n_ad = sum(1 for p in personas.values() if p["adjudicaciones"])
    log(f"OK {OUT} {len(txt.encode())/1e6:.2f} MB · {len(personas)} personas "
        f"(planilla {n_pl}, órdenes {n_or}, adjudicaciones {n_ad})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
