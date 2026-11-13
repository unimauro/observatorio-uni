# Capítulo 1. Diagnóstico y línea de base

> Corte de datos: 12 de noviembre de 2026. Cifras en soles corrientes (S/) salvo indicación. Todas las cifras llevan su fuente; "repo:" remite a archivos del Observatorio UNI (`observatorio-uni/data/…`), que a su vez citan la fuente pública original. Cuando un número es un cálculo propio se indica la fórmula. Cuando no se encontró un dato verificable se escribe **no disponible**.

## 1.1 Alcance y advertencias de método

- **Presupuesto**: pliego 514 del MEF, que agrupa a la UNI y a INICTEL-UNI. Las cifras del pliego no son solo de la universidad: INICTEL-UNI tuvo en 2025 un PIM de S/ 13,9 M (3,7 % del pliego) (repo: `presupuesto-uni.json`, `detalle_ultimo_anio.por_unidad`). 2025 es el último ejercicio cerrado; 2026 está en ejecución (devengado al corte de extracción de julio de 2026).
- **Personal**: dos fuentes oficiales que no coinciden. El Portal de Transparencia Estándar (PTE, planilla nominal de setiembre de 2026) lista 1 282 docentes; el AIRHSP (MEF) registra 1 717 plazas/registros en la carrera docente universitaria. La diferencia (435) no está conciliada: puede deberse a plazas vacantes, cesantes con registro activo o docentes que no figuran en la planilla nominal publicada.
- **Producción científica**: OpenAlex (abierto, CC0). Subestima la producción en ingeniería aplicada, libros, informes técnicos y patentes. La serie por año (extraída en junio de 2026) y la ventana 2021–2025 usada para el cruce por facultad (generada en noviembre de 2026) no suman lo mismo (2 360 vs. 1 862 obras); la diferencia no está conciliada y se reportan ambas.
- **Admisión**: hay dos universos no comparables entre sí (examen de admisión vs. microdatos del proceso completo). Se compara solo dentro de cada serie.

## 1.2 Línea de base 2025/2026

### A. Finanzas

| Indicador | Valor | Año | Fuente |
|---|---|---|---|
| PIA (pliego 514) | S/ 331,2 M | 2025 | MEF – SIAF Datos Abiertos (api.datosabiertos.mef.gob.pe); repo: `presupuesto-uni.json` |
| PIM (pliego 514) | S/ 370,6 M | 2025 | ídem |
| Devengado | S/ 338,3 M | 2025 | ídem |
| Ejecución total (devengado/PIM) | 91,3 % | 2025 | ídem |
| PIM 2026 / devengado a julio 2026 | S/ 331,6 M / S/ 128,5 M (38,7 %) | 2026 (parcial) | ídem |
| Variación nominal del PIM 2012→2025 | +37,6 % (S/ 269,3 M → 370,6 M) | 2012–2025 | ídem; cálculo propio, sin deflactar |
| Variación nominal del devengado 2012→2025 | +54,4 % (S/ 219,1 M → 338,3 M) | 2012–2025 | ídem; cálculo propio, sin deflactar |
| Gasto de capital (inversión, genérica 2.6): PIM / devengado | S/ 70,1 M / S/ 46,4 M | 2025 | ídem, `por_categoria` |
| Ejecución de la inversión | 66,2 % | 2025 | cálculo: 46,4 / 70,1 |
| Inversión no ejecutada | S/ 23,7 M | 2025 | cálculo: 70,1 − 46,4 |
| Gasto corriente / devengado total | 86,3 % (S/ 291,9 M) | 2025 | ídem |
| Presupuesto de I+D (programa "Desarrollo de la CTI") | S/ 6,7 M | 2025 | MEF/SIAF; repo: `bibliometria.json` → `presupuesto.idi` |
| I+D como % del PIM | 1,8 % | 2025 | ídem |
| Fondos concursables VRI adjudicados en 2025 | S/ 4,61 M (1,2 % del PIM) | 2025 | resoluciones VRI (vri.uni.edu.pe); repo: `vri-proyectos.json`; % = cálculo propio |
| Genérica "Personal y obligaciones sociales" (devengado) | S/ 153,0 M = 45,2 % del devengado | 2025 | MEF/SIAF; repo: `presupuesto-uni.json` → `por_generica` |
| Personal + pensiones (genéricas 2.1 + 2.2) | S/ 170,2 M = 50,3 % del devengado | 2025 | ídem; cálculo propio |
| Bienes y servicios (incluye CAS, clasificador 2.3.2.8) | S/ 115,1 M = 34,0 % del devengado | 2025 | ídem. El monto de CAS dentro de esta genérica **no disponible** en el repo |
| Masa salarial nominal mensual (todas las planillas PTE) | S/ 10,65 M | set. 2026 | PTE (transparencia.gob.pe, id_entidad 10048); repo: `planilla-uni.json` |
| Masa salarial nominal acumulada enero–setiembre | S/ 99,4 M | 2026 | repo: `planilla-uni.json` → `serie_mensual` (suma de 9 meses, 3 regímenes) |
| Masa salarial docente mensual | S/ 8,26 M | set. 2026 | ídem (categoría docente) |
| Peso de "otros" ingresos en la planilla docente | 29,7 % (S/ 2,45 M de S/ 8,26 M) | set. 2026 | ídem; cálculo: Σ campo `otros` / Σ `total`, docentes |
| Peso de "otros" en la planilla total (docentes + adm. + funcionarios) | 26,9 % | set. 2026 | ídem |
| Presupuesto etiquetado a facultades (metas por facultad + EPG) | S/ 31,9 M = 8,6 % del PIM | 2025 | MEF/SIAF (`por_facultad`); cálculo propio. El grueso del gasto se ejecuta en metas centrales |
| Escuela de Posgrado: PIM / devengado | S/ 4,57 M / S/ 0 (0 %) | 2025 | ídem |
| Recursos Ordinarios / Directamente Recaudados / Canon | **no disponible** (el campo `por_fuente` del repo está vacío; no se halló el desglose 2025 en fuente oficial). Único dato encontrado: PIA 2023 con S/ 5,0 M de RDR en una disposición transitoria | 2023 | RR N.º 2644-2022-UNI, citada en https://cdn.www.gob.pe/uploads/document/file/5614858/4979089-resolucion-rectoral-nro-0174-2023-uni.pdf |
| Gasto (devengado) por estudiante de pregrado | ≈ S/ 24 960 | 2025 | cálculo: devengado 2025 del pliego (S/ 338,3 M) / 13 553 electores hábiles de pregrado del padrón electoral 2026 (repo: `electoral-uni.json`). Aproximación: el padrón no es la matrícula oficial, el devengado incluye INICTEL-UNI, pensiones y posgrado |
| Adjudicaciones a proveedores (buena pro) | S/ 86,6 M; 338 proveedores; 439 procesos; top 10 = 28,8 % | 2023–2025 | OECE/CONOSCE; repo: `proveedores-uni.json` |

