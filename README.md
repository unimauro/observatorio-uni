# Observatorio UNI

Portal ciudadano de transparencia de la **Universidad Nacional de Ingeniería** (UNI).
Junta en un solo lugar, con **datos públicos**, en qué gasta la UNI cada sol, a quién le paga,
qué produce en investigación y a quién admite.

**Live:** https://unimauro.github.io/observatorio-uni/

## Módulos
- **Presupuesto y ejecución** — pliego 514 (MEF · Datos Abiertos SIAF), serie histórica.
- **En qué se gasta** — desglose por unidad ejecutora, categoría/genérica y función.
- **Proveedores y dueños** — contrataciones de la UNI (OECE · OCDS) → RUC → representantes.
- **Investigación** — publicaciones y citas (OpenAlex), UNI vs. pares.
- **Admisión** — ingresantes por especialidad y modalidad (solo agregados, sin nombres).
- **Planilla** — docentes, funcionarios y planas mayores con remuneraciones (datos nominales públicos).

## Datos y ETL
Dashboard estático (HTML + Chart.js, sin build). Los datos se generan con los scripts de `etl/`:
- `build_mef_uni.py` — presupuesto histórico del pliego 514 desde el datastore CKAN del MEF.
- (próximos) `build_oece_uni.py` (contrataciones), `build_planilla_uni.py` (planilla).

## Privacidad
Solo información pública. **Nunca** se publican nombres de estudiantes; los nombres solo
corresponden a docentes, funcionarios y personal, tal como los publican las fuentes oficiales.

No es un portal oficial de la UNI. Correcciones: carlos@cardenas.pe
