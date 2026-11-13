"""Escenarios financieros UNI 2026-2036 (inercial vs reforma). Cifras en S/ millones nominales.
Base 2025 = ejercicio cerrado (data/presupuesto-uni.json, data/bibliometria.json, data/planilla-uni.json).
Todo supuesto está en el dict SUP y se imprime."""
import json

YEARS = list(range(2025, 2037))
# ---- Línea de base 2025 (datos del repo) ----
B = dict(
    pim=370.588690,            # presupuesto-uni.json serie 2025
    planilla=154.577170,       # genérica PERSONAL Y OBLIGACIONES SOCIALES, PIM 2025
    byss=118.508206,           # BIENES Y SERVICIOS, PIM 2025
    cap_pim=70.088213,         # GASTO DE CAPITAL PIM 2025
    cap_dev=46.398732,         # GASTO DE CAPITAL devengado 2025
    idi=6.7,                   # bibliometria.json presupuesto.idi (programa CTI 2025)
    otros_doc_mes=2.45477989,  # planilla-uni.json: suma 'otros' docentes, set-2026
    doc_total_mes=8.26330273,  # planilla-uni.json: suma 'total' docentes, set-2026
    n_doc=1282,
)
SUP = dict(
    g_pim=0.025,          # CAGR PIM 2012-2025 = 2.49 %
    g_plan=0.030,         # crecimiento vegetativo planilla (supuesto)
    cap_share=B['cap_pim'] / B['pim'],  # 18.9 % del PIM
    ext0=5.0,             # SUPUESTO: fondos externos competitivos 2025 (no publicado)
    g_ext_inercial=0.03,
    # reforma
    idi_share={2025: .018, 2028: .035, 2031: .060, 2036: .080},
    cap_exec_ref={2025: .662, 2026: .70, 2027: .80, 2028: .85, 2029: .90, 2030: .93, 2031: .95, 2036: .95},
    cap_share_ref={2025: .189, 2028: .20, 2031: .22, 2036: .22},
    ext_ref={2025: 5.0, 2028: 12.0, 2031: 30.0, 2036: 60.0},     # PROCIENCIA, internacionales
    ind_ref={2025: 1.0, 2028: 4.0, 2031: 10.0, 2036: 25.0},      # contratos I+D+i con empresas (SUPUESTO base 1.0)
    oxi={2028: 15.0, **{y: 25.0 for y in range(2029, 2037)}},     # obras por impuestos (fuera del PIM)
    phd_new_per_year=15, phd_cost_mes=0.013, phd_from=2027,       # plazas netas nuevas, S/13 000/mes x14
    renacyt={2025: 90, 2028: 150, 2031: 300, 2036: 450},          # docentes RENACYT (base 2020 = 90)
    renacyt_bono=0.5 * (8.26330273 / 1282) * 14,                  # 50 % haberes (art. 86), S/ M por persona-año
    reasig_otros={2025: 0, 2027: .10, 2029: .30, 2036: .30},       # fracción de 'otros' docentes reconvertida a pago por resultados
    efic_byss={2025: 0, 2028: .03, 2031: .05, 2036: .05},          # ahorro bienes y servicios
    endow_aporte={2029: 10.0, **{y: 5.0 for y in range(2030, 2037)}}, endow_ret=0.04,
)


def interp(pts, y):
    ks = sorted(pts)
    if y <= ks[0]: return pts[ks[0]]
    if y >= ks[-1]: return pts[ks[-1]]
    for a, b in zip(ks, ks[1:]):
        if a <= y <= b:
            return pts[a] + (pts[b] - pts[a]) * (y - a) / (b - a)


def geo(pts, y):  # interpolación geométrica para montos
    ks = sorted(pts)
    if y <= ks[0]: return pts[ks[0]]
    if y >= ks[-1]: return pts[ks[-1]]
    for a, b in zip(ks, ks[1:]):
        if a <= y <= b:
            return pts[a] * (pts[b] / pts[a]) ** ((y - a) / (b - a))


