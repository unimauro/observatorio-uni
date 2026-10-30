"""Validador de data/*.json antes de publicar (CI y local).
Falla si algún string trae HTML/URLs peligrosas o es anormalmente largo: los JSON vienen de
fuentes externas (repos hermanos, portal PTE) y el dashboard los pinta en el DOM.
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
MAX_STR = 2000
BAD = re.compile(r'<\s*/?[a-z!?]|javascript:|data:text/html|vbscript:|(?<![a-z_])on[a-z]+\s*=', re.I)  # etiquetas HTML, no el '<' de '< 8 UIT'
URL_KEYS = ('url', 'enlace', 'perfil_url', 'url_sitio', 'url_repo', 'url_fuente', 'fuente_url', 'fuente_dueno')


def _reject_constant(c):
    raise ValueError('constante no permitida en JSON: %s' % c)


def walk(o, path, errs):
    if isinstance(o, dict):
        for k, v in o.items():
            walk(v, path + '.' + str(k), errs)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, '%s[%d]' % (path, i), errs)
    elif isinstance(o, str):
        if len(o) > MAX_STR:
            errs.append('%s: string de %d caracteres' % (path, len(o)))
        if BAD.search(o):
            errs.append('%s: contenido sospechoso %r' % (path, o[:80]))
        if path.rsplit('.', 1)[-1] in URL_KEYS and o and not o.startswith(('http://', 'https://')):
            errs.append('%s: URL no http(s) %r' % (path, o[:80]))


def main():
    errs = []
    files = sorted(glob.glob(os.path.join(ROOT, '*.json')))
    for f in files:
        try:
            with open(f, encoding='utf-8') as fh:
                walk(json.load(fh, parse_constant=_reject_constant), os.path.basename(f), errs)
        except Exception as e:  # JSON inválido
            errs.append('%s: %s' % (os.path.basename(f), e))
    for e in errs:
        print('ERROR', e, file=sys.stderr)
    print('%d archivos, %d errores' % (len(files), len(errs)), file=sys.stderr)
    sys.exit(1 if errs else 0)


if __name__ == '__main__':
    main()