### B. Personas

| Indicador | Valor | Año | Fuente |
|---|---|---|---|
| Docentes en planilla nominal (PTE) | 1 282 | set. 2026 | PTE; repo: `planilla-uni.json`, `facultades-uni.json` |
| Docentes registrados en AIRHSP (carrera docente universitaria) | 1 717 (sueldo promedio S/ 4 102) | 2026 | AIRHSP vía PTE; repo: `planilla-uni.json` → `por_regimen_airhsp` |
| Docentes a tiempo completo + dedicación exclusiva (PTE) | 724 (56,5 %): 613 TC (incluye 10 jefes de práctica) + 111 DE | set. 2026 | PTE; cálculo propio sobre el campo `cargo` |
| Docentes a tiempo parcial con categoría (PTE) | 261 (20,4 %) | set. 2026 | ídem |
| Docentes con cargo genérico "DOCENTE UNIVERSITARIO" (sin categoría ni dedicación en el PTE) | 297 (23,2 %); ingreso medio S/ 4 321 | set. 2026 | ídem. Que sean contratados es una inferencia **no verificada** |
| Docentes por categoría (PTE, con categoría) | Principales 269 · Asociados 234 · Auxiliares 470 · Jefes de práctica 12 | set. 2026 | ídem; cálculo propio |
| Docentes con maestría y/o doctorado | 44 % (de 1 139) | 2017 | SUNEDU, informe de licenciamiento; repo: `bibliometria.json` → `docentes`. Dato actual **no disponible** |
| Administrativos (PTE: CAS + D.Leg. 276) | 728 (+120 funcionarios/directivos) | set. 2026 | PTE; repo: `planilla-uni.json` → `por_categoria` |
| Personal no docente en AIRHSP (276 + CAS + 728 + otros) | 1 526 | 2026 | AIRHSP; cálculo: 760 + 673 + 68 + 22 + 3 |
| Ratio no docente / docente | 0,66 (PTE) · 0,89 (AIRHSP) | 2026 | cálculo: 848/1 282 y 1 526/1 717 |
| Trabajadores CAS (PTE) | 593 (S/ 1,45 M/mes) | set. 2026 | PTE; repo: `planilla-uni.json` → `por_regimen_nominal` |
| Estudiantes de pregrado (proxy) | 13 553 electores hábiles de pregrado | 2026 | Padrón de la elección de autoridades 2026 (CEUNI, vía Observatorio Electoral UNI); repo: `electoral-uni.json`. Es un padrón electoral, no la matrícula oficial |
| Matriculados (cifra de prensa, nivel no especificado) | 10 978 (1 761 mujeres) | 2023-2 | El Peruano: https://elperuano.pe/noticia/236595-uni-cuanto-ha-crecido-la-presencia-de-mujeres-y-que-carreras-prefieren-ellas |
| Estudiantes de pregrado / posgrado (dato oficial más reciente hallado) | 12 060 / 1 200 (docentes: 1 339) | 2019 | UNI, evaluación del PEI 2018–2020: https://www.ocpla.uni.edu.pe/transparencia/file/uplanyprogeinv/EPEIUNI/eval_peo_uni_2018_2020_2019.pdf. Matrícula oficial 2025/2026 **no disponible** |
| Estudiantes por docente (proxy) | 10,6 por docente PTE · 18,7 por docente TC/DE | 2026 | cálculo: 13 553 / 1 282 y 13 553 / 724 |

### C. Investigación

