#!/usr/bin/env python3
"""Buscador público de órdenes de compra/servicio de la UNI a personas naturales.

Entrada: data/pagos-personas-uni.json (privado, no se publica: trae RUC) y data/organos-cruce.json.
Salida:  data/ordenes-uni.json, compacto y SIN RUC ni DNI:
  {"_meta": {...}, "p": [nombre, ...], "o": [[i_persona, "AAAA-MM-DD", "S"|"C", monto, "descripcion", anulada(0/1)], ...],
   "org": {i_persona: "órgano · estamento", ...}}
"""
import json, datetime, re, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAG = ROOT / "data/pagos-personas-uni.json"
CRU = ROOT / "data/organos-cruce.json"
OUT = ROOT / "data/ordenes-uni.json"


def main():
    pag = json.loads(PAG.read_text())
    cru = json.loads(CRU.read_text()) if CRU.exists() else {"personas": []}
    # nombre_fuente de pagos -> resumen del órgano
    org_by_src = {}
    for p in cru["personas"]:
        src = (p.get("pagos") or {}).get("nombre_fuente")
        if src:
            c = p["cargos"][0]
            org_by_src[src] = f'{c["organo"]}{" · " + c["facultad"] if c.get("facultad") else ""} · {c["estamento"]} ({len(p["cargos"])} cargo{"s" if len(p["cargos"]) > 1 else ""})'
    names, rows, org = [], [], {}
    for k, v in pag["personas"].items():
        ords = v.get("ordenes") or []
        # contratos 2025-05+ a personas (OCDS-OECE): único rastro abierto tras el apagón de órdenes en SEACE
        ocds = [a for a in (v.get("adjudicaciones") or []) if a.get("fuente") == "OCDS-OECE" and str(a.get("fecha", "")) >= "2025-05"]
        if not ords and not ocds:
            continue
        i = len(names)
        names.append(v.get("nombre_fuente") or k)
        if names[-1] in org_by_src:
            org[i] = org_by_src[names[-1]]
        for o in ords:
            rows.append([i, o.get("fecha") or str(o.get("anio")), "S" if o.get("tipo") == "servicio" else "C",
                         round(o.get("monto") or 0, 2), re.sub(r"\s+", " ", (o.get("descripcion") or "").strip())[:140],
                         1 if (o.get("estado") or "").lower().startswith("anul") else 0])
        for a in ocds:
            rows.append([i, a.get("fecha"), "P", round(a.get("monto_contrato") or a.get("monto") or 0, 2),
                         re.sub(r"\s+", " ", f'{a.get("descripcion") or ""} · {a.get("proceso") or ""} ({a.get("metodo") or ""})')[:160], 0])
    rows.sort(key=lambda r: r[1], reverse=True)
    cob = pag["_meta"]["cobertura"]["ordenes_seace_por_mes"]
    serie = [[m, cob[m]["filas"], cob[m]["persona_natural"]] for m in sorted(cob) if m <= "2026-10"]
    fo = pag["_meta"]["fuentes"]["ordenes"]
    out = {"_meta": {
        "generado": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "script": "etl/build_ordenes_publico.py",
        "fuente": fo.get("nombre"), "fuente_url": fo.get("url"), "url_patron": fo.get("url_patron"),
        "periodo": fo.get("periodo"),
        "nota": "Órdenes de compra y de servicio de la UNI a personas naturales (RUC 10/15/17) registradas en SEACE. Sin RUC ni DNI. Montos en soles; las órdenes anuladas se muestran marcadas y no suman. Cubre hasta abril de 2025. Desde mayo de 2025 la UNI no registra sus órdenes en SEACE: el buscador oficial devuelve 0 órdenes de la UNI cada mes de mayo de 2025 a octubre de 2026, mientras otras entidades (p. ej. MINEDU, 510 en setiembre de 2026) siguen registrándolas (verificado el 18-11-2026). La marca de órgano de gobierno es una coincidencia de nombre.",
        "serie_seace": serie, "serie_nota": "Órdenes de compra y de servicio de la UNI registradas en SEACE por mes (todas y a personas naturales). Consulta al buscador oficial SEACE OCOS (ruc_entidad=20169004359) del 18-11-2026; se omite el mes en curso.",
        "comparacion": {"entidad": "Ministerio de Educación (RUC 20131370998)", "mes": "2026-09", "ordenes": 510, "uni_mismo_mes": 0},
        "ocds_nota": "Tipo «P»: contratos por procedimiento (no órdenes) adjudicados a personas naturales desde mayo de 2025, tomados de OECE Contrataciones Abiertas (OCDS). Es lo único abierto que existe de ese periodo.",
        "n_personas": len(names), "n_ordenes": len(rows)},
        "p": names, "o": rows, "org": org}
    OUT.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")))
    print(len(names), "personas", len(rows), "órdenes", round(OUT.stat().st_size / 1e6, 2), "MB")


if __name__ == "__main__":
    main()
