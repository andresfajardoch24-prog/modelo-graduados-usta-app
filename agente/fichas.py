"""Fichas técnicas de los indicadores y veredicto de utilidad de cada variable.

Lo usan el Streamlit (documento técnico del modelo) y el generador del Word de
fichas, para que ambos digan exactamente lo mismo. Solo trabaja con salidas
agregadas (datos_dashboard.json y diccionario_variables.csv): nunca abre las
bases con datos personales.

Lo que aquí es propuesta del equipo (nivel de evidencia por indicador,
periodicidad, responsables, verificación externa) está marcado en
ORIGEN_PROPUESTA y debe validarse en la Fase 2.
"""
import json

import pandas as pd

from . import config

ORIGEN_PROPUESTA = "Propuesta del equipo, para validar en la Fase 2"

# Variables de cada indicador: (base, clave en config.BASES[base]["columnas"]).
# Las claves con lista de posiciones (calidad_vida, incidencia) se expanden.
VARIABLES_INDICADOR = {
    "SOC-01": [("percepcion", "estrato_grado"), ("percepcion", "estrato_actual")],
    "SOC-02": [("penser", "madre"), ("penser", "padre"), ("percepcion", "padres")],
    "SOC-03": [("penser", "ingreso_superior")],
    "PRO-01": [("percepcion", "tiempo_primer_empleo")],
    "PRO-02": [("percepcion", "correspondencia_primer"), ("percepcion", "correspondencia_actual"),
               ("percepcion", "continua_primer")],
    "PRO-03": [("percepcion", "contrato_primer"), ("percepcion", "contrato_actual"),
               ("percepcion", "continua_primer")],
    "PRO-04": [("penser", "laborando"), ("formulario", "ocupacion")],
    "PRO-05": [("percepcion", "relacion_primer")],
    "PER-01": [("percepcion", "calidad_vida")],
    "PER-02": [("penser", "incidencia")],
    "ACA-01": [("penser", "max_estudios"), ("percepcion", "otros_titulos")],
    "ACA-02": [("penser", "comunitario"), ("penser", "investigacion"), ("penser", "gremio"),
               ("penser", "distincion")],
    "REL-01": [("percepcion", "formacion_continua"), ("formulario", "interes_posgrado"),
               ("formulario", "tipo_posgrado")],
    "REL-02": [("percepcion", "recomienda")],
}

# Variables del prototipo de índice (posición 2 de Percepción = máximo nivel de estudios).
VARIABLES_INDICE = [("percepcion", "estrato_grado"), ("percepcion", "estrato_actual"),
                    ("percepcion", "correspondencia_primer"), ("percepcion", "correspondencia_actual"),
                    ("percepcion", "relacion_primer"), ("percepcion", "tiempo_primer_empleo"),
                    ("percepcion", "calidad_vida"), ("percepcion", 2)]

# Variables de desagregación que usan todos los indicadores.
VARIABLES_SEGMENTO = [("penser", "sede"), ("penser", "anio_grado"), ("percepcion", "sede"),
                      ("percepcion", "fecha_grado"), ("formulario", "programa_bga")]

