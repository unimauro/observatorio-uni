#!/usr/bin/env python3
"""Índice por nombre de vínculos político-partidarios (JNE, datos abiertos).

Construye build/partidos-jne-index.json a partir de los datasets ABIERTOS del
Jurado Nacional de Elecciones publicados en la Plataforma Nacional de Datos
Abiertos (datosabiertos.gob.pe). Sirve para cruzar nombres (p. ej. miembros de
los órganos de gobierno de la UNI) con candidaturas / cargos de elección popular.

Fuentes (descarga directa, sin captcha, sin formulario):
  - "Autoridades electas en procesos electorales - JNE"
      https://www.datosabiertos.gob.pe/dataset/autoridades-electas-en-procesos-electorales-jurado-nacional-de-elecciones
      ERM 2014/2018/2022, EG 2016/2021/2026, ECE 2020, complementarias, revocatoria 2021...
  - "Autoridades vigentes a nivel nacional - JNE"
      https://www.datosabiertos.gob.pe/dataset/autoridades-vigentes-nivel-nacional-jurado-nacional-de-elecciones
      Incluye accesitarios/reemplazos que asumieron el cargo.
El script lee cada página de dataset y descarga todos los .xls/.xlsx de datos que
enlace (excluye el diccionario), así toma versiones nuevas sin tocar el código.

LÍMITE IMPORTANTE: estas fuentes solo traen AUTORIDADES ELECTAS (y reemplazos), no
a todos los candidatos. Un nombre ausente NO significa que la persona no haya
postulado ni que no esté afiliada. Tampoco traen la condición
afiliado/designado/invitado: el campo "condicion" queda en null. Ver el informe
del ETL para lo que no está disponible en abierto (listas completas de candidatos
de Infogob/Plataforma Electoral y padrones de afiliados del ROP: requieren
captcha o formulario, y NO se automatizan).

Privacidad / DNI
  Algunas versiones del archivo traen DOCUMENTOIDENTIDAD (DNI). El DNI NUNCA se
  escribe en la salida. Para desambiguar homónimos se guarda "dni_hash" =
  HMAC-SHA256(sal, dni)[:16]. No se usa sha256 "a secas" porque el espacio de DNI
  (10^8) se recorre por fuerza bruta en segundos y el hash sería reversible.
  La sal se toma de la variable JNE_DNI_SALT o del archivo
  ~/.config/observatorio-uni/jne_dni_salt (se crea al primer uso, fuera del repo).
  Con la misma sal, quien tenga un DNI puede calcular dni_hash(dni) y comparar.

Uso (necesita xlrd para leer .xls BIFF; p. ej. el python de pyenv del usuario):
    python3 -I etl/build_partidos_jne.py --raw-dir /ruta/vacia/jne_raw
    python3 -I etl/build_partidos_jne.py --raw-dir ... --no-net      # solo caché
    python3 -I etl/build_partidos_jne.py --lookup "LOPEZ CHAU NAVA, PABLO ALFONSO"

Todo lo descargado es dato externo no confiable: solo se lee como tabla.
"""
from __future__ import annotations

import argparse
import hashlib
import hmac
import html
import json
import os
import re
import secrets
import sys
import tempfile
import unicodedata
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "build" / "partidos-jne-index.json"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/130.0 Safari/537.36 observatorio-uni-etl")
PORTAL = "https://www.datosabiertos.gob.pe"
DATASETS = {
    "autoridades_electas": PORTAL + "/dataset/autoridades-electas-en-procesos-electorales-jurado-nacional-de-elecciones",
    "autoridades_vigentes": PORTAL + "/dataset/autoridades-vigentes-nivel-nacional-jurado-nacional-de-elecciones",
}
SALT_FILE = Path.home() / ".config" / "observatorio-uni" / "jne_dni_salt"


