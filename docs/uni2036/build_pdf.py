#!/usr/bin/env python3
"""Genera docs/uni2036/UNI-2036.pdf a partir de los capítulos en Markdown.

Uso: python3 docs/uni2036/build_pdf.py
Requiere: pandoc, weasyprint, matplotlib.
Los capítulos (01_diagnostico.md, 02_referentes_gestion.md, 03_estrategia.md,
00_resumen.md) viven en docs/uni2036/. Los bloques ```json se usan para los
gráficos y se quitan del texto.
"""
import json, re, subprocess, sys, datetime
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
OUT = HERE / "build"
OUT.mkdir(exist_ok=True)

INK, MUTED, GRID = "#1f2430", "#6b7280", "#e5e7eb"
C1, C2, C3, C4 = "#8a1538", "#2563eb", "#0f766e", "#d97706"   # guinda UNI, azul, verde, ámbar
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": GRID,
    "axes.labelcolor": INK, "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True,
    "grid.color": GRID, "grid.linewidth": .6, "axes.axisbelow": True,
    "legend.frameon": False, "figure.dpi": 150,
})


def blocks(md, name):
    for m in re.finditer(r"```json\s*\n(.*?)```", md, re.S):
        try:
            d = json.loads(m.group(1))
        except Exception:
            continue
        if isinstance(d, dict) and name in d:
            return d[name]
    return None


def strip_json(md):
    return re.sub(r"```json\s*\n.*?```\s*", "", md, flags=re.S)


def save(fig, name, caption, source):
    p = OUT / f"{name}.svg"
    fig.tight_layout()
    fig.savefig(p, format="svg", bbox_inches="tight")
    plt.close(fig)
    return (f'<figure class="chart"><img src="{p.name}" alt="{caption}">'
            f'<figcaption><b>{caption}</b><br><span>Fuente: {source}</span></figcaption></figure>')


