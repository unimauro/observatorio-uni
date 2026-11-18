#!/usr/bin/env python3
"""Cruce: integrantes de órganos de gobierno de la UNI × pagos de la UNI × JNE (autoridades electas).

Entradas
  data/organos-gobierno-uni.json   (etl/build_organos_gobierno.py)
  data/pagos-personas-uni.json     (etl/build_pagos_personas.py)
  build/partidos-jne-index.json    (etl/build_partidos_jne.py; opcional)
  data/afiliacion-manual.json      (consultas manuales al ROP del JNE; opcional)
Salida
  data/organos-cruce.json

Reglas: coincidencia por NOMBRE (sin DNI). «exacta» = mismo conjunto de palabras del nombre;
«parcial» = el nombre del órgano (≥3 palabras) está contenido en un único nombre de la fuente de pagos.
Toda coincidencia es de nombre y puede ser un homónimo. No se publica DNI.
"""
import json, re, unicodedata, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ORG = ROOT / "data/organos-gobierno-uni.json"
PAG = ROOT / "data/pagos-personas-uni.json"
JNE = ROOT / "build/partidos-jne-index.json"
MAN = ROOT / "data/afiliacion-manual.json"
OUT = ROOT / "data/organos-cruce.json"


def toks(s: str) -> list[str]:
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().upper()
    s = re.sub(r"\(.*?\)", " ", s.replace("'", ""))                       # «(a.i.)», «(e)»
    stop = {"DE", "DEL", "LA", "LOS", "LAS", "Y", "VDA", "DR", "DRA", "ING", "ARQ", "MSC", "MG", "MAG", "LIC", "PHD", "ECON", "ABOG", "SR", "SRA", "SRTA", "MBA", "SC", "ALUM", "BACH"}
    return [t for t in re.findall(r"[A-Z]+", s) if t not in stop and len(t) > 1]


def key(s: str) -> str:
    return " ".join(sorted(toks(s)))


