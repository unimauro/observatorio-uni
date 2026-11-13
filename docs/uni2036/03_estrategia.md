# 3. Estrategia UNI 2036

> **Convenciones.** Montos en soles corrientes (S/) o millones de soles (S/ M). «Línea de base» = último dato público verificado en los archivos del Observatorio (`data/*.json` del repositorio `observatorio-uni`). Toda cifra que **no** sale de un dato publicado se marca **[S]** (supuesto) y se explica. «s/d» = sin dato público: que el dato no exista ya es un hallazgo, y publicarlo es una meta del plan.
> **Relación con el PEI vigente.** La UNI ya tiene un Plan Estratégico Institucional 2025–2030 (RR 0557-2025-UNI). UNI 2036 **no lo reemplaza**: lo extiende a 2036, le agrega metas cuantitativas verificables con datos públicos y propone que sus objetivos y metas a 2030 se incorporen al PEI en su próxima actualización y sirvan de base al PEI 2031–2036.
>
> El plan habla de **políticas e indicadores agregados** (institución, facultad, programa). No evalúa ni nombra a ninguna persona: la evaluación individual de docentes corresponde a los procesos formales de la universidad, con debido proceso y derecho a descargo.

## 3.0 Punto de partida: las cifras que ordenan la estrategia

| Dato | Valor | Fuente (archivo del repo → origen) |
|---|---|---|
| Producción acumulada (OpenAlex) | UNI **4 697** obras; San Marcos 44 113; PUCP 33 166 | `bibliometria.json` → OpenAlex (extraído 2026-06) |
| Obras UNI por año | 449 (2021) · 446 · 517 · 451 · **497 (2025)**: estancada desde 2021 (+2,6 %/año), tras multiplicarse por 4,4 entre 2015 (101) y 2021 (449) | `bibliometria.json` → `uni.by_year` |
| Calidad e impacto 2021–2025 (mismo filtro OpenAlex, 1 862 obras UNI) | En el 10 % más citado del mundo: **163 (8,8 %)** (PUCP 15,7 %; San Marcos 9,2 %); en el 1 % más citado: 11; con coautoría internacional: 777 (41,7 %); **con coautor de empresa: 5 (0,3 %)** (PUCP 42; San Marcos 48) | OpenAlex API, consulta 2026-11-12 (filtros `citation_normalized_percentile`, `countries_distinct_count`, `authorships.institutions.type:company`) |
| Perfil temático 2021–2025 | Ingeniería 486 obras; Ciencias Sociales 194; Ciencias Ambientales 181; Energía 128; Física 102; Materiales 100; Computación 99 | OpenAlex (`primary_topic.field`) |
| Docentes con al menos una publicación 2021–2025 | **336 de 1 282 = 26,2 %**; rango por facultad 14,5 % (FIIS) a 41,3 % (Ciencias) | `facultades-uni.json` (planilla PTE set-2026 × OpenAlex) |
| Docentes a tiempo completo | 724 de 1 282 = **56,5 %** | `facultades-uni.json` (suma `tiempo_completo`) |
| Planilla docente pagada como «otros» | S/ 2 454 780 de S/ 8 263 303 al mes = **29,7 %** | `planilla-uni.json` (PTE, setiembre 2026, 1 282 docentes) |
| PIM 2025 / devengado / ejecución | S/ 370,6 M / S/ 338,3 M / **91,3 %** | `presupuesto-uni.json` → MEF/SIAF |
| I+D (programa «Desarrollo de la CTI») | S/ 6,7 M = **1,8 % del PIM** 2025 | `bibliometria.json` → `presupuesto.idi` (MEF/SIAF) |
| Gasto de capital 2025 | PIM S/ 70,1 M; devengado S/ 46,4 M = **66,2 %**; **S/ 23,7 M de inversión autorizada no ejecutada** | `presupuesto-uni.json` → `por_categoria` |
| Personal y obligaciones sociales 2025 | PIM S/ 154,6 M (41,7 % del PIM) | `presupuesto-uni.json` → `por_generica` |
| Bienes y servicios 2025 | PIM S/ 118,5 M (32,0 % del PIM) | `presupuesto-uni.json` → `por_generica` |
| Concursos VRI 2022–2026 | **S/ 16 937 548** en 231 proyectos; 2025: S/ 4,61 M; 2026: S/ 3,41 M | `vri-proyectos.json`, `facultades-uni.json` → vri.uni.edu.pe |
| Concentración VRI | Ciencias S/ 5,73 M + Química y Textil S/ 2,77 M + Mecánica S/ 2,40 M = S/ 10,90 M = **64,3 %** del total (64,6 % de lo atribuido a facultad) | `facultades-uni.json` |
| Admisión 2025 (dos procesos) | 16 036 postulantes; 2 757 ingresantes; mujeres 16,7 % y 19,3 % de ingresantes | `admision-uni.json` → datosabiertos.gob.pe |
| Admisión 2026-I | 1 886 vacantes ofertadas; ≈ 6 000 postulantes | Diagnóstico (cap. 1), convocatoria oficial UNI |
| Oferta académica 2026 | 34 carreras en 11 facultades; recientes: Ciberseguridad (2022), Aeroespacial (2025), Biomédica, Inteligencia Artificial y Urbanismo (2026) | Diagnóstico (cap. 1); `admision-uni.json` |
| Acreditación | 19 programas acreditados por ABET desde 2017; Arquitectura con validación RIBA | Diagnóstico (cap. 1) |
| Licencia institucional | SUNEDU, RCD 073-2017-SUNEDU/CD (27-11-2017), 10 años → **renovación hacia noviembre de 2027** | Diagnóstico (cap. 1) |
| Posgrado financiado | Doctorado en Ciencias (Química y Física) con beca PROCIENCIA de S/ 6 500/mes × 36 meses, **76 plazas** (convocatoria 2024) | Diagnóstico (cap. 1); PROCIENCIA |
| Planificación vigente | PEI 2025–2030 (RR 0557-2025-UNI) | Diagnóstico (cap. 1) |
| QS World | 1201–1400 (ed. 2023) · 951–1000 (ed. 2024) · 1201–1400 (ed. 2025 y 2026) · **ausente de la edición 2027** | `bibliometria.json` → QS; diagnóstico (cap. 1) |
| Docentes RENACYT | 90 (cifra 2020) | `bibliometria.json` → CONCYTEC |
| Contrataciones adjudicadas 2023–2025 | S/ 86,6 M, 338 proveedores, 439 procesos; top-10 = 28,8 % del monto | `proveedores-uni.json` → OECE/CONOSCE |

Lectura en una línea: **la UNI no tiene principalmente un problema de dinero total; tiene un problema de asignación y de ejecución.** Gasta 1,8 % en I+D, deja sin ejecutar un tercio de su inversión, paga casi un tercio de la planilla docente como conceptos «otros» no vinculados públicamente a productos, y produce un orden de magnitud menos que sus pares nacionales.

---

## 3.1 Visión, misión-objetivo y objetivos estratégicos

**Visión 2036.** Ser, en 2036, la universidad que lidera la ingeniería y las ciencias aplicadas en el Perú, entre las diez primeras de Hispanoamérica en ingeniería y con nichos de clase mundial, en camino a liderar América Latina, con resultados públicos y verificables año a año (niveles de ambición y su costo en §3.6).

**Misión-objetivo.** Formar ingenieros, científicos y arquitectos de excelencia y generar investigación e innovación que resuelvan problemas del país, usando cada sol público con metas medibles y rendición de cuentas abierta.

**Objetivos estratégicos (OE)**

| # | Objetivo estratégico | Indicador ancla | Base | Meta 2036 |
|---|---|---|---|---|
| OE1 | Hacer de la investigación una función normal de la docencia | % docentes con producción verificable en 5 años | 26,2 % (2021–25) | 70 % |
| OE2 | Renovar y fortalecer el cuerpo docente con mérito y debido proceso | Docentes RENACYT | 90 (2020) | 450 |
| OE3 | Construir un posgrado de investigación a tiempo completo y financiado | Estudiantes de maestría/doctorado TC con beca | 76 plazas doctorales PROCIENCIA (2024) | 450 |
| OE4 | Formar mejor y a más diversidad de estudiantes, y graduarlos a tiempo | Titulación oportuna (≤ 6 años) | s/d | 60 % |
| OE5 | Una administración que ejecute: procesos, compras, inversión y datos | Ejecución de gasto de capital | 66,2 % (2025) | ≥ 95 % sostenido |
| OE6 | Más presupuesto, diversificado y ejecutado, para la ciencia | I+D total (programa CTI + fondos externos de investigación) / PIM | 1,8 % (2025, solo CTI) | 13,9 % (programa CTI propio ≥ 8 % del PIM base) |
| OE7 | Visibilidad y alianzas internacionales, transparencia como norma | QS World / datasets abiertos | ausente en ed. 2027 (1201–1400 en 2025–26) / s/d | ≤ 600 / 30 datasets |

### 3.1.1 Alineamiento con el marco nacional

Cada objetivo se ancla en una norma o política vigente, lo que sirve tanto para justificar la demanda presupuestal (§3.5) como para que la UNI rinda cuentas ante el sistema. *Dispositivos según el capítulo de referentes (`02_referentes_gestion.md`, B.1, B.6 y C.5). Recomendación operativa: cada meta del tablero debe indicar a qué objetivo prioritario de la PNESTP y de la POLCTI contribuye, porque eso condiciona el acceso a los incentivos por resultados del MINEDU y a las líneas que prioriza PROCIENCIA.*

| Marco | Qué exige o prioriza (resumen) | OE1 Investigación | OE2 Docentes | OE3 Posgrado | OE4 Estudiantes/carreras | OE5 Gestión/infraestructura | OE6 Financiamiento | OE7 Internac./transparencia |
|---|---|---|---|---|---|---|---|---|
| **PEI UNI 2025–2030** (RR 0557-2025-UNI) | Instrumento institucional vigente que UNI 2036 extiende | ● | ● | ● | ● | ● | ● | ● |
| **Ley 30220, Ley Universitaria** | Investigación como función esencial y obligatoria; docente investigador con bonificación del 50 % y carga lectiva reducida (art. 86); concurso público (art. 83) y ratificación periódica (art. 84); incubadoras de empresas y propiedad intelectual de la universidad | ● (función esencial) | ● (arts. 83, 84, 85, 86) | ● (escuela de posgrado) | ● (admisión, grados) | ● (transparencia, gestión) | ● (recursos propios, donaciones) | ● (portal de transparencia) |
| **Ley 31250, Sistema Nacional de CTI (SINACTI)**; reglamento DS 062-2024-PCM; DL 1727 (2026) | Universidades como actores del sistema rector (CONCYTEC); PROCIENCIA financia según las líneas priorizadas; reglas de integridad con sanciones (p. ej., compra de autorías); RENACYT | ● | ● (RENACYT) | ● | | | ● (PROCIENCIA) | ● |
| **Política Nacional de CTI al 2030 (POLCTI)**, DS 093-2025-PCM (reemplaza al DS 015-2016-PCM) | 6 objetivos prioritarios; meta país: estar entre los 60 más innovadores en 2030; formación de capital humano altamente calificado y fortalecimiento del SINACTI | ● | ● | ● (doctores) | | | ● | ● |
| **Política Nacional de Educación Superior y Técnico-Productiva (PNESTP)**, DS 012-2020-MINEDU; aplicada vía RVM 013-2022-MINEDU (incentivos por resultados) | OP5: acceso equitativo y tránsito entre opciones formativas; **OP6: asignación de recursos con énfasis en investigación e innovación y financiamiento por resultados** | ● | ● | ● | ● (acceso, permanencia, titulación) | ● (gestión) | ● | ● (información pública) |
| **Proyecto Educativo Nacional al 2036 «El reto de la ciudadanía plena»** (CNE, 2020) | Educación para la ciudadanía plena; equidad de género y territorial; formación docente; investigación al servicio del país | ● | ● | | ● (equidad, mujeres, regiones) | | | ● |
| **Visión del Perú al 2050** (Acuerdo Nacional, 2019, sesión 126) y **PEDN al 2050** (CEPLAN) — sucesores del Plan Bicentenario | Economía diversificada y basada en conocimiento, gestión sostenible del agua y de los recursos naturales, Estado eficiente y transparente | ● (áreas prioritarias: agua, minería, energía) | | ● | ● (carreras de futuro) | ● (Estado eficiente) | ● | ● (transparencia) |

Lectura: **OE1, OE3 y OE6** se justifican ante el MEF con la POLCTI al 2030, la Ley 31250 y el OP6 de la PNESTP (financiamiento por resultados con énfasis en I+D) (metas de investigadores y doctores); **OE2** se sostiene íntegramente en la Ley 30220 (arts. 83–86), lo que da base legal a la evaluación con consecuencias y a la bonificación del docente investigador; **OE4** responde a la Política de Educación Superior y al PEN 2036 (acceso equitativo, culminación oportuna); **OE5 y OE7** a la agenda de Estado eficiente y transparente de la Visión 2050.

---

## 3.2 Estrategias y tácticas

Escala de costo (gasto adicional anual en régimen): **B** = bajo (< S/ 1 M), **M** = medio (S/ 1–10 M), **A** = alto (> S/ 10 M). «Responsable» indica la unidad que debe liderar (o la que haga sus veces en el ROF vigente). Las metas cuantitativas se detallan en el tablero (§3.4).

### E1. Investigación e innovación (OE1, OE6)

| Táctica | Responsable | Inicio | Costo | KPI |
|---|---|---|---|---|
| 1.1 Carga lectiva diferenciada: quien tiene proyecto activo con financiamiento recibe hasta 50 % de horas de investigación; quien no, mantiene carga docente plena. Se publica la distribución agregada por facultad. | VRA + VRI + facultades | 2027 | B | % docentes con horas de investigación asignadas y producto en 3 años |
| 1.2 Reforma de los concursos VRI: bases únicas, evaluación por pares **externos** (al menos 2 por proyecto), resultados y puntajes publicados, informes finales en repositorio abierto. Mantener el mérito como criterio; añadir una línea de «arranque» para facultades con < 20 % de docentes con publicación (hoy FIIS 14,5 %, FIA 16,1 %, FAUA 16,2 %, FIGMM 18,3 %). | VRI | 2027 | M | Monto concursable anual; % proyectos con evaluación externa; % proyectos con producto a 24 meses |
| 1.3 Grupos de investigación reconocidos con financiamiento basal (S/ 50–150 mil/año [S]) condicionado a metas trienales. | VRI | 2028 | M | N.º de grupos activos; producción por grupo |
| 1.4 Red de laboratorios compartidos con reserva en línea, tarifario público y técnico especializado contratado; prioridad a equipos de > S/ 500 mil. | VRI + Dirección de Infraestructura | 2027 | M | Horas de uso / horas disponibles; ingresos por servicios |
| 1.5 Oficina de Transferencia Tecnológica (OTT): patentes INDECOPI, licencias, spin-offs, contratos con empresas con *overhead* institucional fijo (15–20 % [S]). | VRI | 2027 | M | Solicitudes de patente/año; contratos I+D+i (S/) |
| 1.6 Ventanilla única de proyectos: apoyo profesional para postular a PROCIENCIA, ProInnóvate, Horizonte Europa, BID, CAF, fondos de agencias y empresas. | VRI | 2026 | B | Fondos externos captados (S/); tasa de éxito |
| 1.7 Áreas prioritarias (5–6) alineadas a ventajas del país y de la UNI: minería y metalurgia sostenibles, agua y saneamiento, riesgo sísmico y construcción, energía y transición (incl. hidrógeno), computación/IA y datos, materiales. Las convocatorias reservan ≥ 50 % del fondo a estas áreas. | VRI + Consejo Universitario | 2027 | B | % fondo en áreas prioritarias; obras por área |
| 1.8 Afiliación institucional normalizada («Universidad Nacional de Ingeniería, Lima, Perú»), ORCID y CTI Vitae obligatorios para todo docente; repositorio institucional con depósito obligatorio. | VRI + Biblioteca | 2026 | B | % obras OpenAlex con afiliación UNI correcta; % docentes con ORCID |

#### E1-bis. Investigación de impacto en dos frentes: aplicada y básica

La UNI necesita ambas: la **básica/teórica** (física, matemática, química, materiales, computación teórica) produce el prestigio, las citas y los doctores; la **aplicada/práctica** (ingeniería sísmica, minería y metalurgia, agua, energía, software) produce las soluciones, los contratos y las patentes. Hoy la debilidad mayor está en la aplicada vinculada al sector productivo: solo **5 de 1 862** obras 2021–2025 tienen un coautor de empresa (0,3 %). Cada frente tiene su propio instrumento y sus propias metas; un docente no está obligado a ambos (véase E2-bis).