# Metadatos que no salen de los datos: propuesta del equipo.
META = {
    "SOC-01": {"evidencia": "B", "uso": "Transformación · índice (componente social)",
               "verificacion": "No verificable con registros; el estrato es declarado."},
    "SOC-02": {"evidencia": "B", "uso": "Caracterización del origen · movilidad intergeneracional",
               "verificacion": "No verificable con registros."},
    "SOC-03": {"evidencia": "B", "uso": "Transformación (ingresos)",
               "verificacion": "Aportes a seguridad social (PILA) vía Observatorio Laboral para la Educación, si hay convenio."},
    "PRO-01": {"evidencia": "B", "uso": "Transformación · índice (componente profesional) · portafolio de empleabilidad",
               "verificacion": "Fecha del primer aporte a seguridad social (PILA), si hay convenio."},
    "PRO-02": {"evidencia": "C", "uso": "Transformación · currículo (pertinencia) · índice",
               "verificacion": "No verificable; contrastar con empleadores."},
    "PRO-03": {"evidencia": "B", "uso": "Transformación (trayectoria laboral)",
               "verificacion": "No verificable con registros abiertos."},
    "PRO-04": {"evidencia": "B", "uso": "Seguimiento (situación actual) · portafolio de empleabilidad",
               "verificacion": "PILA vía Observatorio Laboral para la Educación, si hay convenio."},
    "PRO-05": {"evidencia": "C", "uso": "Currículo (pertinencia) · índice (componente profesional)",
               "verificacion": "No verificable; contrastar con empleadores."},
    "PER-01": {"evidencia": "B", "uso": "Transformación · índice (componente personal) · portafolio de bienestar",
               "verificacion": "No verificable con registros."},
    "PER-02": {"evidencia": "C", "uso": "Contribución percibida · currículo",
               "verificacion": "No aplica: es una valoración."},
    "ACA-01": {"evidencia": "A", "uso": "Transformación · índice (componente académico) · portafolio de posgrado",
               "verificacion": "Títulos registrados (SNIES / registro de graduados de la USTA)."},
    "ACA-02": {"evidencia": "B", "uso": "Transformación (participación social y académica)",
               "verificacion": "CvLAC (investigación) y RUES (gremios, emprendimientos)."},
    "REL-01": {"evidencia": "C", "uso": "Portafolio de formación continua y posgrado",
               "verificacion": "Contrastar con matrícula real de graduados en la USTA."},
    "REL-02": {"evidencia": "C", "uso": "Vínculo con la Universidad (no mide transformación)",
               "verificacion": "No aplica: es una valoración."},
}

NIVELES = {"A": "Hecho verificable", "B": "Cambio declarado", "C": "Percepción o contribución",
           "D": "No disponible"}

PERIODICIDAD = ("Anual, por cohortes a 1, 3 y 5 años del grado (con línea base al grado "
                "cuando exista el instrumento mínimo común).")
RESPONSABLE = ("Recolección: Dirección de Graduados. Cálculo y validación: Observatorio de "
               "Estadística (equipo técnico del modelo, lámina 7).")
METODO = ("Proporción con intervalo de confianza de Wilson al 95 %. Se reporta por sede y por "
          "cohorte; los grupos con menos de 30 respuestas no se interpretan.")


def _posiciones(base: str, clave) -> list[int]:
    if isinstance(clave, int):
        return [clave]
    pos = config.BASES[base]["columnas"][clave]
    return pos if isinstance(pos, list) else [pos]


def cargar():
    datos = json.loads((config.CARPETA_SALIDAS / "datos_dashboard.json").read_text(encoding="utf-8"))
    dic = pd.DataFrame(datos["diccionario"])
    explica = json.loads(config.CONTENIDO_EXPLICACIONES.read_text(encoding="utf-8"))
    return datos, dic, explica


def mapa_uso(dic: pd.DataFrame) -> dict[tuple[str, int], list[str]]:
    """(base, posición) -> indicadores (y el índice) que usan esa variable."""
    usos: dict[tuple[str, int], list[str]] = {}
    for ind, vars_ in VARIABLES_INDICADOR.items():
        for base, clave in vars_:
            for p in _posiciones(base, clave):
                usos.setdefault((base, p), []).append(ind)
    for base, clave in VARIABLES_INDICE:
        for p in _posiciones(base, clave):
            usos.setdefault((base, p), []).append("Índice")
    for base, clave in VARIABLES_SEGMENTO:
        for p in _posiciones(base, clave):
            usos.setdefault((base, p), []).append("Desagregación")
    return usos


