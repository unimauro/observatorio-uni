#!/usr/bin/env python3
# Mapea cada tabla del datastore MEF a su ANO_EJE (consulta barata LIMIT 1).
import json, urllib.parse, urllib.request, time, os
API = "https://api.datosabiertos.mef.gob.pe/DatosAbiertos/v1/datastore_search_sql"
HERE = os.path.dirname(__file__)
TABLES = json.load(open(os.path.join(HERE, "mef_tables.json")))
def get(sql, timeout=40):
    url = API + "?sql=" + urllib.parse.quote(sql)
    for i in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                t = r.read().decode("utf-8", "ignore")
            if t.strip():
                return json.loads(t).get("records", [])
        except Exception as e:
            print("   retry", i, repr(e)[:60], flush=True); time.sleep(4)
    return None
ymap = {}
for i, rid in enumerate(TABLES):
    r = get(f'SELECT "ANO_EJE" y FROM "{rid}" LIMIT 1')
    y = ""
    if r:
        y = str(r[0].get("y", "")).strip()
        if y.isdigit():
            ymap.setdefault(int(y), []).append(rid)
    print(f"[{i+1}/{len(TABLES)}] {rid[:8]} -> {y}", flush=True)
    time.sleep(0.4)
json.dump(ymap, open(os.path.join(HERE, "year_map.json"), "w"))
print("YEARS:", sorted(ymap.keys()), flush=True)
