#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Indicadores por facultad de la UNI: docentes, masa salarial, presupuesto y producción científica.

Fuentes (todas abiertas):
  - data/planilla-uni.json  (Portal de Transparencia Estándar, planilla nominal; docentes por dependencia)
  - data/presupuesto-uni.json (MEF/SIAF, PIM y devengado por facultad del último año cerrado)
  - OpenAlex (CC0): artículos con afiliación UNI (I62520931) en VENTANA; autores UNI cruzados por nombre
    con la planilla docente de cada facultad.
  - data/vri-proyectos.json (opcional): proyectos financiados por el VRI con facultad, monto y fuente.

Política del observatorio: SOLO se publican agregados por facultad. El cruce persona↔autor es por nombre
(hay homonimia y variantes) y no se usa para calificar a nadie; ningún nombre sale de este script.

Escribe data/facultades-uni.json.
"""
import json, os, re, time, unicodedata, urllib.parse, urllib.request
from collections import defaultdict

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, "..", "data")
OA_INST = "I62520931"
VENTANA = (2021, 2025)
CACHE = os.path.join(HERE, "cache_openalex_uni_%d_%d.json" % VENTANA)

# dependencia de planilla (PTE) → clave corta; y nombre SIAF → clave
FAC = {
    "FIC": ("Ingeniería Civil", ["INGENIERIA CIVIL"], ["Ing. Civil"]),
    "FC": ("Ciencias", ["FACULTAD DE CIENCIAS"], ["Ciencias"]),
    "FIM": ("Ingeniería Mecánica", ["INGENIERIA MECANICA"], ["Ing. Mecanica"]),
    "FIEE": ("Ingeniería Eléctrica y Electrónica", ["ELECTRICA Y ELECTRONICA"], ["Ing. Electrica Y Electronica"]),
    "FIIS": ("Ingeniería Industrial y de Sistemas", ["INDUSTRIAL Y DE SISTEMAS"], ["Ing. Industrial y Sistemas"]),
    "FAUA": ("Arquitectura, Urbanismo y Artes", ["ARQUITECTURA"], ["Arquitectura, Urbanismo Y Artes"]),
    "FIEECS": ("Ing. Económica, Estadística y CC. Sociales", ["ECONOMICA"], ["Ing. Economica, Estadistica Y Ciencias Sociales"]),
    "FIGMM": ("Ing. Geológica, Minera y Metalúrgica", ["GEOLOGICA"], ["Ing. Geologica, Minera Y Metalurgica"]),
    "FIQT": ("Ingeniería Química y Textil", ["QUIMICA Y TEXTIL"], ["Ing. Quimica Y Textil"]),
    "FIA": ("Ingeniería Ambiental", ["INGENIERIA AMBIENTAL"], ["Ing. Ambiental"]),
    "FIP": ("Ing. de Petróleo, Gas Natural y Petroquímica", ["PETROLEO"], ["Ing. De Petroleo, Gas Natural Y Petroquimica"]),
}


def norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().upper()
    return re.sub(r"[^A-Z ]", " ", s)


def fac_de(dep):
    d = norm(dep)
    for k, (_, pats, _) in FAC.items():
        if any(p in d for p in pats):
            return k
    return None


def tokens(s):
    return [t for t in norm(s).split() if len(t) > 1 and t not in {"DE", "DEL", "LA", "LOS", "LAS", "Y", "VDA"}]


def clave_planilla(nombre):
    """'APELLIDO1 APELLIDO2, NOMBRE1 NOMBRE2' → (apellido1, inicial nombre1, set apellidos+nombres)."""
    if "," not in nombre:
        return None
    ap, no = nombre.split(",", 1)
    a, n = tokens(ap), tokens(no)
    if not a or not n:
        return None
    return a[0], n[0][0], set(a) | set(n), n[0]


def oa_get(url):
    for i in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "observatorio-uni (datos abiertos)"}), timeout=60) as r:
                return json.loads(r.read())
        except Exception as e:  # noqa: BLE001
            print("  reintento", i, repr(e)[:80], flush=True)
            time.sleep(5 * (i + 1))
    raise SystemExit("OpenAlex no responde")


def autores_uni():
    """{author_id: {'name':..., 'works': set(work_id)}} para autorías con afiliación UNI en la ventana."""
    if os.path.exists(CACHE):
        raw = json.load(open(CACHE))
    else:
        # paginación por página (el cursor exige API key desde 2026); OpenAlex permite hasta 10,000 resultados así
        raw, page, total = [], 1, None
        while total is None or len(raw) < total:
            url = ("https://api.openalex.org/works?filter=institutions.id:%s,publication_year:%d-%d"
                   "&select=id,publication_year,authorships&per_page=200&page=%d") % (OA_INST, VENTANA[0], VENTANA[1], page)
            d = oa_get(url)
            total = min(d["meta"]["count"], 10000)
            if not d["results"]:
                break
            for w in d["results"]:
                raw.append({"id": w["id"], "y": w["publication_year"],
                            "a": [{"id": (a.get("author") or {}).get("id"), "n": (a.get("author") or {}).get("display_name"),
                                   "raw": a.get("raw_author_name"),
                                   "uni": any((i or {}).get("id", "").endswith(OA_INST) for i in a.get("institutions") or [])}
                                  for a in w.get("authorships") or []]})
            page += 1
            print("  obras:", len(raw), flush=True)
            time.sleep(0.5)
        json.dump(raw, open(CACHE, "w"))
    out = defaultdict(lambda: {"names": set(), "works": set()})
    for w in raw:
        for a in w["a"]:
            if a["uni"] and a["id"]:
                out[a["id"]]["names"].update(x for x in (a["n"], a["raw"]) if x)
                out[a["id"]]["works"].add(w["id"])
    return out, len(raw)


def main():
    plan = json.load(open(os.path.join(DATA, "planilla-uni.json")))
    pres = json.load(open(os.path.join(DATA, "presupuesto-uni.json")))
    docentes = [p for p in plan["personas"] if p.get("categoria") == "docente"]

    # índice apellido1+inicial → docentes (con facultad)
    idx = defaultdict(list)
    sin_fac = 0
    for p in docentes:
        f = fac_de(p.get("dependencia"))
        k = clave_planilla(p["nombre"])
        if not f:
            sin_fac += 1
        if f and k:
            idx[(k[0], k[1])].append((p, f, k))

    autores, n_obras = autores_uni()
    match = {}  # id(persona) → set(obras)
    for aid, a in autores.items():
        cands = set()
        for nm in a["names"]:
            t = tokens(nm)
            if len(t) < 2:
                continue
            # OpenAlex suele dar 'Nombre Apellido1 Apellido2': probar cada token como apellido1
            for i, ap in enumerate(t):
                for ini in {x[0] for x in t if x != ap}:
                    for (p, f, k) in idx.get((ap, ini), []):
                        # exigir ≥2 tokens en común (apellido1 + nombre o apellido2) para reducir homonimia
                        if len(set(t) & k[2]) >= 2:
                            cands.add(id(p))
        if len(cands) == 1:  # ambiguo (2+ docentes posibles) → se descarta
            match.setdefault(cands.pop(), set()).update(a["works"])

    by = {k: {"clave": k, "nombre": v[0], "docentes": 0, "tiempo_completo": 0, "masa_mensual": 0.0,
              "docentes_con_publicacion": 0, "obras": set()} for k, v in FAC.items()}
    for p in docentes:
        f = fac_de(p.get("dependencia"))
        if not f:
            continue
        b = by[f]
        b["docentes"] += 1
        b["tiempo_completo"] += int("TIEMPO COMPLETO" in norm(p.get("cargo")) or "DEDICACION EXCLUSIVA" in norm(p.get("cargo")))
        b["masa_mensual"] += p.get("total") or 0
        ws = match.get(id(p))
        if ws:
            b["docentes_con_publicacion"] += 1
            b["obras"].update(ws)

    siaf = {x["nombre"]: x for x in pres["detalle_ultimo_anio"].get("por_facultad") or []}
    vri_path = os.path.join(DATA, "vri-proyectos.json")
    vri = json.load(open(vri_path)) if os.path.exists(vri_path) else None
    vri_by = defaultdict(lambda: {"proyectos": 0, "monto": 0.0})
    if vri:
        for r in vri.get("proyectos", []):
            if r.get("facultad_clave") in by:
                vri_by[r["facultad_clave"]]["proyectos"] += 1
                vri_by[r["facultad_clave"]]["monto"] += r.get("monto_soles") or 0

    filas = []
    for k, b in by.items():
        s = next((siaf[n] for n in FAC[k][2] if n in siaf), None)
        obras = len(b.pop("obras"))
        n = b["docentes"] or 1
        masa_anual = b["masa_mensual"] * 14  # 12 meses + gratificaciones jul/dic (aprox., ver nota)
        filas.append({**b,
                      "masa_mensual": round(b["masa_mensual"], 2),
                      "obras_ventana": obras,
                      "obras_por_docente": round(obras / n, 2),
                      "pct_docentes_con_publicacion": round(100 * b["docentes_con_publicacion"] / n, 1),
                      "costo_planilla_por_obra": round(masa_anual * (VENTANA[1] - VENTANA[0] + 1) / obras) if obras else None,
                      "presupuesto_pim": s["pim"] if s else None,
                      "presupuesto_dev": s["dev"] if s else None,
                      "vri_proyectos": vri_by[k]["proyectos"] if vri else None,
                      "vri_monto": round(vri_by[k]["monto"], 2) if vri else None})
    filas.sort(key=lambda x: -x["obras_ventana"])
    vri_anio = defaultdict(float)
    for r in (vri or {}).get("proyectos", []):
        vri_anio[str(r.get("anio"))] += r.get("monto_soles") or 0

    tot_doc = sum(f["docentes"] for f in filas)
    out = {
        "_meta": {
            "generado": time.strftime("%Y-%m-%d"),
            "ventana_publicaciones": "%d-%d" % VENTANA,
            "fuentes": [
                {"nombre": "Planilla nominal UNI (Portal de Transparencia Estándar)", "url": plan["_meta"].get("url_fuente"), "periodo": "%s-%02d" % (plan["_meta"]["anio"], int(plan["_meta"]["mes"]))},
                {"nombre": "Presupuesto por facultad (MEF/SIAF, meta presupuestal)", "url": "https://apps5.mineco.gob.pe/transparencia/Navegador/default.aspx", "periodo": str(pres["detalle_ultimo_anio"].get("anio"))},
                {"nombre": "OpenAlex (CC0), obras con afiliación UNI", "url": "https://openalex.org/works?filter=institutions.id:%s,publication_year:%d-%d" % (OA_INST, VENTANA[0], VENTANA[1])},
            ] + ([{"nombre": "Proyectos financiados por el VRI-UNI (resoluciones)", "url": (vri.get("_meta") or {}).get("url")}] if vri else []),
            "obras_uni_ventana": n_obras,
            "autores_uni_ventana": len(autores),
            "docentes_planilla": len(docentes),
            "docentes_sin_facultad": sin_fac,
            "docentes_cruzados": len(match),
            "metodo": ("Docentes = planilla PTE (categoría docente) por dependencia. Publicaciones = obras OpenAlex con afiliación UNI en la ventana, "
                       "atribuidas a la facultad del docente cuando el autor coincide en ≥2 componentes del nombre con UN solo docente "
                       "(los casos ambiguos se descartan). Subestima: autores sin afiliación UNI declarada, nombres transliterados, "
                       "artículos fuera de OpenAlex y libros/patentes. Costo de planilla por obra = masa mensual × 14 × años de la ventana / obras "
                       "(aproxima: usa la planilla actual para toda la ventana). Indicador agregado: no evalúa a personas."),
            "advertencia": "Indicadores por facultad, no por docente. La docencia, la extensión y la gestión no se miden aquí.",
        },
        "totales": {"docentes": tot_doc,
                    "docentes_con_publicacion": sum(f["docentes_con_publicacion"] for f in filas),
                    "masa_mensual": round(sum(f["masa_mensual"] for f in filas), 2)},
        "facultades": filas,
        "vri": {"total": round(sum(vri_anio.values()), 2), "proyectos": len((vri or {}).get("proyectos", [])),
                "por_anio": {k: round(v, 2) for k, v in sorted(vri_anio.items())},
                "nota": (vri.get("_meta") or {}).get("nota")} if vri else None,
    }
    p = os.path.join(DATA, "facultades-uni.json")
    json.dump(out, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1, allow_nan=False)
    print("OK", p, "· obras", n_obras, "· autores UNI", len(autores), "· docentes cruzados", len(match), "de", len(docentes))
    for f in filas:
        print("  %-6s doc %3d  pub %3d (%4.1f%%)  obras %4d  masa %9.0f  pim %s" % (f["clave"], f["docentes"], f["docentes_con_publicacion"], f["pct_docentes_con_publicacion"], f["obras_ventana"], f["masa_mensual"], f["presupuesto_pim"]))


if __name__ == "__main__":
    main()