def main():
    org = json.loads(ORG.read_text())
    pag = json.loads(PAG.read_text())
    P = pag["personas"]
    # índice de pagos con la misma normalización (por si difieren artículos «DE», «LA»)
    pidx = {}
    for k, v in P.items():
        pidx.setdefault(key(v.get("nombre_fuente") or k), []).append(k)
    psets = [(set(kk.split()), kk) for kk in pidx]
    jne = json.loads(JNE.read_text()) if JNE.exists() else {}
    jidx = {}
    for k, v in jne.items() if isinstance(jne, dict) else []:
        if isinstance(v, list):
            jidx[key(k)] = v
    if isinstance(jne, dict) and "index" in jne:
        jidx = {key(k): v for k, v in jne["index"].items()}
    man = json.loads(MAN.read_text()).get("registros", {}) if MAN.exists() else {}

    personas = {}
    for m in org["miembros"]:
        k = key(m["nombre"])
        limpio = re.sub(r"\(.*?\)", "", m["nombre"])
        limpio = re.sub(r"^((Dra?|Ing|Arq|M\.?\s?Sc|Mag|Mg|Lic|Econ|Abog|Alum|Bach|Srta?)\.?\s+)+", "", limpio.strip(), flags=re.I).strip()
        p = personas.setdefault(k, {"nombre": limpio.title() if limpio.isupper() else limpio, "cargos": []})
        p["cargos"].append({x: m.get(x) for x in ("organo", "facultad", "estamento", "cargo", "periodo", "estado", "fuente_url", "fuente_fecha", "nota")})

    for k, p in personas.items():
        match, tipo = pidx.get(k), "exacta"
        if not match:
            s = set(k.split())
            cands = [kk for ss, kk in psets if len(s) >= 3 and s <= ss]
            match, tipo = (pidx[cands[0]], "parcial") if len(cands) == 1 else (None, None)
        p["coincidencia_pagos"] = tipo
        if match:
            r = P[match[0]]
            t = r.get("totales", {})
            ords = r.get("ordenes", [])
            por_anio = {}
            for o in ords:
                if (o.get("estado") or "").lower().startswith("anul"):
                    continue
                a = por_anio.setdefault(str(o["anio"]), {"n": 0, "monto": 0.0})
                a["n"] += 1; a["monto"] = round(a["monto"] + (o.get("monto") or 0), 2)
            p["pagos"] = {
                "nombre_fuente": r.get("nombre_fuente"),
                "homonimos_en_fuente": len(match) > 1,
                "planilla_ultimo_mes": t.get("planilla_ultimo_mes"),
                "planilla_por_anio": {a: {"total": v.get("planilla"), "meses": v.get("planilla_meses")} for a, v in (t.get("por_anio") or {}).items() if v.get("planilla")},
                "ordenes_total": round(sum(v["monto"] for v in por_anio.values()), 2),
                "ordenes_n": sum(v["n"] for v in por_anio.values()),
                "ordenes_por_anio": por_anio,
                "ordenes_muestra": [{x: o.get(x) for x in ("fecha", "tipo", "monto", "descripcion")} for o in sorted((o for o in ords if not (o.get("estado") or "").lower().startswith("anul")), key=lambda o: -(o.get("monto") or 0))[:5]],
                "adjudicaciones_total": t.get("adjudicaciones") or 0,
            }
        j = jidx.get(k)
        if j:
            p["jne_electo"] = [{x: e.get(x) for x in ("proceso", "anio", "organizacion_politica", "cargo_postulado", "estado", "fuente_url")} for e in j]
        if k in man:
            p["rop_manual"] = man[k]

    lst = sorted(personas.values(), key=lambda p: (-(p.get("pagos", {}).get("ordenes_total") or 0), p["nombre"]))
    out = {
        "_meta": {
            "generado": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
            "script": "etl/build_organos_cruce.py",
            "metodo": "Cruce por nombre (sin DNI) entre integrantes de órganos de gobierno (fuentes oficiales: CEUNI, resoluciones en gob.pe) y pagos de la UNI a personas naturales (PTE planilla; SEACE órdenes de compra/servicio; OECE adjudicaciones), más autoridades electas del JNE (datos abiertos). «exacta» = mismas palabras del nombre; «parcial» = nombre contenido en un único registro. Una coincidencia de nombre puede ser un homónimo.",
            "fuentes": {"organos": org["_meta"].get("fuentes", [])[:40], "pagos": pag["_meta"].get("fuentes"), "jne": "datosabiertos.gob.pe: Autoridades electas (2014–2026) y Autoridades vigentes (JNE)"},
            "cobertura_pagos": {"planilla": pag["_meta"]["fuentes"]["planilla"].get("periodo"), "ordenes": pag["_meta"]["fuentes"]["ordenes"].get("periodo")},
            "limites": [
                "Sin DNI: las coincidencias son por nombre y pueden ser homónimos.",
                "Órdenes de servicio de la UNI en SEACE solo hasta abril de 2025 (cambio de plataforma por la Ley 32069).",
                "JNE: solo personas ELECTAS a un cargo público (no lista completa de candidatos ni afiliados).",
                "La afiliación partidaria se consulta por DNI en el ROP del JNE (con captcha); se registra a mano en data/afiliacion-manual.json con fecha y evidencia.",
                "Recibir pagos de la UNI o haber sido electo por un partido no implica irregularidad.",
            ],
            "n_personas": len(lst),
            "n_con_pagos": sum(1 for p in lst if p.get("pagos")),
            "n_con_ordenes": sum(1 for p in lst if p.get("pagos", {}).get("ordenes_n")),
            "n_jne": sum(1 for p in lst if p.get("jne_electo")),
        },
        "personas": lst,
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")))
    print(json.dumps(out["_meta"] | {"fuentes": "…"}, ensure_ascii=False, indent=1)[:1500])


if __name__ == "__main__":
    main()