def charts(estr):
    out = []
    # 1. UNI vs pares
    b = json.loads((ROOT / "data/bibliometria.json").read_text())
    fig, ax = plt.subplots(figsize=(6.6, 2.9))
    for k, lab, c in [("sanmarcos", "San Marcos", C2), ("pucp", "PUCP", C4), ("cayetano", "Cayetano", C3), ("uni", "UNI", C1)]:
        s = [r for r in b[k].get("by_year", []) if 2016 <= r["year"] <= 2025]
        if s:
            ax.plot([r["year"] for r in s], [r["works"] for r in s], label=lab, color=c, lw=2.4 if k == "uni" else 1.6)
    ax.set_ylabel("obras por año"); ax.legend(ncol=4, loc="upper left")
    out.append(save(fig, "g1_pares", "Producción científica anual: UNI frente a universidades peruanas",
                    "OpenAlex (data/bibliometria.json del Observatorio UNI)"))

    # 2. VRI por facultad
    v = json.loads((ROOT / "data/vri-proyectos.json").read_text())
    tot = {}
    for p in v["proyectos"]:
        k = p.get("facultad_clave") or "Otro"
        tot[k] = tot.get(k, 0) + (p.get("monto_soles") or 0)
    items = sorted(tot.items(), key=lambda x: x[1])
    fig, ax = plt.subplots(figsize=(6.6, 3.1))
    ax.barh([k for k, _ in items], [x / 1e6 for _, x in items],
            color=[C1 if x >= sorted(tot.values())[-3] else "#c9a3b0" for _, x in items])
    ax.set_xlabel("S/ millones, 2022–2026"); ax.grid(axis="y", visible=False)
    out.append(save(fig, "g2_vri", "Fondos concursables del VRI por facultad: tres facultades concentran casi dos tercios",
                    "Resoluciones del VRI-UNI (data/vri-proyectos.json, 231 proyectos)"))

    esc = blocks(estr, "escenarios")
    if esc:
        ine, ref = esc["inercial"], esc["reforma"]
        yrs = [r["anio"] for r in ine]
        # 3. I+D
        fig, ax = plt.subplots(figsize=(6.6, 2.8))
        ax.plot(yrs, [r["idi"] for r in ine], color=MUTED, lw=1.8, ls="--", label="Inercial")
        ax.plot(yrs, [r["idi"] for r in ref], color=C1, lw=2.4, label="Reforma UNI 2036")
        ax.set_ylabel("I+D, S/ millones"); ax.legend(loc="upper left")
        out.append(save(fig, "g3_idi", "Gasto en I+D: seguir igual vs. reforma",
                        "Modelo de escenarios del plan (supuestos en el capítulo 3.5)"))
        # 4. Inversión ejecutada
        fig, ax = plt.subplots(figsize=(6.6, 2.8))
        w = .38
        ax.bar([y - w / 2 for y in yrs], [r["inversion_ejecutada"] for r in ine], w, color="#c7cbd3", label="Inercial")
        ax.bar([y + w / 2 for y in yrs], [r["inversion_ejecutada"] for r in ref], w, color=C3, label="Reforma")
        ax.set_ylabel("Inversión ejecutada, S/ M"); ax.legend(loc="upper left"); ax.grid(axis="x", visible=False)
        out.append(save(fig, "g4_inv", "Inversión ejecutada cada año: lo que hoy se deja sin gastar se convierte en obra",
                        "Modelo de escenarios del plan; base MEF/SIAF 2025"))
        # 5. Presupuesto total
        fig, ax = plt.subplots(figsize=(6.6, 2.8))
        ax.fill_between(yrs, [r["pim"] for r in ine], [r["pim"] for r in ref], color=C1, alpha=.15, label="Recursos adicionales")
        ax.plot(yrs, [r["pim"] for r in ine], color=MUTED, ls="--", lw=1.8, label="PIM inercial")
        ax.plot(yrs, [r["pim"] for r in ref], color=C1, lw=2.4, label="PIM reforma")
        ax.set_ylabel("S/ millones"); ax.legend(loc="upper left")
        out.append(save(fig, "g5_pim", "Presupuesto total necesario (PIM)",
                        "Modelo de escenarios del plan"))

    rm = blocks(estr, "roadmap")
    if rm:
        fases = {"Ordenar la casa": (2026, 2028, "#fde7ec"), "Escalar": (2029, 2032, "#dbeafe"), "Liderar": (2033, 2036, "#ccfbf1")}
        fig, ax = plt.subplots(figsize=(6.6, 2.0))
        for f, (a, z, col) in fases.items():
            ax.axvspan(a - .5, z + .5, color=col)
            ax.text((a + z) / 2, .92, f, ha="center", va="top", fontsize=9, weight="bold", color=INK, transform=ax.get_xaxis_transform())
        seen = {}
        for h in rm:
            y = h.get("año") or h.get("anio"); seen[y] = seen.get(y, 0) + 1
            ax.plot(y, .25 + .18 * (seen[y] - 1), "o", color=C1, ms=6)
        ax.set_xlim(2025.5, 2036.5); ax.set_ylim(0, 1); ax.set_yticks([]); ax.set_xticks(range(2026, 2037))
        ax.grid(False); ax.spines["left"].set_visible(False)
        out.append(save(fig, "g6_ruta", "Hoja de ruta 2026–2036: tres fases y sus hitos (cada punto es un hito)",
                        "Capítulo 3.3"))
    return out


def export_json(estr):
    """Datos del plan para la página web lider.html (data/uni2036.json)."""
    esc = blocks(estr, "escenarios") or {}
    keep = ("anio", "pim", "planilla", "idi", "idi_pct", "inversion_ejecutada", "ejec_inv_pct", "fondos_externos", "renacyt")
    out = {
        "_meta": {"fuente": "docs/uni2036 (capítulos 1–5 del plan UNI 2036)", "pdf": "docs/uni2036/UNI-2036.pdf",
                  "generado": datetime.date.today().isoformat(),
                  "nota": "Metas y escenarios son propuestas; cifras marcadas [S] son supuestos. No evalúa a personas."},
        "roadmap": blocks(estr, "roadmap") or [],
        "kpis": blocks(estr, "kpis") or [],
        "escenarios": {
            "unidad": esc.get("unidad"), "base": esc.get("base"),
            "inercial": [{k: r.get(k) for k in keep if k in r} for r in esc.get("inercial", [])],
            "reforma": [{k: r.get(k) for k in keep if k in r} for r in esc.get("reforma", [])],
            "acumulado": esc.get("acumulado_2026_2036"),
            "global_trayectoria": [{k: r.get(k) for k in ("anio", "pim_reforma", "idi")} for r in (esc.get("global") or {}).get("trayectoria", [])],
        },
    }
    (ROOT / "data/uni2036.json").write_text(json.dumps(out, ensure_ascii=False, allow_nan=False, separators=(",", ":")))