| Frente | Instrumento | Indicador | Base (2021–25 salvo indicación) | 2028 | 2031 | 2036 |
|---|---|---|---|---|---|---|
| Básica | Concurso VRI «ciencia de frontera» con pares internacionales; grupos basales (E1.3) | Obras en el 10 % más citado del mundo (ventana 5 años) | 163 (8,8 % del total) | 220 (10 %) | 450 (13 %) | 900 (16 %) [S] |
| Básica | Ídem | Obras en el 1 % más citado (ventana 5 años) | 11 | 15 | 30 | 50 [S] |
| Básica | Doctorados TC (E3) | Tesis doctorales defendidas/año | s/d | publicar base | 15 | 40 [S] |
| Aplicada | Fondo de proyectos con empresa (cofinanciamiento 1:1); OTT (E1.5) | Obras con coautor de empresa (ventana 5 años) | 5 | 20 | 60 | 150 [S] |
| Aplicada | OTT, laboratorios acreditados | Contratos I+D+i y servicios tecnológicos (S/ M/año) | s/d (supuesto 1,0) | 4 | 10 | 25 |
| Aplicada | OTT | Solicitudes de patente/modelo de utilidad en INDECOPI por año | s/d | 10 | 20 | 40 [S] |
| Aplicada | Retos-país (agua, sismos, minería, energía) con el Estado | Obras en áreas prioritarias con aplicación declarada (p. ej., ODS 6 agua) | 130 obras ODS 6 (OpenAlex) | 180 | 260 | 400 [S] |
| Ambas | Coautoría internacional (E9) | % obras con coautor de otro país | 41,7 % | 45 % | 50 % | 55 % |

Regla de asignación: del fondo concursable del VRI, ≈ 40 % a básica, ≈ 40 % a aplicada con socio externo y ≈ 20 % a líneas de arranque y equipamiento [S], revisable cada 3 años según resultados.

### E2. Docentes: mérito, evaluación con consecuencias y retención del talento (OE2)

*Política institucional. El plan no identifica ni enumera personas; los resultados se publican solo en agregados por facultad o categoría.*

| Táctica | Responsable | Inicio | Costo | KPI |
|---|---|---|---|---|
| 2.1 **Evaluación anual integral** de todo docente con rúbrica pública que pondera docencia (encuestas, resultados de aprendizaje), investigación, asesoría de tesis, extensión y gestión. No solo *papers*: el peso de cada dimensión se ajusta al régimen de dedicación. | VRA + Comisión de Evaluación (con miembros externos) | 2027 (piloto 2026) | B | % docentes evaluados; distribución agregada de resultados por facultad |
| 2.2 **Consecuencias con debido proceso**: resultado insuficiente → plan de mejora de 12 meses con apoyo (mentoría, capacitación); dos evaluaciones insuficientes consecutivas → se activa el procedimiento de no ratificación o no renovación previsto en la Ley 30220 (art. 84), con notificación, descargo e instancia de apelación. | VRA + Consejo Universitario + Asesoría Legal | 2028 | B | N.º de planes de mejora y % que mejoran (agregado); % ratificaciones con evaluación documentada |
| 2.3 **Pago por resultados**: los conceptos «otros» de la planilla docente (29,7 % hoy) se mantienen solo contra productos verificables (examen de admisión, CEPRE, proyectos, cursos de extensión) con registro público agregado; reconvertir progresivamente 30 % de ese monto (≈ S/ 8,8 M/año [S]) a incentivos por desempeño y bonificación RENACYT. | Dirección de RR.HH. + OPP | 2027 | B (reasignación) | % planilla docente en «otros» sin producto asociado |
| 2.4 **Retención de los mejores**: bonificación del 50 % al docente investigador (Ley 30220, art. 86) aplicada efectivamente a todo docente RENACYT que cumpla metas; fondo de inicio (*start-up*) para nuevos doctores; año sabático con plan de producción. | VRI + RR.HH. | 2027 | A | Docentes RENACYT; tasa de salida voluntaria de docentes RENACYT |
| 2.5 **Contratación de doctores**: concursos públicos (art. 83) con requisito de doctorado y producción para nuevas plazas, jurados con ≥ 1 miembro externo, convocatoria internacional y difusión en redes de la diáspora; 15 plazas netas nuevas/año [S] además de la reposición. | VRA + facultades | 2027 | A | % de plazas nuevas cubiertas por doctores; % docentes con doctorado |
| 2.6 **Reposición ordenada**: toda plaza liberada por cese (incl. límite de edad legal) se convoca en ≤ 6 meses con el perfil del plan de la facultad, no se pierde. | RR.HH. + OPP | 2026 | B | Meses promedio entre cese y nueva convocatoria |
| 2.7 **Dedicación**: subir docentes a tiempo completo (56,5 % hoy) priorizando áreas con déficit; incompatibilidades y declaraciones de otras actividades remuneradas publicadas en agregado. | VRA | 2027 | M | % docentes TC |
| 2.8 Repatriación y posdoctorados: 10–20 posdocs/año [S] financiados con PROCIENCIA y fondos propios. | VRI | 2028 | M | Posdocs activos |

#### E2-bis. Tres trayectorias docentes: docencia, investigación e innovación-transferencia

No todos los docentes tienen que hacer lo mismo, pero todos tienen que rendir cuentas por algo medible. Cada docente ordinario elige (con aprobación de su departamento y según las necesidades del plan de la facultad) una trayectoria por un **período de 3 años**, renovable o cambiable al final del período. La Ley 30220 ya da la base: regímenes de dedicación (art. 85), docente investigador con carga lectiva reducida y bonificación (art. 86), ratificación periódica (art. 84).

| | **Docencia** | **Investigación** | **Innovación y transferencia** |
|---|---|---|---|
| Para quién | Excelencia en enseñanza, cursos de ciencias básicas y de especialidad, laboratorios docentes | Producción científica de calidad y formación de doctores | Proyectos con empresas y Estado, patentes, spin-offs, servicios tecnológicos |
| Dedicación | TC o TP; carga lectiva alta (≥ 16 h/semana TC [S]) | Dedicación exclusiva o TC; carga lectiva mínima de ley (docente investigador: art. 86) a 8 h/semana [S] | TC; carga lectiva media (≈ 10–12 h/semana [S]); actividad externa autorizada dentro de las incompatibilidades legales |
| Pesos de la evaluación anual (E2.1) [S] | Docencia 70 % · formación y materiales 15 % · gestión 15 % | Investigación 60 % · docencia 25 % · gestión 15 % | Transferencia 55 % · docencia 30 % · gestión 15 % |
| Productos que cuentan | Encuestas y resultados de aprendizaje, innovación pedagógica, tutoría, asesoría de tesis de pregrado, textos y materiales abiertos | Artículos indexados (calidad, no solo número), proyectos con fondos externos, tesistas de maestría y doctorado, RENACYT | Contratos (S/), patentes y licencias, prototipos validados, empresas creadas, practicantes formados en proyectos |
| Reglas de pago (además de la remuneración por categoría) | Incentivo anual a la excelencia docente para el decil superior de cada facultad, condicionado a evaluación [S] | Bono de docente investigador (art. 86; monto fijado por DS anual) mientras se mantengan RENACYT y metas; fondo de inicio para nuevos doctores | Participación en regalías y en el *overhead* de los contratos (véase E10), dentro de los límites legales y con declaración de conflicto de interés |
| Meta de composición 2036 [S] | ≈ 45 % | ≈ 35 % | ≈ 20 % |
| Consecuencia si no cumple | Plan de mejora (E2.2) → no ratificación con debido proceso | Vuelve a la trayectoria docencia en el siguiente período (pierde la bonificación); si tampoco cumple allí, E2.2 | Ídem |

**Viabilidad normativa** (cap. 2, B.6 y C.1): la trayectoria de **investigación ya existe** (docente investigador, art. 86; reglamento UNI RR 1042-2020; bono fijado por decreto supremo anual, para 2026 hasta S/ 4 434/mes según DS 028-2026-EF [cifra a confirmar]); la de **docencia** solo requiere estatuto y reglamento de evaluación con pesos distintos (la categoría no cambia); la de **innovación** es viable en parte: patentes, contratos y startups pueden contar como mérito, pero una **licencia larga para emprender conservando la plaza** y la tenencia de acciones de un docente en una empresa que contrata con la UNI **requieren norma con rango de ley** (p. ej., en la Ley 31250 o una ley de transferencia tecnológica) [a validar con SERVIR y Contraloría].

Salvaguardas: piso mínimo de docencia para todas las trayectorias (todos enseñan); cambio de trayectoria sin pérdida de categoría; publicación solo del número de docentes por trayectoria y facultad, nunca de nombres; revisión de los pesos por el comité de seguimiento (§3.9) a los 3 años.

### E3. Posgrado de investigación a tiempo completo (OE3)

| Táctica | Responsable | Inicio | Costo | KPI |
|---|---|---|---|---|
| 3.1 Reconvertir la Escuela Central de Posgrado: separar maestrías profesionales (autofinanciadas) de maestrías y doctorados **de investigación a tiempo completo**, ligados a grupos de investigación (E1.3). | Escuela de Posgrado + VRA | 2027 | B | N.º de programas de investigación; matrícula TC |
| 3.2 Becas con estipendio, **partiendo de lo que ya existe**: el Doctorado en Ciencias (Química y Física) tiene 76 plazas con beca PROCIENCIA de S/ 6 500/mes × 36 meses (2024). Extender ese modelo a ingeniería: doctorado S/ 6 500/mes × 36–48 meses (estándar PROCIENCIA) y maestría de investigación S/ 2 500/mes × 24 meses [S]. Stock objetivo (maestría/doctorado): 50/100 (2028), 150/150 (2031), 250/200 (2036). Costo en régimen ≈ S/ 16,2 M (2031) y S/ 23,1 M (2036) [S], ≈ 60 % cofinanciado por PROCIENCIA [S]; el resto dentro de la meta de I+D. | VRI + Posgrado | 2027 | A | Becarios activos; titulación en plazo |
| 3.3 Cofinanciamiento con PROCIENCIA (programas de doctorado), empresas (doctorado industrial) y convenios de co-tutela/doble grado. | Posgrado + OTT | 2027 | M | % becas cofinanciadas externamente |
| 3.4 Ejecutar el devengado del posgrado: en 2025 la meta presupuestal «Escuela De Postgrado» tuvo PIM S/ 4,57 M y **devengado S/ 0** (`presupuesto-uni.json`, por_facultad). Primera tarea: explicar y corregir esa inejecución. | Posgrado + OPP | 2026 | B | Ejecución del presupuesto de posgrado |
| 3.5 Acreditación internacional de los doctorados (p. ej., estándares SINEACE/ARCU-SUR o agencias equivalentes). | Posgrado | 2030 | M | Programas acreditados |
| 3.6 Mantener y extender la acreditación de pregrado: hoy 19 programas con ABET (desde 2017) y Arquitectura con RIBA; meta: todas las ingenierías acreditadas (ABET o ICACIT) antes de 2031, incluidas las carreras creadas desde 2022. | VRA + Oficina de Calidad | 2026 | M | Programas acreditados / programas con egresados |

### E4. Evaluación de carreras actuales y creación de carreras nuevas (OE4)

La UNI ofrece **34 carreras en 11 facultades** (2026) y asignó vacantes a las 34 en el proceso 2026-1 (`admision-uni.json`). La oferta ya se renovó: **Ciberseguridad (2022), Aeroespacial (2025), Biomédica, Inteligencia Artificial y Urbanismo (2026)**. La prioridad no es crear más carreras sino **evaluar estas cinco con la táctica 4.1** antes de su primera cohorte de egresados, y revisar las de demanda muy baja en ese proceso (Higiene y Seguridad Industrial: 5 ingresantes; Química: 7; Petroquímica: 8; Petróleo y Gas Natural: 9; Textil: 11). Un solo proceso no basta para concluir: la evaluación debe usar la serie completa.

| Táctica | Responsable | Inicio | Costo | KPI |
|---|---|---|---|---|
| 4.0 **Licencia SUNEDU**: la licencia institucional (RCD 073-2017-SUNEDU/CD, 27-11-2017, 10 años) vence hacia noviembre de 2027; preparar la renovación en 2026–2027 usando la línea de base y el tablero de este plan como evidencia. Toda carrera o mención nueva requiere además modificación de licencia (art. 40 de la Ley 30220). | Rectorado + Oficina de Calidad + OPP | 2026 | B | Licencia renovada a tiempo |
| 4.1 **Evaluación quinquenal de cada carrera** con un tablero de 6 criterios: (a) demanda (postulantes por vacante, serie ≥ 5 años); (b) calidad de ingreso (puntaje mínimo y medio); (c) retención al 2.º año y titulación oportuna; (d) empleabilidad y salario de egresados (MTPE «Ponte en Carrera», SUNEDU); (e) costo por egresado (planilla + bienes y servicios por facultad, MEF/SIAF); (f) investigación asociada. | VRA + Oficina de Calidad | 2027 | B | % carreras evaluadas y publicadas |
| 4.2 Reglas de decisión explícitas: si una carrera cae en el cuartil inferior en ≥ 3 criterios por 2 ciclos de evaluación → rediseño curricular, fusión en un tronco común o cierre de admisión, decidido por el Consejo Universitario con informe público. Nunca se afecta a los estudiantes matriculados. | Consejo Universitario | 2029 | B | N.º de carreras rediseñadas/fusionadas |
| 4.3 **Criterios para crear carreras nuevas**: estudio de demanda laboral, ≥ 60 % de docentes del núcleo con doctorado, laboratorio financiado, plan de 10 años y evaluación a los 5. Ruta preferida: **mención o maestría primero, carrera después** (véase la matriz de carreras de futuro abajo). | VRA + facultades | 2028 | M | Carreras nuevas con plan aprobado y evaluadas a 5 años |
| 4.4 Primer año común de ciencias básicas e ingeniería (matemática, física, química, programación) para facilitar la elección y la movilidad entre especialidades. | VRA + Facultad de Ciencias | 2029 | M | Retención al 2.º año |

#### E4-bis. Carreras de futuro: matriz de decisión

**Criterios y pesos [S]** (puntaje 1–5 cada uno; se aprueba una carrera nueva con ≥ 3,5 ponderado y ningún criterio < 2):

| Criterio | Peso | Cómo se mide |
|---|---|---|
| C1 Demanda laboral y salarial a 10 años | 20 % | MTPE, gremios, estudios sectoriales; vacantes publicadas |
| C2 Prioridad nacional | 15 % | Política Nacional de CTI, PEDN 2050, cartera de inversión pública y minera |
| C3 Capacidad docente propia | 20 % | Doctores en el área y producción OpenAlex 2021–25 de la UNI en el campo |
| C4 Ventaja diferencial de la UNI | 15 % | Laboratorios existentes, carreras afines, ubicación, alianzas |
| C5 Costo por egresado y financiamiento identificado | 15 % | Planilla + equipamiento; fuente asegurada por 10 años |
| C6 Demanda estudiantil | 10 % | Postulantes por vacante en carreras afines (`admision-uni.json`) |
| C7 Socio internacional | 5 % | Convenio de doble grado o laboratorio conjunto (E9) |

**Secuencia obligatoria** (cap. 2, R24): etapa 1 (2027–2029) menciones y especializaciones dentro de carreras existentes; etapa 2 (2028–2031) maestrías y doctorados con socios internacionales (p. ej., Escuela Doctoral Franco-Peruana); etapa 3 (2031–2036) pregrado nuevo solo si la matriz lo justifica. Órdenes de costo: mención S/ 0,2–0,5 M; maestría S/ 1–2 M en 3 años; pregrado S/ 5–10 M en 5 años.

**Aplicación preliminar** (orientativa; la valoración final corresponde a la comisión de la táctica 4.1):

