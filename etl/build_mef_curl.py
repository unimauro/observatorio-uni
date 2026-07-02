#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ETL presupuesto UNI (pliego 514) vía curl (urllib timeouteaba; curl no).
Serie histórica por año (year_map.json) + desglose del último año."""
import json, os, subprocess, urllib.parse, time

API = "https://api.datosabiertos.mef.gob.pe/DatosAbiertos/v1/datastore_search_sql"
HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "..", "data")
PLIEGO = "514"
YEARS_MIN = 2013
YMAP = {int(y): v for y, v in json.load(open(os.path.join(HERE, "year_map.json"))).items()}


def q(sql, tries=3):
    url = API + "?sql=" + urllib.parse.quote(sql)
    for i in range(tries):
        try:
            out = subprocess.run(["curl", "-s", "-m", "130", "-A", "Mozilla/5.0", url],
                                 capture_output=True, text=True, timeout=140).stdout
            if out.strip():
                r = json.loads(out).get("records")
                if r is not None:
                    return r
        except Exception as e:
            print("   retry", i, repr(e)[:50], flush=True)
        time.sleep(8)
    return None


def num(x):
    try:
        return round(float(x or 0), 2)
    except (TypeError, ValueError):
        return 0.0


serie, year_table = {}, {}
for y in sorted(YMAP):
    if y < YEARS_MIN:
        continue
    for rid in YMAP[y]:
        r = q(f'SELECT SUM("MONTO_PIA"::numeric) pia, SUM("MONTO_PIM"::numeric) pim, '
              f'SUM("MONTO_CERTIFICADO"::numeric) cert, SUM("MONTO_DEVENGADO"::numeric) dev, '
              f'SUM("MONTO_GIRADO"::numeric) gir FROM "{rid}" WHERE "PLIEGO"=\'{PLIEGO}\'')
        time.sleep(3)
        if not r:
            continue
        pim = num(r[0]["pim"])
        if pim <= 0:
            continue
        if y not in serie or pim > serie[y]["pim"]:
            serie[y] = {"year": y, "pia": num(r[0]["pia"]), "pim": pim, "cert": num(r[0]["cert"]),
                        "dev": num(r[0]["dev"]), "gir": num(r[0]["gir"]),
                        "ejec_pct": round(100 * num(r[0]["dev"]) / pim, 1) if pim else 0}
            year_table[y] = rid
    if y in serie:
        s = serie[y]
        print(f"[{y}] PIM {s['pim']/1e6:.1f}M dev {s['dev']/1e6:.1f}M ({s['ejec_pct']}%)", flush=True)

serie_list = [serie[y] for y in sorted(serie)]
print("Años:", [s["year"] for s in serie_list], flush=True)

detalle = {}
if serie_list:
    ly = serie_list[-1]["year"]; rid = year_table[ly]
    for col, key in [("EJECUTORA_NOMBRE", "por_unidad"), ("FUNCION_NOMBRE", "por_funcion"),
                     ("CATEGORIA_GASTO_NOMBRE", "por_categoria"), ("GENERICA_NOMBRE", "por_generica"),
                     ("FUENTE_FINANCIAM_NOMBRE", "por_fuente")]:
        r = q(f'SELECT "{col}" nm, SUM("MONTO_PIM"::numeric) pim, SUM("MONTO_DEVENGADO"::numeric) dev '
              f'FROM "{rid}" WHERE "PLIEGO"=\'{PLIEGO}\' GROUP BY "{col}" ORDER BY pim DESC') or []
        time.sleep(3)
        detalle[key] = [{"nombre": x["nm"], "pim": num(x["pim"]), "dev": num(x["dev"])} for x in r if num(x["pim"]) > 0]
        print(f"   {key}: {len(detalle[key])}", flush=True)

out = {"_meta": {"fuente": "MEF - Datos Abiertos SIAF (api.datosabiertos.mef.gob.pe)",
                 "pliego": "514 · U.N. DE INGENIERIA (UNI + INICTEL-UNI)",
                 "unidad": "S/ (soles corrientes)", "extraido": "2026-07"},
       "serie": serie_list,
       "detalle_ultimo_anio": {"anio": serie_list[-1]["year"] if serie_list else None, **detalle}}
json.dump(out, open(os.path.join(OUT, "presupuesto-uni.json"), "w", encoding="utf-8"),
          ensure_ascii=False, separators=(",", ":"))
print(f"OK {len(serie_list)} años", flush=True)