# ----------------------------------------------------------------- normalización
def norm_text(s) -> str:
    if s is None:
        return ""
    s = str(s).strip()
    if s.lower() in ("nan", "none"):
        return ""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.upper()
    s = re.sub(r"[^A-Z0-9 ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def name_key(*parts) -> str:
    """Nombre completo normalizado: mayúsculas, sin tildes, tokens ordenados.

    Acepta "APELLIDOS, NOMBRES" o las partes separadas; el orden no importa.
    """
    toks = []
    for p in parts:
        toks.extend(norm_text(str(p).replace(",", " ")).split())
    return " ".join(sorted(toks))


# ----------------------------------------------------------------- DNI hash
def _salt() -> bytes:
    env = os.environ.get("JNE_DNI_SALT")
    if env:
        return env.encode()
    if SALT_FILE.exists():
        return SALT_FILE.read_text().strip().encode()
    SALT_FILE.parent.mkdir(parents=True, exist_ok=True)
    val = secrets.token_hex(32)
    SALT_FILE.write_text(val + "\n")
    os.chmod(SALT_FILE, 0o600)
    return val.encode()


def dni_hash(dni, salt: bytes | None = None) -> str | None:
    d = re.sub(r"\D", "", str(dni or ""))
    if not d or set(d) == {"0"}:
        return None
    d = d.zfill(8)
    return hmac.new(salt or _salt(), d.encode(), hashlib.sha256).hexdigest()[:16]


# ----------------------------------------------------------------- descarga
def http_get(url: str, timeout=300) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def discover_files(page_url: str) -> list[str]:
    body = http_get(page_url, 60).decode("utf-8", "replace")
    links = re.findall(r'href="([^"]+\.(?:xls|xlsx|csv))"', body, re.I)
    out = []
    for l in links:
        l = html.unescape(l)
        if "diccionario" in l.lower():
            continue
        u = urllib.parse.urljoin(page_url, l)
        if urllib.parse.urlparse(u).netloc.endswith("datosabiertos.gob.pe") and u not in out:
            out.append(u)
    return out


def fetch_all(raw_dir: Path, no_net: bool) -> list[tuple[str, str, Path]]:
    """Devuelve [(dataset, url, ruta_local)]. Guarda manifest.json en raw_dir."""
    raw_dir.mkdir(parents=True, exist_ok=True)
    manifest_p = raw_dir / "manifest.json"
    if no_net:
        man = json.loads(manifest_p.read_text())
        return [(m["dataset"], m["url"], raw_dir / m["file"]) for m in man]
    man = []
    for ds, page in DATASETS.items():
        try:
            urls = discover_files(page)
        except Exception as e:  # portal caído: seguir con lo que haya
            print(f"[warn] no se pudo leer {page}: {e}", file=sys.stderr)
            continue
        for u in urls:
            fname = urllib.parse.unquote(u.rsplit("/", 1)[-1]).replace(" ", "_")
            fname = re.sub(r"[^A-Za-z0-9._-]", "_", fname)
            dest = raw_dir / fname
            if not dest.exists():
                print(f"[get] {u}", file=sys.stderr)
                dest.write_bytes(http_get(u))
            man.append({"dataset": ds, "page": page, "url": u, "file": fname})
    manifest_p.write_text(json.dumps(man, indent=1))
    return [(m["dataset"], m["url"], raw_dir / m["file"]) for m in man]


# ----------------------------------------------------------------- lectura
def read_rows(path: Path) -> list[dict]:
    suf = path.suffix.lower()
    if suf == ".xls":
        try:
            import xlrd  # type: ignore
        except ImportError:
            sys.exit("Falta xlrd (pip install xlrd) para leer .xls del JNE.")
        wb = xlrd.open_workbook(str(path), on_demand=True)
        sh = wb.sheet_by_index(0)
        rows = [sh.row_values(i) for i in range(sh.nrows)]
    elif suf == ".xlsx":
        import zipfile  # noqa: F401  (openpyxl si está; si no, se omite)
        try:
            import openpyxl  # type: ignore
        except ImportError:
            print(f"[warn] sin openpyxl, se omite {path.name}", file=sys.stderr)
            return []
        ws = openpyxl.load_workbook(path, read_only=True, data_only=True).worksheets[0]
        rows = [list(r) for r in ws.iter_rows(values_only=True)]
    else:
        import csv
        with open(path, newline="", encoding="utf-8", errors="replace") as f:
            rows = list(csv.reader(f))
    if not rows:
        return []
    hdr = [re.sub(r"^(TX|NU)(?=[A-Z])", "", norm_text(h).replace(" ", "")) for h in rows[0]]
    out = []
    for r in rows[1:]:
        d = {}
        for h, v in zip(hdr, r):
            if isinstance(v, float) and v.is_integer():
                v = str(int(v))
            d[h] = "" if v is None else str(v).strip()
        out.append(d)
    return out


def anio_de(proceso: str, anio: str) -> int | None:
    m = re.search(r"(19|20)\d\d", anio or "") or re.search(r"(19|20)\d\d", proceso or "")
    return int(m.group(0)) if m else None


def to_entry(r: dict, url: str, dataset: str, salt: bytes) -> tuple[str, dict] | None:
    nombres, ap, am = r.get("NOMBRES", ""), r.get("APELLIDOPATERNO", ""), r.get("APELLIDOMATERNO", "")
    key = name_key(ap, am, nombres)
    if not key or key in ("AUTORIDAD SIN",):  # fila de relleno "SIN AUTORIDAD" del JNE
        return None
    proceso = norm_text(r.get("PROCESOELECTORAL"))
    ubi = r.get("UBIGEO", "")
    loc = " / ".join(x for x in (norm_text(r.get("REGION")), norm_text(r.get("PROVINCIA")),
                                 norm_text(r.get("DISTRITO"))) if x)
    # El archivo de vigentes se reconoce por su columna AUTORIDADREEMPLAZO, no por la
    # página: la página de "vigentes" también enlaza una copia del histórico de electos.
    if "AUTORIDADREEMPLAZO" in r:
        reemplazo = r.get("AUTORIDADREEMPLAZO", "")
        estado = "vigente (accesitario/reemplazo)" if reemplazo not in ("", "0") else "vigente"
    else:
        estado = "electo"
    e = {
        "proceso": proceso,
        "anio": anio_de(proceso, r.get("ANIOELECCION", "")),
        "organizacion_politica": norm_text(r.get("ORGANIZACIONPOLITICA")),
        "tipo_organizacion": norm_text(r.get("TIPOORGPOLITICA")),
        "cargo_postulado": norm_text(r.get("CARGO")),
        "ubigeo/distrito": (ubi + (" " + loc if loc else "")).strip() or None,
        "ambito": norm_text(r.get("AMBITO")),
        "periodo": norm_text(r.get("PERIODO")),
        "condicion": None,  # afiliado/designado/invitado: no viene en estos datasets
        "estado": estado,
        "nombre_fuente": f"{norm_text(ap)} {norm_text(am)}, {norm_text(nombres)}".strip(),
        "dni_hash": dni_hash(r.get("DOCUMENTOIDENTIDAD"), salt) if r.get("DOCUMENTOIDENTIDAD") else None,
        "fuente_url": url,
    }
    return key, e


def build(raw_dir: Path, no_net: bool) -> dict:
    salt = _salt()
    files = fetch_all(raw_dir, no_net)
    index: dict[str, list] = defaultdict(list)
    seen: dict[tuple, dict] = {}
    stats = []
    for ds, url, p in files:
        rows = read_rows(p)
        n = 0
        for r in rows:
            ke = to_entry(r, url, ds, salt)
            if not ke:
                continue
            key, e = ke
            n += 1
            dk = (key, e["proceso"], e["cargo_postulado"], e["ubigeo/distrito"], e["organizacion_politica"])
            prev = seen.get(dk)
            if prev is not None:  # duplicado entre archivos: completar dni_hash / fuentes
                if not prev["dni_hash"] and e["dni_hash"]:
                    prev["dni_hash"] = e["dni_hash"]
                if e["fuente_url"] not in prev["fuentes_url"]:
                    prev["fuentes_url"].append(e["fuente_url"])
                if e["estado"] != prev["estado"] and e["estado"] not in prev["estado"]:
                    prev["estado"] = prev["estado"] + "; " + e["estado"]
                continue
            e["fuentes_url"] = [e["fuente_url"]]
            seen[dk] = e
            index[key].append(e)
        procs = defaultdict(int)
        for r in rows:
            procs[norm_text(r.get("PROCESOELECTORAL"))] += 1
        stats.append({"dataset": ds, "url": url, "archivo": p.name, "filas": len(rows),
                      "filas_con_nombre": n, "procesos": dict(sorted(procs.items()))})
    for k in index:
        index[k].sort(key=lambda e: (e["anio"] or 0, e["proceso"]))
        for e in index[k]:
            if len(e["fuentes_url"]) == 1:  # fuente_url ya lo dice; no duplicar
                del e["fuentes_url"]
    return {
        "meta": {
            "generado": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "clave": "nombre completo normalizado (mayúsculas, sin tildes, tokens ordenados)",
            "cobertura": "Solo autoridades ELECTAS/vigentes (JNE, datosabiertos.gob.pe). "
                         "No incluye candidatos no electos ni afiliación (condicion=null).",
            "dni": "Nunca se guarda el DNI. dni_hash = HMAC-SHA256(sal local, DNI)[:16].",
            "fuentes": stats,
            "personas_clave": len(index),
            "registros": sum(len(v) for v in index.values()),
        },
        "index": dict(sorted(index.items())),
    }


# ----------------------------------------------------------------- lookup
def homonym_risk(entries: list[dict]) -> dict:
    hashes = {e["dni_hash"] for e in entries if e.get("dni_hash")}
    regiones = {(e.get("ubigeo/distrito") or "")[:2] for e in entries if e.get("ubigeo/distrito")}
    regiones.discard("00")  # ámbito nacional / extranjero
    regiones.discard("")
    reasons = []
    if len(hashes) > 1:
        reasons.append(f"{len(hashes)} DNI distintos (hash) con el mismo nombre")
    if len(regiones) > 1:
        reasons.append(f"aparece en {len(regiones)} departamentos distintos (ubigeo)")
    return {"riesgo_homonimo": bool(reasons), "motivos": reasons,
            "dni_hash_distintos": len(hashes)}


def lookup(names: list[str], index: dict | None = None, path: Path = OUT) -> dict:
    """Busca nombres por coincidencia EXACTA de tokens normalizados (orden libre).

    names: ["APELLIDOS, NOMBRES", ...] u otro orden. Devuelve
      {nombre_consultado: {"clave", "encontrado", "registros", "riesgo_homonimo", "motivos", ...}}
    No hay coincidencia difusa: "JUAN RODRIGUEZ" no encuentra "JUAN MARTIN RODRIGUEZ RODRIGUEZ".
    """
    if index is None:
        index = json.loads(Path(path).read_text())["index"]
    out = {}
    for n in names:
        k = name_key(n)
        entries = index.get(k, [])
        res = {"clave": k, "encontrado": bool(entries), "registros": entries}
        res.update(homonym_risk(entries) if entries else
                   {"riesgo_homonimo": False, "motivos": [], "dni_hash_distintos": 0})
        out[n] = res
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--raw-dir", default=os.environ.get("JNE_RAW_DIR",
                    os.path.join(tempfile.gettempdir(), "observatorio-uni-jne_raw")),
                    help="carpeta (vacía, fuera del repo) para los archivos crudos")
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--no-net", action="store_true", help="usar solo la caché de --raw-dir")
    ap.add_argument("--lookup", nargs="*", help="solo consultar el índice ya generado")
    a = ap.parse_args()
    if a.lookup is not None:
        print(json.dumps(lookup(a.lookup, path=Path(a.out)), ensure_ascii=False, indent=1))
        return
    data = build(Path(a.raw_dir), a.no_net)
    if not data["index"]:
        sys.exit("Índice vacío: no se escribe la salida.")
    outp = Path(a.out)
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")))
    m = data["meta"]
    print(f"OK {outp}: {m['personas_clave']} nombres, {m['registros']} registros", file=sys.stderr)
    for s in m["fuentes"]:
        print(f"  {s['filas']:>6} filas  {s['archivo']}  ({s['dataset']})", file=sys.stderr)


if __name__ == "__main__":
    main()