| Área | Situación en la UNI hoy | Ruta propuesta | Fase | Base de la UNI en que se apoya |
|---|---|---|---|---|
| IA y ciencia de datos | Ya existen Ing. de Inteligencia Artificial (creada 2026; 19 ingresantes 2026-1), Ciencia de la Computación (15) y Estadística (36) | Evaluar y consolidar; no crear otra carrera; maestría TC en IA aplicada | 1 | Computación 99 obras 2021–25 |
| Ciberseguridad | Existe desde 2022 (26 ingresantes 2026-1) | Evaluar en 2027–2028, antes de su primera promoción completa, con el criterio de 4.1 | 1 | Sistemas, Telecomunicaciones |
| Espacio | Existe Ing. Aeroespacial desde 2025 (24 ingresantes 2026-1) | Evaluar; laboratorio conjunto con agencia espacial nacional y socio extranjero | 2 | Mecánica, Electrónica |
| Semiconductores y microelectrónica | No existe | Mención en Ing. Electrónica + maestría; carrera solo si C1 y C4 lo justifican tras 5 años | 2 | Electrónica, Ing. Física, Materiales (100 obras) |
| Robótica y automatización | Base en Mecatrónica (42 ingresantes 2026-1) | Mención en Mecatrónica; laboratorio compartido de robótica | 1 | Mecatrónica, Mecánica |
| Cuántica | No existe | Línea de investigación y maestría/doctorado en Física e Ing. Física; no carrera de pregrado | 2–3 | Física 102 obras 2021–25 |
| Biotecnología y bioingeniería | Existe Ing. Biomédica desde 2026 (26 ingresantes 2026-1) | Ing. Bioquímica/Biotecnología industrial como mención de Química; evaluar carrera en 2031 | 2 | Química y Textil (39,3 % docentes publican) |
| Transición energética e hidrógeno | No existe como carrera | **Candidata fuerte**: mención en energía y almacenamiento y maestría; pregrado de Ing. de Energía solo en etapa 3, a partir de Mecánica-Eléctrica, Petróleo y Química | 2 | Energía 128 obras; proyectos VRI de hidrógeno 2026 |
| Minerales críticos (litio, cobre) y metalurgia sostenible | Existen Minas, Metalurgia y Geología | Mención «minerales críticos y metalurgia extractiva» y doctorado con industria; no carrera nueva | 1 | FIGMM; prioridad nacional |
| Clima y agua | Existen Ing. Sanitaria (14), Ambiental (16) y Urbanismo (creada 2026) | **Candidata fuerte**: primero mención y maestría en Recursos Hídricos y Clima (Civil, Sanitaria, Ambiental); pregrado solo en etapa 3 | 2 | Ciencias Ambientales 181 obras; ODS 6: 130 obras |

Regla general: **no abrir una carrera nueva sin cerrar, fusionar o rediseñar al menos otra de baja demanda** cuando la planta docente no crece en la misma proporción.

### E5. Estudiantes: admisión, retención y graduación (OE4)

| Táctica | Responsable | Inicio | Costo | KPI |
|---|---|---|---|---|
| 5.1 Admisión: publicar microdatos anonimizados de cada proceso (ya existen 2021–2026 en datosabiertos.gob.pe) y estudios de validez predictiva del examen (puntaje vs rendimiento a 2 años). | Dirección de Admisión | 2026 | B | Estudio publicado; correlación puntaje–rendimiento |
| 5.2 Equidad: programa de captación en regiones y colegios públicos, sedes CEPRE descentralizadas (ya opera en Juliaca) y meta de mujeres ingresantes (16,8 % en 2026-1 → 33 % en 2036). | Admisión + CEPRE-UNI | 2027 | M | % mujeres ingresantes; % ingresantes de colegio público y de regiones |
| 5.3 Sistema de alerta temprana: tutoría obligatoria en el primer año, nivelación en matemática/física, seguimiento de cursos con alta desaprobación (datos por curso publicados en agregado). | VRA + facultades | 2027 | M | Retención al 2.º año; desaprobación en cursos críticos |
| 5.4 Graduación oportuna: titulación por proyecto/tesis integrada al último año, asesoría reconocida en la carga docente, plazos máximos de dictamen. | VRA + facultades | 2027 | B | Titulación ≤ 6 años; tiempo medio a la titulación |
| 5.5 Bienestar: becas de alimentación, residencia y salud mental proporcionales a la vulnerabilidad. | Dirección de Bienestar | 2027 | M | Deserción por motivos económicos |
| 5.6 Seguimiento de egresados: encuesta anual y cruce con planillas electrónicas (MTPE) en agregados. | Oficina de Egresados | 2027 | B | Empleo formal y salario a 1 y 5 años |

### E6. Administración remodelada (OE5)

| Táctica | Responsable | Inicio | Costo | KPI |
|---|---|---|---|---|
| 6.1 **Mapeo y rediseño de los 30 procesos críticos** (matrícula, contrataciones, pagos a investigadores, viajes, compras de equipos, grados y títulos) con tiempos objetivo publicados. | Dirección General de Administración (DIGA) + OPP | 2026 | M | Días promedio por proceso crítico |
| 6.2 **Compras**: plan anual de contrataciones publicado y cumplido; compras consolidadas y subasta inversa para bienes comunes; acuerdos marco de Perú Compras; unidad especializada en compras científicas (equipos e importaciones). Monitoreo de concentración (top-10 proveedores = 28,8 % del monto adjudicado 2023–2025). | DIGA – Logística | 2026 | B | Días de la requisición a la orden; % del PAC ejecutado; concentración top-10 |
| 6.3 **Digitalización**: cero papel en trámites internos, expediente electrónico, firma digital, sistema académico y de investigación integrados con SIAF/SIGA. | Oficina de TI | 2026 | M | % trámites digitales; tiempo de trámite |
| 6.4 **PMO de inversiones** (oficina de gestión de proyectos): cartera única priorizada en Invierte.pe, cronogramas públicos y seguimiento mensual del devengado de cada proyecto. | OPP + Dirección de Infraestructura | 2026 | B | Ejecución de gasto de capital |
| 6.5 **Unidad de datos e inteligencia institucional**: un solo almacén de datos académicos, de personal, presupuesto e investigación; publica los indicadores de este plan en datos abiertos cada semestre. | Rectorado + Oficina de TI | 2026 | B | Datasets abiertos publicados; puntualidad del reporte |
| 6.6 Perfiles por competencias y meritocracia (Ley Servir) para el personal administrativo; capacitación en compras públicas, inversión y datos. La relación personal no docente/docente (0,66 en la planilla nominal del PTE, 848 / 1 282) se gestiona por perfiles, no por recortes lineales. | RR.HH. | 2027 | M | % puestos con perfil; horas de capacitación |

### E7. Infraestructura e inversión: ejecutar lo que ya está (OE5)

| Táctica | Responsable | Inicio | Costo | KPI |
|---|---|---|---|---|
| 7.1 Plan de choque de ejecución: los S/ 23,7 M de capital no ejecutados en 2025 equivalen a 3,5 años del I+D actual. Comité semanal de inversión; metas trimestrales de devengado por proyecto. | PMO (E6.4) | 2026 | B | Ejecución capital: 80 % (2027), 85 % (2028), 95 % (2031) |
| 7.2 Plan Maestro de Infraestructura 2036: laboratorios, aulas, residencia, red eléctrica y de datos del campus; mantenimiento preventivo con presupuesto propio (≥ 2 % del valor del activo [S]). | Dirección de Infraestructura | 2027 | A | Proyectos del plan maestro concluidos |
| 7.3 **Obras por impuestos** (Ley 29230): cartera de 3–5 proyectos con empresas, S/ 15 M en 2028 y S/ 25 M/año desde 2029 [S]. Ojo: para una entidad del Gobierno Nacional el CIPGN se repaga con presupuesto de la propia entidad; OxI **acelera la ejecución, no es dinero nuevo**. | OPP + PMO | 2027 | — | Monto adjudicado y ejecutado vía OxI |
| 7.4 Equipamiento científico concursable con planes de uso compartido (E1.4) y contratos de mantenimiento incluidos en la compra. | VRI + DIGA | 2027 | M | % equipos > S/ 500 mil con contrato de mantenimiento y registro de uso |
| 7.5 **Auditoría anual de uso de espacios** con método estándar: inventario de todos los ambientes (m², capacidad, facultad) y medición durante 2 semanas por semestre de **frecuencia** (% de horas disponibles en que el espacio se usa) y **ocupación** (% de asientos usados cuando se usa); **utilización = frecuencia × ocupación** (método del Reino Unido, HESA/AUDE). Publicación por edificio y facultad. Costo: S/ 0,3–0,6 M la primera y S/ 0,1–0,2 M/año después (cap. 2, R21). | Dirección de Infraestructura + Unidad de datos | 2026–2027 | B | % de espacios auditados; frecuencia, ocupación y **utilización** |
| 7.6 **Primero terminar y usar, después construir**: moratoria de edificios nuevos (salvo seguridad estructural o compromisos firmados) mientras la utilización de aulas esté por debajo de 35 % o la frecuencia por debajo de 70 % [S, referente Bristol]; prioridad presupuestal a concluir obras inconclusas, equipar y poner en operación lo existente. | Consejo Universitario + PMO | 2027 | — (libera inversión) | Obras inconclusas concluidas; m² nuevos vs m² reactivados |
| 7.7 **Reúso de espacios ociosos**: (a) laboratorios compartidos de investigación (E1.4); (b) incubadora y espacio para spin-offs (E10); (c) laboratorios conjuntos con socios internacionales (E9); (d) **cesión en uso o arrendamiento a empresas e instituciones** para I+D, laboratorios de ensayo o formación — la UNI **ya arrienda** espacios del Sector V del campus por convocatoria pública (RR 3664-2024) —, bajo la Directiva DIR-00004-2022/SBN (Ley 29151), la Ley 30220 y la Ley 32141 (recursos directamente recaudados; alcance sobre alquileres a verificar), con convenio de colaboración académica (pasantías, proyectos, tesis), con tarifa pública, plazo limitado, prioridad a socios que co-investiguen y ingresos destinados a mantenimiento e I+D. | DIGA + OTT + Asesoría Legal | 2028 | B | m² reasignados; ingresos por uso de espacios (S/) |
| 7.8 Programación central de aulas (todas las facultades comparten una sola bolsa de aulas y horarios; se puede disponer por resolución rectoral) para subir la utilización sin construir; parte de lo ahorrado o recaudado vuelve a la facultad que cede espacio. | VRA + Unidad de datos | 2027 | B | Frecuencia y utilización de aulas en horario 8–20 h |

> **Hipótesis del propietario, no verificada.** El promotor del plan sostiene que la UNI tiene muchos edificios con **ocupación inferior al 40 %**. El Observatorio **no** tiene datos que lo confirmen ni lo refuten: no existe un inventario público de uso de espacios. Además, la cifra **depende de qué se mida**: si se refiere a *utilización* (frecuencia × ocupación), < 40 % **no sería atípico** — la meta de referencia en el Reino Unido es 35 % (Bristol: 70 % de frecuencia × 50 % de ocupación) y las aulas británicas se usan en promedio ≈ 20 % del tiempo (Times Higher Education); si se refiere solo a *frecuencia*, sí sería baja. Por eso el plan (1) define el indicador con precisión (frecuencia, ocupación y utilización por separado), (2) ordena la auditoría 7.5 en 2026–2027, (3) publica la línea de base real y (4) fija metas sobre lo medido: **utilización de aulas ≥ 35 % y frecuencia ≥ 70 % en 2029** [S, referente Bristol], ≥ 40 % de utilización en 2036. Fuentes del método: cap. 2, sección C.2.

### E8. Financiamiento (OE6)

| Táctica | Responsable | Inicio | Costo | KPI |
|---|---|---|---|---|
| 8.0 **Aumentar el presupuesto, explícitamente.** La reforma no cabe en el presupuesto inercial. Meta de PIM: S/ 413 M (2028), S/ 485 M (2031), S/ 617 M (2036), es decir **4,7 %/año nominal frente a 2,5 % inercial**, con tres fuentes: recursos ordinarios adicionales (demanda al MEF de S/ 4,3 M en 2028, S/ 22,6 M en 2031 y S/ 53,2 M en 2036), fondos externos y RDR incrementales (S/ 9,5 M, 33,0 M y 77,1 M), y reasignación interna (que no aumenta el PIM). Trayectoria año por año en §3.5. La demanda se presenta cada año en la fase de programación multianual con metas físicas y con la evidencia del tablero. | Rectorado + OPP | 2026 (programación 2027–2029) | — | PIM anual vs trayectoria; RO adicional aprobado |
| 8.1 **Programa presupuestal de I+D** negociado con el MEF con metas físicas (publicaciones, patentes, posgraduados): sustento técnico para el incremento de recursos ordinarios que calcula §3.5. | OPP + VRI | 2027 | B | I+D / PIM |
| 8.2 **Canon**: la UNI está en Lima y no es receptora natural de canon minero/gasífero (el canon se distribuye a universidades de la región productora). Táctica: convenios con gobiernos regionales y universidades receptoras de canon para proyectos conjuntos ejecutados con sus recursos. Verificar en SIAF las fuentes de financiamiento del pliego (el campo `por_fuente` está vacío en el repo). | VRI + OPP | 2027 | B | S/ ejecutados en convenios con recursos de canon |
| 8.3 **PROCIENCIA / ProInnóvate / fondos internacionales**: meta de captación S/ 12 M (2028), S/ 30 M (2031), S/ 60 M (2036) [S]. | VRI (E1.6) | 2026 | B | Fondos externos captados |
| 8.4 **Contratos con la industria** (servicios tecnológicos, I+D por encargo, laboratorios acreditados): S/ 4 M (2028), S/ 10 M (2031), S/ 25 M (2036) [S] en recursos directamente recaudados (RDR). | OTT | 2027 | B | RDR por I+D+i |
| 8.5 **RDR**: tarifas con estructura de costos pública para posgrado profesional, extensión y CEPRE; un % fijo del RDR de cada unidad va al fondo de investigación [S: 10 %]. | OPP | 2027 | B | RDR total y % destinado a I+D |
| 8.6 **Donaciones y fondo patrimonial (endowment)**: fundación o patronato con gobierno independiente; capital semilla S/ 10 M en 2029 y S/ 5 M/año después [S]; solo se gasta el 4 % anual. Cátedras con nombre de exalumnos y empresas. | Rectorado + Oficina de Egresados | 2028 | B | Capital del fondo; donaciones/año |
| 8.7 **Eficiencia en bienes y servicios**: 3 % (2028) a 5 % (2031) de ahorro sobre S/ 118,5 M [S] por compras consolidadas y digitalización, reasignado a I+D. | DIGA | 2027 | B | S/ ahorrados y reasignados |

### E9. Internacionalización y rankings (OE7)

| Táctica | Responsable | Inicio | Costo | KPI |
|---|---|---|---|---|
| 9.1 Estrategia de rankings basada en fundamentos (producción, citas, reputación, internacionalización), no en «maquillaje»: corregir la afiliación (E1.8) y reportar datos completos a QS/THE/SCImago. | Unidad de datos + Relaciones Internacionales | 2026 | B | QS World; QS by Subject Engineering; SCImago |
| 9.2 Movilidad: 5 % de estudiantes de pregrado con experiencia internacional en 2036 [S]; profesores visitantes con financiamiento compartido. | Relaciones Internacionales | 2027 | M | Estudiantes en movilidad |
| 9.3 Doble grado y co-tutela con 10 universidades líderes de la región y fuera de ella. | Posgrado + RR.II. | 2028 | B | Convenios activos con estudiantes |
| 9.4 Coautoría internacional: incentivos a proyectos con socios extranjeros (bonus en concursos VRI). | VRI | 2027 | B | % obras con coautor internacional (OpenAlex): 41,7 % → 55 % |
| 9.5 **Socio ancla estratégico (modelo tipo MIT/KAIST)**: 1–2 alianzas de 10 años con universidades técnicas de primer nivel: co-diseño curricular, programa doctoral conjunto, estancias de docentes, fondos semilla bilaterales y un laboratorio conjunto. Se elige por complementariedad con las áreas prioritarias (E1.7), no por marca. | Rectorado + RR.II. | 2027 (firma 2028) | M | Alianza firmada; doctorandos y obras conjuntas |
| 9.6 **Laboratorios conjuntos internacionales** (3 a 2031, 6 a 2036 [S]) en agua y clima andino, ingeniería sísmica, minería/metalurgia sostenible y energía/hidrógeno, cofinanciados por el socio y por PROCIENCIA. | VRI | 2028 | M | Laboratorios conjuntos activos; fondos captados |
| 9.7 **Ventanilla de fondos internacionales** (dentro de E1.6): Horizonte Europa (participación como socio en consorcios; elegibilidad de financiamiento a verificar por convocatoria), Erasmus+ (movilidad y desarrollo de capacidades), Fulbright y becas de gobiernos extranjeros para docentes y doctorandos, y proyectos con socios de EE. UU. financiados por NSF a la contraparte estadounidense. | VRI + RR.II. | 2026 | B | Propuestas presentadas/ganadas por programa |
| 9.8 **Doble grado y co-tutela**: 10 convenios activos con estudiantes a 2031, 20 a 2036 [S]. | Posgrado + RR.II. | 2028 | B | Convenios con estudiantes inscritos |

### E10. Emprendimiento de base tecnológica y propiedad intelectual (OE1, OE6)

