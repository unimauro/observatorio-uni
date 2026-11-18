#!/usr/bin/env python3
"""Miembros de los órganos de gobierno y órganos autónomos de la UNI.

Genera data/organos-gobierno-uni.json a partir de fuentes oficiales:

* Portal del CEUNI (https://www.ceuni.uni.edu.pe/organos-de-gobierno-de-la-uni/):
  listas en PDF (texto) de representantes docentes y estudiantiles, decanos y
  autoridades, compartidas mediante enlaces públicos de OneDrive/SharePoint.
* La Gaceta N.º 232 (04-11-2026), proclamación de ganadores del CEUNI (PDF
  escaneado: transcrita a mano a partir de la imagen, ver TRANSCRITOS).
* Resoluciones rectorales y de Asamblea Universitaria publicadas en gob.pe
  (PDF con texto o leídas por OCR).
* Directorio de funcionarios de gob.pe (fecha de consulta 2026-11-18).
* Proclamaciones estudiantiles 2021-2025 del CEUNI (las de 2021-2023, desde
  copias del Internet Archive del portal anterior), La Gaceta N.º 209 (AU
  2025-2026, transcrita) y la publicación definitiva de candidaturas 2026.

Reglas: no se guarda DNI, código, teléfono ni correo; cada miembro lleva
fuente_url, fuente_fecha y fuente_tipo. Los nombres se copian tal como figuran
en la fuente (la mayoría en orden NOMBRES APELLIDOS).

Uso:
    python3 etl/build_organos_gobierno.py [--raw DIR] [--offline]

--raw     directorio de caché de los PDF descargados (por defecto
          ./.cache/organos_raw). Los PDF son datos no confiables: solo se leen
          con pdftotext.
--offline no descarga; usa lo que haya en --raw.
Requiere pdftotext (poppler) y curl.
"""
import argparse
import base64
import datetime as dt
import json
import os
import re
import subprocess
import sys
import time
import unicodedata

HOY = dt.date(2026, 11, 18)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "organos-gobierno-uni.json")
UA = "Mozilla/5.0 (observatorio-uni ETL)"

# ---------------------------------------------------------------- fuentes ---
SP_CEUNI = "https://uniedupe93141-my.sharepoint.com/:b:/g/personal/ceuni_uni_edu_pe/"
SP_INSC = "https://uniedupe93141-my.sharepoint.com/:b:/g/personal/inscripcionceuni_uni_edu_pe/"
F = {
    "ceuni_organos": "https://www.ceuni.uni.edu.pe/organos-de-gobierno-de-la-uni/",
    "doc_au": SP_CEUNI + "IQAc2zLZSSBNSIrNu0KWt5JZAY3d4ivwLtM52q9Bh_tlMhY?e=xDsaUx",
    "doc_cf": SP_CEUNI + "IQCBqCYwderOQJgZtIDHB3lUARpGGVIDOv4fZfHdV9g2EWY?e=YUT8Ze",
    "est_au": SP_CEUNI + "IQAVM64qBUt8QrR1EdZGl2YiAQZAKwNfixnAE1wui2CZ1qs?e=AMZEtV",
    "est_cf": SP_CEUNI + "IQAqUYXbt0MrRb8ncm89RbELAQmD7ZrocA2FJdPs0MCsrkw?e=NEaMDc",
    "est_cu": SP_CEUNI + "IQAJsLVAcPCzQLXBjQDfyculASiS_32zigRpbUf1ACpH6M8?e=Uwlnbh",
    "rect_folder": "https://uniedupe93141-my.sharepoint.com/:f:/g/personal/ceuni_uni_edu_pe/IgBGDPPK29DgSKkNiWuR1kbeAT-0sUz74LSURG4dUqauHXw?e=Ma5Ts7",
    "dec_folder": "https://uniedupe93141-my.sharepoint.com/:f:/g/personal/ceuni_uni_edu_pe/IgAwYmnQbZ6zTrFWGzo2_DCpAVhBFqxsYxa65tox1246YP8?e=WjB7As",
    "gaceta232": SP_INSC + "IQC2plyPK5BqSbPnsvsL76gAAfAbjNHzJf_vABQTe6W4x90?e=m4SaCc",
    "ceuni_2026_web": "https://www.ceuni.uni.edu.pe/comite-electoral-universitario-de-la-uni/",
    "ceuni_2025_web": "https://www.ceuni.uni.edu.pe/comite-electoral-universitario-de-la-uni-2/",
    "rr0183_2026": "https://cdn.www.gob.pe/uploads/document/file/9614531/7867608-0183-2026-uni.pdf",
    "rr0177_2025": "https://cdn.www.gob.pe/uploads/document/file/7714941/6527957-0177-2025-uni.pdf",
    "rr0020_2024": "https://cdn.www.gob.pe/uploads/document/file/5688274/5051474-resolucion-rectoral-nro-0020-2024-uni.pdf",
    "rr0047_2023": "https://cdn.www.gob.pe/uploads/document/file/5614716/4978961-resolucion-rectoral-nro-0047-2023-uni.pdf",
    "rr2657_2025": "https://cdn.www.gob.pe/uploads/document/file/9614853/7867828-2657-2025-uni.pdf",
    "rr0870_2024": "https://cdn.www.gob.pe/uploads/document/file/6956668/6001326-0870-2024.pdf",
    "rr2167_2023": "https://cdn.www.gob.pe/uploads/document/file/5677490/5039432-rr-2167-2023-uni.pdf",
    "rau0012_2026": "https://cdn.www.gob.pe/uploads/document/file/10665431/8629095-0012-2026-uni.pdf",
    "rr0817_2022": "https://cdn.www.gob.pe/uploads/document/file/5676480/5038728-r-r-n-0817-2022.pdf",
    "rr3398_2025": "https://cdn.www.gob.pe/uploads/document/file/9613404/7866874-3398-2025-uni.pdf",
    "rr0247_2025": "https://cdn.www.gob.pe/uploads/document/file/7715011/6527999-0247-2025-uni.pdf",
    "rr1865_2023": "https://cdn.www.gob.pe/uploads/document/file/5677515/5039452-rr-1865-2023-uni.pdf",
    "rr3999_2023": "https://cdn.www.gob.pe/uploads/document/file/5680822/5042068-rr-3999-2023.pdf",
    "rr0158_2025": "https://cdn.www.gob.pe/uploads/document/file/8031807/6745087-0158-2025-uni.pdf",
    "rr0549_2025": "https://cdn.www.gob.pe/uploads/document/file/8032027/6745225-0549-2025-uni.pdf",
    "rr0550_2025": "https://cdn.www.gob.pe/uploads/document/file/8032033/6745229-0550-2025-uni.pdf",
    "rr0551_2025": "https://cdn.www.gob.pe/uploads/document/file/8032048/6745240-0551-2025-uni.pdf",
    "rr0804_2025": "https://cdn.www.gob.pe/uploads/document/file/8032063/6745250-0804-2025-uni.pdf",
    "rau0020_2026": "https://cdn.www.gob.pe/uploads/document/file/10649133/8617961-0020-2026-uni.pdf",
    "rau0022_2026": "https://cdn.www.gob.pe/uploads/document/file/10649305/8618268-0022-2026-uni.pdf",
    "rr00002_2026i": "https://cdn.www.gob.pe/uploads/document/file/10974599/8833389-00002-2026-uni-i.pdf",
    "rau002_2026": "https://cdn.www.gob.pe/uploads/document/file/9609532/7864019-002-2026-uni.pdf",
    "rr1353_2021": "https://uniedupe93141-my.sharepoint.com/:f:/g/personal/ceuni_uni_edu_pe/IgBGDPPK29DgSKkNiWuR1kbeAT-0sUz74LSURG4dUqauHXw?e=Ma5Ts7",
    "rr1355_2021": "https://uniedupe93141-my.sharepoint.com/:f:/g/personal/ceuni_uni_edu_pe/IgAwYmnQbZ6zTrFWGzo2_DCpAVhBFqxsYxa65tox1246YP8?e=WjB7As",
    "gobpe_dir": "https://www.gob.pe/institucion/uni/funcionarios",
}

FAC_CANON = {
    # nombre (sin tildes, mayúsculas) -> sigla usada en el observatorio
    "ARQUITECTURA": "FAUA", "CIENCIAS": "FC", "AMBIENTAL": "FIA", "CIVIL": "FIC",
    "ECONOMICA": "FIECS", "ELECTRICA": "FIEE", "GEOLOGICA": "FIGMM",
    "INDUSTRIAL": "FIIS", "MECANICA": "FIM", "PETROLEO": "FIP", "QUIMICA": "FIQT",
}
SIGLA_CANON = {"FIPGNP": "FIP", "FIEECS": "FIECS", "FIECS": "FIECS"}