| Indicador | Valor | Año | Fuente |
|---|---|---|---|
| Publicaciones UNI en OpenAlex (histórico total) | 4 697 obras; 65 514 citas; índice h 90; 68,9 % acceso abierto | corte jun. 2026 | OpenAlex (openalex.org/I62520931); repo: `bibliometria.json` |
| Publicaciones UNI en el año | 497 | 2025 | ídem (`by_year`) |
| Publicaciones 2021–2025 (serie por año) | 2 360 | 2021–2025 | ídem; suma de `by_year` |
| Obras con afiliación UNI en la ventana del cruce por facultad | 1 862 obras; 1 643 autores | 2021–2025 | OpenAlex; repo: `facultades-uni.json` |
| Publicaciones por docente | 0,39 por docente-año (2025) · 1,45 por docente en 5 años (2021–25) | 2021–2025 | cálculo: 497/1 282 y 1 862/1 282 |
| Docentes con ≥1 publicación identificada | 336 de 1 282 = 26,2 % | 2021–2025 | repo: `facultades-uni.json` (cruce de nombres PTE–OpenAlex; subestima) |
| Mejor y peor facultad en % de docentes que publican | Ciencias 41,3 % · Ing. Industrial y de Sistemas 14,5 % | 2021–2025 | ídem |
| Facultad con más obras | Ciencias: 300 obras (2,0 por docente) | 2021–2025 | ídem |
| Facultad con menos obras por docente | FIIS: 28 obras (0,25 por docente) | 2021–2025 | ídem |
| Fondos concursables VRI adjudicados | S/ 16,94 M en 231 proyectos (206 responsables distintos) | 2022–2026 | resoluciones rectorales VRI (vri.uni.edu.pe); repo: `vri-proyectos.json` |
| VRI por año | 2023: S/ 4,08 M · 2024: 4,78 M · 2025: 4,61 M · 2026: 3,41 M | 2023–2026 | ídem (2024 reconstruido con relaciones de gasto) |
| Concentración VRI | Ciencias 33,8 %; top 3 (FC, FIQT, FIM) 64,3 %; FIIS 1,2 %; FIEECS 1,8 % | 2022–2026 | ídem; cálculo propio sobre la facultad del responsable |
| Investigadores RENACYT afiliados a la UNI | 90 (último dato verificado). Cifra 2025/2026 **no disponible** | 2020 | CONCYTEC vía La República; repo: `bibliometria.json` → `renacyt` |
| Solicitudes de patentes (INDECOPI) | 1.º lugar entre universidades en 2020; 3.º en 2022 con 34 solicitudes; ≈200 solicitudes acumuladas 1990–2021 (fuentes discrepan: 202 vs. 197). En 2025 la UNI **no figura** en el top reportado (lidera U. Continental con 194) | 2020–2025 | Andina: https://andina.pe/agencia/noticia-uni-fue-universidad-lider-solicitudes-patentes-durante-2020-840544.aspx · Gestión: https://gestion.pe/economia/indecopi-estas-son-las-universidades-con-mas-solicitudes-de-patentes-en-el-2022-noticia/ · Gestión: https://gestion.pe/peru/estas-son-las-universidades-empresas-y-regiones-con-un-mayor-numero-de-patentes-ante-indecopi-indecopi-noticia/ · Energiminas (2025): https://energiminas.com/2026/02/09/indecopi-universidades-peruanas-lideraron-ranking-de-solicitudes-de-patentes-en-2025/. Cifra UNI 2024–2025 **no disponible** |
| Impacto: citas medias normalizadas (OpenAlex `mean_citedness`) | UNI 1,75 · PUCP 1,45 · San Marcos 0,73 · Cayetano 2,06 | corte jun. 2026 | repo: `bibliometria.json` |

### D. Oferta académica

