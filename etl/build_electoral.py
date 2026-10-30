#!/usr/bin/env python3
"""Construye data/electoral-uni.json con el resumen de la elección de autoridades UNI 2026,
a partir de los datos del Observatorio Electoral Universitario (repo hermano).

Lee site.json + electoral-lists.json + candidates.json del repo local
(../observatorio-electoral-uni/src/data/) y, si no existe, de raw.githubusercontent.com (main).
Solo se copian: número de lista, nombre del candidato a rector (ya público, CEUNI) y votos agregados.

Uso:  python3 etl/build_electoral.py
"""
import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'data', 'electoral-uni.json')
LOCAL_DIR = os.path.join(HERE, '..', '..', 'observatorio-electoral-uni', 'src', 'data')
RAW = 'https://raw.githubusercontent.com/unimauro/observatorio-electoral-uni/main/src/data/'
SITIO = 'https://unimauro.github.io/observatorio-electoral-uni/'
FILES = ['site.json', 'electoral-lists.json', 'candidates.json']
# fecha a partir de la cual los eventos del cronograma se consideran "pendientes" (2.ª vuelta en adelante)
PENDIENTE_DESDE = '2026-10-28'


def read(name):
    local = os.path.join(LOCAL_DIR, name)
    if os.path.exists(local):
        with open(local, encoding='utf-8') as f:
            return json.load(f), 'local'
    with urllib.request.urlopen(RAW + name, timeout=30) as r:
        return json.loads(r.read().decode('utf-8')), 'raw'


def _num(rx, txt):
    m = re.search(rx, txt or '')
    return int(m.group(1)) if m else None


def write_atomic(path, obj):
    tmp = path + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
        f.write('\n')
    os.replace(tmp, path)


def main():
    site, o1 = read(FILES[0])
    lists, _ = read(FILES[1])
    cands, _ = read(FILES[2])
    print('origen de los datos:', o1, file=sys.stderr)
    # Validación mínima: abortar sin escribir si la fuente no trae listas/candidaturas
    if not isinstance(lists, list) or not lists or not isinstance(cands, list) or not cands or not isinstance(site, dict):
        sys.exit('datos electorales incompletos o con estructura inesperada')

    by_list = {l['id']: l for l in lists}
    rector = {}
    for c in cands:
        if c.get('role') == 'rector':
            rector[c['listId']] = {'nombre': c.get('name'), 'slug': c.get('slug'), 'facultad': c.get('facultyId')}

    res = site.get('results') or {}
    rows = []
    for r in res.get('lists') or []:
        lid = r['listId']
        rows.append({
            'lista': lid,
            'numero': by_list.get(lid, {}).get('number'),
            'rector': (rector.get(lid) or {}).get('nombre'),
            'rector_facultad': (rector.get(lid) or {}).get('facultad'),
            'votosDocentes': r.get('votesDocentes'),
            'votosEstudiantes': r.get('votesEstudiantes'),
            'pct_ponderado': r.get('weightedPct'),
            'nota': r.get('note'),
            'perfil_url': SITIO + '#/listas/%s' % by_list.get(lid, {}).get('number', ''),
        })
    rows.sort(key=lambda x: -(x['pct_ponderado'] or 0))

    # electores / emitidos por estamento (solo si hay actas)
    actas = []
    for a in res.get('actas') or []:
        actas.append({k: a.get(k) for k in ('estamento', 'electoresHabiles', 'emitidos', 'blancos', 'nulos')})

    sr = res.get('secondRound') or {}
    sr_lists = [next((x for x in rows if x['lista'] == lid), {'lista': lid, 'numero': by_list.get(lid, {}).get('number'), 'rector': (rector.get(lid) or {}).get('nombre')}) for lid in sr.get('lists') or []]
    sr_result = sr.get('result') or sr.get('results') or None
    generado = datetime.now(timezone.utc).replace(microsecond=0)
    hoy = generado.date().isoformat()
    if sr_result:
        estado = 'con resultados (preliminar)'
    elif sr.get('date') and hoy >= sr['date']:
        estado = 'realizada; resultados pendientes de publicación en esta fuente'
    else:
        estado = 'programada'

    segunda = {
        'fecha': sr.get('date'),
        'listas': [{k: x.get(k) for k in ('lista', 'numero', 'rector', 'votosDocentes', 'votosEstudiantes', 'pct_ponderado')} for x in sr_lists],
        'estado': estado,
        'resultado': sr_result,
        'nota': sr.get('note'),
        'url': SITIO + '#/segunda-vuelta',
    }

    calendario = [{'fecha': e['date'], 'evento': e['event']} for e in site.get('calendar') or [] if e.get('date', '') >= PENDIENTE_DESDE]

    out = {
        '_meta': {
            'fuente': 'Observatorio Electoral Universitario · UNI 2026 (proyecto ciudadano, a partir de actas y cómputo del CEUNI)',
            'url_sitio': SITIO,
            'url_repo': site.get('repoUrl'),
            'actualizado_fuente': site.get('updatedAt'),
            'computo_al': res.get('asOf'),
            'generado': generado.isoformat(),
            'estado': res.get('status'),
            'nota': 'PRELIMINAR: cómputo difundido el 16-10-2026 y transcrito por el observatorio electoral; '
                    'no es un resultado oficial hasta la proclamación del Comité Electoral Universitario (CEUNI). '
                    + (res.get('note') or ''),
            'fecha_eleccion_nota': site.get('electionDateNote'),
            'independencia': site.get('independenceNote'),
        },
        'primera_vuelta': {
            'fecha': site.get('electionDate'),
            'listas': rows,
            'actas': actas,
            'validos_docentes': _num(r'docentes \((\d+)\)', res.get('note')),
            'validos_estudiantes': _num(r'estudiantes \((\d+)', res.get('note')),
            'ponderacion': '2/3 docentes · 1/3 estudiantes (art. 50 del Reglamento, RCU 0650-2026)',
        },
        'segunda_vuelta': segunda,
        'proclamacion': res.get('proclaimed'),
        'calendario_pendiente': calendario,
        'n_listas': len(lists),
        'n_candidaturas': len(cands),
    }
    write_atomic(OUT, out)
    print('OK %s: %d listas, 2.ª vuelta %s (%s), proclamación %s' % (OUT, len(rows), segunda['fecha'], estado, out['proclamacion']), file=sys.stderr)


if __name__ == '__main__':
    main()
