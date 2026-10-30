#!/usr/bin/env python3
"""Construye data/admision-uni.json a partir de uni-admision-stats (stats.json).

Fuente preferente: la copia publicada en GitHub (raw). Fallback: el repo hermano local.
Solo agregados: NUNCA se copian nombres (stats.json trae top-10 con nombre; se descartan).

Uso:  python3 etl/build_admision.py
"""
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'data', 'admision-uni.json')
URL = 'https://raw.githubusercontent.com/unimauro/uni-admision-stats/main/data/stats.json'
LOCAL = os.path.join(HERE, '..', '..', 'uni-admision-stats', 'data', 'stats.json')
ENLACE = 'https://unimauro.github.io/uni-admision-stats/'
PROCESO = '2026-1'  # proceso con detalle completo (historico_2026_1)


def fetch():
    try:
        with urllib.request.urlopen(URL, timeout=30) as r:
            d = json.loads(r.read().decode('utf-8'))
            print('stats.json: descargado de', URL, file=sys.stderr)
            return d, URL
    except Exception as e:  # noqa: BLE001
        print('No se pudo descargar (%s); uso copia local %s' % (e, LOCAL), file=sys.stderr)
        with open(LOCAL, encoding='utf-8') as f:
            return json.load(f), LOCAL


def pct(a, b):
    return round(100.0 * a / b, 1) if b else None


def resumen_puntaje(p):
    """{n,min,max,media,...} -> {n,min,max,prom} (claves que app.js ya consume)."""
    if not p:
        return None
    return {'n': p.get('n'), 'min': p.get('min'), 'max': p.get('max'), 'prom': round(p.get('media', 0), 1)}


def write_atomic(path, obj):
    tmp = path + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
        f.write('\n')
    os.replace(tmp, path)