rows_in, rows_rf, rows_gap = [], [], []
endow = 0.0
for i, y in enumerate(YEARS):
    t = y - 2025
    pim = B['pim'] * (1 + SUP['g_pim']) ** t
    plan = B['planilla'] * (1 + SUP['g_plan']) ** t
    idi = 0.018 * pim
    capp = SUP['cap_share'] * pim
    capd = 0.662 * capp
    ext = SUP['ext0'] * (1 + SUP['g_ext_inercial']) ** t
    rows_in.append(dict(anio=y, pim=pim, planilla=plan, idi=idi, idi_pct=1.8, cap_pim=capp, inversion_ejecutada=capd, ejec_inv_pct=66.2, fondos_externos=ext))

    # reforma
    sh = interp(SUP['idi_share'], y)
    idi_r = sh * pim
    cs = interp(SUP['cap_share_ref'], y)
    capp_r = cs * pim
    ex = interp(SUP['cap_exec_ref'], y)
    oxi = SUP['oxi'].get(y, 0.0)
    capd_r = ex * capp_r   # OxI es modalidad de ejecución dentro del capital (CIPGN se repaga con presupuesto propio): no se suma
    ext_r = geo(SUP['ext_ref'], y)
    ind_r = geo(SUP['ind_ref'], y)
    nphd = max(0, y - SUP['phd_from'] + 1) * SUP['phd_new_per_year']
    phd_cost = nphd * SUP['phd_cost_mes'] * 14 * (1 + SUP['g_plan']) ** t
    nren = interp(SUP['renacyt'], y)
    ren_cost = max(0, nren - 90) * SUP['renacyt_bono'] * (1 + SUP['g_plan']) ** t
    plan_r = plan + phd_cost + ren_cost
    if y in SUP['endow_aporte']: endow = endow * (1 + SUP['endow_ret']) + SUP['endow_aporte'][y]
    else: endow = endow * (1 + SUP['endow_ret']) if endow else 0
    payout = endow * 0.04 if y >= 2030 else 0
    reasig = interp(SUP['reasig_otros'], y) * B['otros_doc_mes'] * 12 * (1 + SUP['g_plan']) ** t
    efic = interp(SUP['efic_byss'], y) * B['byss'] * (1 + SUP['g_pim']) ** t
    # necesidades incrementales vs inercial (todas pasan por el PIM: PROCIENCIA y contratos entran como DyT/RDR)
    need_idi = idi_r - idi
    need_plan = phd_cost + ren_cost
    need_cap = capp_r - capp
    need = need_idi + need_plan + need_cap
    # fuentes por uso elegible
    f_ext = (ext_r - ext) + (ind_r - SUP['ind_ref'][2025])     # solo puede financiar I+D (proyectos, becas, equipos)
    f_ext_used = min(f_ext, need_idi)
    f_int = reasig + efic                                        # reasignación interna -> planilla por resultados
    f_end = payout
    f_int_used = min(f_int + f_end, need_plan)
    resid = (need_idi - f_ext_used) + (need_plan - f_int_used) + need_cap
    pim_r = pim + need - f_int_used + (f_ext - f_ext_used)       # reasignación no suma PIM; excedente externo sí
    rows_rf.append(dict(anio=y, pim=pim_r, planilla=plan_r, idi=idi_r, idi_pct=round(sh * 100, 2), cap_pim=capp_r,
                        inversion_ejecutada=capd_r, ejec_inv_pct=round(ex * 100, 1), obras_por_impuestos=oxi,
                        fondos_externos=ext_r + ind_r, docentes_phd_nuevos=nphd, renacyt=round(nren), endowment=endow))
    rows_gap.append(dict(anio=y, necesidad_idi=need_idi, necesidad_planilla=need_plan, necesidad_capital=need_cap, necesidad_total=need,
                         fuente_externos=f_ext_used, externos_excedente=f_ext - f_ext_used, fuente_reasignacion=f_int, fuente_endowment=f_end, fuente_internas_usadas=f_int_used, brecha_ro_mef=resid,
                         inversion_extra_ejecutada=capd_r - capd))

r = lambda v: round(v, 1) if isinstance(v, float) else v
out = dict(supuestos={k: (v if not isinstance(v, float) else round(v, 4)) for k, v in SUP.items()},
           inercial=[{k: r(v) for k, v in d.items()} for d in rows_in],
           reforma=[{k: r(v) for k, v in d.items()} for d in rows_rf],
           brecha=[{k: r(v) for k, v in d.items()} for d in rows_gap])
s = lambda k, a=2026, b=2036: sum(d[k] for d in rows_gap if a <= d['anio'] <= b)
out['acumulado_2026_2036'] = {k: round(s(k), 1) for k in rows_gap[0] if k != 'anio'}
out['acumulado_inv_ejecutada'] = dict(inercial=round(sum(d['inversion_ejecutada'] for d in rows_in if d['anio'] >= 2026), 1),
                                      reforma=round(sum(d['inversion_ejecutada'] for d in rows_rf if d['anio'] >= 2026), 1))
out['acumulado_idi'] = dict(inercial=round(sum(d['idi'] for d in rows_in if d['anio'] >= 2026), 1),
                            reforma=round(sum(d['idi'] for d in rows_rf if d['anio'] >= 2026), 1))
json.dump(out, open(__file__.replace('.py', '.json'), 'w'), ensure_ascii=False, indent=1)

def tab(rows, cols):
    print('| ' + ' | '.join(cols) + ' |'); print('|' + '---|' * len(cols))
    for d in rows: print('| ' + ' | '.join(f"{d[c]:,.1f}" if isinstance(d[c], float) else str(d[c]) for c in cols) + ' |')
print('INERCIAL'); tab(rows_in, ['anio', 'pim', 'planilla', 'idi', 'cap_pim', 'inversion_ejecutada', 'fondos_externos'])
print('REFORMA'); tab(rows_rf, ['anio', 'pim', 'planilla', 'idi', 'idi_pct', 'cap_pim', 'inversion_ejecutada', 'ejec_inv_pct', 'obras_por_impuestos', 'fondos_externos', 'docentes_phd_nuevos', 'renacyt', 'endowment'])
print('BRECHA'); tab(rows_gap, ['anio', 'necesidad_idi', 'necesidad_planilla', 'necesidad_capital', 'necesidad_total', 'fuente_externos', 'externos_excedente', 'fuente_reasignacion', 'fuente_endowment', 'fuente_internas_usadas', 'brecha_ro_mef', 'inversion_extra_ejecutada'])
print(out['acumulado_2026_2036'], out['acumulado_inv_ejecutada'], out['acumulado_idi'])
print('renacyt bono por persona S/M', SUP['renacyt_bono'], 'otros anual', B['otros_doc_mes'] * 12)
