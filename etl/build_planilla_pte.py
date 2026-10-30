#!/usr/bin/env python3
"""Planilla nominal de la UNI desde el Portal de Transparencia Estándar (PTE).

Descarga, para un año, todos los meses y regímenes laborales del rubro "Personal"
de la entidad (id_entidad=10048 = Universidad Nacional de Ingeniería) y genera
data/planilla-uni.json (schema v2) que consume app.js (sección Planilla).

Solo stdlib. Idempotente: el HTML crudo se guarda en etl/cache_pte/ (gitignorado);
si el archivo ya existe no se vuelve a descargar. Borrar la caché para refrescar.

Uso:
    python3 etl/build_planilla_pte.py                # año en curso, meses 1..mes actual (sin argumentos; apto para CI)
    python3 etl/build_planilla_pte.py --anio 2026 --meses 1-12 --threads 4
    python3 etl/build_planilla_pte.py --no-net       # solo caché (sin red)
    PTE_MONTHS=3 python3 etl/build_planilla_pte.py   # CI: solo los últimos 3 meses calendario; la serie de los
                                                     # meses anteriores del mismo año se conserva del JSON previo

Salida ≠ 0 (y NO se sobreescribe data/planilla-uni.json) si el portal falla, si ningún mes trae filas
o si el mes más reciente trae menos de la mitad de personas que el JSON anterior (portal a medias).

Tabla PTE: RÉGIMEN | APELLIDOS Y NOMBRES | CARGO | DEPENDENCIA |
           REMUNERACIONES | HONORARIOS | INCENTIVO | AGUINALDO/GRATIFICACIÓN | OTROS | TOTAL
A veces sigue una fila "DESCRIPCIÓN:" con el detalle de "OTROS" → campo `descripcion`.

Todo lo que llega del portal es dato externo no confiable: se normaliza y se
escapa en el front (esc()). Nunca se listan estudiantes (el PTE no los publica).
"""
from __future__ import annotations

import argparse
import html
import json
import os
import re
import statistics
import sys
import time
import unicodedata
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "etl" / "cache_pte"
OUT = ROOT / "data" / "planilla-uni.json"
CANDIDATES = Path(os.environ.get("CANDIDATES_JSON")
                  or "/Users/unimauro/Documents/Repos/observatorio-electoral-uni/src/data/candidates.json")
CANDIDATES_URL = "https://raw.githubusercontent.com/unimauro/observatorio-electoral-uni/main/src/data/candidates.json"
ELECTORAL_SITE = "https://unimauro.github.io/observatorio-electoral-uni/"

BASE = "https://www.transparencia.gob.pe/personal/pte_transparencia_personal.aspx"
ID_ENTIDAD = 10048
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
TIMEOUT = 60
RETRIES = 4

