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
- **Admisión** — ingresantes por especialidad y modalidad (examen 2026-1), serie histórica 2013-1…2026-1 de postulantes/ingresantes, % de mujeres y proceso en curso, vía [uni-admision-stats](https://unimauro.github.io/uni-admision-stats/) (solo agregados, sin nombres).
- **Elección de autoridades 2026** — cómputo 1.ª vuelta por lista (votos docentes/estudiantes, % ponderado), 2.ª vuelta Lista 8 vs Lista 1 del 28-10-2026 (nulidad parcial declarada por el CEUNI; sin resultado publicado), cronograma y feed "En los medios" (prensa verificada), vía el [Observatorio Electoral UNI](https://unimauro.github.io/observatorio-electoral-uni/). Preliminar hasta la proclamación del CEUNI.
- **Planilla** — lista nominal completa del Portal de Transparencia Estándar (PTE, rubro Personal): 2,124 personas / 2,130 registros en setiembre 2026 (1,297 en «Régimen 728/otros», donde el PTE lista a los docentes; 593 CAS; 240 DL 276), masa mensual S/ 10.7 M, serie mensual enero–setiembre 2026 por régimen, top cargos, buscador y filtro por régimen, agregado AIRHSP de docentes, y cruce con los 27 candidatos a autoridades 2026 (badge con enlace al observatorio electoral). Nunca estudiantes.

## Datos y ETL
Dashboard estático (HTML + Chart.js, sin build). Los datos se generan con los scripts de `etl/`:
- `build_mef_uni.py` — presupuesto histórico del pliego 514 desde el datastore CKAN del MEF.
- `build_admision.py` — admisión: lee `stats.json` publicado por uni-admision-stats (fallback: repo local) → `data/admision-uni.json`.
- `build_electoral.py` — elección 2026: lee `site.json`/`electoral-lists.json`/`candidates.json`/`press.json` del observatorio electoral (local o raw de GitHub) → `data/electoral-uni.json`.
- `validate_data.py` — valida `data/*.json` antes de publicar (tipos, HTML, URLs); lo corre el workflow mensual.
- `build_planilla_pte.py` — planilla nominal desde el Portal de Transparencia Estándar (PTE, id_entidad 10048): todos los
  meses del año y regímenes 1–7 y 9 (sin pensionistas), caché en `etl/cache_pte/` (gitignorada), cruce con
  `candidates.json` del observatorio electoral, sin dependencias externas. Sin argumentos usa el año en curso;
  `PTE_MONTHS=3` limita a los últimos 3 meses (CI). No sobrescribe el JSON si el portal falla o viene incompleto.
- (próximos) `build_oece_uni.py` (contrataciones).

## Ecosistema
Sitios hermanos del mismo autor, enlazados desde la sección «Más observatorios y datos UNI»:

| Proyecto | Qué es | Enlace |
|---|---|---|
| Observatorio Electoral UNI 2026 | 9 listas y 27 candidaturas a rector/vicerrectores, con fuentes y cómputo | https://unimauro.github.io/observatorio-electoral-uni/ |
| Admisión UNI en cifras | Estadísticas agregadas y anónimas de los procesos de admisión (2013–2026, proceso en curso) | https://unimauro.github.io/uni-admision-stats/ |
| uniexamen | Scraper/estadísticas de resultados del examen de admisión UNI | repositorio privado (sin enlace público) |
| UNI CEPRE | Scraper y análisis de resultados CEPRE-UNI | repositorio privado (sin enlace público) |
| Gemelo Digital de la UNI | Simulador de impacto académico por sol invertido (datos ilustrativos) | https://unimauro.github.io/gemelo-digital-uni/ |
| Observatorio San Marcos | Transparencia de la UNMSM (pliego 510) | https://unimauro.github.io/observatorio-sanmarcos/ |
| Observatorio ENSAD | Transparencia de la ENSAD (UE 123 MINEDU) | https://unimauro.github.io/observatorio-ensad/ |
| Universidades del Perú | Ranking de investigación de 96 universidades (OpenAlex) | https://unimauro.github.io/universidades-peru/ |
| Perú Transparente | Mapa nacional de funcionarios, entidades y redes de poder (origen de la planilla PTE) | https://unimauro.github.io/peru-transparente/ |
| Poder Económico del Perú | Grafo de grupos económicos, empresas y directorios (SMV · BVL · SBS) | https://unimauro.github.io/observatorio-poder-economico/ |

## Privacidad
Solo información pública. **Nunca** se publican nombres de estudiantes; los nombres solo
corresponden a docentes, funcionarios y personal, tal como los publican las fuentes oficiales.

No es un portal oficial de la UNI. Correcciones: carlos@cardenas.pe