| Táctica | Responsable | Inicio | Costo | KPI |
|---|---|---|---|---|
| 10.1 **Startup UNI 2.0**: fortalecer la incubadora existente (Startup UNI, ya integrada a la red de incubadoras de ProInnóvate) en espacios reactivados (E7.7), con mentoría de egresados y empresas; meta ≥ 15 startups/año postulando a StartUp Perú; suspensión de estudios para emprender sin perder la matrícula (reglamento académico); alianza con fondos existentes en vez de competir con ellos. Costo S/ 1–2 M/año cofinanciado con ProInnóvate (cap. 2, R26). | VRI + OTT | 2027 | M | Startups incubadas/año; supervivencia a 3 años; fondos captados |
| 10.2 **Política de spin-offs**: permite a docentes y estudiantes crear empresas a partir de resultados UNI, mediante licencia con regalías o participación. **Que una universidad pública tenga acciones en una empresa privada no tiene un régimen claro** y probablemente requiera norma habilitante o un vehículo intermedio (fundación o asociación sin fines de lucro) [riesgo legal alto, validar antes de 2028]; si se habilita, topes publicados: 5–10 % (software) o 10–20 % (PI dura). Licencia larga del docente fundador conservando la plaza: requiere ley (E2-bis). Reglas de conflicto de interés. | Consejo Universitario + OTT + Asesoría Legal | 2027 | B | Spin-offs creadas (5 activas en 2033) |
| 10.3 **Política de propiedad intelectual y regalías**: titularidad institucional de lo creado con recursos UNI, reparto de regalías netas publicado de antemano (propuesta: un tercio inventores, un tercio unidad/laboratorio, un tercio fondo central de I+D [S]; alternativa de referencia 40/20/40, modelo Nottingham, cap. 2 R25); plazos máximos de respuesta de la OTT; registro ágil ante INDECOPI con presupuesto para protección y vigilancia tecnológica. | OTT + Asesoría Legal | 2027 | B | Solicitudes de patente; licencias firmadas; regalías (S/) |
| 10.4 **Fondo de capital semilla con egresados** (*venture fund*): vehículo privado separado de la universidad, aportes de exalumnos y empresas, co-inversión con instrumentos de StartUp Perú/ProInnóvate; la UNI aporta *deal flow*, no capital público. | Patronato/fundación (E8.6) | 2029 | — (privado) | Capital comprometido; inversiones realizadas |
| 10.5 Cursos de emprendimiento e innovación con créditos en todas las carreras y proyecto final con empresa o startup como opción de titulación. | VRA | 2028 | B | Estudiantes en proyectos con empresa/startup |

### E11. Transparencia como motor (OE7)

| Táctica | Responsable | Inicio | Costo | KPI |
|---|---|---|---|---|
| 11.1 Portal de datos abiertos de la UNI: presupuesto por facultad, concursos VRI (ganadores, montos, informes finales), planilla agregada por concepto, admisión, matrícula, egreso. | Unidad de datos | 2026 | B | Datasets publicados y actualizados |
| 11.2 Rendición de cuentas anual de cada decano y vicerrector con los indicadores del tablero, en audiencia pública. | Rectorado + facultades | 2027 | B | Informes publicados a tiempo |
| 11.3 Publicar los resultados agregados de la evaluación docente (E2.1) por facultad y categoría, nunca individuales. | VRA | 2028 | B | Reporte publicado |
| 11.4 Seguimiento ciudadano: el Observatorio UNI replica y audita los indicadores con fuentes públicas (MEF, PTE, OpenAlex, OECE, datosabiertos). | Observatorio UNI (externo) | 2026 | B | Diferencia entre cifra oficial y cifra auditada |

---

## 3.3 Hoja de ruta 2026–2036

**Fase 1 — Ordenar la casa (2026–2028).** Datos, procesos, ejecución y reglas de juego.
**Fase 2 — Escalar (2029–2032).** Más doctores, posgrado TC, fondos externos, nuevas carreras.
**Fase 3 — Liderar (2033–2036).** Consolidación, impacto internacional y sostenibilidad financiera.

| Fase | Año | Hitos |
|---|---|---|
| 1 | 2026 | Plan aprobado por Consejo Universitario y Asamblea como extensión del PEI 2025–2030; preparación del expediente de renovación de licencia SUNEDU; unidad de datos y PMO creadas; ventanilla única de proyectos; afiliación/ORCID obligatorios; diagnóstico de los S/ 4,57 M sin devengar del posgrado 2025; piloto de evaluación docente; línea de base publicada (titulación, retención, doctorado); **inicio de la auditoría de uso de espacios**; demanda presupuestal 2027–2029 presentada con la trayectoria de §3.5 |
| 1 | 2027 | **Renovación de la licencia institucional SUNEDU (vence ≈ nov-2027)**; evaluación de Ciberseguridad (primera de las carreras nuevas); evaluación docente anual en régimen; reconversión de 10 % de «otros» a pago por resultados; concursos VRI con pares externos; OTT operativa; 15 plazas de doctores; becas de posgrado TC extendidas a ingeniería (sobre las 76 plazas doctorales PROCIENCIA de Ciencias); ejecución de capital ≥ 80 %; evaluación de carreras (1.ª ronda); **tres trayectorias docentes aprobadas**; políticas de spin-offs y de propiedad intelectual; incubadora operativa; auditoría de espacios publicada y moratoria de edificios nuevos |
| 1 | 2028 | I+D (programa CTI) = 3,5 % del PIM base; ejecución de capital ≥ 85 %; primeras consecuencias de evaluación (planes de mejora concluidos); 1.ª OxI adjudicada (S/ 15 M); fondos externos S/ 12 M; 150 docentes RENACYT; 35 % docentes publican (ventana 2024–28); plan maestro de infraestructura aprobado; línea de base de utilización de espacios publicada; socio ancla internacional firmado; primeros docentes en sus trayectorias |
| 2 | 2029 | Fondo patrimonial constituido (S/ 10 M); reconversión de «otros» al 30 %; reglas de rediseño/fusión de carreras aplicadas; primer año común; ejecución de capital 90 %; fondo de capital semilla de egresados; 1.er laboratorio conjunto internacional |
| 2 | 2030 | Formulación del PEI 2031–2036 sobre la base de UNI 2036; 1.ª maestría «de futuro» con socio internacional (candidatas: Energía, Recursos Hídricos y Clima); acreditación internacional de un doctorado; 250 RENACYT; QS 1001–1200 estable |
| 2 | 2031 | **Metas intermedias**: I+D (programa CTI) 6 % del PIM base (I+D total 8,4 %); ejecución de capital 95 %; 60 % docentes con producción (2027–31); 1 000 obras/año; fondos externos S/ 30 M; 300 RENACYT; QS ≤ 800; utilización de aulas ≥ 35 % con frecuencia ≥ 70 % (meta 2029 cumplida); 3 laboratorios conjuntos; PIM ≈ S/ 485 M |
| 2 | 2032 | Evaluación externa de medio término del plan; ajuste de metas; 300 becarios de posgrado TC; decisión sobre el nivel B de ambición (§3.6); evaluación de pregrados nuevos (etapa 3) |
| 3 | 2033 | 2.ª ronda de evaluación quinquenal de carreras; 5 spin-offs activas; contratos con industria ≥ S/ 15 M |
| 3 | 2034 | 40 % de docentes con doctorado [meta sujeta a línea de base]; 52 % obras con coautoría internacional; top-10 de América Latina en producción de ingeniería (OpenAlex) |
| 3 | 2035 | Fondo patrimonial ≥ S/ 45 M; titulación oportuna ≥ 55 %; 20 convenios de doble grado |
| 3 | 2036 | **Metas finales**: I+D (programa CTI) 8 % del PIM base (I+D total 13,9 %); 1 600 obras/año; 70 % docentes con producción; 450 RENACYT; 450 becarios TC; QS ≤ 600; PIM ≈ S/ 617 M; 6 laboratorios conjuntos; evaluación final y plan 2046 |

```json
{"roadmap":[
{"fase":"Ordenar la casa","año":2026,"hito":"Plan aprobado; unidad de datos y PMO creadas; ventanilla única de proyectos; ORCID y afiliación obligatorios; línea de base publicada"},
{"fase":"Ordenar la casa","año":2026,"hito":"Diagnóstico del posgrado (PIM S/ 4,57 M, devengado S/ 0 en 2025); piloto de evaluación docente"},
{"fase":"Ordenar la casa","año":2026,"hito":"Inicio de la auditoría de uso de espacios; demanda presupuestal 2027–2029 con la trayectoria de reforma"},
{"fase":"Ordenar la casa","año":2027,"hito":"Evaluación docente anual en régimen; 10 % de 'otros' reconvertido a pago por resultados; concursos VRI con pares externos"},
{"fase":"Ordenar la casa","año":2027,"hito":"Renovación de la licencia institucional SUNEDU (vence ≈ noviembre 2027)"},
{"fase":"Ordenar la casa","año":2027,"hito":"OTT operativa; 15 plazas netas de doctores; becas TC extendidas a ingeniería (base: 76 plazas doctorales PROCIENCIA); ejecución de capital ≥ 80 %"},
{"fase":"Ordenar la casa","año":2027,"hito":"Tres trayectorias docentes aprobadas; políticas de spin-offs y PI; incubadora; auditoría de espacios publicada y moratoria de edificios nuevos"},
{"fase":"Ordenar la casa","año":2028,"hito":"I+D (programa CTI) 3,5 % del PIM base; ejecución de capital ≥ 85 %; 1.ª obra por impuestos (S/ 15 M); fondos externos S/ 12 M; 150 RENACYT; línea de base de utilización de espacios; socio ancla internacional firmado"},
{"fase":"Escalar","año":2029,"hito":"Fondo patrimonial constituido (S/ 10 M); 30 % de 'otros' reconvertido; primer año común; ejecución de capital 90 %; fondo semilla de egresados; 1.er laboratorio conjunto internacional"},
{"fase":"Escalar","año":2030,"hito":"PEI 2031–2036 formulado sobre UNI 2036; 1.ª maestría de futuro con socio internacional; 1.er doctorado acreditado internacionalmente; 250 RENACYT"},
{"fase":"Escalar","año":2031,"hito":"Metas intermedias: I+D (programa CTI) 6 % del PIM base (I+D total 8,4 %); ejecución de capital 95 %; 60 % docentes con producción; 1 000 obras/año; QS ≤ 800; utilización de aulas ≥ 35 %; PIM ≈ S/ 485 M"},
{"fase":"Escalar","año":2032,"hito":"Evaluación externa de medio término; 300 becarios de posgrado TC; decisión sobre el nivel B de ambición"},
{"fase":"Liderar","año":2033,"hito":"2.ª evaluación quinquenal de carreras; 5 spin-offs activas; contratos con industria ≥ S/ 15 M"},
{"fase":"Liderar","año":2034,"hito":"40 % de docentes con doctorado; 52 % de obras con coautoría internacional; top-10 de América Latina en producción de ingeniería"},
{"fase":"Liderar","año":2035,"hito":"Fondo patrimonial ≥ S/ 45 M; titulación oportuna ≥ 55 %; 20 convenios de doble grado"},
{"fase":"Liderar","año":2036,"hito":"Metas finales: I+D (programa CTI) 8 % del PIM base (I+D total 13,9 %); 1 600 obras/año; 70 % docentes con producción; 450 RENACYT; 450 becarios TC; QS ≤ 600; PIM ≈ S/ 617 M; 6 laboratorios conjuntos"}
]}
```

---

## 3.4 Tablero de indicadores

Las metas 2028/2031/2036 son las del escenario de **reforma** (§3.5). Donde la base es «s/d», la primera meta es publicar el dato.

| # | Indicador | Línea de base (valor, año, fuente) | Meta 2028 | Meta 2031 | Meta 2036 | Fuente de seguimiento |
|---|---|---|---|---|---|---|
| 1 | Obras por año (OpenAlex, afiliación UNI) | 497 (2025), OpenAlex | 700 | 1 000 | 1 600 | OpenAlex API (`bibliometria.json`) |
| 2 | % docentes con ≥ 1 obra en ventana de 5 años | 26,2 % (2021–25), PTE × OpenAlex | 35 % | 60 % | 70 % | PTE + OpenAlex (`facultades-uni.json`) |
| 3 | Obras atribuidas por docente (5 años) | 1,45 (1 862 / 1 282; 2021–25) | 2,0 | 3,0 | 4,5 | `facultades-uni.json` |
| 4 | Facultades con ≥ 30 % de docentes con producción | 4 de 11 (2021–25) | 7 | 10 | 11 | `facultades-uni.json` |
| 5 | Impacto medio (citas medias a 2 años, OpenAlex) | 1,75 (2026) | ≥ 1,75 | ≥ 1,9 | ≥ 2,0 | OpenAlex |
| 6 | % obras en acceso abierto | 68,9 % (2026), OpenAlex | 75 % | 85 % | 90 % | OpenAlex |
| 7 | Docentes RENACYT | 90 (2020), CONCYTEC | 150 | 300 | 450 | CTI Vitae / RENACYT (CONCYTEC) |
| 8 | % docentes a tiempo completo | 56,5 % (set-2026), PTE | 60 % | 65 % | 70 % | PTE (`planilla-uni.json`, `facultades-uni.json`) |
| 9 | % docentes con doctorado | s/d (44 % con maestría y/o doctorado, 2017, SUNEDU) | publicar base | ≥ 30 % [S] | ≥ 45 % [S] | SUNEDU (registro de grados) × PTE |
| 10 | % planilla docente pagada como «otros» | 29,7 % (set-2026), PTE | 25 % | 15 % | ≤ 10 % sin producto asociado | PTE (`planilla-uni.json`) |
| 11 | I+D total (programa CTI + fondos externos de investigación) / PIM | 1,8 % (2025, solo CTI), MEF/SIAF | 4,0 % | 8,4 % | 13,9 % | MEF/SIAF programa CTI y fuente DyT/RDR (`presupuesto-uni.json`) |
| 12 | I+D del programa CTI en S/ M (meta: 3,5 % / 6 % / 8 % del PIM base) | 6,7 (2025) | 14,0 | 25,8 | 38,9 | MEF/SIAF |
| 13 | Ejecución del gasto de capital | 66,2 % (2025), MEF/SIAF | 85 % | 95 % | 95 % | MEF/SIAF (`presupuesto-uni.json`) |
| 14 | Ejecución presupuestal total | 91,3 % (2025), MEF/SIAF | 93 % | 95 % | 96 % | MEF/SIAF |
| 15 | Fondos externos competitivos captados (S/ M) | s/d (supuesto 5,0) | 12 | 30 | 60 | MEF/SIAF fuente «Donaciones y Transferencias»; PROCIENCIA (resultados de concursos) |
| 16 | Contratos I+D+i con empresas (S/ M) | s/d (supuesto 1,0) | 4 | 10 | 25 | MEF/SIAF fuente RDR; portal de transparencia UNI |
| 17 | Fondos concursables VRI por año (S/ M) | 4,61 (2025); 3,41 (2026), VRI | 8 | 15 | 22 | `vri-proyectos.json` (resoluciones VRI) |
| 18 | % proyectos VRI con evaluación externa y resultados publicados | s/d | 100 % | 100 % | 100 % | vri.uni.edu.pe |
| 19 | Becarios de posgrado de investigación TC | 76 plazas doctorales con beca PROCIENCIA (2024, Doctorado en Ciencias) | 150 | 300 | 450 | Datos abiertos UNI; PROCIENCIA; SUNEDU |
| 20 | Mujeres entre ingresantes | 16,8 % (2026-1), datosabiertos.gob.pe | 22 % | 27 % | 33 % | `admision-uni.json` |
| 21 | Postulantes por ingresante (año) | 5,8 (2025: 16 036 / 2 757) | ≥ 5,0 | ≥ 5,0 | ≥ 5,0 | `admision-uni.json` |
| 22 | Retención al 2.º año | s/d | publicar base | 85 % [S] | 90 % [S] | Datos abiertos UNI / MINEDU |
| 23 | Titulación oportuna (≤ 6 años desde ingreso) | s/d | publicar base | 50 % [S] | 60 % [S] | SUNEDU (registro de grados y títulos) |
| 24 | QS World University Rankings | ausente en la edición 2027 (1201–1400 en ediciones 2025 y 2026), QS | volver: 1001–1200 | ≤ 800 | ≤ 600 | topuniversities.com |
| 25 | Datasets institucionales en datos abiertos | s/d (≈0 de la UNI) | 10 | 20 | 30 | datosabiertos.gob.pe; portal UNI |

**Indicadores complementarios** (requerimientos de trayectorias, investigación aplicada/básica, infraestructura, alianzas y presupuesto):