# Códigos de régimen del PTE. 8 = Pensionistas se excluye (no son cargos vigentes).
REGIMENES = {
    1: "CAS", 2: "Régimen 276", 3: "Régimen 728/OTROS", 4: "PAC", 5: "FAG",
    6: "PNUD", 7: "Altos Funcionarios", 9: "Ley Servir",
}
# Etiquetas legibles para el front
REG_LABEL = {
    "CAS": "CAS (D.Leg. 1057)",
    "Régimen 276": "D.Leg. 276 (nombrados)",
    "Régimen 728/OTROS": "Régimen 728 / otros (donde el PTE lista a los docentes)",
    "PAC": "PAC", "FAG": "FAG", "PNUD": "PNUD",
    "Altos Funcionarios": "Altos funcionarios", "Ley Servir": "Ley Servir (30057)",
}
MESES = ["", "enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "setiembre", "octubre", "noviembre", "diciembre"]

_HEADER_TOKENS = (
    "APELLIDOS Y", "RÉGIMEN LABORAL", "REGIMEN LABORAL", "DETALLE DE INGRESOS", "TOTAL INGRESOS",
    "REMUNERACIONES", "HONORARIOS", "DEPENDENCIA Y/O", "NO SE ENCONTR", "NO EXISTE INFORMACI",
    "FILTROS DE B", "SELECCIONE",
)


def log(*a):
    print(*a, file=sys.stderr, flush=True)


# ---------------------------------------------------------------- red + caché
def query_url(anio: int, mes: int, reg: int, pag: int) -> str:
    return (f"{BASE}?id_entidad={ID_ENTIDAD}&in_anno_consulta={anio}&ch_mes_consulta={mes:02d}"
            f"&vc_nombre_funcionario=&vc_dni_funcionario=&ch_tipo_regimen={reg}&id_tema=32&Ver=&pag={pag}")


def fetch(url: str) -> str:
    last = None
    for i in range(RETRIES):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,*/*",
                                                      "Accept-Language": "es-PE,es;q=0.9"})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                raw = r.read()
            for enc in ("utf-8", "latin-1"):
                try:
                    return raw.decode(enc)
                except UnicodeDecodeError:
                    continue
            return raw.decode("utf-8", "replace")
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as e:
            last = e
            wait = 2 ** i + 0.5
            log(f"  ! reintento {i + 1}/{RETRIES} en {wait:.0f}s: {url[-40:]} ({e})")
            time.sleep(wait)
    raise RuntimeError(f"fallo definitivo: {url} ({last})")


def get_page(anio: int, mes: int, reg: int, pag: int, no_net: bool) -> str | None:
    f = CACHE / f"{anio}_{mes:02d}_r{reg}_p{pag}.html"
    if f.exists():
        return f.read_text(encoding="utf-8", errors="replace")
    if no_net:
        return None
    t = fetch(query_url(anio, mes, reg, pag))
    CACHE.mkdir(parents=True, exist_ok=True)
    f.write_text(t, encoding="utf-8")
    return t


# ---------------------------------------------------------------- parseo
def _strip(s: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


class BadMoney(ValueError):
    """Monto no numérico en el portal: se aborta sin escribir (nunca se inventa un 0)."""


BAD_ROWS: list[str] = []  # filas con montos no numéricos (si hay alguna, no se escribe el JSON)


def money(s: str) -> float:
    s = (s or "").replace("S/.", "").replace("S/", "").replace(",", "").strip()
    if s in ("", "-", "--"):
        return 0.0
    if not re.fullmatch(r"-?\d{1,9}(\.\d{1,2})?", s):
        raise BadMoney(s)
    return round(float(s), 2)


def last_page(page: str) -> int:
    """Número de la última página según el enlace 'Ultimo' (1 si no hay paginación)."""
    m = re.search(r"pag=(\d+)'>\s*Ultimo\s*</a>", page, re.I)
    return int(m.group(1)) if m else 1


def has_next(page: str) -> bool:
    return bool(re.search(r"pag=\d+'>\s*Siguiente\s*</a>", page, re.I))


def parse_rows(page: str) -> list[dict]:
    t = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", page, flags=re.S | re.I)
    out: list[dict] = []
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", t, flags=re.S | re.I):
        cells = [_strip(td) for td in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", tr, flags=re.S | re.I)]
        if not cells:
            continue
        if cells[0].upper().startswith("DESCRIPCI"):
            if out and len(cells) >= 2:
                out[-1]["descripcion"] = cells[1][:400]
            continue
        cells = [c for c in cells if c != ""]
        if len(cells) < 10:
            continue
        up = " ".join(cells).upper()
        if any(h in up for h in _HEADER_TOKENS):
            continue
        regimen, nombre, cargo, dep = cells[0], cells[1], cells[2], cells[3]
        if not re.search(r"[A-Za-zÁÉÍÓÚÑ]", nombre) or ("," not in nombre and len(nombre.split()) < 2):
            continue
        try:
            inc = [money(c) for c in cells[-6:]]
        except BadMoney as e:
            BAD_ROWS.append(f"{nombre} | {cargo} | monto no numérico {e!r}")
            continue
        out.append({
            "regimen_pte": str(regimen), "nombre": str(nombre)[:120], "cargo": str(cargo)[:160],
            "dependencia": str(dep)[:160],
            "remun": float(inc[0]), "honorarios": float(inc[1]), "incentivo": float(inc[2]),
            "aguinaldo": float(inc[3]), "otros": float(inc[4]), "total": float(inc[5]),
        })
    return out


# ---------------------------------------------------------------- descarga por (mes, régimen)
def download_month_regime(anio: int, mes: int, reg: int, no_net: bool, pool_pages: int) -> tuple[int, int, list[dict]]:
    """Devuelve (mes, reg, filas). Página 1 primero; si hay 'Ultimo' se traen las demás en paralelo."""
    p1 = get_page(anio, mes, reg, 1, no_net)
    if p1 is None:
        return mes, reg, []
    rows = parse_rows(p1)
    if not rows:
        return mes, reg, []
    n_last = last_page(p1)
    pages: dict[int, list[dict]] = {1: rows}
    if n_last > 1:
        with ThreadPoolExecutor(max_workers=pool_pages) as ex:
            futs = {ex.submit(get_page, anio, mes, reg, p, no_net): p for p in range(2, n_last + 1)}
            for fu in as_completed(futs):
                p = futs[fu]
                t = fu.result()
                pages[p] = parse_rows(t) if t else []
    elif has_next(p1):  # sin 'Ultimo' pero con 'Siguiente': recorrer secuencialmente
        p = 2
        while True:
            t = get_page(anio, mes, reg, p, no_net)
            r = parse_rows(t) if t else []
            if not r:
                break
            pages[p] = r
            if not has_next(t):
                break
            p += 1
    allrows: list[dict] = []
    for p in sorted(pages):
        for r in pages[p]:
            r["pag"] = p
            allrows.append(r)
    return mes, reg, allrows


# ---------------------------------------------------------------- normalización
def categoria(cargo: str) -> str:
    c = cargo.upper()
    if re.search(r"DOCENTE|PROFESOR|JEFE DE PR[AÁ]CTICA|CATEDR|INVESTIGADOR", c):
        return "docente"
    if re.search(r"\bRECTOR|VICE\s?RECTOR|VICERRECTOR|DECAN|DIRECTOR|\bJEFE\b|JEFA\b|SECRETARI[AO] GENERAL|GERENTE|SUBDIRECTOR|SUB DIRECTOR", c):
        return "funcionario"
    return "administrativo"


def norm_tokens(name: str) -> tuple[str, ...]:
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    s = re.sub(r"[^A-Za-z ]+", " ", s.upper())
    return tuple(sorted(t for t in s.split() if t))


def load_candidates(no_net: bool) -> list[dict]:
    """candidates.json del observatorio electoral: ruta local (o $CANDIDATES_JSON) y, si no existe, el raw de GitHub."""
    if CANDIDATES.exists():
        data = json.loads(CANDIDATES.read_text(encoding="utf-8"))
    elif not no_net:
        try:
            data = json.loads(fetch(CANDIDATES_URL))
            log(f"  candidatos desde {CANDIDATES_URL}")
        except Exception as e:  # noqa: BLE001
            log(f"  (no se pudo leer candidates.json local ni remoto: {e}; se omite cruce electoral)")
            return []
    else:
        log(f"  (sin candidates.json en {CANDIDATES}; se omite cruce electoral)")
        return []
    if not isinstance(data, list):
        return []
    out = []
    for c in data:
        names = [c.get("officialName") or c.get("name") or ""] + list(c.get("nameVariants") or [])
        out.append({
            "id": c.get("id"), "listId": c.get("listId"), "role": c.get("role"), "slug": c.get("slug"),
            "officialName": c.get("officialName") or c.get("name"),
            "keys": {norm_tokens(n) for n in names if n},
        })
    return out


def median(xs: list[float]) -> float:
    return round(statistics.median(xs), 2) if xs else 0.0


# ---------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser()
    hoy = datetime.now(timezone.utc)
    ap.add_argument("--anio", type=int, default=hoy.year)
    ap.add_argument("--meses", default=None, help="rango 'a-b' o lista '7,8,9' (por defecto 1..mes actual; $PTE_MONTHS=N limita a los últimos N meses)")
    ap.add_argument("--regimenes", default=",".join(str(k) for k in REGIMENES))
    ap.add_argument("--threads", type=int, default=4, help="máx. hilos (tareas × páginas en total)")
    ap.add_argument("--no-net", action="store_true", help="solo caché, sin descargas")
    ap.add_argument("--out", default=str(OUT))
    a = ap.parse_args()

    if a.meses is None:
        hi = hoy.month if a.anio == hoy.year else 12
        n_env = os.environ.get("PTE_MONTHS", "").strip()
        lo = max(1, hi - int(n_env) + 1) if n_env.isdigit() and int(n_env) > 0 else 1
        meses = list(range(lo, hi + 1))
    elif "-" in a.meses:
        lo, hi = a.meses.split("-")
        meses = list(range(int(lo), int(hi) + 1))
    else:
        meses = [int(x) for x in a.meses.split(",") if x]
    regs = [int(x) for x in a.regimenes.split(",") if x and int(x) in REGIMENES]
    threads = max(1, min(4, a.threads))

    prev = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    airhsp = (prev.get("resumen") or {}).get("por_regimen_airhsp") or []
    airhsp_total = (prev.get("_meta") or {}).get("total_planilla_airhsp")
    prev_total = (prev.get("_meta") or {}).get("total") or 0
    # serie previa del mismo año para los meses que esta corrida no consulta (modo PTE_MONTHS)
    prev_serie = [s for s in (prev.get("serie_mensual") or []) if s.get("anio") == a.anio and s.get("mes") not in meses]

    log(f"PTE UNI {a.anio}: meses {meses}, regímenes {regs}, hilos {threads}, no_net={a.no_net}")
    t0 = time.time()
    # Las tareas (mes, régimen) corren de a `threads`; cada tarea pagina con 1 hilo para
    # no superar `threads` conexiones simultáneas al portal.
    result: dict[tuple[int, int], list[dict]] = {}
    try:
        with ThreadPoolExecutor(max_workers=threads) as ex:
            futs = [ex.submit(download_month_regime, a.anio, m, r, a.no_net, 1) for m in meses for r in regs]
            for fu in as_completed(futs):
                mes, reg, rows = fu.result()
                result[(mes, reg)] = rows
                if rows:
                    log(f"  {a.anio}-{mes:02d} r{reg} {REGIMENES[reg]:<20} {len(rows):5d} filas  ({time.time() - t0:.0f}s)")
    except Exception as e:  # noqa: BLE001
        log(f"ERROR: el portal falló ({e}); no se sobreescribe {a.out}")
        return 2
    dur = time.time() - t0
    log(f"descarga/caché lista en {dur:.0f}s")
    if BAD_ROWS:
        log(f"ERROR: {len(BAD_ROWS)} fila(s) con montos no numéricos; no se sobreescribe {a.out}:")
        for b in BAD_ROWS[:20]:
            log("   " + b)
        return 4

    # --- series y meta
    serie = list(prev_serie)
    meses_con_datos = sorted({m for (m, r), rows in result.items() if rows})
    regs_con_datos = sorted({r for (m, r), rows in result.items() if rows})
    discrepancias = 0
    for (m, r), rows in sorted(result.items()):
        if not rows:
            continue
        for x in rows:
            suma = x["remun"] + x["honorarios"] + x["incentivo"] + x["aguinaldo"] + x["otros"]
            if abs(suma - x["total"]) > 1.0:
                discrepancias += 1
                if discrepancias <= 10:
                    log(f"  ! suma≠total {a.anio}-{m:02d} {REGIMENES[r]}: {x['nombre']} | {x['cargo']} | suma {suma:.2f} vs total {x['total']:.2f}")
        serie.append({"anio": a.anio, "mes": m, "regimen": REG_LABEL.get(REGIMENES[r], REGIMENES[r]),
                      "n": len(rows), "masa_total": round(sum(x["total"] for x in rows), 2)})
    if not meses_con_datos:
        log("Sin datos en ningún mes consultado: no se sobreescribe el JSON.")
        return 1
    mes_ult = meses_con_datos[-1]
    serie.sort(key=lambda s: (s["mes"], s["regimen"]))
    meses_con_datos = sorted({s["mes"] for s in serie})

    # --- personas del mes más reciente
    cands = load_candidates(a.no_net)
    personas = []
    for r in regs:
        for x in result.get((mes_ult, r), []):
            p = {
                "nombre": x["nombre"], "cargo": x["cargo"], "dependencia": x["dependencia"],
                "regimen": REG_LABEL.get(x["regimen_pte"], x["regimen_pte"]),
                "categoria": categoria(x["cargo"]),
                "remun": x["remun"], "honorarios": x["honorarios"], "incentivo": x["incentivo"],
                "aguinaldo": x["aguinaldo"], "otros": x["otros"], "total": x["total"],
            }
            if x.get("descripcion"):
                p["descripcion"] = x["descripcion"]
            personas.append(p)
    personas.sort(key=lambda p: (-p["total"], p["nombre"], p["regimen"], p["cargo"]))
    if prev_total and len(personas) < 0.5 * prev_total:
        log(f"ERROR: {MESES[mes_ult]} trae {len(personas)} personas, menos de la mitad del JSON anterior ({prev_total}); "
            f"portal probablemente incompleto. No se sobreescribe {a.out}.")
        return 3

    # --- cruce electoral (match exacto de multiconjunto de tokens del nombre completo)
    cruzados = []
    if cands:
        by_key: dict[tuple[str, ...], dict] = {}
        for c in cands:
            for k in c["keys"]:
                by_key[k] = c
        for p in personas:
            c = by_key.get(norm_tokens(p["nombre"]))
            if c:
                p["electoral"] = {"candidateId": c["id"], "listId": c["listId"], "role": c["role"],
                                  "url": f"{ELECTORAL_SITE}#/candidatos/{c['slug']}"}
                cruzados.append({"candidateId": c["id"], "listId": c["listId"], "role": c["role"],
                                 "nombre": p["nombre"], "cargo": p["cargo"], "regimen": p["regimen"],
                                 "total": p["total"]})
        # Un candidato podría aparecer dos veces en el mismo mes (dos regímenes); contamos personas distintas.
        ids_distintos = sorted({c["candidateId"] for c in cruzados})
    else:
        ids_distintos = []

    # --- resúmenes
    def stats(xs: list[float]) -> dict:
        xs = [v for v in xs if v > 0]
        return {"n": len(xs), "prom": round(sum(xs) / len(xs), 2) if xs else 0, "mediana": median(xs),
                "min": min(xs) if xs else 0, "max": max(xs) if xs else 0}

    por_reg = []
    grupos: dict[str, list[dict]] = defaultdict(list)
    for p in personas:
        grupos[p["regimen"]].append(p)
    for rg, grp in sorted(grupos.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        s = stats([p["total"] for p in grp])
        por_reg.append({"nombre": rg, "n": len(grp), "total_mes": round(sum(p["total"] for p in grp), 2),
                        "prom": s["prom"], "mediana": s["mediana"], "max": s["max"]})
    cargos = Counter(p["cargo"] for p in personas)
    top_cargos = []
    for cg, n in sorted(cargos.items(), key=lambda kv: (-kv[1], kv[0]))[:20]:
        tot = [p["total"] for p in personas if p["cargo"] == cg]
        top_cargos.append({"cargo": cg, "n": n, "prom": round(sum(tot) / n, 2), "total_mes": round(sum(tot), 2)})
    deps: dict[str, list[float]] = defaultdict(list)
    for p in personas:
        deps[p["dependencia"]].append(p["total"])
    por_dep = sorted(({"dependencia": d, "n": len(v), "total_mes": round(sum(v), 2), "prom": round(sum(v) / len(v), 2)}
                      for d, v in deps.items()), key=lambda x: (-x["total_mes"], x["dependencia"]))[:25]
    por_cat = [{"nombre": k, "n": v} for k, v in Counter(p["categoria"] for p in personas).most_common()]
    remun = stats([p["total"] for p in personas])
    remun["n_cero"] = sum(1 for p in personas if p["total"] <= 0)
    remun["nota"] = (f"Estadísticos sobre TOTAL INGRESOS (S/) del mes {MESES[mes_ult]} {a.anio}, todos los regímenes "
                     f"nominales del PTE, excluyendo {remun['n_cero']} registros con total 0.")
    top_ing = [{"nombre": p["nombre"], "cargo": p["cargo"], "regimen": p["regimen"], "total": p["total"]} for p in personas[:25]]
    masa_mes = round(sum(p["total"] for p in personas), 2)

    meses_sin = [m for m in range(1, max(meses) + 1) if m not in meses_con_datos]
    regs_sin = [REGIMENES[r] for r in regs if r not in regs_con_datos]
    url_fuente = query_url(a.anio, mes_ult, 1, 1)
    out = {
        "_meta": {
            "schema": 2,
            "fuente": "Portal de Transparencia Estándar (PTE) · rubro Personal · transparencia.gob.pe (nominal) + AIRHSP (agregado docentes)",
            "url_fuente": url_fuente,
            "entidad": f"Universidad Nacional de Ingeniería (UNI) - pliego 514 / id_entidad PTE {ID_ENTIDAD}",
            "anio": a.anio, "mes": mes_ult, "mes_nombre": MESES[mes_ult],
            "total": len(personas),
            "personas_distintas": len({p["nombre"] for p in personas}),
            "nota_total": "total = registros (una persona puede figurar con dos cargos, p.ej. vicerrector + profesor); personas_distintas = nombres únicos",
            "masa_mensual_total": masa_mes,
            "total_planilla_airhsp": airhsp_total,
            "meses_consultados": meses, "meses_con_datos": meses_con_datos, "meses_sin_datos": meses_sin,
            "regimenes_consultados": [REGIMENES[r] for r in regs],
            "regimenes_con_datos": [REGIMENES[r] for r in regs_con_datos],
            "regimenes_sin_datos": regs_sin,
            "discrepancias_suma": discrepancias,
            "cruce_electoral": {
                "candidatos_total": len(cands), "candidatos_en_planilla": len(ids_distintos),
                "metodo": "igualdad exacta del multiconjunto de tokens del nombre completo (sin tildes, mayúsculas) entre 'APELLIDOS, NOMBRES' del PTE y officialName/nameVariants de candidates.json",
                "fuente_candidatos": "observatorio-electoral-uni/src/data/candidates.json (CEUNI, listas definitivas 2026)",
                "matches": cruzados,
            },
            "nota": (f"Solo docentes, funcionarios y personal administrativo: nunca estudiantes. Lista NOMINAL del PTE (rubro Personal) "
                     f"para la UNI, mes más reciente con datos: {MESES[mes_ult]} {a.anio} ({len(personas)} personas; regímenes "
                     f"{', '.join(REGIMENES[r] for r in regs_con_datos)}). El TOTAL mensual incluye aguinaldo/gratificación y 'otros' "
                     f"(julio y diciembre traen aguinaldo, por eso la masa de esos meses sube). El bucket 'Régimen 728/OTROS' es la etiqueta "
                     f"del PTE: ahí publica a los docentes (Ley 30220), no es el DL 728 del agregado AIRHSP. El PTE puede no listar a todo el "
                     f"personal (el agregado AIRHSP registra {airhsp_total} plazas). El 'sueldo_promedio' AIRHSP es remuneración base por plaza; "
                     f"el promedio PTE es total de ingresos del mes (incluye otros ingresos y aguinaldo), no son comparables. Meses sin datos en el portal: {meses_sin or 'ninguno'}. "
                     f"Regímenes consultados sin filas: {', '.join(regs_sin) or 'ninguno'}. No se inventaron personas ni sueldos."),
            "generado": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        },
        "resumen": {
            "por_regimen_nominal": por_reg,
            "por_regimen_airhsp": airhsp,
            "por_categoria": por_cat,
            "top_cargos": top_cargos,
            "por_dependencia": por_dep,
            "remun": remun,
        },
        "serie_mensual": serie,
        "top_ingresos": top_ing,
        "personas": personas,
    }
    Path(a.out).write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

    # --- reporte
    log(f"\n== {MESES[mes_ult]} {a.anio}: {len(personas)} personas, masa S/ {masa_mes:,.2f}, discrepancias suma: {discrepancias}")
    for r in por_reg:
        log(f"   {r['nombre']:<32} n={r['n']:5d}  masa={r['total_mes']:>14,.2f}  prom={r['prom']:>10,.2f}  med={r['mediana']:>10,.2f}  max={r['max']:>10,.2f}")
    log("== serie mensual")
    for s in serie:
        log(f"   {s['anio']}-{s['mes']:02d} {s['regimen']:<32} n={s['n']:5d}  masa={s['masa_total']:>14,.2f}")
    log(f"== cruce electoral: {len(ids_distintos)}/{len(cands)} candidatos en planilla")
    for c in cruzados:
        log(f"   {c['candidateId']} {c['listId']} {c['role']:<26} {c['nombre']:<40} {c['cargo']:<45} S/ {c['total']:,.2f}")
    log(f"escrito {a.out} (descarga {dur:.0f}s, total {time.time() - t0:.0f}s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