| Indicador | Valor | Año | Fuente |
|---|---|---|---|
| Facultades | 11 | 2026 | repo: `facultades-uni.json` (dependencias con docentes en el PTE) |
| Programas de pregrado | 34 (las 34 especialidades tuvieron ingresantes en el examen 2026-1) | 2026 | repo: `admision-uni.json` → `ingresantes_por_especialidad`; coincide con prensa ("34 carreras"): https://ecosistemastartup.com/?p=115362 |
| Carreras creadas recientemente | Ing. de Ciberseguridad (reconocida por SUNEDU, Res. N.º 024-2022-SUNEDU/CD); Ing. Aeroespacial (aprobada por la Asamblea Universitaria para 2025-I); Ing. de Inteligencia Artificial (aprobada 2023, 30 vacantes en 2026-I); Ing. Biomédica, Urbanismo e Ing. de Software (incorporadas en años recientes; fecha y resolución de Software **no disponibles**) | 2022–2026 | El Peruano (Res. 024-2022): https://busquedas.elperuano.pe/normaslegales/aprueban-modificacion-de-licencia-institucional-solicitada-p-resolucion-n-024-2022-suneducd-2055528-1/ · Andina (Aeroespacial): https://andina.pe/ingles/noticia-ya-puedes-postular-a-carrera-ingenieria-aeroespacial-la-uni-para-ciclo-2025i-1013581.aspx · El Peruano (IA): https://elperuano.pe/noticia/286941-ingenieria-del-futuro-uni-ofrece-30-primeras-vacantes-para-carrera-de-ingenieria-de-inteligencia-artificial. Reconocimiento SUNEDU de IA, Aeroespacial y Software **no verificado** |
| Ingresantes de las carreras nuevas | IA 19 · Aeroespacial 24 · Ciberseguridad 26 · Software 21 · Biomédica 26 · Urbanismo 21 (de 922) | 2026-1 | repo: `admision-uni.json` |
| Maestrías y doctorados (número de programas) | Último dato oficial: 41 maestrías, 6 doctorados y 13 segundas especialidades (licenciamiento SUNEDU). Cifra 2026 **no disponible**: posgrado.uni.edu.pe figura "en construcción" y cada facultad convoca por separado (convocatorias de maestría 2026-1 y 2026-2 en portal.uni.edu.pe). Fuente no oficial: 57 maestrías y 10 doctorados (tramitesperu.com) | 2017 | Andina: https://andina.pe/agencia/noticia-sunedu-entrego-licenciamiento-institucional-a-uni-692641.aspx · https://portal.uni.edu.pe/images/EVENTOS-2026/202607/PDFS/MAESTRIA_2026-2.pdf |
| Modelo de financiamiento del posgrado | Autofinanciado, con pago por crédito. Montos solo en fuente no oficial: admisión S/ 875; crédito S/ 424 (maestría) y S/ 532 (doctorado). Las maestrías son en general a tiempo parcial (horario vespertino o de fin de semana según las convocatorias); no se halló ninguna maestría a tiempo completo con beca propia de la UNI | 2026 | tramitesperu.com/universidades/uni/posgrado/ (confianza baja); montos oficiales **no disponibles** |
| Doctorados a tiempo completo con beca | Sí, pero dependen de fondos externos: Doctorado en Ciencias con menciones en Física y en Química, con becas PROCIENCIA (CONCYTEC) de dedicación exclusiva (S/ 6 500/mes durante 36 meses). La convocatoria ofreció 76 plazas (32 para mujeres) y se seleccionaron 16 becarios en Física y 15 en Química. No se halló convocatoria 2026 | 2024 | PROCIENCIA, Alianzas Interinstitucionales: https://prociencia.gob.pe/wp-content/uploads/2024/convocatorias/Becas%20en%20Programas%20de%20Doctorado%20en%20Alianzas%20Interinstitucionales/Resolucion_nro_037_2024_ID_9552412341712502515.pdf · El Peruano: https://www.elperuano.pe/noticia/237285-el-40-de-becas-para-doctorados-en-la-uni-seran-destinadas-para-mujeres. Maestrías a tiempo completo con beca propia de la UNI: **no disponible** |
| Licenciamiento SUNEDU | Licencia institucional otorgada por Res. del Consejo Directivo N.º 073-2017-SUNEDU/CD (27-11-2017), vigencia 10 años → vence en noviembre de 2027 (cálculo: 2017 + 10); modificada en 2022 (Res. 024-2022-SUNEDU/CD) | 2017 | Andina: https://andina.pe/agencia/noticia-sunedu-entrego-licenciamiento-institucional-a-uni-692641.aspx · texto: https://portal.uni.edu.pe/images/noticias/201711/1591199-1.pdf. La RCD 0004-2025-SUNEDU/CD dio por concluidos los procedimientos de renovación porque SUNEDU perdió esa potestad tras la Ley 32105 (https://www.unife.edu.pe/transparencia1/1_normatividad/institucional/RESOLUCION_DEL_CONSEJO_DIRECTIVO_0004-2025-SUNEDU-CD.pdf). Cómo se aplicará a la UNI en 2027: **no disponible** |
| Acreditaciones internacionales | 20 programas acreditados internacionalmente: 19 por ABET y 1 por RIBA (Arquitectura). Los ABET son Estadística, Geológica, Metalúrgica, Minas, Mecánica, Mecánica-Eléctrica, Naval, Mecatrónica, Física, Petroquímica, Petróleo y Gas Natural, Química, Textil, Industrial, Sistemas, Eléctrica, Electrónica, Telecomunicaciones y Civil (esta última desde 2014). Ninguna de las carreras creadas desde 2022 figura acreditada. La reacreditación ABET de Civil está en curso (visita prevista en 2027). Vigencia actual de cada acreditación **no verificada** | 2017 (cifra); 2025 (proceso FIC) | https://acreditacion.uni.edu.pe/abet · https://acreditacion.uni.edu.pe/wp-content/uploads/2025/11/Acreditacion-FIC-Nov-2025.pdf |
| Acreditación ICACIT / SINEACE | ICACIT: **no disponible**. SINEACE reconoció acreditaciones ABET (p. ej., Ing. Sanitaria, Minas, Química, Petroquímica) con vigencia hasta 30-09-2020; reconocimiento vigente **no verificado** | 2020 | https://www.gob.pe/institucion/sineace/noticias/186056-sineace-reconoce-acreditaciones-de-la-uni-y-la-pucp |
| Titulados por año | ≈ 1 000 ingenieros titulados al año (declaración del rector; cifra redondeada); el rector mencionó ≈ 11 000 estudiantes | 2026 (mayo) | Andina: https://andina.pe/agencia/noticia-uni-proyecta-abrir-filiales-provincias-carreras-alta-demanda-laboral-1076885.aspx |
| Tasa de graduación / titulación (cohortes) | **no disponible** | — | — |
| Plan Estratégico Institucional vigente | PEI 2025–2030, aprobado por RR 0557-2025-UNI (18-02-2025). Texto y metas **no disponibles** en línea; el plan anterior es el PEI 2020–2025 | 2025 | citado en RR 1383-2025-UNI: https://cdnuni.uni.edu.pe/dn/laravel/storage/app/public/RR%201383-2025.pdf · PEI 2020–2025: https://www.diga.uni.edu.pe/index.php/files/39/Plan-Estrategico/14/Plan-Estrategico-UNI---2020-2025.pdf |

### E. Admisión

| Indicador | Valor | Año | Fuente |
|---|---|---|---|
| Examen de admisión 2026-1: postulantes / ingresantes | 5 713 / 922 (16,1 %) | 2026 | puntajes.admision.uni.edu.pe vía uni-admision-stats; repo: `admision-uni.json` |
| Concurso de admisión 2026-2: postulantes / ingresantes | 4 454 / 924 (20,7 %) | 2026 | ídem (`ciclo_actual`) |
| Proceso completo 2025 (microdatos): postulantes / ingresantes | 16 036 / 2 757 (17,2 %) | 2025 | datosabiertos.gob.pe vía uni-admision-stats; repo: `admision-uni.json` → `serie_historica` |
| Postulantes 2026-1 vs. 2025-1 (microdatos) | 6 114 vs. 10 608 (−42,4 %) | 2025–2026 | ídem; cálculo propio |
| Mujeres: % de postulantes / % de ingresantes | 21,8 % / 16,8 % | 2026-1 | ídem (`mujeres`) |
| Puntaje promedio ingresantes vs. postulantes | 1 092,4 vs. 695,1 | 2026-1 | ídem |
| Presupuesto devengado por ingresante | ≈ S/ 122 700 | 2025 | cálculo: 338,3 M / 2 757 ingresantes 2025 (como lo calcula `app.js`, `valorCalc`) |
| Vacantes ofertadas | 2026-I: 1 886 (34 carreras, todas las modalidades) · 2026-II: 1 630 | 2026 | Prensa (Gestión, Andina) que cita los cuadros oficiales: https://admision.uni.edu.pe/wp-content/uploads/2026/01/CUADRO-DE-VACANTES-2026-1-AVL-12_01R.pdf y https://admision.uni.edu.pe/wp-content/uploads/2026/06/CUADRO-VACANTES-2026-2.pdf (el total no se verificó directamente en los PDF) |
| Vacantes de procesos anteriores | 2024-2: 1 453 · 2025-I: 1 510. Es decir, las vacantes subieron 24,9 % de 2025-I a 2026-I mientras los postulantes bajaban | 2024–2025 | prensa y cuadros de vacantes (vía investigación web; confianza media); variación = cálculo propio |
| Composición de las vacantes 2026-2 | 1 219 por especialidad · 180 reservadas por ley · 231 supernumerarias | 2026 | https://admision.uni.edu.pe/wp-content/uploads/2026/06/CUADRO-VACANTES-2026-2.pdf |
| Postulantes por vacante | 3,0 (2026-I, examen) · 2,7 (2026-II) | 2026 | cálculo: 5 713 / 1 886 y 4 454 / 1 630 |
| Vacantes cubiertas en el examen | 48,9 % (922 / 1 886) en 2026-I · 56,7 % (924 / 1 630) en 2026-II. Con microdatos del proceso completo 2026-1: 69,9 % (1 319 / 1 886) | 2026 | cálculo propio; universos distintos (ver advertencias) |