| # | Indicador | Línea de base (valor, año, fuente) | Meta 2028 | Meta 2031 | Meta 2036 | Fuente de seguimiento |
|---|---|---|---|---|---|---|
| 26 | Obras en el 10 % más citado (ventana 5 años) | 163 = 8,8 % (2021–25), OpenAlex | 10 % | 13 % | 16 % | OpenAlex (`citation_normalized_percentile`) |
| 27 | Obras con coautor de empresa (ventana 5 años) | 5 (2021–25), OpenAlex | 20 | 60 | 150 | OpenAlex (`authorships.institutions.type:company`) |
| 28 | % obras con coautoría internacional | 41,7 % (2021–25), OpenAlex | 45 % | 50 % | 55 % | OpenAlex (`countries_distinct_count`) |
| 29 | Solicitudes de patente/modelo de utilidad por año | s/d | 10 | 20 | 40 | INDECOPI (búsqueda por titular) |
| 30 | Spin-offs activas (acumulado) | s/d | 1 | 3 | 8 | Registro de la OTT; SUNARP |
| 31 | **Utilización de aulas** = frecuencia × ocupación (se publican también frecuencia y ocupación por separado; laboratorios aparte) | **s/d**: hipótesis del propietario «< 40 %», no verificada y sin definición precisa | publicar base (auditoría 2027) | ≥ 35 % (frecuencia ≥ 70 %), desde 2029 | ≥ 40 % | Auditoría de espacios (E7.5), publicada por la UNI |
| 32 | Docentes por trayectoria (docencia / investigación / innovación) | no existe | 1.ª asignación | 50/33/17 % | 45/35/20 % | Datos abiertos UNI (agregado) |
| 33 | PIM anual (S/ M) vs trayectoria de reforma | 370,6 (2025), MEF/SIAF | 413 | 485 | 617 | MEF/SIAF (`presupuesto-uni.json`) |
| 34 | Laboratorios conjuntos internacionales activos | s/d | 0–1 | 3 | 6 | Convenios publicados; OpenAlex (coautoría) |
| 35 | Programas de pregrado acreditados (ABET/ICACIT/RIBA) | 20 (19 ABET desde 2017 + Arquitectura RIBA) | 24 | todos los que tienen egresados | todos | Directorios públicos de ABET, ICACIT y RIBA |

```json
{"kpis":[
{"id":1,"indicador":"Obras por año (OpenAlex)","base":{"valor":497,"anio":2025,"fuente":"OpenAlex"},"meta_2028":700,"meta_2031":1000,"meta_2036":1600,"seguimiento":"OpenAlex API (bibliometria.json)"},
{"id":2,"indicador":"% docentes con ≥1 obra en ventana de 5 años","base":{"valor":26.2,"anio":"2021-2025","fuente":"PTE × OpenAlex"},"meta_2028":35,"meta_2031":60,"meta_2036":70,"seguimiento":"facultades-uni.json"},
{"id":3,"indicador":"Obras atribuidas por docente (5 años)","base":{"valor":1.45,"anio":"2021-2025","fuente":"facultades-uni.json"},"meta_2028":2.0,"meta_2031":3.0,"meta_2036":4.5,"seguimiento":"facultades-uni.json"},
{"id":4,"indicador":"Facultades con ≥30 % de docentes con producción","base":{"valor":4,"anio":"2021-2025","fuente":"facultades-uni.json"},"meta_2028":7,"meta_2031":10,"meta_2036":11,"seguimiento":"facultades-uni.json"},
{"id":5,"indicador":"Citas medias a 2 años","base":{"valor":1.75,"anio":2026,"fuente":"OpenAlex"},"meta_2028":1.75,"meta_2031":1.9,"meta_2036":2.0,"seguimiento":"OpenAlex"},
{"id":6,"indicador":"% obras en acceso abierto","base":{"valor":68.9,"anio":2026,"fuente":"OpenAlex"},"meta_2028":75,"meta_2031":85,"meta_2036":90,"seguimiento":"OpenAlex"},
{"id":7,"indicador":"Docentes RENACYT","base":{"valor":90,"anio":2020,"fuente":"CONCYTEC"},"meta_2028":150,"meta_2031":300,"meta_2036":450,"seguimiento":"RENACYT/CTI Vitae"},
{"id":8,"indicador":"% docentes a tiempo completo","base":{"valor":56.5,"anio":"2026-09","fuente":"PTE"},"meta_2028":60,"meta_2031":65,"meta_2036":70,"seguimiento":"planilla-uni.json"},
{"id":9,"indicador":"% docentes con doctorado","base":{"valor":null,"anio":null,"fuente":"s/d (44 % con posgrado, SUNEDU 2017)"},"meta_2028":"publicar base","meta_2031":30,"meta_2036":45,"seguimiento":"SUNEDU × PTE","supuesto":true},
{"id":10,"indicador":"% planilla docente pagada como 'otros'","base":{"valor":29.7,"anio":"2026-09","fuente":"PTE"},"meta_2028":25,"meta_2031":15,"meta_2036":10,"seguimiento":"planilla-uni.json"},
{"id":11,"indicador":"I+D total (programa CTI + fondos externos de investigación) / PIM (%)","base":{"valor":1.8,"anio":2025,"fuente":"MEF/SIAF (solo CTI)"},"meta_2028":4.0,"meta_2031":8.4,"meta_2036":13.9,"seguimiento":"presupuesto-uni.json"},
{"id":12,"indicador":"I+D programa CTI (S/ M; 3,5/6/8 % del PIM base)","base":{"valor":6.7,"anio":2025,"fuente":"MEF/SIAF"},"meta_2028":14.0,"meta_2031":25.8,"meta_2036":38.9,"seguimiento":"MEF/SIAF"},
{"id":13,"indicador":"Ejecución del gasto de capital (%)","base":{"valor":66.2,"anio":2025,"fuente":"MEF/SIAF"},"meta_2028":85,"meta_2031":95,"meta_2036":95,"seguimiento":"presupuesto-uni.json"},
{"id":14,"indicador":"Ejecución presupuestal total (%)","base":{"valor":91.3,"anio":2025,"fuente":"MEF/SIAF"},"meta_2028":93,"meta_2031":95,"meta_2036":96,"seguimiento":"presupuesto-uni.json"},
{"id":15,"indicador":"Fondos externos competitivos (S/ M)","base":{"valor":5.0,"anio":2025,"fuente":"supuesto (s/d)"},"meta_2028":12,"meta_2031":30,"meta_2036":60,"seguimiento":"MEF/SIAF Donaciones y Transferencias; PROCIENCIA","supuesto":true},
{"id":16,"indicador":"Contratos I+D+i con empresas (S/ M)","base":{"valor":1.0,"anio":2025,"fuente":"supuesto (s/d)"},"meta_2028":4,"meta_2031":10,"meta_2036":25,"seguimiento":"MEF/SIAF RDR","supuesto":true},
{"id":17,"indicador":"Fondos concursables VRI por año (S/ M)","base":{"valor":4.61,"anio":2025,"fuente":"vri-proyectos.json"},"meta_2028":8,"meta_2031":15,"meta_2036":22,"seguimiento":"vri-proyectos.json"},
{"id":18,"indicador":"% proyectos VRI con evaluación externa publicada","base":{"valor":null,"anio":null,"fuente":"s/d"},"meta_2028":100,"meta_2031":100,"meta_2036":100,"seguimiento":"vri.uni.edu.pe"},
{"id":19,"indicador":"Becarios de posgrado de investigación TC","base":{"valor":76,"anio":2024,"fuente":"PROCIENCIA, Doctorado en Ciencias (plazas)"},"meta_2028":150,"meta_2031":300,"meta_2036":450,"seguimiento":"Datos abiertos UNI; SUNEDU"},
{"id":20,"indicador":"% mujeres entre ingresantes","base":{"valor":16.8,"anio":"2026-1","fuente":"datosabiertos.gob.pe"},"meta_2028":22,"meta_2031":27,"meta_2036":33,"seguimiento":"admision-uni.json"},
{"id":21,"indicador":"Postulantes por ingresante","base":{"valor":5.8,"anio":2025,"fuente":"datosabiertos.gob.pe"},"meta_2028":5.0,"meta_2031":5.0,"meta_2036":5.0,"seguimiento":"admision-uni.json"},
{"id":22,"indicador":"Retención al 2.º año (%)","base":{"valor":null,"anio":null,"fuente":"s/d"},"meta_2028":"publicar base","meta_2031":85,"meta_2036":90,"seguimiento":"Datos abiertos UNI / MINEDU","supuesto":true},
{"id":23,"indicador":"Titulación oportuna ≤6 años (%)","base":{"valor":null,"anio":null,"fuente":"s/d"},"meta_2028":"publicar base","meta_2031":50,"meta_2036":60,"seguimiento":"SUNEDU","supuesto":true},
{"id":24,"indicador":"QS World","base":{"valor":"ausente (ed. 2027); 1201-1400 en ed. 2025 y 2026","anio":2027,"fuente":"QS"},"meta_2028":"1001-1200","meta_2031":"≤800","meta_2036":"≤600","seguimiento":"topuniversities.com"},
{"id":25,"indicador":"Datasets institucionales abiertos","base":{"valor":null,"anio":null,"fuente":"s/d"},"meta_2028":10,"meta_2031":20,"meta_2036":30,"seguimiento":"datosabiertos.gob.pe"},
{"id":26,"complementario":true,"indicador":"Obras en el 10 % más citado (% , ventana 5 años)","base":{"valor":8.8,"anio":"2021-2025","fuente":"OpenAlex"},"meta_2028":10,"meta_2031":13,"meta_2036":16,"seguimiento":"OpenAlex"},
{"id":27,"complementario":true,"indicador":"Obras con coautor de empresa (ventana 5 años)","base":{"valor":5,"anio":"2021-2025","fuente":"OpenAlex"},"meta_2028":20,"meta_2031":60,"meta_2036":150,"seguimiento":"OpenAlex"},
{"id":28,"complementario":true,"indicador":"% obras con coautoría internacional","base":{"valor":41.7,"anio":"2021-2025","fuente":"OpenAlex"},"meta_2028":45,"meta_2031":50,"meta_2036":55,"seguimiento":"OpenAlex"},
{"id":29,"complementario":true,"indicador":"Solicitudes de patente/modelo de utilidad por año","base":{"valor":null,"anio":null,"fuente":"s/d"},"meta_2028":10,"meta_2031":20,"meta_2036":40,"seguimiento":"INDECOPI"},
{"id":30,"complementario":true,"indicador":"Spin-offs activas (acumulado)","base":{"valor":null,"anio":null,"fuente":"s/d"},"meta_2028":1,"meta_2031":3,"meta_2036":8,"seguimiento":"OTT; SUNARP"},
{"id":31,"complementario":true,"indicador":"Utilización de aulas = frecuencia × ocupación (%)","base":{"valor":null,"anio":null,"fuente":"s/d; hipótesis del propietario <40 % no verificada ni definida"},"meta_2028":"publicar base","meta_2031":35,"meta_2036":40,"meta_aux":"frecuencia ≥70 % desde 2029","seguimiento":"Auditoría de espacios (E7.5)","referente":"Bristol 35 % (70×50); promedio aulas Reino Unido ≈20 %","supuesto":true},
{"id":32,"complementario":true,"indicador":"Docentes por trayectoria docencia/investigación/innovación (%)","base":{"valor":null,"anio":null,"fuente":"no existe"},"meta_2028":"1.ª asignación","meta_2031":"50/33/17","meta_2036":"45/35/20","seguimiento":"Datos abiertos UNI","supuesto":true},
{"id":33,"complementario":true,"indicador":"PIM anual (S/ M) vs trayectoria de reforma","base":{"valor":370.6,"anio":2025,"fuente":"MEF/SIAF"},"meta_2028":413,"meta_2031":485,"meta_2036":617,"seguimiento":"presupuesto-uni.json"},
{"id":34,"complementario":true,"indicador":"Laboratorios conjuntos internacionales activos","base":{"valor":null,"anio":null,"fuente":"s/d"},"meta_2028":1,"meta_2031":3,"meta_2036":6,"seguimiento":"Convenios publicados"},
{"id":35,"complementario":true,"indicador":"Programas de pregrado acreditados (ABET/ICACIT/RIBA)","base":{"valor":20,"anio":2026,"fuente":"19 ABET desde 2017 + Arquitectura RIBA (diagnóstico)"},"meta_2028":24,"meta_2031":"todos con egresados","meta_2036":"todos","seguimiento":"ABET, ICACIT, RIBA (directorios públicos)"}
]}
```

---

## 3.5 Escenarios financieros 2026–2036: inercial vs reforma

Modelo reproducible: `escenarios.py` (Python, en la carpeta del capítulo). Base 2025 = ejercicio cerrado (`presupuesto-uni.json`). 2026 aún está en ejecución (PIM S/ 331,6 M a la fecha de extracción, julio de 2026, **por debajo** del PIM 2025): por eso el modelo proyecta desde 2025 y no desde 2026. Cifras en S/ M nominales.

### Supuestos explícitos

**Inercial (todo sigue como va)**
- PIM crece **2,5 %/año** = tasa compuesta 2012–2025 (S/ 269,3 M → S/ 370,6 M; 2,49 %). (2019–2025 fue 3,6 %; usamos la serie larga, más conservadora.)
- Planilla (personal y obligaciones sociales) crece **3,0 %/año** [S] (crecimiento vegetativo y ajustes).
- I+D se queda en **1,8 % del PIM**; gasto de capital en **18,9 % del PIM** con **66,2 %** de ejecución.
- Fondos externos competitivos: **S/ 5 M en 2025 [S]** (no hay dato publicado), +3 %/año.

**Reforma**
- I+D sube linealmente a **3,5 % (2028), 6 % (2031), 8 % (2036)** del PIM inercial. Incluye concursos VRI, grupos, becas de posgrado TC y equipamiento menor.
- Capital: 20 % del PIM (2028), 22 % (2031–2036); ejecución 70 % (2026), 80 % (2027), 85 % (2028), 90 % (2029), 93 % (2030), **95 % desde 2031**.
- Docentes: **15 plazas netas nuevas de doctores por año** desde 2027 a S/ 13 000/mes × 14 [S]; bonificación RENACYT 50 % de haberes (art. 86) ≈ S/ 45 100/persona-año (50 % × S/ 6 446 promedio mensual docente PTE × 14) para cada docente RENACYT por encima de 90 (150 en 2028, 300 en 2031, 450 en 2036).
- Fuentes por **uso elegible**: los fondos externos (PROCIENCIA, internacionales, contratos con empresas) solo financian I+D; la reasignación interna (30 % de «otros» docentes desde 2029, ≈ S/ 29,5 M/año × 30 % [S: «otros» × 12 meses]; ahorro de 3–5 % en bienes y servicios) y el retorno del fondo patrimonial financian incentivos y plazas; el mayor gasto de capital requiere recursos ordinarios (MEF). Lo que no cubren las fuentes es la **brecha de recursos ordinarios** a solicitar al MEF.
- Fondos externos: S/ 12 M (2028), 30 M (2031), 60 M (2036); contratos con empresas: S/ 1 M (2025 [S]) → 4 → 10 → 25 M; interpolación geométrica.
- Obras por impuestos: S/ 15 M (2028), S/ 25 M/año (2029–2036) [S]; se muestran como modalidad de ejecución **dentro** del capital (el CIPGN se repaga con presupuesto propio), no como dinero adicional.
- Fondo patrimonial: S/ 10 M (2029) + S/ 5 M/año; rendimiento 4 %, gasto 4 % del capital desde 2030 [S].

### Escenario inercial (S/ M)

| Año | PIM | Planilla | I+D | Capital PIM | Inversión ejecutada | Fondos externos |
|---|---|---|---|---|---|---|
| 2025 (real) | 370,6 | 154,6 | 6,7 | 70,1 | 46,4 | 5,0 [S] |
| 2026 | 379,9 | 159,2 | 6,8 | 71,8 | 47,6 | 5,2 |
| 2027 | 389,3 | 164,0 | 7,0 | 73,6 | 48,7 | 5,3 |
| 2028 | 399,1 | 168,9 | 7,2 | 75,5 | 50,0 | 5,5 |
| 2029 | 409,1 | 174,0 | 7,4 | 77,4 | 51,2 | 5,6 |
| 2030 | 419,3 | 179,2 | 7,5 | 79,3 | 52,5 | 5,8 |
| 2031 | 429,8 | 184,6 | 7,7 | 81,3 | 53,8 | 6,0 |
| 2032 | 440,5 | 190,1 | 7,9 | 83,3 | 55,2 | 6,1 |
| 2033 | 451,5 | 195,8 | 8,1 | 85,4 | 56,5 | 6,3 |
| 2034 | 462,8 | 201,7 | 8,3 | 87,5 | 57,9 | 6,5 |
| 2035 | 474,4 | 207,7 | 8,5 | 89,7 | 59,4 | 6,7 |
| 2036 | 486,2 | 214,0 | 8,8 | 92,0 | 60,9 | 6,9 |

### Escenario de reforma (S/ M)

