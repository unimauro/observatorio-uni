#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fusiona la serie histórica 2012-2024 (Consulta Amigable) en presupuesto-uni.json
sin tocar 2025/2026 ni detalle_ultimo_anio."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
JSON = os.path.join(HERE, "..", "data", "presupuesto-uni.json")
RAW = os.path.join(HERE, "ca_uni_raw.json")

data = json.load(open(JSON, encoding="utf-8"))
raw = json.load(open(RAW, encoding="utf-8"))  # {"2012": {...}, ...}

# serie existente por año
serie = {rec["year"]: rec for rec in data["serie"]}
existing_before = {y: serie[y]["pim"] for y in serie}

for ystr, rec in raw.items():
    y = int(ystr)
    if y in serie:
        continue  # no pisar años ya presentes (2025/2026)
    pim = rec["pim"]
    serie[y] = {"year": y, "pia": rec["pia"], "pim": pim, "cert": rec["cert"],
                "dev": rec["dev"], "gir": rec["gir"],
                "ejec_pct": round(100 * rec["dev"] / pim, 1) if pim else 0}

data["serie"] = [serie[y] for y in sorted(serie)]

# actualizar solo la nota de _meta con el rango real
yrs = [s["year"] for s in data["serie"]]
data["_meta"]["nota"] = (f"Serie histórica {min(yrs)}-{max(yrs)} del pliego 514 "
                         f"(fuente Consulta Amigable MEF para 2012-2024; SIAF Datos Abiertos para 2025-2026). "
                         f"2025 = ejercicio cerrado. 2026 = en ejecución (parcial).")

json.dump(data, open(JSON, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))

# verificación
print("Años en serie:", [s["year"] for s in data["serie"]])
for s in data["serie"]:
    print(f"  {s['year']}: PIM {s['pim']/1e6:8.1f}M  Dev {s['dev']/1e6:8.1f}M  ({s['ejec_pct']}%)")
chk = {s["year"]: s["pim"] for s in data["serie"]}
print("\n2025 PIM:", chk.get(2025), "(esperado ~370.6M)")
print("2026 PIM:", chk.get(2026), "(esperado ~331.6M)")
print("detalle_ultimo_anio.anio:", data["detalle_ultimo_anio"]["anio"])
print("detalle intacto (por_generica filas):", len(data["detalle_ultimo_anio"]["por_generica"]))
