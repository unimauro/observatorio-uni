# Hoja de ruta — Observatorio UNI

Portal ciudadano de transparencia de la Universidad Nacional de Ingeniería. Solo datos públicos.
Live: https://unimauro.github.io/observatorio-uni/ · Sugerencias: carlos@cardenas.pe

## ✅ Hecho (v1 — julio 2026)

- **Presupuesto histórico 2012–2026** del pliego 514 (PIA/PIM/Certificado/Devengado/Girado + % ejecución).
  Fuente: MEF Consulta Amigable (2012–2024) + SIAF Datos Abiertos (2025–2026). 2026 en ejecución (parcial).
- **En qué se gasta cada sol** (2025): por genérica (planilla, bienes y servicios, inversión, pensiones),
  categoría, unidad ejecutora (UNI + INICTEL) y función.
- **Presupuesto por facultad / escuela** (2025): 12 facultades con presupuesto etiquetado por meta SIAF.
- **Proveedores y dueños** (OECE/CONOSCE, 2023–2025): 338 proveedores, S/ 86.6M adjudicados.
  Ranking por monto y por nº de licitaciones, empresas vs. personas naturales/terceros,
  representantes/dueños con fuente, buscador. Lista de terceros que más ganaron.
- **Planilla** (Portal de Transparencia Estándar + AIRHSP, setiembre 2026): lista nominal completa con nombre, cargo,
  dependencia y desglose de ingresos — 2,124 personas / 2,130 registros (1,297 en «728/otros», el bucket donde el PTE lista a los docentes; 593 CAS; 240 DL 276),
  masa mensual S/ 10.7 M; serie mensual enero–setiembre 2026 por régimen (julio sube por aguinaldo); top cargos por
  ingreso; buscador + filtro por régimen; 1,717 docentes (agregado AIRHSP); cruce con la elección de autoridades 2026
  (los 27 candidatos figuran en la planilla, con badge y enlace a su perfil). ETL mensual idempotente. Nunca estudiantes.
- **Investigación** (OpenAlex): publicaciones, citas, h-index y UNI vs. pares.
- **Admisión**: 922 ingresantes / 5,713 postulantes (examen 2026-1) por especialidad y modalidad (solo agregados, sin nombres).
- **Admisión: serie histórica 2013–2026 (vía uni-admision-stats)** — postulantes e ingresantes por proceso (26 procesos),
  tasa de ingreso, % de mujeres, ciclo 2026-2 y proceso 2027-1 en curso. Fuente: datosabiertos.gob.pe + Dirección de Admisión UNI.
- **Elección de autoridades 2026 (resumen + enlace)** — cómputo 1.ª vuelta (16-10-2026) por lista, 2.ª vuelta Lista 8 vs Lista 1 (28-10-2026: nulidad parcial declarada por el CEUNI, sin resultado publicado) y feed "En los medios"
  (28-10-2026, resultado pendiente en la fuente), cronograma CEUNI y enlace al Observatorio Electoral UNI. Preliminar hasta proclamación.
- **Ecosistema** — sección con los sitios hermanos (electoral, admisión, gemelo digital, San Marcos, ENSAD, universidades-peru,
  Perú Transparente, poder económico), con fecha de última actualización de cada repo.
- **Gasto ↔ valor público** — eficiencia investigadora: costo por publicación (base I+D, la métrica justa),
  publicaciones por S/ 10M ejecutado, presupuesto por ingresante, y presupuesto vs. publicaciones por año
  (pedido de Tobías: "gasto vs. valor público generado").
- Asistente IA, barra de apoyo (WhatsApp/Yape/café), tema día/noche, Google Analytics, OG/SEO.

## 🔜 En cola (prioridad de valor)

1. **Órdenes de compra < 8 UIT** — cola larga de proveedores pequeños (dataset CONOSCE aparte),
   para completar el mapa de "a quién más le paga la UNI".
2. **Grafo proveedor → dueño** — cruzar los proveedores con el [observatorio de poder económico](https://unimauro.github.io/observatorio-poder-economico/)
   y profundizar dueños más allá del top 15.
3. **Serie histórica de proveedores** — extender contrataciones a años anteriores a 2023.
4. **Fuente de financiamiento** — desglose por fuente (recursos ordinarios / directamente recaudados / donaciones).
5. **Presupuesto por facultad multi-año** — evolución del presupuesto de cada facultad.
6. **Dimensionamiento de procesos vs. personal** — carga de procesos misionales vs. recursos (debate del grupo).

## 🧭 Ideas / por evaluar (necesitan fuente)

- **Aprobados / desaprobados por carrera** — rendimiento académico (requiere fuente pública; hoy no disponible).
- Empleabilidad / seguimiento de egresados.
- Ingresos propios y unidades de negocio (INICTEL, centro pre, posgrado) a mayor detalle.
- Export a Excel/PDF e internacionalización.

## Principios

- Solo información pública. **Nunca** nombres de estudiantes (los nombres solo corresponden a
  docentes/funcionarios/personal, tal como los publican las fuentes oficiales).
- Anti-overclaiming: cada cifra con su fuente y su alcance; los cruces se marcan con su nivel de certeza.
- No es un portal oficial de la UNI.