| Año | PIM | Planilla | I+D | I+D % | Capital PIM | Inversión ejecutada | Ejec. % | de ella OxI | Fondos externos + industria | Doctores netos nuevos (acum.) | RENACYT | Fondo patrimonial |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026 | 383,4 | 160,1 | 9,0 | 2,4 | 73,2 | 51,2 | 70 | 0 | 8,3 | 0 | 110 | 0 |
| 2027 | 397,3 | 168,8 | 11,4 | 2,9 | 76,4 | 61,2 | 80 | 0 | 11,5 | 15 | 130 | 0 |
| 2028 | 413,0 | 177,8 | 14,0 | 3,5 | 79,8 | 67,8 | 85 | 15 | 16,0 | 30 | 150 | 0 |
| 2029 | 431,4 | 188,8 | 17,7 | 4,3 | 84,5 | 76,1 | 90 | 25 | 21,7 | 45 | 200 | 10,0 |
| 2030 | 456,5 | 200,2 | 21,7 | 5,2 | 89,4 | 83,2 | 93 | 25 | 29,5 | 60 | 250 | 15,4 |
| 2031 | 485,4 | 212,2 | 25,8 | 6,0 | 94,5 | 89,8 | 95 | 25 | 40,0 | 75 | 300 | 21,0 |
| 2032 | 507,9 | 223,6 | 28,2 | 6,4 | 96,9 | 92,1 | 95 | 25 | 46,5 | 90 | 330 | 26,9 |
| 2033 | 532,1 | 235,5 | 30,7 | 6,8 | 99,3 | 94,4 | 95 | 25 | 54,0 | 105 | 360 | 32,9 |
| 2034 | 558,0 | 247,8 | 33,3 | 7,2 | 101,8 | 96,7 | 95 | 25 | 62,8 | 120 | 390 | 39,2 |
| 2035 | 586,1 | 260,8 | 36,1 | 7,6 | 104,4 | 99,1 | 95 | 25 | 73,0 | 135 | 420 | 45,8 |
| 2036 | 616,5 | 274,2 | 38,9 | 8,0 | 107,0 | 101,6 | 95 | 25 | 85,0 | 150 | 450 | 52,7 |

*El PIM de reforma incluye la brecha de recursos ordinarios y los fondos externos que exceden la meta de I+D (entran al pliego como Donaciones y Transferencias o RDR); la reasignación interna no aumenta el PIM.*

### Brecha y cómo se cierra (S/ M, incremental sobre el escenario inercial)

| Año | Necesidad I+D | Necesidad planilla (doctores + RENACYT) | Necesidad capital | **Necesidad total** | Cubre: fondos externos | Cubre: reasignación + ahorro + fondo patrimonial | **Brecha RO (MEF)** | Inversión ejecutada adicional |
|---|---|---|---|---|---|---|---|---|
| 2026 | 2,2 | 0,9 | 1,3 | 4,4 | 2,1 | 0,9 | 1,4 | 3,7 |
| 2027 | 4,4 | 4,8 | 2,8 | 12,0 | 4,4 | 4,8 | 2,8 | 12,4 |
| 2028 | 6,8 | 8,9 | 4,3 | 20,0 | 6,8 | 8,9 | 4,3 | 17,9 |
| 2029 | 10,4 | 14,8 | 7,2 | 32,3 | 10,4 | 14,7 | 7,2 | 24,9 |
| 2030 | 14,1 | 21,0 | 10,1 | 45,3 | 14,1 | 16,7 | 14,5 | 30,7 |
| 2031 | 18,1 | 27,6 | 13,3 | 58,9 | 18,1 | 18,3 | 22,6 | 36,0 |
| 2032 | 20,3 | 33,5 | 13,6 | 67,3 | 20,3 | 19,0 | 28,1 | 36,9 |
| 2033 | 22,6 | 39,6 | 13,9 | 76,2 | 22,6 | 19,7 | 33,8 | 37,8 |
| 2034 | 25,0 | 46,2 | 14,3 | 85,4 | 25,0 | 20,5 | 39,9 | 38,8 |
| 2035 | 27,5 | 53,0 | 14,6 | 95,2 | 27,5 | 21,3 | 46,4 | 39,8 |
| 2036 | 30,1 | 60,3 | 15,0 | 105,4 | 30,1 | 22,1 | 53,2 | 40,7 |
| **Acum. 2026–36** | **181,4** | **310,7** | **110,6** | **602,6** | **181,4** | **167,0** | **254,3** | **319,6** |

### Lo que tenemos vs lo que se necesita

| Concepto | Lo que tenemos (2025) | Lo que se necesita (2031) | Lo que se necesita (2036) |
|---|---|---|---|
| I+D anual (programa CTI) | S/ 6,7 M (1,8 %) | S/ 25,8 M (6 % del PIM base) — **×3,9** | S/ 38,9 M (8 % del PIM base) — **×5,8** |
| PIM total | S/ 370,6 M | S/ 485,4 M | S/ 616,5 M |
| Inversión ejecutada anual | S/ 46,4 M (66,2 %) | S/ 89,8 M (95 %) | S/ 101,6 M |
| Inversión no ejecutada | S/ 23,7 M (2025) | ≈ S/ 4,7 M | ≈ S/ 5,4 M |
| Fondos externos + industria | ≈ S/ 6 M [S] | S/ 40 M | S/ 85 M |
| Concursos VRI | S/ 4,61 M | S/ 15 M [S] | S/ 22 M [S] |

**Acumulado 2026–2036.** I+D: S/ 85,4 M (inercial) vs **S/ 266,7 M** (reforma). Inversión ejecutada: S/ 593,7 M vs **S/ 913,3 M** (+S/ 319,6 M, de los cuales una parte importante sale solo de **ejecutar** lo que ya se presupuesta).

**Lectura.** La reforma cuesta **S/ 602,6 M adicionales en 11 años** (≈ S/ 55 M/año en promedio; 21,7 % sobre el PIM inercial en 2036). **58 % se cubre sin pedir más recursos ordinarios**: fondos externos (S/ 181,4 M, y otros S/ 190,0 M de fondos externos por encima de la meta si se logra la captación supuesta) y reasignación interna, ahorro y fondo patrimonial (S/ 167,0 M). La **brecha de recursos ordinarios a negociar con el MEF es S/ 254,3 M acumulados** (S/ 22,6 M en 2031 y S/ 53,2 M en 2036, es decir 5,3 % y 10,9 % del PIM inercial de esos años). El rubro más caro es humano (doctores + RENACYT: S/ 310,7 M): el plan es, antes que todo, una apuesta por personas.

**Sensibilidades (para no engañarse).** Recalculadas con el mismo modelo: (i) si los fondos externos y los contratos con empresas llegan solo a la **mitad** de lo supuesto, la brecha RO sube de S/ 254,3 M a **S/ 290,3 M** (el efecto es acotado porque la meta de I+D se cubre igual hasta ~2031 y se pierde sobre todo el excedente); (ii) si la reconversión de «otros» se queda en **10 %**, la brecha sube a **S/ 315,1 M**: la reasignación interna es la palanca más sensible; (iii) si el PIM crece **3,6 %/año** (ritmo 2019–2025) en vez de 2,5 %, el PIM inercial 2036 sería S/ 546,8 M, pero la brecha casi no cambia (**S/ 258,9 M**) porque las metas de I+D y capital son porcentajes del PIM: más presupuesto no sustituye a la reforma. (iv) El modelo calcula el bono del docente investigador como 50 % del haber promedio docente (≈ S/ 3 223/mes × 14); si se usa el monto fijado por DS 028-2026-EF (hasta S/ 4 434/mes × 12 [cifra a confirmar]), la necesidad total sube a S/ 624,1 M y la brecha RO a **S/ 274,8 M**. Estas variables se publican cada año en el tablero.


### Trayectoria de financiamiento de la reforma: subir el presupuesto, explícitamente

La reforma **exige un presupuesto mayor**; no se financia solo con eficiencia. El PIM pasa de S/ 370,6 M (2025) a **S/ 413,0 M (2028), S/ 485,4 M (2031) y S/ 616,5 M (2036)**: **4,74 %/año nominal** frente a 2,5 % del escenario inercial (+S/ 130,3 M en 2036 sobre el inercial, +26,8 %). Composición del PIM de reforma (S/ M):

| Año | PIM inercial | + RO adicional (MEF) | + Externos y RDR incrementales | **= PIM reforma** | Crec. anual | Reasignación interna (dentro del PIM) |
|---|---|---|---|---|---|---|
| 2026 | 379,9 | 1,4 | 2,1 | **383,4** | 3,5 % | 0,9 |
| 2027 | 389,3 | 2,8 | 5,2 | **397,3** | 3,6 % | 4,8 |
| 2028 | 399,1 | 4,3 | 9,5 | **413,0** | 3,9 % | 8,9 |
| 2029 | 409,1 | 7,2 | 15,1 | **431,4** | 4,5 % | 14,7 |
| 2030 | 419,3 | 14,5 | 22,7 | **456,5** | 5,8 % | 16,7 |
| 2031 | 429,8 | 22,6 | 33,0 | **485,4** | 6,3 % | 18,3 |
| 2032 | 440,5 | 28,1 | 39,3 | **507,9** | 4,6 % | 19,0 |
| 2033 | 451,5 | 33,8 | 46,7 | **532,1** | 4,8 % | 19,7 |
| 2034 | 462,8 | 39,9 | 55,3 | **558,0** | 4,9 % | 20,5 |
| 2035 | 474,4 | 46,4 | 65,3 | **586,1** | 5,0 % | 21,3 |
| 2036 | 486,2 | 53,2 | 77,1 | **616,5** | 5,2 % | 22,1 |

*Identidad: PIM reforma = PIM inercial + RO adicional + externos/RDR incrementales. La reasignación interna (conversión de «otros» y ahorro en bienes y servicios) cambia el destino del gasto, no su monto. El año de mayor esfuerzo es 2031 (+6,3 %), cuando convergen la meta de I+D y la ejecución de capital al 95 %.*

**Nota sobre la medida de I+D.** Las metas de 3,5 % / 6 % / 8 % se definen para el **programa CTI propio sobre el PIM base (inercial)**, para que la meta no se mueva cuando entran fondos externos. Medido sobre el PIM total de reforma, el programa CTI propio es 5,3 % (2031) y 6,3 % (2036); y el **I+D total** (programa CTI + fondos externos de investigación que exceden la meta) llega a **8,4 % (2031) y 13,9 % (2036)**, que es el indicador 11 del tablero.

