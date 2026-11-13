"""(a) Trayectoria de financiamiento del escenario de reforma: PIM por componente y crecimiento anual.
(b) Escenario 'global' (liderar el mundo): mismo modelo que escenarios.py con supuestos más altos.
Ejecuta escenarios.py con reemplazos de supuestos; no lo modifica."""
import json, os, contextlib, io
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = open(os.path.join(HERE, 'escenarios.py')).read()
SRC = SRC.replace("json.dump(out, open(__file__.replace('.py', '.json'), 'w'), ensure_ascii=False, indent=1)", "")
SRC = SRC[:SRC.index("def tab")]


def run(reps):
    s = SRC
    for a, b in reps:
        assert a in s, a
        s = s.replace(a, b)
    g = {}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(s, g)
    return g


R = run([])
GLOBAL_REPS = [
    ("idi_share={2025: .018, 2028: .035, 2031: .060, 2036: .080}", "idi_share={2025: .018, 2028: .040, 2031: .080, 2036: .120}"),
    ("cap_share_ref={2025: .189, 2028: .20, 2031: .22, 2036: .22}", "cap_share_ref={2025: .189, 2028: .21, 2031: .25, 2036: .25}"),
    ("ext_ref={2025: 5.0, 2028: 12.0, 2031: 30.0, 2036: 60.0}", "ext_ref={2025: 5.0, 2028: 15.0, 2031: 50.0, 2036: 150.0}"),
    ("ind_ref={2025: 1.0, 2028: 4.0, 2031: 10.0, 2036: 25.0}", "ind_ref={2025: 1.0, 2028: 6.0, 2031: 20.0, 2036: 60.0}"),
    ("phd_new_per_year=15", "phd_new_per_year=40"),
    ("renacyt={2025: 90, 2028: 150, 2031: 300, 2036: 450}", "renacyt={2025: 90, 2028: 180, 2031: 400, 2036: 700}"),
    ("endow_aporte={2029: 10.0, **{y: 5.0 for y in range(2030, 2037)}}", "endow_aporte={2029: 30.0, **{y: 20.0 for y in range(2030, 2037)}}"),
]
G = run(GLOBAL_REPS)


def traj(g):
    rows = []
    prev = None
    for di, dr, dg in zip(g['rows_in'], g['rows_rf'], g['rows_gap']):
        ext_inc = dr['fondos_externos'] - (di['fondos_externos'] + 1.0)  # incremental externos + industria
        row = dict(anio=di['anio'], pim_inercial=di['pim'], ro_adicional=dg['brecha_ro_mef'], externos_rdr_incremental=ext_inc,
                   pim_reforma=dr['pim'], crec_pct=None if prev is None else 100 * (dr['pim'] / prev - 1),
                   reasignacion_interna=dg['fuente_internas_usadas'], idi=dr['idi'], planilla=dr['planilla'], inversion_ejecutada=dr['inversion_ejecutada'])
        prev = dr['pim']
        rows.append(row)
    return rows


out = {}
for name, g in (('reforma', R), ('global', G)):
    t = traj(g)
    acc = {k: round(sum(d[k] for d in g['rows_gap'] if d['anio'] >= 2026), 1) for k in ('necesidad_total', 'fuente_externos', 'fuente_internas_usadas', 'brecha_ro_mef')}
    cagr = 100 * ((t[-1]['pim_reforma'] / t[0]['pim_reforma']) ** (1 / 11) - 1)
    out[name] = dict(trayectoria=[{k: (round(v, 1) if isinstance(v, float) else v) for k, v in d.items()} for d in t if d['anio'] >= 2026],
                     acumulado_2026_2036=acc, cagr_pim_2025_2036=round(cagr, 2),
                     pim_2036=round(t[-1]['pim_reforma'], 1), idi_2036=round(t[-1]['idi'], 1),
                     ro_adicional_2036=round(t[-1]['ro_adicional'], 1),
                     docentes_phd_nuevos_2036=g['rows_rf'][-1]['docentes_phd_nuevos'], renacyt_2036=g['rows_rf'][-1]['renacyt'])
json.dump(out, open(os.path.join(HERE, 'trayectoria_global.json'), 'w'), ensure_ascii=False, indent=1)
for name in out:
    print('==', name, {k: v for k, v in out[name].items() if k != 'trayectoria'})
    print('| Año | PIM inercial | + RO adicional | + externos/RDR | = PIM | crec. % | reasignación interna | I+D | inversión ejecutada |')
    for d in out[name]['trayectoria']:
        print(f"| {d['anio']} | {d['pim_inercial']:.1f} | {d['ro_adicional']:.1f} | {d['externos_rdr_incremental']:.1f} | {d['pim_reforma']:.1f} | {d['crec_pct']:.1f} | {d['reasignacion_interna']:.1f} | {d['idi']:.1f} | {d['inversion_ejecutada']:.1f} |")
