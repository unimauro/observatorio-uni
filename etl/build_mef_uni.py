#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ETL presupuesto UNI (pliego 514 "U.N. DE INGENIERIA") desde MEF/SIAF Datos Abiertos.

Recorre TODAS las tablas anuales del datastore CKAN (etl/mef_tables.json, descubiertas
con: SELECT table_name FROM information_schema.columns WHERE column_name='MONTO_GIRADO'),
filtra por PLIEGO='514' y arma:
  - serie histórica anual (PIA/PIM/Certificado/Devengado/Girado + % ejecución)
  - último año: desglose por UNIDAD EJECUTORA (UNI, INICTEL...), FUNCION,
    CATEGORIA/GENERICA de gasto y FUENTE de financiamiento ("en qué se gasta cada cosa").
Escribe data/presupuesto-uni.json. Resiliente e idempotente.
"""
import json, os, urllib.parse, urllib.request, time

API = "https://api.datosabiertos.mef.gob.pe/DatosAbiertos/v1/datastore_search_sql"
HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "..", "data")
PLIEGO = "514"
TABLES = json.load(open(os.path.join(HERE, "mef_tables.json")))


def get(sql, retries=3, timeout=290):
    url = API + "?sql=" + urllib.parse.quote(sql)
    for i in range(retries + 1):
        try:
            with urllib.request.urlopen(url, timeout=timeout) as r:
                txt = r.read().decode("utf-8", "ignore")
            if not txt.strip():
                raise ValueError("vacio")
            return json.loads(txt).get("records", [])
        except Exception as e:
            if i == retries:
                print("   FAIL", repr(e)[:80], flush=True)
                return None
            time.sleep(5)


def n(x):
    try:
        return round(float(x or 0), 2)
    except (TypeError, ValueError):
        return 0.0


# --- 1) Serie histórica: recorrer cada tabla, sacar el/los años del pliego 514 ---
serie = {}          # year -> dict
year_table = {}     # year -> resource_id (para drill-down del último año)
print(f"Escaneando {len(TABLES)} tablas por PLIEGO={PLIEGO}...", flush=True)
for i, rid in enumerate(TABLES):
    q = (f'SELECT "ANO_EJE" y, SUM("MONTO_PIA"::numeric) pia, SUM("MONTO_PIM"::numeric) pim, '
         f'SUM("MONTO_CERTIFICADO"::numeric) cert, SUM("MONTO_DEVENGADO"::numeric) dev, '
         f'SUM("MONTO_GIRADO"::numeric) gir FROM "{rid}" WHERE "PLIEGO"=\'{PLIEGO}\' GROUP BY "ANO_EJE"')
    r = get(q)
    if not r:
        continue
    for row in r:
        y = str(row.get("y") or "").strip()
        if not y.isdigit():
            continue
        y = int(y)
        pim = n(row["pim"])
        if pim <= 0:
            continue
        # preferir la tabla con mayor PIM para ese año (tabla mensual completa)
        if y not in serie or pim > serie[y]["pim"]:
            serie[y] = {"year": y, "pia": n(row["pia"]), "pim": pim,
                        "cert": n(row["cert"]), "dev": n(row["dev"]), "gir": n(row["gir"]),
                        "ejec_pct": round(100 * n(row["dev"]) / pim, 1) if pim else 0}
            year_table[y] = rid
    print(f"  [{i+1}/{len(TABLES)}] {rid[:8]} -> años UNI: {sorted(set(int(str(x['y']).strip()) for x in r if str(x.get('y','')).strip().isdigit()))}", flush=True)

serie_list = [serie[y] for y in sorted(serie)]
print("Años con datos UNI:", [s["year"] for s in serie_list], flush=True)

# --- 2) Drill-down del último año disponible ---
detalle = {}
if serie_list:
    ly = serie_list[-1]["year"]
    rid = year_table[ly]
    print(f"Drill-down {ly} (tabla {rid[:8]})...", flush=True)

    def breakdown(col_code, col_name, key):
        q = (f'SELECT "{col_name}" nm, SUM("MONTO_PIM"::numeric) pim, '
             f'SUM("MONTO_DEVENGADO"::numeric) dev FROM "{rid}" '
             f'WHERE "PLIEGO"=\'{PLIEGO}\' GROUP BY "{col_name}" ORDER BY pim DESC')
        r = get(q) or []
        detalle[key] = [{"nombre": x["nm"], "pim": n(x["pim"]), "dev": n(x["dev"])}
                        for x in r if n(x["pim"]) > 0]
        print(f"   {key}: {len(detalle[key])} filas", flush=True)

    breakdown("EJECUTORA", "EJECUTORA_NOMBRE", "por_unidad")
    breakdown("FUNCION", "FUNCION_NOMBRE", "por_funcion")
    breakdown("CATEGORIA_GASTO", "CATEGORIA_GASTO_NOMBRE", "por_categoria")
    breakdown("GENERICA", "GENERICA_NOMBRE", "por_generica")
    breakdown("FUENTE_FINANCIAM", "FUENTE_FINANCIAM_NOMBRE", "por_fuente")
    breakdown("PRODUCTO_PROYECTO", "PRODUCTO_PROYECTO_NOMBRE", "por_proyecto")

out = {
    "_meta": {"fuente": "MEF - Datos Abiertos SIAF (api.datosabiertos.mef.gob.pe)",
              "pliego": "514 · U.N. DE INGENIERIA (UNI + INICTEL-UNI)",
              "unidad": "S/ (soles corrientes)",
              "nota": "Presupuesto institucional (PIA/PIM) y ejecucion (Devengado/Girado)."},
    "serie": serie_list,
    "detalle_ultimo_anio": {"anio": serie_list[-1]["year"] if serie_list else None, **detalle},
}
os.makedirs(OUT, exist_ok=True)
p = os.path.join(OUT, "presupuesto-uni.json")
json.dump(out, open(p, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print(f"OK -> {p} ({os.path.getsize(p)/1024:.0f} KB), {len(serie_list)} años", flush=True)