def sin_tildes(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def fac_de_titulo(t):
    u = sin_tildes(t.upper())
    for k, v in FAC_CANON.items():
        if k in u and not (k == "CIENCIAS" and "ECONOMICA" in u):
            return v
    return None


def sigla(s):
    s = s.strip().upper()
    return SIGLA_CANON.get(s, s)


def limpia(n):
    return re.sub(r"\s+", " ", n).strip()


# -------------------------------------------------------------- descargas ---
def curl(url, dest, cookie=None):
    cmd = ["curl", "-sL", "-m", "120", "-A", UA, "-o", dest]
    if cookie:
        cmd += ["-c", cookie, "-b", cookie]
    cmd.append(url)
    for intento in range(3):
        subprocess.run(cmd, check=False)
        if os.path.exists(dest) and open(dest, "rb").read(5) == b"%PDF-":
            return True
        if os.path.exists(dest):
            os.remove(dest)  # p. ej. "Internet Archive: Temporarily Offline"
        time.sleep(5 * (intento + 1))
    return False


def descarga_sp(url, dest):
    """Archivo compartido de OneDrive con enlace público (sin login)."""
    if os.path.exists(dest):
        return True
    ok = curl(url + "&download=1", dest, cookie=dest + ".cj")
    if not ok and os.path.exists(dest):
        os.remove(dest)
    return ok


def descarga_sp_carpeta(url, nombre, dest, raw):
    """Archivo dentro de una carpeta compartida públicamente (API v2 de shares)."""
    if os.path.exists(dest):
        return True
    cj = os.path.join(raw, "cj_folder.txt")
    subprocess.run(["curl", "-sL", "-m", "60", "-A", UA, "-c", cj, "-b", cj, "-o", os.devnull, url])
    tok = "u!" + base64.urlsafe_b64encode(url.encode()).decode().rstrip("=")
    api = "https://uniedupe93141-my.sharepoint.com/personal/ceuni_uni_edu_pe/_api/v2.0"
    out = subprocess.run(["curl", "-s", "-m", "60", "-A", UA, "-b", cj, "-H", "Accept: application/json",
                          f"{api}/shares/{tok}/driveItem/children?$select=name,id,parentReference"],
                         capture_output=True, text=True).stdout
    try:
        items = json.loads(out)["value"]
    except Exception:
        return False
    for it in items:
        if it["name"] == nombre:
            drv = it["parentReference"]["driveId"]
            return curl(f"{api}/drives/{drv}/items/{it['id']}/content", dest, cookie=cj)
    return False


def pdftext(path):
    if not os.path.exists(path):
        return ""
    return subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout


# ---------------------------------------------------------------- parsers ---
MAND = r"(\d{2}/\d{2}/\d{4}\s*-\s*\d?\s*\d{1,2}/\d{2}/\d{4})"


def mandato(s):
    s = re.sub(r"\s+", "", s).replace("-0", "-0")
    a, b = s.split("-", 1)
    return f"{a} - {b}"


def vig_por_fin(fin):
    d, m, y = map(int, fin.split("/"))
    return dt.date(y, m, d) >= HOY


def parse_doc_au(txt):
    out, acc = [], False
    for ln in txt.splitlines():
        if "ACCESITARIO" in ln.upper():
            acc = True
        m = re.match(r"^\s*\d+\s+(.+?)\s{2,}(PRINCIPAL|ASOCIADO|AUXILIAR)\s+(\S+)\s+\d{8}\s+" + MAND, ln)
        if m:
            out.append(dict(nombre=limpia(m.group(1)), categoria=m.group(2).lower(), facultad=sigla(m.group(3)),
                            accesitario=acc, mandato=mandato(m.group(4))))
    return out


def parse_por_facultad(txt, con_categoria):
    out, fac, acc = [], None, False
    for ln in txt.splitlines():
        if re.match(r"^\s*\d+\.\s+FACULTAD", ln):
            fac, acc = fac_de_titulo(ln), False
            continue
        if re.match(r"^\s*ACCESITARIO", ln.strip()):
            acc = True
            continue
        if con_categoria:
            m = re.match(r"^\s*\d+\s+(.+?)\s+\d{8}\s+(PRINCIPAL|ASOCIADO|AUXILIAR)\s+" + MAND, ln)
            if m:
                out.append(dict(nombre=limpia(m.group(1)), categoria=m.group(2).lower(), facultad=fac,
                                accesitario=acc, mandato=mandato(m.group(3))))
        else:
            m = re.match(r"^\s*(?:\d+\s+)?([A-ZÁÉÍÓÚÑ'][A-ZÁÉÍÓÚÑ' .]+?)\s+\d{8}\s+" + MAND, ln)
            if m:
                out.append(dict(nombre=limpia(m.group(1)), facultad=fac, accesitario=acc,
                                mandato=mandato(m.group(2))))
    return out


def parse_est_cu(txt):
    out, acc = [], False
    for ln in txt.splitlines():
        if "ACCESITARIO" in ln.upper():
            acc = True
        m = re.match(r"^\s*\d+\s+(.+?)\s{2,}(\S+)\s+\d{8}\s+" + MAND, ln)
        if m:
            out.append(dict(nombre=limpia(m.group(1)), facultad=sigla(m.group(2)), accesitario=acc,
                            mandato=mandato(m.group(3))))
    return out


# ----------------------------------- proclamaciones históricas (estudiantes) ---
SIG_RE = "FAUA|FC|FIA|FIC|FIEECS|FIECS|FIEE|FIGMM|FIIS|FIM|FIPGNP|FIP|FIQT|POSGRADO"
ROW_PROC = re.compile(
    r"^\s*(?:\d{1,2}\s+)?(?:\d{1,2}\s+)?"            # n.º y, a veces, n.º de lista
    r"([A-ZÁÉÍÓÚÑÜ][A-ZÁÉÍÓÚÑÜ'´, .\-]*?[A-ZÁÉÍÓÚÑÜ.])\s+"
    r"(?:(%s)\s+)?\d{8}(?:\s+(%s))?\s*$" % (SIG_RE, SIG_RE))


def parse_proclamacion_estudiantes(txt):
    """Secciones de representantes ESTUDIANTILES de una proclamación del CEUNI
    (PDF con texto). Devuelve (organo AU|CU|CF, facultad, accesitario, nombre).
    El DNI solo se usa como ancla de la fila y se descarta."""
    lines = txt.splitlines()
    out, org, fac, acc = [], None, None, False
    for i, ln in enumerate(lines):
        u = sin_tildes(ln.upper())
        nxt = sin_tildes(lines[i + 1].upper()) if i + 1 < len(lines) else ""
        if (re.match(r"^\s*([IVX]+|\d+)\.\s+(REPRESENTANTES|DECANO|RECTOR|LISTA)", u)
                or "LISTAS DE CANDIDATOS" in u or "AUTORIDADES Y MIEMBROS" in u):
            h = re.sub(r"\s+", " ", u + " " + nxt)
            org = None
            if "REPRESENTANTES" in h and "ESTUDIANT" in h:
                org = "AU" if "ASAMBLEA" in h else ("CF" if "FACULTAD" in h else "CU")
            fac, acc = None, False
            continue
        if org is None:
            continue
        if re.match(r"^\s*\d+\.\s+FACULTAD", u):
            fac, acc = fac_de_titulo(u + " " + nxt), False
            continue
        if "ACCESITARIO" in u:
            acc = True
            continue
        mm = ROW_PROC.match(ln)
        if mm:
            fa = mm.group(2) or mm.group(3)
            f = fac if org == "CF" else (None if fa in (None, "POSGRADO") else sigla(fa))
            out.append((org, f, acc, limpia(mm.group(1)), fa == "POSGRADO"))
    return out


ROW_LISTA = re.compile(r"(?:^|\s)(\d{1,2})\s+([A-ZÁÉÍÓÚÑÜ][A-ZÁÉÍÓÚÑÜ'´ .\-]*?[A-ZÁÉÍÓÚÑÜ])\s+(?:(%s)\s+)?\d{8}[A-Z]" % SIG_RE)


def parse_listas_candidatos(txt):
    """Publicación definitiva de candidaturas 2026 (columnas por lista).
    Devuelve (organo, facultad, lista, accesitario, nombre); el código de
    estudiante solo se usa como ancla y se descarta."""
    out, org, fac, cab, acc = [], None, None, [], {}
    for ln in txt.splitlines():
        u = sin_tildes(ln.upper())
        if re.match(r"^\s*[IVX]+\.\s+", u):
            org = ("AU" if "ASAMBLEA" in u else "CU" if "CONSEJO UNIVERSITARIO" in u
                   else "CF" if "CONSEJOS DE FACULTAD" in u else None) if "ESTUDIANT" in u else None
            fac, cab, acc = None, [], {}
            continue
        if org is None:
            continue
        if re.match(r"^\s*\d+\s+FACULTAD", u):
            fac, cab, acc = fac_de_titulo(u), [], {}
            continue
        hs = [(mm.start(), int(mm.group(1))) for mm in re.finditer(r"LISTA\s+(\d+)", u)]
        if hs:
            cab, acc = hs, {}
            continue
        if "ACCESITARIO" in u:
            for k in range(len(cab)):
                acc[k] = True
            continue
        for mm in ROW_LISTA.finditer(ln):
            k = max(0, sum(1 for pos, _ in cab if pos < mm.start() + 40) - 1)
            lista = cab[k][1] if cab else None
            fa = mm.group(3)
            f = fac if org == "CF" else (None if fa in (None, "POSGRADO") else sigla(fa))
            out.append((org, f, lista, acc.get(k, False), limpia(mm.group(2)), fa == "POSGRADO"))
    return out


WB = "https://web.archive.org/web/{ts}/https://www.ceuni.uni.edu.pe/images/{p}"
# (clave, url, archivo, fecha de la fuente, periodo, descripción, nota)
PROC_EST = [
    ("p2021", WB.format(ts="20220301221232", p="CEUNI2021/PROCLAMACIN-DE-GANADORES.pdf"), "2021-11-03",
     "2021-2022", "elección general del 26-10-2021",
     "Copia archivada (Wayback Machine) del PDF que el CEUNI publicó en su portal anterior."),
    ("p2022c", WB.format(ts="20230119065609", p="CEUNI2022/RESULTADOS-Y-PROCLAMACIN-DEL-ESCRUTINIO.pdf"), "2022",
     "2021-2022", "elección complementaria de 2022; ciclo inferido por la fecha",
     "Copia archivada del portal anterior del CEUNI; el PDF no trae fecha (incluye la 1.ª vuelta de decano FAUA 2022)."),
    ("p2022", WB.format(ts="20230119070015", p="CEUNI2022/PROCLAMACIN-DEL-ESCRUTINIO.pdf"), "2022-11-11",
     "2022-2023", "elección general del 04-11-2022", "Copia archivada del portal anterior del CEUNI."),
    ("p2023c", WB.format(ts="20250124174442", p="CEUNI2023/Resultado-unin.pdf"), "2023-06-02",
     "2022-2023", "elección complementaria del 26-05-2023; ciclo inferido por la fecha", "Copia archivada del portal anterior del CEUNI."),
    ("p2023", WB.format(ts="20250124174442", p="CEUNI2023/elecciones2023/PROCLAMACIN-DEL-GANADORES.pdf"), "2023-10-19",
     "2023-2024", "elección general del 13-10-2023",
     "Copia archivada del portal anterior del CEUNI. Esta elección no incluyó representantes estudiantiles ante la AU."),
    ("p2024c", SP_INSC + "IQDFY966fc7ISq0YDPCNBfVKAZFIEg8sTqrCUKsQ7aIC8OU?e=mehOlM", "2024-05-27",
     "2023-2024", "elección complementaria del 22-05-2024; ciclo inferido por la fecha", None),
    ("p2024", SP_INSC + "IQDELnB_ZutpSrDrvsopSiJyAZMyd_YFiBp6OwobRzO2Zpc?e=lemmoX", "2024-12-10",
     "2024-2025", "elección general del 04-12-2024",
     "La proclamación no trae la lista de la FIC ante su consejo de facultad (se eligió en la complementaria de mayo de 2025)."),
    ("p2025c", SP_INSC + "IQAS7LKdfgSjR5wN8lmhhdb1AemP35h54Cks6ypPbH9CtPY?e=MZhlRK", "2025-05-20",
     "2024-2025", "elección complementaria del 20-05-2025; ciclo inferido por la fecha", None),
]
F["gaceta209"] = SP_INSC + "IQDKk8HcTSOzQYjeULfmNCi7AWfkaRCDcCTx4Dqrq2wzzJI?e=dAWhsA"
F["listas2026"] = SP_INSC + "IQBRw9W2xYWUTZg6mpLG_sGOAVQe74SZriNxHssGNuYc_ro?e=dah4ex"
F["ceuni2021"] = WB.format(ts="20220302025203", p="CEUNI2021/Comunicado-nuevo-ceuni-GACETA.pdf")

# La Gaceta N.º 209 (27-10-2025) es un PDF escaneado; la pág. 03 (estudiantes
# ante la AU 2025-2026) se transcribe a mano. Las demás páginas coinciden con
# las listas en texto del CEUNI ya cargadas (CU y consejos de facultad).
G209_AU = [
    ("FRANCO RAFAEL ESPINOZA ALVARADO", "FIEE"), ("VALERIA CALDERON GUEVARA", "FC"),
    ("ALANIS AMANDA MERMA MUÑOZ", "FIGMM"), ("JOHANN DANIEL RIOS SANTIAGO", "FIEE"),
    ("ADRIAN ALONSO RIOS HERRERA", "FIECS"), ("EINSTEIN DILFREDO PEREZ MENA", "FIP"),
    ("DIEGO FELIX SOTELO JUAREZ", "FIIS"), ("JESUS ANDRES TOMAS RAMIREZ", "FIP"),
    ("ANGEL SEBASTIAN ALFARO VASQUEZ", "FIM"), ("CLIF JEFFERSON ALVAREZ GALVAN", "FIM"),
    ("KEVIN BRAYAMS SORIANO FERNANDEZ", "FIC"), ("NOELIA SOFIA ROJAS AVILA", "FIGMM"),
    ("FABRICIO WASHINGTON PECEROS MALLMA", "FAUA"), ("ROCIO NICOL OBISPO CARRILLO", "FAUA"),
    ("JOSE MARTIN ROJAS SANCHEZ", "FIIS"), ("ALDAIR ALESSANDRO LARA GIRALDO", "FIA"),
    ("ANTHONY DANIEL GALLEGOS GUERRERO", "FIA"), ("JOSE MANUEL RAMIREZ OSCCO", "FIC"),
    ("FLAVIA FERNANDA CAVERO BENITES", "FC"), ("JERAMYR URIEL CHAVEZ QUISPE", "FIECS"),
    ("REYMUNDO JESUS VILCAPOMA HUALPA", "FIQT"), ("ARNOLD BRANDON BETTETA CAMPOS", "FIQT"),
    ("ELVIS FRANZ HUANCHI MAMANI", "POSGRADO"),
]
G209_AU_ACC = [
    ("ARIANNA MICAELA YAURI AZABACHE", "FIEE"), ("EDDY ANTONY CHUQUIMAMANI PALOMINO", "FIC"),
    ("ANTONIO FERNANDO ESPINOZA ROCHA", "FIP"), ("JESUS ALESANDRO VELEZ DE VILLA SANTIAGO", "FAUA"),
    ("JUAN MATIAS COSTERIAL TIMANA", "FIECS"), ("JOSUA CARIN CANCAPA LUQUE", "FIQT"),
    ("EDGAR ALONSSO HUAYTA TTITO", "FIIS"),
]
# Comunicado del CEUNI (06-04-2021): conformación 2021. La fuente no indica el
# estamento de cada integrante.
CEUNI_2021 = [("ANTONIO NOLBERTO LAZO JARA", "presidente"), ("LUÍS ALBERTO MOSQUERA LEIVA", "vicepresidente"),
              ("LEANDRO JOSUE GAMEZ RAMOS", "secretario"), ("ABEL ELIAS TORRES MORA", "prosecretario"),
              ("MODESTO TOMÁS PALMA GARCÍA", "relator"), ("CARLOS EDUARDO ARÁMBULO OSTOS", "vocal"),
              ("OSCAR GUILLERMO MIRANDA HOSPINAL", "vocal"), ("LEOPOLDO PAREDES SORIA", "vocal"),
              ("RENZO GILBERT AQUINO JULCARIMA", "vocal")]


# ------------------------------------------------------------ transcritos ---
# La Gaceta N.º 232 (04-11-2026) es un PDF escaneado. Transcripción manual de
# las páginas 03-08 (se omiten los códigos de estudiante).
G232_AU = [  # (nombre, facultad) titulares; luego accesitarios
    ("JHOHAN DAVID RUIZ ALFARO", "FIA"), ("LUCIANA PAOLA VARA SOLORZANO", "FIEE"),
    ("EDWARD JAVIER OLIVA LLUEN", "FIIS"), ("VICTOR PAÚL RODRIGUEZ CABRERA", "FIEE"),
    ("JENNIFER KATHERINE VARGAS BAJONERO", "FIP"), ("AXEL BRAIN PINCHI CACHI", "FIM"),
    ("FERNANDO JEANPIER PACHECO SANCHEZ", "FIC"), ("GIORDANO DANIEL MEDRANO CANGALAYA", "FC"),
    ("BELEN RUTH GONZALES SOLES", "FIQT"), ("ALVARO FABRICIO NUÑEZ RIVAS", "FIIS"),
    ("GUADALUPE ANTHUANET MIGUEL COLAN", "FIECS"), ("STHEFANNY NUZAT RIQUE GARCIA", "FAUA"),
    ("SANDRO SEBASTIAN CASTILLO ALARCON", "POSGRADO"), ("ALEJANDRO MANUEL ROMAN JULCA", "FIGMM"),
    ("JUNIOR JUAN PORRAS ESPINOZA", "FIGMM"), ("MAYLY SOFIA ZAPATA MENDOZA", "FIA"),
    ("SUGEY ELIA CAQUI RAMIREZ", "FIQT"), ("EDMERSON HEIDER POLO VALVERDE", "FAUA"),
    ("ANDRE EMANUEL BACA TAIPE", "FIM"), ("LUCERO RAQUEL BALDEON MACHAHUAY", "FIC"),
    ("JAMES ALLAN JARA FUSTAMANTE", "FIECS"), ("JOSE CARLOS MATIAS MUÑOZ", "FC"),
    ("FLAVIO LUIS TAMAYO VELASQUEZ", "FIP"),
]
G232_AU_ACC = [
    ("RICHARD GIANLUCA VALDEZ BARRETO", "FIM"), ("VALERIA ELIZABETH BENAVIDES PALOMINO", "FIA"),
    ("ANDREA ISABEL CHAVEZ INCHE", "FIECS"), ("PIERO RODRIGUEZ RIOS", "FIA"),
    ("MIGUEL GABRIEL CAPCHA VIGILIO", "FIIS"), ("YAMIL DYLAN AUCCA QUISPE", "FC"),
]
G232_CU = [("CESAR JESUS GOMEZ ROJAS", "FIM"), ("CRISTHIAN SAMUEL MORILLO ZAVALETA", "FIEE"),
           ("JOSE ANTONIO GUTIERREZ SARAVIA", "FIC"), ("NELSON MIGUEL BEJAR CALLAÑAUPA", "FIA")]
G232_CU_ACC = [("ADRIAN ALONSO RIOS HERRERA", "FIECS"), ("ANTONY BRAYAN PÉREZ SALVATIERRA", "FIA"),
               ("MARIA FERNANDA EVANGELISTA AGUEDO", "FIEE"), ("MARIA GABRIELA TRINIDAD JORGE QUISPE", "FIIS")]
G232_CF = {  # facultad: (titulares, accesitarios)
    "FAUA": (["ALEXANDER ORTIZ PEREZ", "GREICY MENESES CHAVEZ", "CAMILA YULIANA CHOQUE CHIPANA"],
             ["JHORDAN ALEXIS LEANDRO SALAZAR", "ANGHELY ESMERALDA RIOS LUQUE", "BENJAMIN CHRISTOPH SULCA TAYPE"]),
    "FC": (["ALEJANDRO OSWALDO NEYRA OTOYA", "VICTOR JESÚS POMACAJA HERNANDEZ", "FABIANA BELEN ZUÑIGA ENRIQUEZ"],
           ["HENRY CHRISTIAN FERREYRA CORDERO", "LUIS FERNANDO FLORES ALBITES", "VALENTINO JAIR PÉREZ MELO"]),
    "FIA": (["DIEGO ARMANDO DAVILA JUAREZ", "SEBASTIAN FELIPE RAMOS GUEVARA", "DANIEL FERNANDO SALVATIERRA GONZALEZ"],
            ["JOSÚE ABRAHAM MAGUIÑA PALIÁN", "STEFANO MILLER PILCO CAYCHO", "CANTUTA AZUCENA MARIANA VILLAFRANCA SOLIS"]),
    "FIC": (["ALEJANDRO JESUS PACASE DE LA CRUZ", "JHEREMIN SANDRO LUCAS JESUS", "DIEGO ARMANDO MAMANI PALOMINO"],
            ["ANGIE SAYURI LLACCHUA ORTEGA", "STEFANNY FABIANA MILIANO GAMBOA", "KEVEIN GARCIA ESTRADA"]),
    "FIECS": (["JHOSADAC HELFER MOLINA LOJA", "BRYAN DAMIAN DE LA CRUZ MUNAYCO", "LIZ LORENA FERNANDEZ CAPANI"],
              ["POOL DANNY LIMACHI MAMANI", "JOAQUIN MATIAS LOPEZ OCAMPO", "KEVIN LUIS CORNEJO ATUNGA"]),
    "FIEE": (["DAVID ORLANDO QUISPE QUIROZ", "DIEGO SEBASTIAN INCIO GARCIA", "FLAVIO CESAR GARCIA FERRER"],
             ["KATHERINE XIMENA BRAVO FALCON", "LESLY VALESKA HILARIO SALAS", "VALERIA MERCEDES SOLIS CORDOVA"]),
    "FIGMM": (["JHORDAN JERSON MELÉNDEZ BLAS", "JHONNY MOISES BAZALAR HERRERA", "BRENER BRANDON CUEVA RIVERA"],
              ["PAUL ELIAS HERRERA VARGAS", "ADELI MABEL RICRA MIRANDA", "LEYDI CORNEJO PANTALEON"]),
    "FIIS": (["BALLACK ZIDANE QUINTANILLA HUAMANRAIME", "CAMILA NICOLE RUPAY RODRIGUEZ", "THALIA AYLINE VARGAS SILVA"],
             ["ROBINSON FRANCO MALAVER URETA", "PERCY SAUL MENDOZA OSCANOA"]),
    "FIM": (["GIAN PIERO JUAN BLAS MORALES", "ROSA ILLARI ZARATE MANCHAY", "ZACKARY MARTIN FERRER BALTAZAR"],
            ["LUIS CHRISTOPHER ZEGARRA RUIZ", "DIEGO LEANDRO MARTINEZ DIEZ", "JESUS EMMANUEL VILLADEZA SANCHEZ"]),
    "FIP": (["EINSTEIN DILFREDO PÉREZ MENA", "CARLOS JOAQUIN IZQUIERDO GUERRERO", "NICOLE XIOMARA BLAS MORALES"],
            ["CARLOS JOAQUIN IZQUIERDO GUERRERO", "NICOLE XIOMARA BLAS MORALES", "NICOLAS DAVID ALVARADO MUÑOZ"]),
    "FIQT": (["FRANCESCO RENATO LEANDRO SANDOVAL", "ANDY GABRIEL TERAN SIERRA", "JAIRO MATHIAS CCUNO ESTEBA"],
             ["ANGEL EDUARDO NOE PERLA", "NAOMI JENNY BALDEON PORRAS", "ANTHONY ELIAS ARAUJO SANTOS"]),
}

# Decanos según la tabla "DECANOS" (2025-2029.pdf) de la carpeta del CEUNI
# (PDF con texto, creado 05-05-2026); el script la vuelve a leer si está.
DECANOS_CEUNI = [
    ("FAUA", "Dr. ROSARIO ALICIA PACHECO ACERO", "04.12.2023 – 03.12.2027"),
    ("FC", "Dr. HERIBERTO ABRAHAM SANCHEZ CÓDOVA", "13.11.2023 – 12.11.2027"),
    ("FIA", "Dr. MARIO ARISTIDES CHAVEZ MUÑOZ", "13.11.2023 – 12.11.2027"),
    ("FIC", "Dr. MIGUEL LUIS ESTRADA MENDOZA", "09.08.2025 – 08.08.2029"),
    ("FIECS", "Ing. LUIS CABEZAS (a.i)", "Autoridad interina"),
    ("FIEE", "M.Sc. TRINI SANDRO CASTILLO BELSUZARRI", "Autoridad interina"),
    ("FIGMM", "Dr. ALBERTO LANDAURO ABANTO", "13.11.2023 – 12.11.2027"),
    ("FIIS", "Dra. MERY NOEMI MORALES CUELLAR", "13.11.2023 – 12.11.2027"),
    ("FIM", "Dr. TITO ROBERTO VILCHEZ VILCHEZ", "13.11.2023 – 12.11.2027"),
    ("FIP", "MSc. EDGAR ARGUME CHÁVEZ", "31.07.2023 – 30.07.2027"),
    ("FIQT", "Mag. WARREN REATEGUI ROMERO", "12.11.2025 – 11.11.2029"),
]


# ------------------------------------------------------------- utilidades ---
def m(nombre, organo, facultad, estamento, cargo, periodo, vigente, url, fecha, tipo, estado=None, nota=None):
    r = dict(nombre=nombre, organo=organo, facultad=facultad, estamento=estamento, cargo=cargo,
             periodo=periodo, vigente=vigente, fuente_url=url, fuente_fecha=fecha, fuente_tipo=tipo)
    if estado is None:
        estado = {True: "en_funciones", False: "concluido", None: "incierto"}[vigente]
    r["estado"] = estado
    if nota:
        r["nota"] = nota
    return r


def build(raw, offline):
    os.makedirs(raw, exist_ok=True)
    P = lambda n: os.path.join(raw, n)
    if not offline:
        for k in ("doc_au", "doc_cf", "est_cf", "est_cu", "est_au"):
            descarga_sp(F[k], P(k + ".pdf"))
        descarga_sp_carpeta(F["dec_folder"], "2025-2029.pdf", P("decanos.pdf"), raw)
        descarga_sp_carpeta(F["rect_folder"], "AUTORIDADES UNIVERSITARIAS.pdf", P("autoridades.pdf"), raw)
        for k in ("rr0183_2026", "rr3398_2025", "rr0247_2025", "rr2657_2025", "rau0012_2026"):
            curl(F[k], P(k + ".pdf"))

    M = []
    notas = []
    AU, CU, CEU = "Asamblea Universitaria", "Consejo Universitario", "Comité Electoral Universitario (CEUNI)"
    CF = "Consejo de Facultad"

    # --- Docentes ante la AU (2024-2027) ------------------------------------
    doc_au = parse_doc_au(pdftext(P("doc_au.pdf")))
    for r in doc_au:
        fin = r["mandato"].split(" - ")[1]
        M.append(m(r["nombre"], AU, r["facultad"], "docente",
                   ("accesitario" if r["accesitario"] else "miembro titular") + f" (profesor {r['categoria']})",
                   r["mandato"], vig_por_fin(fin), F["doc_au"], "2025-10-01", "proclamacion"))
    # --- Docentes ante los consejos de facultad (2024-2027) ------------------
    doc_cf = parse_por_facultad(pdftext(P("doc_cf.pdf")), True)
    for r in doc_cf:
        fin = r["mandato"].split(" - ")[1]
        nota = None
        if r["nombre"] == "NESTOR DAVID CORDOVA ROJAS":
            nota = "La fuente lo consigna dos veces en FIGMM: como titular (mandato 23/01/2024-12/11/2027) y como accesitario."
        if r["nombre"] == "JORGE CARMELO RAMOS CARRION":
            nota = "En la fuente su DNI coincide con el de otro docente de la lista de la AU; posible error de digitación del CEUNI (no afecta el nombre)."
        M.append(m(r["nombre"], CF, r["facultad"], "docente",
                   ("accesitario" if r["accesitario"] else "miembro titular") + f" (profesor {r['categoria']})",
                   r["mandato"], vig_por_fin(fin), F["doc_cf"], "2026-05-05", "proclamacion", nota=nota))
    # --- Estudiantes ante el CU (2025-2026) ----------------------------------
    for r in parse_est_cu(pdftext(P("est_cu.pdf"))):
        fin = r["mandato"].split(" - ")[1]
        M.append(m(r["nombre"], CU, r["facultad"], "estudiante",
                   "accesitario" if r["accesitario"] else "miembro titular (tercio estudiantil)",
                   r["mandato"], vig_por_fin(fin), F["est_cu"], "2026-03-03", "proclamacion"))
    # --- Estudiantes ante los CF (2025-2026) ---------------------------------
    for r in parse_por_facultad(pdftext(P("est_cf.pdf")), False):
        fin = r["mandato"].split(" - ")[1]
        M.append(m(r["nombre"], CF, r["facultad"], "estudiante",
                   "accesitario" if r["accesitario"] else "miembro titular (tercio estudiantil)",
                   r["mandato"], vig_por_fin(fin), F["est_cf"], "2026-03-03", "proclamacion"))
    if not os.path.exists(P("est_au.pdf")):
        notas.append("La lista 'Representantes estudiantiles ante la Asamblea Universitaria' (periodo 2025-2026) del portal "
                     "del CEUNI devuelve 'no puede acceder a este documento' (enlace restringido): no se registran sus miembros vigentes.")

    # --- Electos 2026 (La Gaceta 232, proclamación del 04-11-2026) ----------
    per26 = "2026-2027 (proclamados el 04-11-2026; la fecha de inicio no consta en la proclamación)"
    g = F["gaceta232"]
    for lst, acc in ((G232_AU, False), (G232_AU_ACC, True)):
        for n, f in lst:
            est = "estudiante"
            M.append(m(n, AU, None if f == "POSGRADO" else f, est,
                       ("accesitario" if acc else "miembro titular (tercio estudiantil)") + (" – posgrado" if f == "POSGRADO" else ""),
                       per26, False, g, "2026-11-04", "proclamacion", estado="electo_por_asumir"))
    for lst, acc in ((G232_CU, False), (G232_CU_ACC, True)):
        for n, f in lst:
            M.append(m(n, CU, f, "estudiante", "accesitario" if acc else "miembro titular (tercio estudiantil)",
                       per26, False, g, "2026-11-04", "proclamacion", estado="electo_por_asumir"))
    for f, (tit, acc) in G232_CF.items():
        for lst, a in ((tit, False), (acc, True)):
            for n in lst:
                nota = None
                if f == "FIP" and n in ("CARLOS JOAQUIN IZQUIERDO GUERRERO", "NICOLE XIOMARA BLAS MORALES"):
                    nota = "La proclamación lo consigna a la vez como titular y como accesitario de la FIP (error material de la fuente)."
                M.append(m(n, CF, f, "estudiante", "accesitario" if a else "miembro titular (tercio estudiantil)",
                           per26, False, g, "2026-11-04", "proclamacion", estado="electo_por_asumir", nota=nota))

    # --- Estudiantes 2021-2025 según las proclamaciones del CEUNI -------------
    # (reemplaza la inferencia anterior de la AU 2024-2025 a partir de las RR de
    # comisiones: la proclamación del 10-12-2024 trae la lista completa)
    ORG = {"AU": AU, "CU": CU, "CF": CF}
    for clave, url, fecha, periodo, desc, nota_src in PROC_EST:
        dest = P(clave + ".pdf")
        if not offline and not os.path.exists(dest):
            if "web.archive.org" in url:
                curl(url.replace("/https://", "id_/https://", 1), dest)
            else:
                descarga_sp(url, dest)
        filas = parse_proclamacion_estudiantes(pdftext(dest))
        if not filas:
            notas.append(f"No se pudo leer la proclamación {desc} ({url}).")
        for org, f, acc, n, posg in filas:
            cargo = ("accesitario" if acc else "miembro titular (tercio estudiantil)") + (" – posgrado" if posg else "")
            M.append(m(n, ORG[org], f, "estudiante", cargo, f"{periodo} ({desc})", False, url, fecha,
                       "proclamacion", nota=nota_src))
    # AU 2025-2026 (La Gaceta 209, transcrita a mano)
    for lst, acc in ((G209_AU, False), (G209_AU_ACC, True)):
        for n, f in lst:
            M.append(m(n, AU, None if f == "POSGRADO" else f, "estudiante",
                       ("accesitario" if acc else "miembro titular (tercio estudiantil)") + (" – posgrado" if f == "POSGRADO" else ""),
                       "2025-2026 (elección general del 21-10-2025)", True, F["gaceta209"], "2025-10-27", "proclamacion",
                       nota="La Gaceta N.° 209, pág. 03 (PDF escaneado, transcrito a mano). Mandato no indicado en la fuente; "
                            "se asume el de los demás representantes estudiantiles 2025-2026 (10/12/2025 - 09/12/2026)."))

    # --- Candidatos estudiantiles 2026 (publicación definitiva de candidaturas) ---
    dest = P("listas2026.pdf")
    if not offline and not os.path.exists(dest):
        descarga_sp(F["listas2026"], dest)
    for org, f, lista, acc, n, posg in parse_listas_candidatos(pdftext(dest)):
        M.append(m(n, ORG[org], f, "estudiante",
                   "candidato" + (" accesitario" if acc else " titular") + (f" – Lista {lista}" if lista else "") + (" – posgrado" if posg else ""),
                   "elección general 2026 (votación del 16-10-2026)", False, F["listas2026"], "2026-10-01",
                   "proclamacion", estado="candidato",
                   nota="Publicación definitiva de candidaturas del CEUNI; no implica que haya sido elegido (ver filas 'electo_por_asumir')."))

    # --- CEUNI 2021 (comunicado del 06-04-2021) ------------------------------
    for n, c in CEUNI_2021:
        M.append(m(n, CEU, None, "otro", c, "2021 (desde el 05-04-2021)", False, F["ceuni2021"], "2021-04-06", "proclamacion",
                   nota="Comunicado del CEUNI (copia archivada del portal anterior). La fuente no indica si cada integrante es docente o estudiante."))

    # --- Autoridades ---------------------------------------------------------
    gob, gobf = F["gobpe_dir"], "2026-11-18"
    for org in (AU, CU):
        M.append(m("Dr. Ing. Alberto Landauro Abanto", org, None, "autoridad", "rector interino (preside)",
                   "desde 2026-11-12 (sucesión por Ley N.° 32418, decano más antiguo)", True,
                   F["rr00002_2026i"], "2026-11-13", "resolucion",
                   nota="El directorio de gob.pe lo registra como 'Rector (i)' con fecha de inicio 12-11-2026."))
        M.append(m("Dr. ARTURO FERNANDO TALLEDO CORONADO (a.i.)", org, None, "autoridad", "rector (a.i.)",
                   "hasta 11/11/2026", False, F["rect_folder"], "2026-05-05", "portal",
                   nota="Fuente: 'AUTORIDADES UNIVERSITARIAS.pdf' (CEUNI). Designado por RR 1315-2025-UNI tras la renuncia del rector."))
        M.append(m("Dra. ROCIO MARGARITA CACHO CRUZ (a.i.)", org, None, "autoridad", "vicerrectora académica (a.i.)",
                   "hasta 11/11/2026", False, F["rect_folder"], "2026-05-05", "portal",
                   nota="Designada por RR 002-2026-UNI. En set-2026 la RAU 0020-2026-UNI designó a otra persona en el cargo; hubo disputa judicial."))
        M.append(m("Dr. JORGE GUSTAVO BUTLER BLACKER (a.i.)", org, None, "autoridad", "vicerrector de investigación (a.i.)",
                   "hasta 11/11/2026", False, F["rect_folder"], "2026-05-05", "portal",
                   nota="En set-2026 la RAU 0022-2026-UNI designó a otra persona en el cargo; hubo disputa judicial."))
        M.append(m("Dr. JOSÉ CARLOS MATÍAS LEÓN", org, None, "autoridad", "vicerrector académico interino (designado por la AU)",
                   "16/09/2026 - 11/11/2026", False, F["rau0020_2026"], "2026-09", "resolucion",
                   nota="Designación en el contexto del rectorado interino disputado de setiembre de 2026."))
        M.append(m("Dr. WARREN REATEGUI ROMERO", org, None, "autoridad", "vicerrector de investigación interino (designado por la AU)",
                   "16/09/2026 - 11/11/2026", False, F["rau0022_2026"], "2026-09", "resolucion",
                   nota="Designación en el contexto del rectorado interino disputado de setiembre de 2026."))
        for n, c in (("Dr. PABLO ALFONSO LOPEZ CHAU NAVA", "rector"),
                     ("Dra. SHIRLEY EMPERATRIZ CHILET CAMA", "vicerrectora académica"),
                     ("Dr. ARTURO FERNANDO TALLEDO CORONADO", "vicerrector de investigación")):
            M.append(m(n, org, None, "autoridad", c, "12/11/2021 - 11/11/2026 (elegido; ver notas)", False,
                       F["rr1353_2021"], "2021", "resolucion",
                       nota="RR 1353-2021 (archivo en la carpeta 'RECTOR Y VICERRECTORES' del CEUNI). El mandato no se completó: hubo renuncia y encargaturas en 2025."))
        M.append(m("Víctor Antonio Caicedo Bustamante", org, None, "autoridad", "director (e) de la Escuela de Posgrado",
                   "vigente al 2026-11-18", True, gob, gobf, "portal",
                   nota="Integra el órgano por ser director de la Escuela de Posgrado (Ley 30220, arts. 56 y 58)."))

    # --- Decanos (AU: todos; CF: presiden; CU: solo 1/4 elegidos entre ellos, sin fuente) ---
    dec_txt = pdftext(P("decanos.pdf"))
    gob_fiqt = ("Walter Fernando Zaldivar Alvarez", "desde 2026-09-16")
    for fac, n, per in DECANOS_CEUNI:
        vig, nota, url, fe, tipo = True, None, F["dec_folder"], "2026-05-05", "portal"
        if dec_txt and sin_tildes(n.split(" ", 1)[1][:15]).upper() not in sin_tildes(dec_txt).upper():
            nota = "Ya no figura en la versión actual de la tabla de decanos del CEUNI; revisar."
        if fac == "FIQT":
            vig, nota = None, ("La RAU 0022-2026-UNI lo designó vicerrector de investigación interino (16-09 a 11-11-2026); "
                               "el directorio de gob.pe registra a Walter Fernando Zaldivar Alvarez como decano desde 16-09-2026.")
        if fac == "FIGMM":
            vig, nota = None, "Asumió el rectorado interino el 12-11-2026; gob.pe lo sigue listando también como decano."
        for org, cargo in ((CF, "decano (preside)"), (AU, "decano (miembro nato)")):
            M.append(m(n, org, fac, "autoridad", cargo, per, vig, url, fe, tipo, nota=nota))
    for org, cargo in ((CF, "decano (preside)"), (AU, "decano (miembro nato)")):
        M.append(m("Walter Fernando Zaldivar Alvarez", org, "FIQT", "autoridad", cargo, gob_fiqt[1], True, gob, gobf, "portal",
                   nota="Directorio de gob.pe ('Decano de la Facultad de Ingeniería Química y Textil', fecha de inicio 16-09-2026)."))
    # Decanos 2021-2025 (RR 1355-2021)
    for fac, n, per in (("FIQT", "Dr. EMERSON ALCIDES COLLADO DOMINGUEZ", "12/11/2021 - 11/11/2025"),
                        ("FIECS", "M.Sc. CESAR CETRARO CARDO", "11/11/2021 - 10/11/2025")):
        M.append(m(n, CF, fac, "autoridad", "decano (preside)", per, False, F["rr1355_2021"], "2021", "resolucion",
                   nota="RR 1355-2021 (archivo escaneado en la carpeta 'DECANOS/DESIGNACION DE AUTORIDADES' del CEUNI; leído por OCR)."))
    M.append(m("Dr. Jorge Gustavo Butler Blacker", CF, "FIEE", "autoridad", "decano (electo)", "13/11/2023 - (no concluido)", False,
               F["dec_folder"], "2023-11-10", "resolucion",
               nota="RR 3541-2023-UNI (carpeta del CEUNI). Pasó a vicerrector; la FIEE tiene decano interino."))

    # --- CEUNI ---------------------------------------------------------------
    ceu26 = [("Dra. RAQUEL MEDINA RODRIGUEZ", "presidenta", "docente"),
             ("Dra. KARIN MARÍA PAUCAR CUBA", "vicepresidenta", "docente"),
             ("Alum. LEANDRO JOSUE GAMEZ RAMOS", "secretario", "estudiante"),
             ("Alum. CRISTIAN ANDERSON CUEVAS RAMIREZ", "prosecretario", "estudiante"),
             ("Alum. PIERO ANDRES ALIAGA FERNANDEZ", "relator", "estudiante"),
             ("Dr. TINO EDUARDO REYNA MONTEVERDE", "vocal", "docente"),
             ("Mag. ALFREDO EFRAÍN RODRIGUEZ GUTIERREZ", "vocal", "docente"),
             ("Mag. LUIS FELIPE MEDINA AQUINO", "vocal", "docente"),
             ("Mag. PAVEL CHUQUIVILCA LOPEZ", "vocal", "docente"),
             ("Alum. SANDRO GONZALO NIÑO EGOAVIL", "accesitario", "estudiante")]
    for n, c, e in ceu26:
        M.append(m(n, CEU, None, e, c, "2026", True, F["rr0183_2026"], "2026-01-09", "resolucion",
                   nota="Integrantes según RR 0183-2026-UNI; cargos según la página 'Comité Electoral – Período 2026' del portal del CEUNI "
                        "(la presidenta firma como Raquel Medina Rodríguez de Castañeda)." if c != "accesitario" else "RR 0183-2026-UNI."))
    ceu25 = [("M.Sc. ELISEO PAEZ APOLINARIO", "presidente", "docente"), ("Mag. RAQUEL MARTHA CHÁVARRI ARCE", "vicepresidenta", "docente"),
             ("Alum. ENRIQUE ISRAEL MARIN RIOS", "secretario", "estudiante"), ("Alum. ANGEL SEBASTIAN LEYVA SALAS", "prosecretario", "estudiante"),
             ("Alum. YORYI ORLANDO WONG SAMAME", "relator", "estudiante"), ("Mag. CARLOS ALBERTO HUAYLLASCO MONTALVA", "vocal", "docente"),
             ("Ing. MANUEL SEBES TOLEDO PAREDES", "vocal", "docente"), ("Mag. CESAR HERBOZO Y ROMERO", "vocal", "docente"),
             ("M.Sc. MAURICIO PEDRO GALVEZ LEGUA", "vocal", "docente")]
    for n, c, e in ceu25:
        M.append(m(n, CEU, None, e, c, "13/01/2025 - 12/01/2026", False, F["rr0177_2025"], "2025-01-13", "resolucion"))
    ceu24 = [("Mg. Oscar Felipe Silva Campos", "presidente", "docente"), ("Dra. Raquel Medina Rodríguez de Castañeda", "vicepresidenta", "docente"),
             ("Alum. Cristian Anderson Cuevas Ramírez", "secretario", "estudiante"), ("Mg. Milder Freddy García Vallejo", "prosecretario", "docente"),
             ("Alum. Leslie Consuelo Arango Huaman", "relator", "estudiante"), ("Ing. Cesar Aurelio Miranda Torres", "vocal", "docente"),
             ("Mg. Walter Héctor Gonzales Arnao", "vocal", "docente"), ("Ing. Olga Frida Bullón Camarena", "vocal", "docente"),
             ("Alum. Sebastian Eduardo Quinto Granda", "vocal", "estudiante")]
    for n, c, e in ceu24:
        M.append(m(n, CEU, None, e, c, "29/12/2023 - 28/12/2024", False, F["rr0020_2024"], "2023-12-29", "resolucion"))
    ceu23 = [("Dr. Luis Antonio Lastra Espinoza", "presidente", "docente"), ("Mag. Julio Herman Cruzado Quiroz", "vicepresidente", "docente"),
             ("Alum. Jorge Guillermo Achong Bonilla", "secretario", "estudiante"), ("Alum. Diana Lucia Ayala Villafuerte", "prosecretaria", "estudiante"),
             ("Mag. Manuel Teodosio Toribio Cangana", "relator", "docente"), ("Mag. Mario Garayar Ávalos", "vocal", "docente"),
             ("Ing. César Bayardo Ugarte López", "vocal", "docente"), ("Mag. Ricardo Alejandro Chung Ching", "vocal", "docente"),
             ("Alum. Lupe Jackeline Mejia Pedraza", "vocal", "estudiante")]
    for n, c, e in ceu23:
        M.append(m(n, CEU, None, e, c, "29/12/2022 - 28/12/2023", False, F["rr0047_2023"], "2023-01", "resolucion"))

    # --- Tribunal de Honor ---------------------------------------------------
    TH = "Tribunal de Honor Universitario"
    for n, c in (("Dr. JOSE MANUEL ZAPATA SAMATA", "presidente"), ("Dr. FERNANDO HUAMAN PEREZ", "secretario"),
                 ("Dr. LUIS ANTONIO LASTRA ESPINOZA", "vocal")):
        M.append(m(n, TH, None, "docente", c, "setiembre 2026 - agosto 2027", True, F["rr2657_2025"], "2025-10-01", "resolucion",
                   nota="El directorio de gob.pe aún muestra a Lastra Espinoza como presidente (dato del periodo anterior)." if "LASTRA" in n else None))
    for n, c in (("Dr. LUIS ANTONIO LASTRA ESPINOZA", "presidente"), ("Dr. FERNANDO HUAMAN PEREZ", "secretario"),
                 ("Dr. JOSE MANUEL ZAPATA SAMATA", "vocal")):
        M.append(m(n, TH, None, "docente", c, "setiembre 2025 - agosto 2026", False, F["rr2657_2025"], "2025-10-01", "resolucion"))
    for n in ("Dr. Antonio Nolberto Lazo Jara", "Mag. Rubén Gómez Sánchez Soto", "Dr. Walter Esteban Barrutia Feijoo"):
        M.append(m(n, TH, None, "docente", "miembro", "desde 2024-03 (conformación vigente en 2024)", False, F["rr0870_2024"], "2024-03-12", "resolucion"))
    for n, c in (("Dr. Luis Alberto Mosquera Leiva", "presidente"), ("Dr. Antonio Nolberto Lazo Jara", "secretario"),
                 ("Dra. Ana Cecilia Valderrama Negron", "vocal")):
        M.append(m(n, TH, None, "docente", c, "2023 - 2024-03", False, F["rr2167_2023"], "2023-08-01", "resolucion"))

    # --- Defensoría Universitaria -------------------------------------------
    DU = "Defensoría Universitaria"
    M.append(m("Msc. SYRA PATRICIA ÁLVAREZ ORTEGA", DU, None, "docente", "defensora universitaria interina",
               "desde 17/06/2026 hasta la elección de un titular", True, F["rau0012_2026"], "2026-06-17", "resolucion"))
    M.append(m("Mag. MARÍA ANGÉLICA DAMIÁN BRIONES", DU, None, "docente", "defensora universitaria",
               "05/05/2022 - 16/06/2026 (prorrogada por RR 1336-2025; renunció)", False, F["rau0012_2026"], "2026-06-17", "resolucion"))
    CDU = "Comisión de elección del Defensor Universitario (AU)"
    for n, c, f, e in (("Dr. Jorge Gustavo Butler Blacker", "presidente (vicerrector de investigación)", None, "autoridad"),
                       ("Dr. Fortunato Alva Dávila", "miembro", "FIM", "docente"),
                       ("M.Sc. Teodardo Javier Cárdenas Mendoza", "miembro", "FIQT", "docente"),
                       ("M.Sc. Carlos Gady León", "miembro", "FAUA", "docente"),
                       ("Alum. Franco Rafael Espinoza Alvarado", "miembro", "FIEE", "estudiante"),
                       ("Alum. Adrián Alonso Ríos Herrera", "miembro", "FIECS", "estudiante")):
        M.append(m(n, CDU, f, e, c, "desde 17/06/2026 (plazo de 3 meses para presentar terna)", None, F["rau0012_2026"],
                   "2026-06-17", "resolucion", nota="No consta que la comisión haya concluido ni que se haya elegido titular."))

    # --- Comisión Permanente de Fiscalización -------------------------------
    CPF = "Comisión Permanente de Fiscalización (AU)"
    for n, c, e, per, vig in (("Mg. MARIO GARAYAR AVALOS", "presidente", "docente", "hasta el 12/01/2028", True),
                              ("Dra. Arq. ROCIO MARGARITA CACHO CRUZ", "secretaria", "docente", "hasta el 12/01/2028", True),
                              ("CAMILA VARILLAS CAMARGO", "miembro (estudiante de pregrado)", "estudiante", "hasta el 12/01/2026", False),
                              ("JAIME EDILBERTO GUZMAN SALINAS", "miembro (estudiante de posgrado)", "estudiante", "hasta el 12/01/2026", False)):
        M.append(m(n, CPF, None, e, c, per, vig, F["rr3398_2025"], "2025-11-20", "resolucion"))
    for n, c, e, f in (("Mag. CIRILO ALVAREZ ROJAS", "presidente", "docente", None),
                       ("Mag. MARIO GARAYAR AVALOS", "secretario", "docente", None),
                       ("ARELY YADIRA CCOYLLO TOMAIRO", "representante de estudiantes", "estudiante", "FIA"),
                       ("JAIME EDILBERTO GUZMAN SALINAS", "miembro (estudiante de posgrado)", "estudiante", None)):
        M.append(m(n, CPF, f, e, c, "13/01/2025 - 20/11/2025 (reconformada por RR 3398-2025)", False, F["rr0247_2025"], "2025-01-30", "resolucion"))
    for n, c, e, f in (("Dra. GLORIA TERESITA HUAMANÍ HUAMANÍ", "presidenta (13/05/2022 - 12/08/2023)", "docente", "FIIS"),
                       ("Mag. JOSÉ ALEX CHAPARRO MÉNDEZ", "titular; presidente desde 2023 (RR 3999-2023)", "docente", "FAUA"),
                       ("Alum. ROBERTO BETO CACHA SILVA", "titular", "estudiante", "FIA")):
        M.append(m(n, CPF, f, e, c, "2023", False, F["rr1865_2023"], "2023-07-11", "resolucion"))

    # Orden estable
    orden = {AU: 0, CU: 1, CF: 2, CEU: 3, TH: 4, DU: 5, CDU: 6, CPF: 7}
    M.sort(key=lambda r: (orden.get(r["organo"], 9), r["facultad"] or "", {"en_funciones": 0, "incierto": 1, "electo_por_asumir": 2, "concluido": 3, "candidato": 4}[r["estado"]],
                          r["estamento"], r["cargo"]))

    fuentes = sorted({(r["fuente_url"], r["fuente_tipo"]) for r in M})
    cobertura = {
        AU: "parcial",
        CU: "parcial",
        **{f"{CF} {f}": "parcial" for f in ["FAUA", "FC", "FIA", "FIC", "FIECS", "FIEE", "FIGMM", "FIIS", "FIM", "FIP", "FIQT"]},
        CEU: "completa",
        TH: "completa",
        DU: "completa",
        CPF: "parcial",
        "Representantes de graduados (AU, CU y CF)": "sin_fuente",
        "Estudiantes AU 2021-2026 (por periodo)": "completa: 2021-22, 2022-23, 2023-24 (complementaria de mayo-2024), 2024-25, 2025-26 y electos 2026-27",
        "Estudiantes CU 2021-2026 (por periodo)": "completa: 2021-22, 2022-23, 2023-24, 2024-25, 2025-26 y electos 2026-27",
        "Estudiantes consejos de facultad 2021-2026": "completa: las 11 facultades en cada ciclo, sumando la elección general y la complementaria",
        "Estudiantes CEUNI 2021-2026": "parcial: 2021 sin estamento; 2022 sin fuente; 2023-2026 completa",
        "Estudiantes Comisión Permanente de Fiscalización 2021-2026": "parcial: solo 2023, 2025 y la reconformación de nov-2025",
        "Candidatos estudiantiles 2026": "completa (AU, CU y 11 consejos de facultad)",
        "Personeros de listas 2026": "sin_fuente",
    }
    notas = [
        "Fecha de corte: 2026-11-18. 'vigente' = true si el mandato está en curso a esa fecha; false si concluyó o aún no empieza; null si es incierto.",
        "Campo adicional 'estado': en_funciones | concluido | electo_por_asumir | incierto | candidato.",
        "Los nombres se copian tal como figuran en la fuente; la mayoría de las listas oficiales usan el orden NOMBRES APELLIDOS (no APELLIDOS, NOMBRES), por lo que no se invierte el orden para no introducir errores en apellidos compuestos.",
        "No se guardan DNI, códigos de estudiante ni datos de contacto, aunque figuren en las fuentes.",
        "Siglas de facultad normalizadas: FIPGNP -> FIP, FIEECS -> FIECS. 'facultad' = null para posgrado o miembros sin facultad indicada.",
        "Representantes docentes ante AU y consejos de facultad: mandato 10/12/2024 - 09/12/2027 (listas del CEUNI). Estudiantes ante CU y consejos de facultad: 10/12/2025 - 09/12/2026, todavía en funciones al corte.",
        "Electos 2026 (tercio estudiantil de AU, CU y consejos de facultad): proclamados por el CEUNI en La Gaceta N.° 232 (04-11-2026, PDF escaneado, transcrito a mano). Se marcan 'electo_por_asumir'.",
        "Rectorado: el 11-11-2026 concluyó el periodo 2021-2026; desde el 12-11-2026 ejerce como rector interino el decano más antiguo (Alberto Landauro Abanto) por sucesión de la Ley N.° 32418. Los vicerrectores vigentes después del 11-11-2026 no constan en fuente abierta.",
        "Elección de rector y vicerrectores 2026-2031: la segunda vuelta (Lista 1 vs Lista 8) se repitió el 10-11-2026; el escrutinio y la proclamación del CEUNI solo están disponibles con cuenta institucional. No se registran ganadores hasta contar con una fuente abierta (los candidatos de la 2.ª vuelta figuran en La Gaceta 232, pág. 02).",
        "Consejo Universitario: por Ley 30220 (art. 58) lo integran 1/4 de los decanos elegidos por y entre ellos; no se encontró la resolución que los designa, por eso los decanos solo se cargan en la AU y en su consejo de facultad.",
        "Representantes de los graduados (AU, CU y consejos de facultad): no se encontró ninguna fuente abierta que los nombre.",
        "Estudiantes 2021-2025: se leen de las proclamaciones de ganadores del CEUNI (PDF con texto). Las de 2021-2023 ya no están en el portal actual del CEUNI; se usan las copias del Internet Archive (web.archive.org) del portal anterior, y la nota de cada fila lo indica.",
        "Estudiantes ante la AU 2025-2026: La Gaceta N.° 209 (27-10-2025), pág. 03, transcrita a mano porque el enlace directo del CEUNI a esa lista está restringido.",
        "Periodo 2023-2024: la elección general del 13-10-2023 no incluyó representantes estudiantiles ante la AU; la AU se completó en la complementaria del 22-05-2024.",
        "Candidatos 2026: filas con estado 'candidato' (publicación definitiva de candidaturas, 01-10-2026). No son miembros. Los personeros de lista no se publicaron en fuente abierta.",
        "Se eliminaron las 13 filas de estudiantes de la AU 2024-2025 que antes se inferían de las RR de comisiones de la AU: la proclamación del 10-12-2024 trae la lista completa y oficial.",
        "Comisión Permanente de Fiscalización: los representantes estudiantiles para 2026 no constan en fuente abierta (los anteriores cesaron el 12/01/2026).",
        "Docentes 2021-2024: no se cargan (solo se pidió ampliar a estudiantes); las mismas proclamaciones archivadas los incluyen.",
    ] + notas
    meta = {
        "generado": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "fecha_corte": HOY.isoformat(),
        "metodo": ("Descarga de las listas oficiales del CEUNI (enlaces públicos de OneDrive enlazados desde ceuni.uni.edu.pe) y de "
                   "resoluciones publicadas en gob.pe; extracción con pdftotext; documentos escaneados leídos por OCR (tesseract) o "
                   "transcritos a mano desde la imagen. Script: etl/build_organos_gobierno.py."),
        "fuentes": [{"url": u, "tipo": t} for u, t in fuentes] + [{"url": F["ceuni_organos"], "tipo": "portal"},
                                                                   {"url": F["ceuni_2026_web"], "tipo": "portal"}],
        "cobertura": cobertura,
        "notas": notas,
        "conteos": {},
    }
    for r in M:
        meta["conteos"].setdefault(r["organo"], {}).setdefault(r["estado"], 0)
        meta["conteos"][r["organo"]][r["estado"]] += 1
    return {"_meta": meta, "miembros": M}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default=os.path.join(ROOT, ".cache", "organos_raw"))
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--out", default=OUT)
    a = ap.parse_args()
    data = build(a.raw, a.offline)
    n = len(data["miembros"])
    fallas = [x for x in data["_meta"]["notas"] if x.startswith("No se pudo leer")]
    if fallas:
        sys.exit("Fuentes no descargadas; no se escribe el archivo:\n" + "\n".join(fallas))
    if n < 100:
        sys.exit(f"Solo {n} miembros: ¿fallaron las descargas? No se escribe {a.out}")
    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    print(f"{n} miembros -> {a.out}")
    print(json.dumps(data["_meta"]["conteos"], ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