```json
{"escenarios":{"unidad":"S/ millones nominales","base":"2025 cerrado (MEF/SIAF)","fuente_modelo":"escenarios.py","supuestos":{"inercial":{"g_pim":0.025,"g_planilla":0.03,"idi_pct_pim":1.8,"capital_pct_pim":18.9,"ejecucion_capital_pct":66.2,"fondos_externos_2025_supuesto":5.0,"g_fondos_externos":0.03},"reforma":{"idi_pct_pim":{"2028":3.5,"2031":6.0,"2036":8.0},"capital_pct_pim":{"2028":20,"2031":22,"2036":22},"ejecucion_capital_pct":{"2027":80,"2028":85,"2029":90,"2030":93,"2031":95},"fondos_externos_competitivos":{"2028":12,"2031":30,"2036":60},"contratos_industria":{"2025_supuesto":1,"2028":4,"2031":10,"2036":25},"docentes_doctores_netos_nuevos_por_anio":15,"costo_docente_doctor_mes_soles":13000,"renacyt":{"2028":150,"2031":300,"2036":450},"bono_renacyt":"50% haberes (Ley 30220 art. 86)","reasignacion_otros_docentes":{"2027":0.1,"2029":0.3},"ahorro_bienes_servicios":{"2028":0.03,"2031":0.05},"obras_por_impuestos":{"2028":15,"2029_2036":25},"endowment":{"aporte_2029":10,"aporte_anual_2030_2036":5,"retorno":0.04,"payout":0.04}}},"inercial":[
{"anio":2026,"pim":379.9,"planilla":159.2,"idi":6.8,"cap_pim":71.8,"inversion_ejecutada":47.6,"fondos_externos":5.2},
{"anio":2027,"pim":389.3,"planilla":164.0,"idi":7.0,"cap_pim":73.6,"inversion_ejecutada":48.7,"fondos_externos":5.3},
{"anio":2028,"pim":399.1,"planilla":168.9,"idi":7.2,"cap_pim":75.5,"inversion_ejecutada":50.0,"fondos_externos":5.5},
{"anio":2029,"pim":409.1,"planilla":174.0,"idi":7.4,"cap_pim":77.4,"inversion_ejecutada":51.2,"fondos_externos":5.6},
{"anio":2030,"pim":419.3,"planilla":179.2,"idi":7.5,"cap_pim":79.3,"inversion_ejecutada":52.5,"fondos_externos":5.8},
{"anio":2031,"pim":429.8,"planilla":184.6,"idi":7.7,"cap_pim":81.3,"inversion_ejecutada":53.8,"fondos_externos":6.0},
{"anio":2032,"pim":440.5,"planilla":190.1,"idi":7.9,"cap_pim":83.3,"inversion_ejecutada":55.2,"fondos_externos":6.1},
{"anio":2033,"pim":451.5,"planilla":195.8,"idi":8.1,"cap_pim":85.4,"inversion_ejecutada":56.5,"fondos_externos":6.3},
{"anio":2034,"pim":462.8,"planilla":201.7,"idi":8.3,"cap_pim":87.5,"inversion_ejecutada":57.9,"fondos_externos":6.5},
{"anio":2035,"pim":474.4,"planilla":207.7,"idi":8.5,"cap_pim":89.7,"inversion_ejecutada":59.4,"fondos_externos":6.7},
{"anio":2036,"pim":486.2,"planilla":214.0,"idi":8.8,"cap_pim":92.0,"inversion_ejecutada":60.9,"fondos_externos":6.9}],"reforma":[
{"anio":2026,"pim":383.4,"planilla":160.1,"idi":9.0,"idi_pct":2.4,"cap_pim":73.2,"inversion_ejecutada":51.2,"ejec_inv_pct":70.0,"obras_por_impuestos":0.0,"fondos_externos":8.3,"docentes_phd_nuevos":0,"renacyt":110,"endowment":0},
{"anio":2027,"pim":397.3,"planilla":168.8,"idi":11.4,"idi_pct":2.9,"cap_pim":76.4,"inversion_ejecutada":61.2,"ejec_inv_pct":80.0,"obras_por_impuestos":0.0,"fondos_externos":11.5,"docentes_phd_nuevos":15,"renacyt":130,"endowment":0},
{"anio":2028,"pim":413.0,"planilla":177.8,"idi":14.0,"idi_pct":3.5,"cap_pim":79.8,"inversion_ejecutada":67.8,"ejec_inv_pct":85.0,"obras_por_impuestos":15.0,"fondos_externos":16.0,"docentes_phd_nuevos":30,"renacyt":150,"endowment":0},
{"anio":2029,"pim":431.4,"planilla":188.8,"idi":17.7,"idi_pct":4.3,"cap_pim":84.5,"inversion_ejecutada":76.1,"ejec_inv_pct":90.0,"obras_por_impuestos":25.0,"fondos_externos":21.7,"docentes_phd_nuevos":45,"renacyt":200,"endowment":10.0},
{"anio":2030,"pim":456.5,"planilla":200.2,"idi":21.7,"idi_pct":5.2,"cap_pim":89.4,"inversion_ejecutada":83.2,"ejec_inv_pct":93.0,"obras_por_impuestos":25.0,"fondos_externos":29.5,"docentes_phd_nuevos":60,"renacyt":250,"endowment":15.4},
{"anio":2031,"pim":485.4,"planilla":212.2,"idi":25.8,"idi_pct":6.0,"cap_pim":94.5,"inversion_ejecutada":89.8,"ejec_inv_pct":95.0,"obras_por_impuestos":25.0,"fondos_externos":40.0,"docentes_phd_nuevos":75,"renacyt":300,"endowment":21.0},
{"anio":2032,"pim":507.9,"planilla":223.6,"idi":28.2,"idi_pct":6.4,"cap_pim":96.9,"inversion_ejecutada":92.1,"ejec_inv_pct":95.0,"obras_por_impuestos":25.0,"fondos_externos":46.5,"docentes_phd_nuevos":90,"renacyt":330,"endowment":26.9},
{"anio":2033,"pim":532.1,"planilla":235.5,"idi":30.7,"idi_pct":6.8,"cap_pim":99.3,"inversion_ejecutada":94.4,"ejec_inv_pct":95.0,"obras_por_impuestos":25.0,"fondos_externos":54.0,"docentes_phd_nuevos":105,"renacyt":360,"endowment":32.9},
{"anio":2034,"pim":558.0,"planilla":247.8,"idi":33.3,"idi_pct":7.2,"cap_pim":101.8,"inversion_ejecutada":96.7,"ejec_inv_pct":95.0,"obras_por_impuestos":25.0,"fondos_externos":62.8,"docentes_phd_nuevos":120,"renacyt":390,"endowment":39.2},
{"anio":2035,"pim":586.1,"planilla":260.8,"idi":36.1,"idi_pct":7.6,"cap_pim":104.4,"inversion_ejecutada":99.1,"ejec_inv_pct":95.0,"obras_por_impuestos":25.0,"fondos_externos":73.0,"docentes_phd_nuevos":135,"renacyt":420,"endowment":45.8},
{"anio":2036,"pim":616.5,"planilla":274.2,"idi":38.9,"idi_pct":8.0,"cap_pim":107.0,"inversion_ejecutada":101.6,"ejec_inv_pct":95.0,"obras_por_impuestos":25.0,"fondos_externos":85.0,"docentes_phd_nuevos":150,"renacyt":450,"endowment":52.7}],"brecha":[
{"anio":2026,"necesidad_idi":2.2,"necesidad_planilla":0.9,"necesidad_capital":1.3,"necesidad_total":4.4,"fuente_externos":2.1,"fuente_internas_usadas":0.9,"brecha_ro_mef":1.4,"inversion_extra_ejecutada":3.7},
{"anio":2027,"necesidad_idi":4.4,"necesidad_planilla":4.8,"necesidad_capital":2.8,"necesidad_total":12.0,"fuente_externos":4.4,"fuente_internas_usadas":4.8,"brecha_ro_mef":2.8,"inversion_extra_ejecutada":12.4},
{"anio":2028,"necesidad_idi":6.8,"necesidad_planilla":8.9,"necesidad_capital":4.3,"necesidad_total":20.0,"fuente_externos":6.8,"fuente_internas_usadas":8.9,"brecha_ro_mef":4.3,"inversion_extra_ejecutada":17.9},
{"anio":2029,"necesidad_idi":10.4,"necesidad_planilla":14.8,"necesidad_capital":7.2,"necesidad_total":32.3,"fuente_externos":10.4,"fuente_internas_usadas":14.7,"brecha_ro_mef":7.2,"inversion_extra_ejecutada":24.9},
{"anio":2030,"necesidad_idi":14.1,"necesidad_planilla":21.0,"necesidad_capital":10.1,"necesidad_total":45.3,"fuente_externos":14.1,"fuente_internas_usadas":16.7,"brecha_ro_mef":14.5,"inversion_extra_ejecutada":30.7},
{"anio":2031,"necesidad_idi":18.1,"necesidad_planilla":27.6,"necesidad_capital":13.3,"necesidad_total":58.9,"fuente_externos":18.1,"fuente_internas_usadas":18.3,"brecha_ro_mef":22.6,"inversion_extra_ejecutada":36.0},
{"anio":2032,"necesidad_idi":20.3,"necesidad_planilla":33.5,"necesidad_capital":13.6,"necesidad_total":67.3,"fuente_externos":20.3,"fuente_internas_usadas":19.0,"brecha_ro_mef":28.1,"inversion_extra_ejecutada":36.9},
{"anio":2033,"necesidad_idi":22.6,"necesidad_planilla":39.6,"necesidad_capital":13.9,"necesidad_total":76.2,"fuente_externos":22.6,"fuente_internas_usadas":19.7,"brecha_ro_mef":33.8,"inversion_extra_ejecutada":37.8},
{"anio":2034,"necesidad_idi":25.0,"necesidad_planilla":46.2,"necesidad_capital":14.3,"necesidad_total":85.4,"fuente_externos":25.0,"fuente_internas_usadas":20.5,"brecha_ro_mef":39.9,"inversion_extra_ejecutada":38.8},
{"anio":2035,"necesidad_idi":27.5,"necesidad_planilla":53.0,"necesidad_capital":14.6,"necesidad_total":95.2,"fuente_externos":27.5,"fuente_internas_usadas":21.3,"brecha_ro_mef":46.4,"inversion_extra_ejecutada":39.8},
{"anio":2036,"necesidad_idi":30.1,"necesidad_planilla":60.3,"necesidad_capital":15.0,"necesidad_total":105.4,"fuente_externos":30.1,"fuente_internas_usadas":22.1,"brecha_ro_mef":53.2,"inversion_extra_ejecutada":40.7}],"acumulado_2026_2036":{"necesidad_idi":181.4,"necesidad_planilla":310.7,"necesidad_capital":110.6,"necesidad_total":602.6,"fuente_externos":181.4,"externos_excedente":190.0,"fuente_internas_usadas":167.0,"brecha_ro_mef":254.3,"inversion_ejecutada":{"inercial":593.7,"reforma":913.3},"idi":{"inercial":85.4,"reforma":266.7}},"trayectoria_reforma":[
{"anio":2026,"pim_inercial":379.9,"ro_adicional":1.4,"externos_rdr_incremental":2.1,"pim_reforma":383.4,"crec_pct":3.5,"reasignacion_interna":0.9,"idi":9.0,"planilla":160.1,"inversion_ejecutada":51.2},
{"anio":2027,"pim_inercial":389.3,"ro_adicional":2.8,"externos_rdr_incremental":5.2,"pim_reforma":397.3,"crec_pct":3.6,"reasignacion_interna":4.8,"idi":11.4,"planilla":168.8,"inversion_ejecutada":61.2},
{"anio":2028,"pim_inercial":399.1,"ro_adicional":4.3,"externos_rdr_incremental":9.5,"pim_reforma":413.0,"crec_pct":3.9,"reasignacion_interna":8.9,"idi":14.0,"planilla":177.8,"inversion_ejecutada":67.8},
{"anio":2029,"pim_inercial":409.1,"ro_adicional":7.2,"externos_rdr_incremental":15.1,"pim_reforma":431.4,"crec_pct":4.5,"reasignacion_interna":14.7,"idi":17.7,"planilla":188.8,"inversion_ejecutada":76.1},
{"anio":2030,"pim_inercial":419.3,"ro_adicional":14.5,"externos_rdr_incremental":22.7,"pim_reforma":456.5,"crec_pct":5.8,"reasignacion_interna":16.7,"idi":21.7,"planilla":200.2,"inversion_ejecutada":83.2},
{"anio":2031,"pim_inercial":429.8,"ro_adicional":22.6,"externos_rdr_incremental":33.0,"pim_reforma":485.4,"crec_pct":6.3,"reasignacion_interna":18.3,"idi":25.8,"planilla":212.2,"inversion_ejecutada":89.8},
{"anio":2032,"pim_inercial":440.5,"ro_adicional":28.1,"externos_rdr_incremental":39.3,"pim_reforma":507.9,"crec_pct":4.6,"reasignacion_interna":19.0,"idi":28.2,"planilla":223.6,"inversion_ejecutada":92.1},
{"anio":2033,"pim_inercial":451.5,"ro_adicional":33.8,"externos_rdr_incremental":46.7,"pim_reforma":532.1,"crec_pct":4.8,"reasignacion_interna":19.7,"idi":30.7,"planilla":235.5,"inversion_ejecutada":94.4},
{"anio":2034,"pim_inercial":462.8,"ro_adicional":39.9,"externos_rdr_incremental":55.3,"pim_reforma":558.0,"crec_pct":4.9,"reasignacion_interna":20.5,"idi":33.3,"planilla":247.8,"inversion_ejecutada":96.7},
{"anio":2035,"pim_inercial":474.4,"ro_adicional":46.4,"externos_rdr_incremental":65.3,"pim_reforma":586.1,"crec_pct":5.0,"reasignacion_interna":21.3,"idi":36.1,"planilla":260.8,"inversion_ejecutada":99.1},
{"anio":2036,"pim_inercial":486.2,"ro_adicional":53.2,"externos_rdr_incremental":77.1,"pim_reforma":616.5,"crec_pct":5.2,"reasignacion_interna":22.1,"idi":38.9,"planilla":274.2,"inversion_ejecutada":101.6}],"cagr_pim_reforma_2025_2036":4.74,"global":{"trayectoria":[
{"anio":2026,"pim_inercial":379.9,"ro_adicional":2.6,"externos_rdr_incremental":2.9,"pim_reforma":385.3,"crec_pct":4.0,"reasignacion_interna":1.4,"idi":9.6,"planilla":160.6,"inversion_ejecutada":52.1},
{"anio":2027,"pim_inercial":389.3,"ro_adicional":10.4,"externos_rdr_incremental":7.4,"pim_reforma":407.1,"crec_pct":5.7,"reasignacion_interna":5.6,"idi":12.7,"planilla":174.6,"inversion_ejecutada":63.2},
{"anio":2028,"pim_inercial":399.1,"ro_adicional":18.4,"externos_rdr_incremental":14.5,"pim_reforma":432.0,"crec_pct":6.1,"reasignacion_interna":10.3,"idi":16.0,"planilla":189.3,"inversion_ejecutada":71.2},
{"anio":2029,"pim_inercial":409.1,"ro_adicional":32.1,"externos_rdr_incremental":24.7,"pim_reforma":465.9,"crec_pct":7.8,"reasignacion_interna":14.7,"idi":21.8,"planilla":206.9,"inversion_ejecutada":82.2},
{"anio":2030,"pim_inercial":419.3,"ro_adicional":48.0,"externos_rdr_incremental":40.1,"pim_reforma":507.3,"crec_pct":8.9,"reasignacion_interna":18.1,"idi":28.0,"planilla":225.3,"inversion_ejecutada":92.3},
{"anio":2031,"pim_inercial":429.8,"ro_adicional":66.0,"externos_rdr_incremental":63.0,"pim_reforma":558.8,"crec_pct":10.1,"reasignacion_interna":20.4,"idi":34.4,"planilla":244.7,"inversion_ejecutada":102.1},
{"anio":2032,"pim_inercial":440.5,"ro_adicional":79.3,"externos_rdr_incremental":80.1,"pim_reforma":599.9,"crec_pct":7.4,"reasignacion_interna":21.8,"idi":38.8,"planilla":264.4,"inversion_ejecutada":104.6},
{"anio":2033,"pim_inercial":451.5,"ro_adicional":93.4,"externos_rdr_incremental":101.3,"pim_reforma":646.2,"crec_pct":7.7,"reasignacion_interna":23.2,"idi":43.3,"planilla":284.9,"inversion_ejecutada":107.2},
{"anio":2034,"pim_inercial":462.8,"ro_adicional":108.3,"externos_rdr_incremental":127.8,"pim_reforma":698.9,"crec_pct":8.2,"reasignacion_interna":24.7,"idi":48.1,"planilla":306.5,"inversion_ejecutada":109.9},
{"anio":2035,"pim_inercial":474.4,"ro_adicional":124.0,"externos_rdr_incremental":160.9,"pim_reforma":759.2,"crec_pct":8.6,"reasignacion_interna":26.3,"idi":53.1,"planilla":329.1,"inversion_ejecutada":112.7},
{"anio":2036,"pim_inercial":486.2,"ro_adicional":140.6,"externos_rdr_incremental":202.1,"pim_reforma":828.9,"crec_pct":9.2,"reasignacion_interna":27.9,"idi":58.3,"planilla":352.8,"inversion_ejecutada":115.5}],"acumulado_2026_2036":{"necesidad_total":1196.2,"fuente_externos":278.8,"fuente_internas_usadas":194.4,"brecha_ro_mef":723.0},"cagr_pim_2025_2036":7.59,"pim_2036":828.9,"idi_2036":58.3,"ro_adicional_2036":140.6,"docentes_phd_nuevos_2036":400,"renacyt_2036":700,"supuestos":{"idi_pct_pim_base":{"2028":4,"2031":8,"2036":12},"capital_pct_pim":{"2028":21,"2031":25,"2036":25},"fondos_externos_competitivos":{"2028":15,"2031":50,"2036":150},"contratos_industria":{"2028":6,"2031":20,"2036":60},"docentes_doctores_netos_nuevos_por_anio":40,"renacyt":{"2028":180,"2031":400,"2036":700},"endowment":{"aporte_2029":30,"aporte_anual_2030_2036":20},"resto":"igual que reforma"}},"sensibilidades_brecha_ro":{"base":254.3,"externos_mitad":290.3,"reasignacion_10pct":315.1,"pim_inercial_3_6pct":258.9}}}
```

---

## 3.6 Horizonte «liderar América Latina y competir en el mundo»

La ambición del promotor es liderar en América Latina y competir globalmente. Este capítulo la toma en serio y por eso la **cuantifica**: qué significa cada nivel, contra quién se mide y cuánto cuesta. La conclusión honesta es que **el escenario de reforma (§3.5) lleva a la UNI a liderar la ingeniería en el Perú, no a liderar América Latina**; esto último exige el escenario «global», cuyo costo está abajo.

### Dónde está hoy la UNI frente al mundo (OpenAlex)

| Institución | Obras acumuladas | Citas medias (2 años) |
|---|---|---|
| UNI (Perú) | 4 697 | 1,75 |
| U. Nacional Agraria La Molina | 6 948 | — |
| UPC (Perú) | 8 320 | — |
| U. Peruana Cayetano Heredia | 22 045 | 2,06 |
| U. de los Andes (Colombia) | 25 901 | — |
| PUCP | 33 166 | 1,45 |
| Tecnológico de Monterrey | 38 644 | — |
| U. Nacional Mayor de San Marcos | 44 113 | 0,73 |
| P. U. Católica de Chile | 81 520 | — |
| U. Nacional de Colombia | 97 352 | 1,63 |
| U. de Chile | 112 952 | 0,95 |
| U. de Buenos Aires | 129 078 | 1,78 |
| UNAM | 248 299 | 2,01 |
| U. de São Paulo | 471 028 | 1,95 |

Fuente: `bibliometria.json` (OpenAlex, extraído 2026-06). La UNI tiene **impacto medio comparable al de las grandes** (1,75 citas medias, por encima de PUCP, San Marcos, U. de Chile y U. Nacional de Colombia), pero **escala muy pequeña**. El problema es de volumen y de masa crítica, no de calidad media.

**Ingeniería en América Latina.** En obras cuyo tema principal es Ingeniería (campo OpenAlex «Engineering», 2021–2025, consulta 2026-11-12), la UNI tiene **486 obras** y ocupa el **puesto ≈ 99** entre las instituciones con producción latinoamericana (la lista incluye algunos centros extranjeros coautores). El umbral del **top-10 latinoamericano** está en ≈ 2 700 obras (puesto 10: Instituto Politécnico Nacional, 2 730), dominado por Brasil; el umbral del **top-10 hispanohablante** está en ≈ 1 350 obras (U. de Chile 1 348; U. Técnica Federico Santa María 1 357; P. U. Católica de Chile 1 492; U. Nacional de Colombia 1 674; Tecnológico de Monterrey 2 160). Es decir: **×2,8** para entrar al top-10 hispanohablante y **×5,6** para el top-10 latinoamericano en volumen de ingeniería.

### Tres niveles de ambición y lo que cuesta cada uno

| Nivel | Qué significa en 2036 | Benchmarks explícitos | Escenario financiero | Lo que implica |
|---|---|---|---|---|
| **A. Liderar en el Perú** (meta oficial del plan) | La universidad peruana con mejor investigación en ingeniería por docente y por calidad | 1 600 obras/año (≈ volumen actual de la PUCP: 1 555 en 2025); 16 % de obras en el 10 % más citado (PUCP hoy 15,7 %); QS World ≤ 600; **top-10 hispanohablante en ingeniería** (≥ 1 350 obras de ingeniería por quinquenio) | **Reforma**: PIM S/ 616,5 M en 2036 (4,7 %/año); costo adicional S/ 602,6 M en 11 años; RO adicional S/ 254,3 M | 150 doctores nuevos netos, 450 RENACYT, ejecución 95 % |
| **B. Liderar América Latina en ingeniería** (meta aspiracional, condicionada al financiamiento) | Top-10 latinoamericano en ingeniería; entrada posible al QS top-500 | ≈ 3 000 obras/año [S]; ≥ 2 700 obras de ingeniería por quinquenio; 18–20 % en el 10 % más citado [S]; QS top-500 **posible pero no asegurado** | **Global** (abajo): PIM S/ 828,9 M en 2036 (**7,6 %/año**, ×2,2); costo adicional **S/ 1 196,2 M**; **RO adicional S/ 723,0 M** | 400 doctores nuevos netos, 700 RENACYT, I+D total ≈ S/ 211 M/año en 2036 (programa CTI S/ 58,3 M + externos S/ 152,5 M), fondo patrimonial ≈ S/ 197 M |
| **C. Competir en el mundo** (horizonte 2046) | Liderazgo mundial en 2–3 **nichos** donde el Perú tiene ventaja natural, no en el ranking general | Top-50 mundial en producción y citas por tema en: ingeniería sísmica y estructural; minería, metalurgia y minerales críticos; agua y clima de montaña [S] | Continúa el escenario global después de 2036, concentrado en los nichos | Laboratorios conjuntos de clase mundial con socios ancla (E9.5–9.6) |

### Escenario «global» (S/ M) — supuestos

Igual al de reforma salvo: programa CTI 4 % (2028), 8 % (2031), 12 % (2036) del PIM base; capital 25 % del PIM desde 2031; fondos externos competitivos S/ 15 M (2028), 50 M (2031), 150 M (2036); contratos con empresas S/ 6 / 20 / 60 M; **40 doctores netos nuevos por año** desde 2027; RENACYT 180 / 400 / 700; fondo patrimonial con S/ 30 M en 2029 y S/ 20 M/año. Todo [S]. Modelo: `trayectoria_global.py` → `trayectoria_global.json`.