def veredicto(fila: pd.Series, usada_en: list[str]) -> tuple[str, str]:
    """Clasifica una variable según si sirve al modelo y explica por qué."""
    uso, momento, falt = fila["uso"], fila["momento"], fila["faltantes_pct"]
    nota_falt = (" Solo la responde un subgrupo (pregunta filtrada o por sede): "
                 f"{falt:.0f} % sin dato." if falt >= 80 else "")
    if uso.startswith("Excluida"):
        return ("No se usa: dato personal",
                "Identifica a la persona (nombre, documento, correo, teléfono o empresa). "
                "Se excluye por la Ley 1581 de 2012; solo serviría, cifrada, para unir bases.")
    if uso == "Control de calidad":
        return ("No se usa: control",
                "Es un metadato del formulario o el consentimiento. Sirve para depurar, no para medir.")
    indicadores = [u for u in usada_en if u != "Desagregación"]
    if indicadores:
        return ("Sirve: ya se usa",
                f"Alimenta {', '.join(dict.fromkeys(indicadores))}. Tiene un momento claro "
                f"({momento.lower()}) y suficientes respuestas.")
    if uso == "Indicador de transformación":
        if momento in ("Antes", "Actual", "Cambio percibido", "Retrospectivo"):
            return ("Sirve: disponible",
                    f"Mide un aspecto de la transformación (momento: {momento.lower()}) pero aún "
                    "no entra en un indicador. Candidata para la Fase 2." + nota_falt)
        return ("Sirve con reservas",
                "Es percepción de la contribución de la formación (evidencia C): útil para el "
                "currículo, no prueba un cambio." + nota_falt)
    if uso in ("Segmentación", "Caracterización"):
        if "Desagregación" in usada_en:
            return ("Sirve: para desagregar",
                    "Se usa para cortar los resultados por sede o cohorte. No mide transformación.")
        return ("Sirve: para describir",
                "Describe al graduado o su contexto (edad, territorio, programa). No mide "
                "transformación, pero permite comparar grupos." + nota_falt)
    if uso == "Portafolio de servicios":
        return ("Sirve: para el portafolio",
                "Dice qué servicios o formación demanda el graduado (uso 2 del modelo, lámina 4). "
                "No mide transformación." + nota_falt)
    if uso.startswith("Currículo"):
        return ("Sirve con reservas",
                "Texto abierto sobre la formación: útil para el currículo (uso 1, lámina 4), pero "
                "exige codificar las respuestas antes de analizarlas.")
    return ("Revisar", "Sin regla de clasificación.")


ORDEN_VEREDICTO = ["Sirve: ya se usa", "Sirve: disponible", "Sirve con reservas",
                   "Sirve: para desagregar", "Sirve: para describir", "Sirve: para el portafolio",
                   "No se usa: control", "No se usa: dato personal", "Revisar"]


def diccionario_con_veredicto(dic: pd.DataFrame) -> pd.DataFrame:
    usos = mapa_uso(dic)
    filas = []
    for _, f in dic.iterrows():
        usada = usos.get((f["base"], int(f["posicion"])), [])
        v, porque = veredicto(f, usada)
        filas.append({**f.to_dict(), "usada_en": ", ".join(dict.fromkeys(usada)),
                      "veredicto": v, "por_que": porque})
    return pd.DataFrame(filas)


def fichas(datos: dict, dic: pd.DataFrame, explica: dict) -> list[dict]:
    """Una ficha por indicador, con su línea base calculada."""
    preguntas = {(r.base, int(r.posicion)): r.pregunta for r in dic.itertuples()}
    nombres_base = {k: v["nombre"] for k, v in config.BASES.items()}
    salida = []
    for ind in datos["indicadores"]:
        vars_ = []
        for base, clave in VARIABLES_INDICADOR.get(ind["id"], []):
            for p in _posiciones(base, clave):
                vars_.append({"base": nombres_base[base], "posicion": p,
                              "pregunta": preguntas.get((base, p), "—")})
        lectura = explica["lecturas"].get(ind["id"], {})
        meta = META[ind["id"]]
        salida.append({
            **{k: ind[k] for k in ("id", "nombre", "dimension", "aspecto", "tipo", "definicion",
                                   "formula", "universo", "limitaciones")},
            "pregunta": lectura.get("pregunta", ""),
            "interpretacion": lectura.get("ojo", ""),
            "fuentes": sorted({nombres_base[r["base"]] for r in ind["resultados"]}),
            "variables": vars_,
            "linea_base": ind["resultados"],
            "evidencia": meta["evidencia"],
            "evidencia_nombre": NIVELES[meta["evidencia"]],
            "uso": meta["uso"],
            "verificacion": meta["verificacion"],
            "unidad": "Porcentaje de graduados (0–100 %)",
            "metodo": METODO,
            "desagregacion": "Sede y cohorte de grado; a futuro programa, sexo y territorio.",
            "periodicidad": PERIODICIDAD,
            "responsable": RESPONSABLE,
            "meta": "Por definir en la Fase 2, una vez se valide la línea base.",
        })
    return salida