### F. Posición frente a pares

| Indicador | UNI | Pares | Año | Fuente |
|---|---|---|---|---|
| Publicaciones en el año | 497 | San Marcos 2 849 · PUCP 1 555 · Cayetano 1 321 | 2025 | OpenAlex; repo: `bibliometria.json` |
| Publicaciones históricas | 4 697 | San Marcos 44 113 · PUCP 33 166 · Cayetano 22 045 · UPC 8 320 · UNALM 6 948 · Tec de Monterrey 38 644 · U. Andes 25 901 · UNAL 97 352 · U. de Chile 112 952 · PUC Chile 81 520 · UBA 129 078 · UNAM 248 299 · USP 471 028 | corte jun. 2026 | ídem |
| Índice h | 90 | UPC 92 · UNALM 123 · San Marcos 162 · PUCP 205 · Cayetano 301 · UNAL 296 · Andes 422 · PUC Chile 479 · U. de Chile 514 · UNAM 639 · USP 866 | corte jun. 2026 | ídem |
| QS World University Rankings | 2023: 1201–1400 · 2024: 951–1000 · ed. 2026: 1201–1400 · **ed. 2027 (jun. 2026): no clasificada**. El repo no precisa si "2023/2024" es el año de edición o de publicación; la prensa ubica la ed. 2025 en 1201–1400 | San Marcos 951–1000 en ed. 2027 (única pública peruana en el top 1000) | 2022–2026 | repo: `bibliometria.json` → `qs`; La República (ed. 2027): https://larepublica.pe/sociedad/2026/06/18/la-uni-fuera-del-ranking-qs-world-2027-esta-es-la-unica-universidad-publica-del-peru-que-figura-entre-las-mejores-1000-del-mundo-206874 |
| QS Latinoamérica 2026 | puesto 125 (según prensa; no cotejado con la tabla oficial de QS) | — | 2025 | La República (confianza media-baja) |
| THE World University Rankings 2026 | No figura entre las universidades peruanas listadas | — | 2026 | https://larepublica.pe/sociedad/2026/01/19/ni-la-uni-ni-unmsm-esta-es-la-mejor-universidad-publica-del-peru-segun-world-university-rankings-2026-1493552 |
| Scimago (SIR) | 4.º en el Perú en ingeniería (2025, prensa); ranking general (23.º en el Perú) **no verificado** porque scimagoir.com bloquea la extracción | — | 2025 | https://www.revistaeconomia.com/?p=93020 (confianza media) |
| Ranking histórico SUNEDU 1980–2022 | 4.º lugar (25,30 puntos) | — | 2024 | https://larepublica.pe/sociedad/2024/02/17/uni-en-que-puesto-del-ranking-de-las-10-mejores-universidades-del-peru-se-ubica-ranking-historico-de-sunedu-universidad-nacional-de-ingenieria-evat-1061361 |
| ShanghaiRanking (ARWU) | **no disponible** | — | — | repo: `bibliometria.json` → `_meta.rankings_nota` |

### G. Infraestructura y uso de espacios

| Indicador | Valor | Año | Fuente |
|---|---|---|---|
| Tasa de ocupación de aulas, laboratorios y edificios | **no disponible – hipótesis del autor** ("muchos edificios con menos de 40 % de ocupación"). No se halló ningún inventario ni medición pública de uso | — | — |
| Locales licenciados | Sede principal SL01 (Av. Túpac Amaru 210, Rímac) y locales en La Molina (SL02, Calle Los Biólogos 245), San Borja y Miraflores | 2017–2022 | Res. 024-2022-SUNEDU/CD: https://busquedas.elperuano.pe/normaslegales/aprueban-modificacion-de-licencia-institucional-solicitada-p-resolucion-n-024-2022-suneducd-2055528-1/ |
| Área construida, número de aulas, laboratorios y talleres | **no disponible**. Deberían figurar en el Informe Técnico de Licenciamiento N.º 015-2017-SUNEDU/02-12 (21-11-2017), que no está publicado en formato consultable | 2017 | citado en RCD 073-2017: https://portal.uni.edu.pe/images/noticias/201711/1591199-1.pdf |
| Plan Maestro / Plan de infraestructura vigente | **no disponible** (no se halló publicado) | — | — |
| Terreno del ex supermercado "Metro UNI" | Más de 32 000 m² del campus, arrendados desde 1999. La UNI no renovó el contrato y el local cerró en agosto de 2024; uso futuro **no disponible** | 2024 | Perú Retail: https://www.peru-retail.com/?p=344608 · https://www.peru-retail.com/?p=407668 |
| Inversión (gasto de capital) no ejecutada | S/ 23,7 M (33,8 % del PIM de capital) | 2025 | MEF/SIAF; repo: `presupuesto-uni.json` (ver sección A) |
| Proyectos de inversión (Invierte.pe) por CUI y su avance | **no disponible**: la API del MEF no respondió desde este entorno y la consulta pública de Invierte.pe requiere navegador. Ejemplos aislados: CUI 2110015 (plaza estudiantil FIEECS) y CUI 2112732 (equipamiento TI FIEECS, S/ 1,18 M), ambos con modificaciones en la fase de ejecución en 2023. Un proyecto anunciado de 12 laboratorios en FIEE por ≈ S/ 28 M no tiene fecha ni estado verificables | 2023 | RR 0057/0058-2023-UNI: https://cdn.www.gob.pe/uploads/document/file/5614733/4978972-resolucion-rectoral-nro-0058-2023-uni.pdf · Andina: https://andina.pe/agencia/noticia-implementara-12-nuevos-laboratorios-la-universidad-nacional-ingenieria-772055.aspx |
| Obras paralizadas o inconclusas (INFOBRAS / Contraloría) | No se halló evidencia pública de obras paralizadas de la UNI (Perú) en las búsquedas realizadas. Atención: muchos resultados corresponden a la UNI de Nicaragua. Ausencia de evidencia ≠ evidencia de ausencia: falta consultar INFOBRAS directamente | 2026 | búsqueda web, 12-11-2026 |
| Gasto en mantenimiento de infraestructura | **no disponible** (requiere el desglose por específica de gasto del SIAF) | — | — |