def main():
    st, origen = fetch()
    # Validación: si la fuente no trae lo esencial, abortar SIN escribir (exit != 0)
    try:
        hist = st['historico_2026_1']['admision']
        serie = st['serie_historica']
        assert hist['total_postulantes'] > 0 and hist['total_ingresantes'] > 0
        assert serie['procesos'] and serie['por_proceso'] and hist['ingresantes_por_especialidad']
    except (KeyError, TypeError, AssertionError) as e:
        sys.exit('stats.json incompleto o con estructura inesperada: %r' % (e,))

    # --- detalle del proceso 2026-1 (examen de admisión, puntajes.admision.uni.edu.pe) ---
    esp = [{'nombre': k, 'n': v['ingresantes']} for k, v in hist['ingresantes_por_especialidad'].items() if k]
    esp.sort(key=lambda x: (-x['n'], x['nombre']))
    mod = [{'nombre': k, 'n': v['ingresantes']} for k, v in hist['por_modalidad'].items() if k and v.get('ingresantes')]
    mod.sort(key=lambda x: (-x['n'], x['nombre']))

    # puntaje de ingresantes: agregamos min/max y media ponderada desde por_especialidad
    ing_stats = [v for v in hist['ingresantes_por_especialidad'].values() if v.get('ingresantes')]
    n_ing = sum(v['ingresantes'] for v in ing_stats)
    prom_ing = round(sum(v['media'] * v['ingresantes'] for v in ing_stats) / n_ing, 1) if n_ing else None
    puntaje_ingresantes = {
        'n': n_ing,
        'min': min(v['min'] for v in ing_stats) if ing_stats else None,
        'max': max(v['max'] for v in ing_stats) if ing_stats else None,
        'prom': prom_ing,
    }
    puntaje_postulantes = resumen_puntaje(hist.get('puntaje_final'))

    # --- serie histórica 2013-1 .. 2026-1 (datosabiertos.gob.pe + PDFs oficiales) ---
    serie_rows = []
    for p in serie['procesos']:
        x = serie['por_proceso'][p]
        f = (x.get('por_sexo') or {}).get('F') or {}
        serie_rows.append({
            'proceso': p,
            'postulantes': x['postulantes'],
            'ingresantes': x['ingresantes'],
            'tasa_pct': pct(x['ingresantes'], x['postulantes']),
            'mujeres_pct_ingresantes': pct(f.get('ingresantes', 0), x['ingresantes']),
        })
    s26 = serie['por_proceso'].get(PROCESO, {})
    f26 = (s26.get('por_sexo') or {}).get('F') or {}
    mujeres = {
        'proceso': PROCESO,
        'postulantes_pct': pct(f26.get('postulantes', 0), s26.get('postulantes', 0)),
        'ingresantes_pct': pct(f26.get('ingresantes', 0), s26.get('ingresantes', 0)),
        'fuente': 'serie histórica (microdatos datosabiertos.gob.pe)',
    }

    # --- ciclo actual (2026-2) y proceso en curso (2027-1): solo totales, sin nombres ---
    ca = st.get('ciclo_actual') or {}
    pubs = ca.get('publicaciones') or {}
    concurso = pubs.get('resultados-concurso-admision-2026-2') or {}
    arq = pubs.get('resultados-concurso-admision-2026-2-arquitectura') or {}
    ciclo_actual = {
        'ciclo': ca.get('ciclo'),
        'ultima_fecha': ca.get('ultima_fecha'),
        'postulantes_examen': (concurso.get('total') or 0) + (arq.get('total') or 0) or None,
        'ingresantes_examen': (concurso.get('ingresantes') or 0) + (arq.get('ingresantes') or 0) or None,
        'nota': 'Concurso de admisión %s (resultados generales + Arquitectura), según publicaciones oficiales. No incluye CEPRE ni modalidades especiales.' % ca.get('ciclo'),
    }
    pc = st.get('proceso_en_curso') or {}
    pc_pubs = pc.get('publicaciones') or {}
    proceso_en_curso = {
        'ciclo': pc.get('ciclo'),
        'ultima_fecha': pc.get('ultima_fecha'),
        'publicaciones': [{'nombre': v.get('nombre_oficial'), 'total': v.get('total'), 'presentes': v.get('presentes'), 'pct_ausentismo': v.get('pct_ausentismo')} for v in pc_pubs.values()],
        'nota': 'Proceso en curso: parciales y simulacros CEPRE-UNI publicados hasta la fecha indicada; no hay todavía resultados del concurso de admisión %s.' % pc.get('ciclo'),
    }

    out = {
        '_meta': {
            'fuente': 'Resultados oficiales de admisión UNI (puntajes.admision.uni.edu.pe)',
            'fuente_detalle': 'Agregados vía uni-admision-stats (%s). Serie histórica: %s' % (ENLACE, serie.get('fuente')),
            'enlace': ENLACE,
            'generado': datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            'fuente_actualizada': st.get('generado_utc'),
            'proceso': PROCESO,
            'total_postulantes': hist['total_postulantes'],
            'total_ingresantes': hist['total_ingresantes'],
            'nota': 'Postulantes = todos los que rindieron el examen. Ingresantes = quienes obtuvieron vacante (con especialidad asignada). Solo datos agregados; sin nombres.',
            'nota_serie': 'La serie histórica proviene de microdatos de datosabiertos.gob.pe (2021–2026) y de PDFs oficiales (2013–2020), y abarca el proceso completo; por eso su cifra de %s (%s postulantes / %s ingresantes) no coincide con la del examen de admisión (%s / %s). 2020 solo tuvo un proceso (2020-1).' % (
                PROCESO, s26.get('postulantes'), s26.get('ingresantes'), hist['total_postulantes'], hist['total_ingresantes']),
        },
        'proceso': PROCESO,
        'ingresantes_por_especialidad': esp,
        'ingresantes_por_modalidad': mod,
        'puntaje_postulantes': puntaje_postulantes,
        'puntaje_ingresantes': puntaje_ingresantes,
        'serie_historica': serie_rows,
        'mujeres': mujeres,
        'ciclo_actual': ciclo_actual,
        'proceso_en_curso': proceso_en_curso,
        'fuente_detalle': 'uni-admision-stats · Dirección de Admisión UNI · datosabiertos.gob.pe (ODC-BY)',
        'enlace': ENLACE,
    }
    # Verificación: nunca nombres
    txt = json.dumps(out, ensure_ascii=False)
    assert 'top10' not in txt and 'top_puntajes' not in txt, 'no deben copiarse rankings nominales'
    write_atomic(OUT, out)
    print('OK %s: %s esp, %s mod, serie %s procesos, %s/%s' % (OUT, len(esp), len(mod), len(serie_rows), hist['total_ingresantes'], hist['total_postulantes']), file=sys.stderr)


if __name__ == '__main__':
    main()
