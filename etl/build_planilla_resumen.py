"""Resumen liviano de la planilla: data/planilla-uni.json (~900 KB, lista nominal) → data/planilla-resumen.json (~25 KB).

Lo usan la portada (KPI de docentes AIRHSP), la hoja «UNI líder» (% de «otros» en la planilla docente) y el
contexto del asistente, para no descargar la lista nominal completa fuera de planilla.html.
Sin dependencias; se corre después de build_planilla_pte.py (workflow mensual).
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "data"
SRC = ROOT / "planilla-uni.json"
OUT = ROOT / "planilla-resumen.json"


def main() -> int:
    try:
        p = json.loads(SRC.read_text(encoding="utf-8"))
    except Exception as e:  # sin planilla no hay resumen; no se toca el archivo previo
        print("ERROR leyendo", SRC.name, e, file=sys.stderr)
        return 1
    personas = p.get("personas") or []
    doc = [x for x in personas if x.get("categoria") == "docente"]
    out = {
        "_meta": p.get("_meta", {}),
        "resumen": p.get("resumen", {}),
        "serie_mensual": p.get("serie_mensual", []),
        "top_ingresos": (p.get("top_ingresos") or [])[:10],
        "n_registros": len(personas),
        "docentes_pte": {
            "n": len(doc),
            "total": round(sum(x.get("total") or 0 for x in doc), 2),
            "otros": round(sum(x.get("otros") or 0 for x in doc), 2),
        },
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1, allow_nan=False), encoding="utf-8")
    print("OK", OUT.name, len(personas), "registros", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