**Datos que permitirían medir la ocupación** (para verificar o descartar la hipótesis):
1. El inventario físico de ambientes de la Oficina de Infraestructura: aulas, laboratorios, talleres y auditorios, con su aforo y m², por edificio.
2. Los horarios de clase de cada semestre (sistema de matrícula/ORCE), que asignan secciones a ambientes. Con ellos se calcula ocupación = horas programadas / horas disponibles (por ejemplo, 14 h × 6 días), y uso del aforo = matriculados / aforo.
3. Los registros de reserva y uso de laboratorios, y las horas de uso de los equipos mayores.
4. El control de acceso o los conteos WiFi por edificio, como medida de uso real (agregado y anónimo).
5. El consumo eléctrico por subestación o edificio. La UNI tiene subestaciones propias según sus planes de funcionamiento.
6. El margesí de bienes inmuebles (SBN/SINABIP) y los informes de licenciamiento (ITL 015-2017) como línea de base de área.
7. El registro de proyectos en Invierte.pe e INFOBRAS (CUI, avance físico y financiero, estado: paralizada/en ejecución/culminada).

### H. Innovación, transferencia y vínculos

| Indicador | Valor | Año | Fuente |
|---|---|---|---|
| Incubadora | Startup UNI, que depende de la Dirección de Innovación y Transferencia Tecnológica (DITT) del VRI. Prepara postulaciones a ProInnóvate (cofinanciamiento de hasta S/ 67 000 para emprendimientos innovadores y S/ 150 000 para dinámicos) | 2026 | Bases: https://startup.uni.edu.pe/Bases_Incubacion.pdf |
| Startups presentadas con ProInnóvate | 4 startups (publicidad, construcción, agroexportación, minería) financiadas por StartUp Perú, generaciones 11G y 12G | 2026 (26 de mayo) | gob.pe/ProInnóvate: https://www.gob.pe/institucion/proinnovate/noticias/1397617-proinnovate-y-startup-uni-presentaron-startups-que-transforman-con-tecnologia-sectores-economicos-claves |
| Número de startups incubadas o graduadas, empleo e inversión levantada | **no disponible** oficialmente (un portal no oficial dice "más de 39"; dato no confiable) | — | https://ecosistemastartup.com/?p=92159 (confianza baja) |
| Patentes | ver sección C: líder histórico en solicitudes (≈200 entre 1990 y 2021) pero ausente del top de 2025; cifras 2024–2025 **no disponibles** | — | INDECOPI vía prensa |
| Licencias de tecnología, spin-offs e ingresos por transferencia | **no disponible** | — | — |
| Convenios internacionales (total vigente) | **no disponible** (no se halló un registro público consolidado) | — | — |
| Dobles titulaciones recientes | Acuerdos de doble titulación con ENSTA Paris y Télécom Paris (Institut Polytechnique de Paris), firmados en 2026. Hay acercamiento con IMT Atlantique (intercambio docente en exploración) | 2026 | https://proactivo.com.pe/uni-firma-acuerdos-con-ensta-paris-y-telecom-paris/ · https://proactivo.com.pe/uni-propicia-doble-titulacion-e-intercambio-estudiantil-con-prestigiosa-escuela-francesa-de-ingenieria/ |
| Proyecto con préstamo del Banco Mundial vía PROCIENCIA | La UNI es entidad ejecutora de un proyecto de fortalecimiento de servicios de CTI financiado por PROCIENCIA (préstamo BM); monto **no disponible** | 2025 | avisos de adquisición VRI, p. ej. https://vri.uni.edu.pe/wp-content/uploads/2025/11/SDC-N°03-2025-ADQUISICION-DE-DETECTOR-DE-MATERIALES-EN-PARED.pdf |
| Nombramiento docente | 148 docentes contratados nombrados como auxiliares y asociados (RR 1688-2025-UNI) | 2025 | https://proactivo.com.pe/uni-aprueba-el-nombramiento-de-148-docentes-como-profesores-auxiliares-y-asociados/ |

## 1.3 Hallazgos clave