| Año | PIM inercial | + RO adicional | + Externos y RDR incrementales | **= PIM global** | Crec. anual | I+D programa CTI | Inversión ejecutada |
|---|---|---|---|---|---|---|---|
| 2026 | 379,9 | 2,6 | 2,9 | **385,3** | 4,0 % | 9,6 | 52,1 |
| 2027 | 389,3 | 10,4 | 7,4 | **407,1** | 5,7 % | 12,7 | 63,2 |
| 2028 | 399,1 | 18,4 | 14,5 | **432,0** | 6,1 % | 16,0 | 71,2 |
| 2029 | 409,1 | 32,1 | 24,7 | **465,9** | 7,8 % | 21,8 | 82,2 |
| 2030 | 419,3 | 48,0 | 40,1 | **507,3** | 8,9 % | 28,0 | 92,3 |
| 2031 | 429,8 | 66,0 | 63,0 | **558,8** | 10,1 % | 34,4 | 102,1 |
| 2032 | 440,5 | 79,3 | 80,1 | **599,9** | 7,4 % | 38,8 | 104,6 |
| 2033 | 451,5 | 93,4 | 101,3 | **646,2** | 7,7 % | 43,3 | 107,2 |
| 2034 | 462,8 | 108,3 | 127,8 | **698,9** | 8,2 % | 48,1 | 109,9 |
| 2035 | 474,4 | 124,0 | 160,9 | **759,2** | 8,6 % | 53,1 | 112,7 |
| 2036 | 486,2 | 140,6 | 202,1 | **828,9** | 9,2 % | 58,3 | 115,5 |

Acumulado 2026–2036: necesidad adicional **S/ 1 196,2 M**; cubren fondos externos S/ 278,8 M y reasignación interna/fondo patrimonial S/ 194,4 M; **brecha de recursos ordinarios S/ 723,0 M** (S/ 66,0 M en 2031 y S/ 140,6 M en 2036, el 15,4 % y el 28,9 % del PIM inercial de esos años). Inversión ejecutada acumulada S/ 1 013,1 M.

### Juicio de realismo

1. **QS top-500 en 2036 no es una meta realista con el escenario de reforma.** Supone volver al ranking (la UNI está ausente de la edición 2027, tras figurar en 1201–1400 en las ediciones 2025 y 2026) y luego subir más de 700 posiciones; la reputación académica y la de empleadores (casi la mitad del puntaje QS) cambian lentamente. Se mantiene como meta *aspiracional* del nivel B y la meta oficial queda en **QS ≤ 600** con la condición de estabilidad (no entrar y salir, como en 2023–2027).
2. **Top-10 de ingeniería en América Latina** (incluido Brasil) requiere multiplicar por 5,6 la producción de ingeniería: solo es alcanzable en el escenario global y probablemente después de 2036. **Top-10 hispanohablante** (×2,8) sí es alcanzable con la reforma hacia 2034–2036.
3. **El dinero no basta sin las personas**: el escenario global supone contratar 400 doctores en 10 años; el mercado peruano no los produce, por lo que depende de la repatriación, del posgrado propio (E3) y de las alianzas (E9). Si el reclutamiento no llega a 25 doctores/año en 2027–2029, la meta B se descarta en la evaluación de medio término (2032) y los recursos se concentran en el nivel A y los nichos del nivel C.
4. **Orden de magnitud**: el nivel B exige que el Estado aporte, en promedio, ≈ S/ 66 M/año adicionales de recursos ordinarios durante 11 años (≈ 2,8 veces la brecha de la reforma). Es una decisión de política nacional (MEF, CONCYTEC, Congreso), no solo de la UNI; el plan entrega el sustento y el tablero para pedirla.

---

## 3.7 Hipótesis contrastables

Trece hipótesis. Cada hipótesis dice qué debería pasar, cómo se mide y con qué dato se refuta. El Observatorio las evaluará en las fechas indicadas.

| # | Hipótesis | Medida y fecha | Se refuta si… | Datos |
|---|---|---|---|---|
| H1 | Si los concursos VRI usan evaluación externa y exigen producto a 24 meses, el número de obras por S/ 1 M concursado sube ≥ 50 %. | Obras atribuidas a proyectos VRI / S/ M; cohorte 2027 vs 2023–2025, medido en 2030 | el aumento es < 20 % | `vri-proyectos.json` + OpenAlex (título/autores) |
| H2 | Si se asignan horas reales de investigación a docentes con proyecto, el % de docentes con producción sube de 26,2 % a ≥ 35 % en la ventana 2024–2028. | `pct docentes con publicación` 2024–28, medido en 2029 | queda < 30 % | PTE × OpenAlex (`facultades-uni.json`) |
| H3 | Si la ejecución de capital sube a ≥ 85 % (2028), la inversión ejecutada crece ≥ 35 % sobre 2025 sin aumentar el PIM de capital en la misma proporción. | Devengado capital 2028 vs 2025 | devengado < S/ 62,6 M | MEF/SIAF |
| H4 | Si el 30 % del pago «otros» se condiciona a productos, el % de «otros» en la planilla docente baja a ≤ 25 % (2028) sin caída de la masa total docente real. | % «otros» en PTE, dic-2028 | % «otros» ≥ 28 % | PTE (`planilla-uni.json`) |
| H5 | Las facultades con mayor % de docentes TC publican más: la correlación (11 facultades) entre % TC y % docentes con producción es positiva y se mantiene al subir la dedicación. | Pearson/Spearman 2021–25 y 2026–30 | correlación ≤ 0 en ambas ventanas | `facultades-uni.json` |
| H6 | Si se contratan 15 doctores/año con concurso abierto, las nuevas contrataciones tienen ≥ 2× la producción de la media a 3 años de ingresar. | Obras por docente nuevo vs media institucional, 2030 | razón < 1,3 | PTE (fechas de ingreso, agregado) × OpenAlex |
| H7 | La ventanilla única eleva los fondos externos captados a ≥ S/ 12 M en 2028. | MEF/SIAF fuente DyT + resultados PROCIENCIA, 2028 | < S/ 8 M | MEF/SIAF; PROCIENCIA |
| H8 | Corregir la afiliación y exigir ORCID aumenta las obras registradas en OpenAlex ≥ 10 % en un año sin cambio real de producción (efecto de medición). | Obras 2027 vs 2026 con/ sin variantes de afiliación | aumento < 3 % | OpenAlex |
| H9 | Las acciones de equidad elevan el % de mujeres ingresantes a ≥ 22 % en 2028 sin bajar el puntaje medio de ingreso más de 5 %. | Ingresantes 2028-1 y 2028-2 | < 19 % o caída de puntaje > 5 % | `admision-uni.json` (microdatos) |
| H10 | La concentración de concursos VRI en tres facultades (64,3 %) baja a ≤ 50 % en 2027–2030 **sin** caída de la producción por S/ adjudicado (más mérito distribuido, no reparto). | % top-3 facultades y obras/S/ M | top-3 > 60 % o producción por S/ cae > 20 % | `vri-proyectos.json` + OpenAlex |
| H11 | El aumento del programa CTI a 6 % del PIM base (2031) se traduce en ≥ 1 000 obras/año en 2032 (rezago de un año). | Obras OpenAlex 2032 | < 800 | MEF/SIAF + OpenAlex |
| H12 | (Hipótesis del propietario) La ocupación de los edificios es < 40 %. Reformulada con método estándar: la **utilización de aulas** (frecuencia × ocupación) medida en 2027 es < 35 % y la **frecuencia** < 70 %; si es así, la programación central (E7.8) y el reúso (E7.7) llevan la utilización a ≥ 35 % con frecuencia ≥ 70 % en 2029 sin construir m² nuevos. | Auditoría de espacios (E7.5), 2027 y 2029 | la auditoría mide ya utilización ≥ 35 % y frecuencia ≥ 70 % en 2027 (la premisa es falsa: se levanta la moratoria 7.6) o, siendo baja, no llega a la meta en 2029 | Auditoría publicada por edificio |
| H13 | Separar trayectorias docentes eleva la producción sin bajar la calidad docente: en 2031 la trayectoria investigación (≈ 1/3 de docentes) concentra ≥ 70 % de las obras y las encuestas docentes de la trayectoria docencia mejoran. | Obras por trayectoria (agregado) y encuestas, 2031 vs 2028 | la producción total no crece o las encuestas caen | Datos abiertos UNI (agregados) + OpenAlex |

---

## 3.8 Riesgos y mitigaciones

| Riesgo | Prob. | Impacto | Mitigación |
|---|---|---|---|
| Resistencia interna a la evaluación con consecuencias | Alta | Alto | Rúbrica co-diseñada con docentes; piloto sin consecuencias en 2026; debido proceso y apelación; publicación solo agregada; reconocimiento económico a quien cumple (la evaluación premia, no solo sanciona) |
| Litigios y nulidades por procedimientos mal llevados | Media | Alto | Asesoría legal en el diseño; reglamento aprobado por Consejo Universitario; actas y motivación de cada decisión; nunca listas ni nombres públicos |
| Cambio de autoridades (ciclos electorales universitarios) y discontinuidad | Alta | Alto | Aprobación del plan por la Asamblea Universitaria; metas en el PEI/POI; comité de seguimiento con miembros externos y mandato que cruza gestiones |
| El MEF no amplía recursos ordinarios | Media | Alto | 58 % de la reforma no depende del MEF; priorizar ejecución y reasignación; programa presupuestal con metas físicas como argumento |
| Fondos externos por debajo de lo supuesto | Media | Medio | Ventanilla profesional; metas por facultad; sensibilidad publicada; reordenar prioridades de I+D |
| Inflación de indicadores (publicaciones de baja calidad, revistas depredadoras, autoría ficticia) | Media | Alto | Medir también impacto (citas, cuartiles), lista negra de revistas, verificación aleatoria, rúbrica que no premia solo cantidad |
| Ejecución de inversión trabada por compras e Invierte.pe | Alta | Alto | PMO; unidad de compras científicas; acuerdos marco; OxI para obras grandes |
| Fuga de talento por salarios no competitivos | Media | Alto | Bonificación RENACYT efectiva; fondos de inicio; mejores condiciones de laboratorio; doctorados industriales |
| Riesgos de datos personales al publicar | Baja | Alto | Solo agregados; anonimización; cumplimiento de la Ley 29733 |
| Captura de fondos por pocos grupos | Media | Medio | Pares externos; tope por investigador responsable; línea de arranque para facultades rezagadas |
| Trayectorias usadas como refugio (elegir «docencia» para evitar metas) | Media | Medio | Toda trayectoria tiene metas y consecuencias; cupos por facultad según plan; revisión a 3 años |
| Arrendamiento o cesión de espacios con riesgo legal o de captura privada | Media | Alto | Reglas del Sistema Nacional de Bienes Estatales; tarifa y contratos públicos; plazos cortos; prioridad a co-investigación; control del OCI |
| La premisa de ocupación < 40 % resulta falsa o mal definida | Media | Medio | Indicador definido con método estándar (frecuencia × ocupación); la auditoría decide; el plan no presupone el resultado (H12) |
| **Renovación de la licencia institucional SUNEDU** (vence ≈ noviembre de 2027) coincide con la fase de reformas | Media | Muy alto | Expediente preparado desde 2026 (táctica 4.0); no cerrar ni fusionar carreras durante el proceso sin coordinación con SUNEDU; usar el tablero como evidencia de mejora continua |
| Participación accionaria en spin-offs sin base legal | Alta | Alto | Usar licencias con regalías o un vehículo intermedio hasta que exista norma habilitante (10.2) |
| Desalineación con el PEI 2025–2030 vigente | Media | Medio | Incorporar metas de UNI 2036 al PEI en su actualización; mismo tablero para ambos |
| Ambición global sin financiamiento (nivel B) | Alta | Alto | Meta oficial = nivel A; nivel B solo se activa si se aprueba el RO adicional; decisión explícita en 2032 |
| Conflictos de interés en spin-offs y contratos con empresas | Media | Alto | Política de PI y conflicto de interés publicada; comité independiente en la OTT; declaraciones juradas |

## 3.9 Gobernanza del plan

- **Dueño político:** Rectorado; aprobación por Asamblea Universitaria e incorporación de las metas a 2030 al PEI 2025–2030 vigente (RR 0557-2025-UNI) en su próxima actualización, y al Plan Operativo Institucional (POI) cada año; el PEI 2031–2036 se formula en 2030 sobre la base de UNI 2036.
- **Dueño técnico:** Oficina de Planeamiento y Presupuesto con la nueva unidad de datos (E6.5) y la PMO (E6.4).
- **Comité de Seguimiento UNI 2036:** 7 miembros —2 docentes elegidos, 1 estudiante, 1 representante de egresados, 1 de la industria, 1 académico externo internacional y el jefe de planeamiento (secretario técnico)—; sesiona trimestralmente; actas públicas.
- **Reporte público anual (cada marzo):** avance de los 34 indicadores del tablero (25 principales + 10 complementarios), del PIM real frente a la trayectoria de reforma (§3.5) contra metas, ejecución de cada táctica, revisión de las 13 hipótesis, actualización de los escenarios financieros con el PIM real. Formato abierto (CSV/JSON) además de PDF.
- **Auditoría ciudadana:** el Observatorio UNI recalcula los indicadores con fuentes públicas independientes (MEF/SIAF, PTE, OpenAlex, OECE/CONOSCE, datosabiertos.gob.pe) y publica las discrepancias.
- **Evaluaciones externas:** medio término (2032) y final (2036), por un panel independiente; sus recomendaciones se responden por escrito.
- **Regla de ajuste:** las metas se pueden modificar solo una vez por fase, con justificación pública y sin rebajar una meta ya cumplida.

---

### Fuentes

- `data/presupuesto-uni.json` — MEF, Consulta Amigable y Datos Abiertos SIAF (api.datosabiertos.mef.gob.pe), pliego 514, 2012–2026.
- `data/planilla-uni.json` — Portal de Transparencia Estándar, rubro Personal (transparencia.gob.pe, id_entidad 10048), setiembre 2026; AIRHSP.
- `data/facultades-uni.json` — PTE × OpenAlex (ventana 2021–2025) × MEF/SIAF por meta × VRI.
- `data/vri-proyectos.json` — resoluciones rectorales y relaciones de proyectos del VRI (vri.uni.edu.pe), 2022–2026.
- `data/bibliometria.json` — OpenAlex (CC0), extraído 2026-06; QS (topuniversities.com / El Peruano); CONCYTEC; SUNEDU.
- `data/admision-uni.json` — Dirección de Admisión UNI; datosabiertos.gob.pe (microdatos 2021–2026); uni-admision-stats.
- `data/proveedores-uni.json` — OECE/CONOSCE, adjudicaciones 2023–2025.
- `app.js`, función `renderLid` — plan de seis ejes con metas a 2031 del Observatorio (base de este capítulo).
- Marco legal citado: Ley 30220 (arts. 83, 84, 86), Ley 29230 (obras por impuestos), Ley 29733 (datos personales).
- `02_referentes_gestion.md` (capítulo de referentes, secciones B.1, B.6, C.1–C.5): POLCTI al 2030 (DS 093-2025-PCM), PNESTP (DS 012-2020-MINEDU) y RVM 013-2022-MINEDU, DS 062-2024-PCM y DL 1727, reglamento docente investigador UNI (RR 1042-2020), DS 028-2026-EF, RR 3664-2024 (arrendamiento Sector V), Directiva DIR-00004-2022/SBN, Ley 32141, método de utilización de espacios (Bristol, THE), Startup UNI en la red ProInnóvate.
- Capítulo de diagnóstico: PEI 2025–2030 (RR 0557-2025-UNI); licencia SUNEDU RCD 073-2017-SUNEDU/CD; 34 carreras/11 facultades y fechas de creación; ABET (19 programas) y RIBA; Doctorado en Ciencias con beca PROCIENCIA (76 plazas, 2024); vacantes 2026-I; QS ediciones 2025–2027.
- Modelo financiero: `escenarios.py` / `escenarios.json` y `trayectoria_global.py` / `trayectoria_global.json` (esta carpeta).
- OpenAlex API, consultas del 2026-11-12: obras UNI 2021–2025 por percentil de citas, coautoría internacional y de empresa, campo temático; ranking latinoamericano en el campo «Engineering» (filtros `primary_topic.field.id:fields/22`, `institutions.country_code` de 13 países latinoamericanos, `group_by=institutions.id`).
- Marco nacional (§3.1.1): Ley 31250 (SINACTI); Política Nacional de CTI (CONCYTEC); Política Nacional de Educación Superior y Técnico-Productiva (MINEDU); Proyecto Educativo Nacional al 2036 (CNE); Visión del Perú al 2050 y Plan Estratégico de Desarrollo Nacional al 2050 (CEPLAN); Ley 29151 (Sistema Nacional de Bienes Estatales).
