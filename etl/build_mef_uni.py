#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ETL presupuesto UNI (pliego 514 "U.N. DE INGENIERIA") desde MEF/SIAF Datos Abiertos.

Usa etl/year_map.json (generado por map_years.py) = {año:[resource_id,...]}.
Para cada año objetivo consulta el agregado del pliego 514 en sus tablas y se queda
con la de mayor PIM (la mensual completa). Arma serie histórica + desglose del último año.
Escribe data/presupuesto-uni.json. Resiliente (reintentos, pausas anti-409).
"""
import json, os, urllib.parse, urllib.request, time

API = "https://api.datosabiertos.mef.gob.pe/DatosAbiertos/v1/datastore_search_sql"
HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "..", "data")
PLIEGO = "514"
YEARS_MIN = 2013  # últimos ~12 años
YMAP = {int(y): v for y, v in json.load(open(os.path.join(HERE, "year_map.json"))).items()}


def get(sql, timeout=200):
    url = API + "?sql=" + urllib.parse.quote(sql)
    for i in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                t = r.read().decode("utf-8", "ignore")
            if t.strip():
                return json.loads(t).get("records", [])
        except Exception as e:
            print("   retry", i, repr(e)[:60], flush=True); time.sleep(6)
    return None


def num(x):
    try:
        return round(float(x or 0), 2)
    except (TypeError, ValueError):
        return 0.0


serie = {}
year_table = {}
for y in sorted(YMAP):
    if y < YEARS_MIN:
        continue
    for rid in YMAP[y]:
        q = (f'SELECT SUM("MONTO_PIA"::numeric) pia, SUM("MONTO_PIM"::numeric) pim, '
             f'SUM("MONTO_CERTIFICADO"::numeric) cert, SUM("MONTO_DEVENGADO"::numeric) dev, '
             f'SUM("MONTO_GIRADO"::numeric) gir FROM "{rid}" WHERE "PLIEGO"=\'{PLIEGO}\'')
        r = get(q)
        time.sleep(1)
        if not r:
            continue
        row = r[0]
        pim = num(row["pim"])
        if pim <= 0:
            continue
        if y not in serie or pim > serie[y]["pim"]:
            serie[y] = {"year": y, "pia": num(row["pia"]), "pim": pim,
                        "cert": num(row["cert"]), "dev": num(row["dev"]), "gir": num(row["gir"]),
                        "ejec_pct": round(100 * num(row["dev"]) / pim, 1) if pim else 0}
            year_table[y] = rid
    if y in serie:
        print(f"[{y}] PIM {serie[y]['pim']/1e6:.1f}M dev {serie[y]['dev']/1e6:.1f}M ({serie[y]['ejec_pct']}%) tabla {year_table[y][:8]}", flush=True)

serie_list = [serie[y] for y in sorted(serie)]
print("Años:", [s["year"] for s in serie_list], flush=True)

detalle = {}
if serie_list:
    ly = serie_list[-1]["year"]
    rid = year_table[ly]
    print(f"Drill-down {ly} (tabla {rid[:8]})...", flush=True)

    def breakdown(col, key):
        q = (f'SELECT "{col}" nm, SUM("MONTO_PIM"::numeric) pim, SUM("MONTO_DEVENGADO"::numeric) dev '
             f'FROM "{rid}" WHERE "PLIEGO"=\'{PLIEGO}\' GROUP BY "{col}" ORDER BY pim DESC')
        r = get(q) or []
        time.sleep(1)
        detalle[key] = [{"nombre": x["nm"], "pim": num(x["pim"]), "dev": num(x["dev"])}
                        for x in r if num(x["pim"]) > 0]
        print(f"   {key}: {len(detalle[key])} filas", flush=True)

    breakdown("EJECUTORA_NOMBRE", "por_unidad")
    breakdown("FUNCION_NOMBRE", "por_funcion")
    breakdown("CATEGORIA_GASTO_NOMBRE", "por_categoria")
    breakdown("GENERICA_NOMBRE", "por_generica")
    breakdown("FUENTE_FINANCIAM_NOMBRE", "por_fuente")

out = {
    "_meta": {"fuente": "MEF - Datos Abiertos SIAF (api.datosabiertos.mef.gob.pe)",
              "pliego": "514 · U.N. DE INGENIERIA (UNI + INICTEL-UNI)",
              "unidad": "S/ (soles corrientes)",
              "extraido": "2026-07"},
    "serie": serie_list,
    "detalle_ultimo_anio": {"anio": serie_list[-1]["year"] if serie_list else None, **detalle},
}
os.makedirs(OUT, exist_ok=True)
p = os.path.join(OUT, "presupuesto-uni.json")
json.dump(out, open(p, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print(f"OK -> {p} ({os.path.getsize(p)/1024:.0f} KB), {len(serie_list)} años", flush=True)