1. **La UNI ejecuta bien el gasto corriente, pero deja sin ejecutar un tercio de su inversión.** En 2025 devengó el 91,3 % del PIM (S/ 338,3 M de 370,6 M), pero solo el 66,2 % del gasto de capital: S/ 23,7 M de inversión no se ejecutaron (MEF/SIAF; repo `presupuesto-uni.json`). La Escuela de Posgrado tuvo S/ 4,57 M de PIM y devengó S/ 0.
2. **La investigación recibe una fracción mínima del presupuesto.** El programa de CTI sumó S/ 6,7 M (1,8 % del PIM 2025) y los concursos del VRI adjudicaron S/ 4,61 M en 2025 (1,2 % del PIM) (MEF/SIAF; `vri-proyectos.json`). Personal y pensiones absorben el 50,3 % del devengado, y bienes y servicios (que incluye CAS) el 34,0 %.
3. **Una parte importante del ingreso docente no es remuneración básica.** En setiembre de 2026 el 29,7 % de la planilla docente (S/ 2,45 M de S/ 8,26 M al mes) se pagó como "otros" ingresos (PTE; `planilla-uni.json`). El PTE no detalla estos pagos ni los vincula a productos.
4. **Solo uno de cada cuatro docentes tiene producción científica identificable.** 336 de 1 282 docentes (26,2 %) aparecen como autores en OpenAlex en 2021–2025; la UNI produjo 0,39 publicaciones por docente en 2025 (497 / 1 282). La brecha entre facultades es de casi 3 a 1: Ciencias 41,3 % frente a FIIS 14,5 % (`facultades-uni.json`).
5. **Los fondos del VRI están concentrados.** Ciencias recibió el 33,8 % de los S/ 16,9 M adjudicados en 2022–2026 y las tres primeras facultades (FC, FIQT, FIM) el 64,3 %; FIIS (1,2 %) y FIEECS (1,8 %) casi no participan (`vri-proyectos.json`).
6. **La UNI tiene producción de buen impacto relativo, pero pequeña en volumen frente a sus pares.** En 2025 publicó 497 obras frente a 2 849 de San Marcos y 1 555 de la PUCP (5,7 y 3,1 veces más). Su impacto medio por obra (1,75) supera al de PUCP (1,45) y San Marcos (0,73). Su índice h (90) es el más bajo del grupo de comparación (`bibliometria.json`). La producción creció de 55 obras en 2012 a 497 en 2025, pero se ha estancado desde 2021 (entre 446 y 517 al año).
7. **La UNI salió del QS World en la edición 2027.** Estuvo en 951–1000 (ed. 2024) y en 1201–1400 (eds. 2023 y 2026), y no figura en la ed. 2027 publicada en junio de 2026 (La República; `bibliometria.json`). El RENACYT más reciente verificado es de 2020 (90 investigadores).
8. **La demanda de admisión cae, la oferta de vacantes sube y las vacantes no se cubren.** Los postulantes del proceso 2026-1 bajaron 42,4 % frente a 2025-1 (6 114 vs. 10 608, microdatos), mientras las vacantes subieron de 1 510 a 1 886 (+24,9 %). En el examen 2026-I ingresaron 922 personas para 1 886 vacantes (48,9 % cubiertas; 3,0 postulantes por vacante). Las mujeres son el 16,8 % de los ingresantes (`admision-uni.json`; prensa para vacantes).
9. **La oferta de pregrado se renueva; el posgrado es autofinanciado, de tiempo parcial y no está documentado.** Hay 34 carreras (28 en 2017), 6 de ellas creadas o abiertas desde 2022 (Ciberseguridad, Aeroespacial, IA, Software, Biomédica, Urbanismo), con 19 a 26 ingresantes cada una en 2026-1; ninguna está acreditada todavía. Del posgrado, el último conteo oficial es de 2017 (41 maestrías, 6 doctorados). Hoy el portal de posgrado está "en construcción" y cada facultad convoca por separado. La única oferta doctoral a tiempo completo con estipendio verificada depende de becas externas de PROCIENCIA (Física y Química: 31 becarios seleccionados en 2024).
10. **Infraestructura sin línea de base pública.** No hay inventario de ambientes, Plan Maestro publicado ni medición de ocupación. La hipótesis de subocupación (< 40 %) no se puede verificar ni descartar con datos públicos. Al mismo tiempo, en 2025 quedaron sin ejecutar S/ 23,7 M de inversión. Además, un terreno de más de 32 000 m² (ex Metro UNI) quedó libre en agosto de 2024 sin destino público conocido (MEF/SIAF; Perú Retail).
11. **La transferencia tecnológica es incipiente y no se mide.** Startup UNI opera con fondos ProInnóvate (4 startups presentadas en mayo de 2026), pero no hay cifras oficiales de startups, licencias ni ingresos por transferencia. La UNI, que fue líder histórico en solicitudes de patentes, no aparece en el top 2025 de INDECOPI. Las alianzas internacionales recientes verificadas son dos dobles titulaciones con escuelas francesas (2026).
12. **El licenciamiento vence pronto y la información sobre el personal no cuadra.** La licencia SUNEDU (Res. 073-2017-SUNEDU/CD) cumple 10 años en noviembre de 2027. El PTE lista 1 282 docentes y el AIRHSP 1 717. De los docentes del PTE, 297 (23,2 %) figuran sin categoría ni dedicación, y el último dato público sobre grados del cuerpo docente es de 2017 (44 % con posgrado).

## 1.4 Series para gráficos

Unidades: S/ millones (soles corrientes) para montos; número de obras para publicaciones. `null` = no disponible en las fuentes revisadas. 2026 es parcial (presupuesto: devengado a julio de 2026; publicaciones: OpenAlex a junio de 2026). Fuentes: `presupuesto-uni.json` (MEF), `bibliometria.json` (OpenAlex; I+D 2025 = programa CTI), `vri-proyectos.json` (VRI). "planilla" = genérica 2.1 Personal y obligaciones sociales (devengado); solo está disponible para 2025. "inversion" = gasto de capital devengado.