def chapter(path, title):
    md = path.read_text()
    md = strip_json(md)
    md = re.sub(r"^# .*\n", "", md, count=1)          # el H1 lo ponemos nosotros
    return f"\n\n# {title}\n\n" + md


def main():
    src = {n: HERE / n for n in ["00_resumen.md", "01_diagnostico.md", "02_referentes_gestion.md", "03_estrategia.md"]}
    for n, p in src.items():
        if not p.exists():
            sys.exit(f"falta {p}")
    estr = src["03_estrategia.md"].read_text()
    ref = src["02_referentes_gestion.md"].read_text()
    parts = re.split(r"^# Cap[ií]tulo B\..*$", ref, maxsplit=1, flags=re.M)
    bc = re.split(r"^# Cap[ií]tulo C\..*$", parts[1], maxsplit=1, flags=re.M)
    (OUT / "A.md").write_text(parts[0]); (OUT / "B.md").write_text("# B\n" + bc[0])
    (OUT / "C.md").write_text("# C\n" + (bc[1] if len(bc) > 1 else ""))

    figs = charts(estr)
    export_json(estr)
    md = (src["00_resumen.md"].read_text()
          + "\n\n# El plan en gráficos\n\n" + "\n\n".join(f'```{{=html}}\n{f}\n```' for f in figs)
          + chapter(src["01_diagnostico.md"], "1. Diagnóstico: dónde está la UNI hoy")
          + chapter(OUT / "A.md", "2. Referentes: cómo se transformaron otras universidades")
          + chapter(src["03_estrategia.md"], "3. Estrategia UNI 2036")
          + chapter(OUT / "B.md", "4. Remodelación de la gestión y de la oferta académica")
          + chapter(OUT / "C.md", "5. Docentes, espacios, carreras de futuro, alianzas y marco nacional"))
    (OUT / "all.md").write_text(md)

    hoy = datetime.date.today()
    cover = f"""
<section class="cover">
  <div class="kicker">Observatorio UNI · Propuesta abierta a debate</div>
  <h1 class="ctitle">UNI 2036</h1>
  <p class="csub">Estrategia, tácticas, metas y financiamiento para que la Universidad Nacional de Ingeniería lidere en ciencia, tecnología e innovación</p>
  <div class="cmeta">Versión 1.0 · {hoy.strftime('%d-%m-%Y')}<br>unimauro.github.io/observatorio-uni/lider.html</div>
  <p class="cnote">Documento elaborado con datos públicos (MEF, Portal de Transparencia Estándar, OpenAlex, resoluciones del VRI, SUNEDU, CONCYTEC). Cada cifra lleva su fuente. Las cifras marcadas como supuesto [S] son hipótesis de trabajo, no datos. No evalúa ni menciona a docentes individuales.</p>
</section>"""
    (OUT / "cover.html").write_text(cover)
    subprocess.run(["pandoc", str(OUT / "all.md"), "-f", "markdown+pipe_tables+raw_html", "-t", "html5", "-s",
                    "--toc", "--toc-depth=2", "-V", "toc-title=Contenido", "--metadata", "title=UNI 2036",
                    "--metadata", "lang=es", "-c", "style.css", "--include-before-body", str(OUT / "cover.html"),
                    "-o", str(OUT / "UNI-2036.html")], check=True)
    (OUT / "style.css").write_text((HERE / "style.css").read_text())
    subprocess.run(["weasyprint", str(OUT / "UNI-2036.html"), str(HERE / "UNI-2036.pdf")], check=True)
    print("✔", HERE / "UNI-2036.pdf")


if __name__ == "__main__":
    main()