```json series
{
  "unidad_montos": "S/ millones corrientes",
  "fuentes": {
    "pim_devengado": "MEF Consulta Amigable (2012-2024) y SIAF Datos Abiertos (2025-2026), pliego 514 — repo data/presupuesto-uni.json",
    "inversion_planilla_idi": "MEF/SIAF 2025 — repo data/presupuesto-uni.json (por_categoria, por_generica) y data/bibliometria.json (presupuesto.idi)",
    "vri": "Resoluciones VRI-UNI — repo data/vri-proyectos.json",
    "publicaciones": "OpenAlex by_year — repo data/bibliometria.json (extraído 2026-06)"
  },
  "anios":         [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026],
  "pim":           [269.3, 260.5, 274.3, 292.0, 311.6, 321.9, 299.0, 300.0, 291.2, 283.4, 303.1, 330.8, 386.3, 370.6, 331.6],
  "devengado":     [219.1, 215.4, 227.1, 233.4, 252.8, 255.7, 254.3, 266.2, 218.9, 247.4, 271.3, 301.3, 344.3, 338.3, 128.5],
  "ejecucion_pct": [81.4, 82.7, 82.8, 79.9, 81.1, 79.5, 85.1, 88.7, 75.2, 87.3, 89.5, 91.1, 89.1, 91.3, 38.7],
  "inversion_pim": [null, null, null, null, null, null, null, null, null, null, null, null, null, 70.1, null],
  "inversion_devengado": [null, null, null, null, null, null, null, null, null, null, null, null, null, 46.4, null],
  "idi_programa_cti": [null, null, null, null, null, null, null, null, null, null, null, null, null, 6.7, null],
  "vri_concursos_adjudicado": [null, null, null, null, null, null, null, null, null, null, 0.06, 4.08, 4.78, 4.61, 3.41],
  "planilla_generica_2_1_devengado": [null, null, null, null, null, null, null, null, null, null, null, null, null, 153.0, null],
  "publicaciones_uni":        [55, 64, 104, 101, 112, 132, 261, 276, 373, 449, 446, 517, 451, 497, 287],
  "publicaciones_san_marcos": [1046, 1295, 5075, 1237, 1239, 1602, 1833, 2058, 2874, 3698, 3620, 4143, 3533, 2849, 1739],
  "publicaciones_pucp":       [873, 1090, 1233, 1126, 1170, 1213, 1228, 1308, 1428, 1682, 1653, 1956, 1586, 1555, 671],
  "notas": [
    "San Marcos 2014 (5075) es un valor atípico de OpenAlex; no se corrigió.",
    "VRI 2022 = S/ 57 000 de 2 proyectos listados en ejecución 2023; 2024 reconstruido con relaciones de gasto.",
    "Admisión (otra serie disponible en data/admision-uni.json → serie_historica, 2013-1 a 2026-1)."
  ]
}
```

## 1.5 Vacíos de información

1. **Fuentes de financiamiento** (Recursos Ordinarios, Directamente Recaudados, Canon y regalías, donaciones): no hay desglose 2025/2026 en el repo (`por_fuente` vacío) ni en las fuentes web revisadas. Se puede obtener en la Consulta Amigable del MEF por pliego 514.
2. **Series históricas de inversión, I+D y planilla**: el repo solo tiene el detalle por genérica, categoría y programa para 2025.
3. **Gasto en CAS** dentro de bienes y servicios (clasificador 2.3.2.8): no está separado, lo que subestima el gasto total en personal.
4. **Matrícula oficial 2025/2026** de pregrado y posgrado: el último dato oficial hallado es de 2019 (12 060 y 1 200). El padrón electoral (13 553 electores de pregrado) es solo un proxy.
5. **Número de programas de maestría y doctorado**, su modalidad (tiempo completo o parcial), sus costos y becas: no hay registro oficial consolidado. La cifra 57/10 viene de un sitio no oficial.
6. **Tasas de graduación, titulación y deserción**, y tiempo medio de egreso: no disponibles.
7. **Conciliación de docentes PTE (1 282) y AIRHSP (1 717)**, condición de los 297 docentes sin categoría, y grados actuales del cuerpo docente (último dato: 44 % con posgrado, 2017).
8. **Investigadores RENACYT** actuales: el último dato es de 2020 (90).
9. **Patentes UNI 2023–2025** (solicitudes y concesiones): no se halló la cifra; hay que consultar el tablero de INDECOPI.
10. **Acreditaciones vigentes**: no hay una lista con fechas de vigencia de ABET, RIBA, ICACIT ni del reconocimiento de SINEACE.
11. **Rankings Scimago SIR, THE y ShanghaiRanking**: no verificados (bloqueo de extracción).
12. **Conciliación de la producción científica**: la serie OpenAlex 2021–2025 (2 360 obras) y la ventana del cruce por facultad (1 862) no coinciden. Además no hay datos de docentes de las universidades pares, por lo que no se puede comparar la productividad por docente con ellas.
13. **Detalle de los pagos "otros"** de la planilla docente (concepto, base legal, producto asociado): el PTE los agrega.
14. **Planilla nominal enero–agosto de 2026**: los archivos `planilla-meses/2026-01` a `2026-08` están vacíos; solo hay agregados mensuales por régimen.
15. **Estado de la renovación del licenciamiento SUNEDU** (vence en noviembre de 2027) bajo el marco de la Ley 32105.
16. **Texto y metas del PEI 2025–2030** (RR 0557-2025-UNI): no se encontró publicado.
17. **Infraestructura**: inventario de edificios, aulas, laboratorios y m²; Plan Maestro; ocupación de ambientes (horarios × aforo); mantenimiento; cartera Invierte.pe por CUI con avance; obras en INFOBRAS; destino del terreno ex Metro UNI. Ninguno de estos datos es público o se halló.
18. **Innovación y alianzas**: número de startups incubadas o graduadas, licencias, spin-offs, ingresos por servicios tecnológicos, total de convenios internacionales vigentes y movilidad entrante y saliente.
19. **Vacantes 2026**: los totales (1 886 y 1 630) vienen de prensa; no se verificaron sumando los cuadros oficiales en PDF.
