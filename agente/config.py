"""Configuración del agente de perfilado.

Todo lo que el agente decide de forma automática está escrito aquí: qué bases
lee, qué columnas son datos personales, y con qué reglas asigna cada variable
a una dimensión del Modelo de Seguimiento y Evaluación de la Transformación de
los Graduados. Cambiar una regla aquí cambia el diccionario completo, así que
cada ajuste debe quedar registrado en la bitácora de decisiones de Obsidian.
"""
import os
from pathlib import Path

CARPETA_ANALISIS = Path(__file__).resolve().parents[1]  # raíz del repositorio
RAIZ_PROYECTO = CARPETA_ANALISIS.parent  # carpeta de la consultoría (documentos del proyecto)


def _cargar_env(ruta: Path):
    """Lee variables KEY=valor de un .env sin pisar las que ya existen en el sistema."""
    if not ruta.exists():
        return
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if linea and not linea.startswith("#") and "=" in linea:
            clave, valor = linea.split("=", 1)
            os.environ.setdefault(clave.strip(), valor.strip().strip('"'))


_cargar_env(CARPETA_ANALISIS / ".env")


def _carpeta(variable: str, *candidatas: Path) -> Path:
    """Ruta de la variable de entorno si existe; si no, la primera candidata que exista."""
    if os.environ.get(variable):
        return Path(os.environ[variable]).expanduser().resolve()
    return next((c for c in candidatas if c.exists()), candidatas[0])


# Bases originales: datos/DATAS GRADUADOS (descifradas con datos_seguros.py) o, en el
# equipo de la consultoría, la carpeta hermana DATAS GRADUADOS.
CARPETA_DATOS = _carpeta("GRADUADOS_DATOS", CARPETA_ANALISIS / "datos" / "DATAS GRADUADOS",
                         RAIZ_PROYECTO / "DATAS GRADUADOS")
CARPETA_ENTREGABLES = _carpeta("GRADUADOS_ENTREGABLES", CARPETA_ANALISIS / "entregables")
CARPETA_SALIDAS = CARPETA_ANALISIS / "salidas"
CARPETA_BOVEDA = CARPETA_ANALISIS / "boveda_obsidian"
CARPETA_DASHBOARD = CARPETA_ANALISIS / "dashboard"
PLANTILLA_DASHBOARD = CARPETA_ANALISIS / "plantilla" / "dashboard.html"
CONTENIDO_CONCEPTUAL = CARPETA_ANALISIS / "contenido" / "conceptual.json"
CONTENIDO_CONSULTORIA = CARPETA_ANALISIS / "contenido" / "consultoria.json"
CONTENIDO_MARCOS = CARPETA_ANALISIS / "contenido" / "marcos.json"
CONTENIDO_EXPLICACIONES = CARPETA_ANALISIS / "contenido" / "explicaciones.json"

# ---------------------------------------------------------------------------
# Bases de datos
# ---------------------------------------------------------------------------
# `patron` se busca con glob dentro de DATAS GRADUADOS (evita problemas con
# tildes en los nombres de archivo). `columnas` fija las variables clave por
# posición, verificadas el 12-oct-2026 contra los archivos originales.
BASES = {
    "penser": {
        "nombre": "Estudio PENSER 2025",
        "patron": "DATA DEPURADA SANTO TOMAS_ESTUDIO PENSER*.xlsx",
        "hoja": "DATA VALIDA",
        "encabezado": 0,
        "recoleccion": "nov-2024 a abr-2025",
        "descripcion": "Encuesta del Índice de Impacto de Egresados (Corporación PENSER) aplicada a graduados de las cuatro sedes.",
        "columnas": {
            "consentimiento": 1, "documento": 2, "sede": 4, "programa": 5,
            "anio_grado": 9, "laborando": 10, "vinculacion": 12, "tipo_cargo": 14,
            "pertinencia": 20, "distincion": 22, "gremio": 25, "comunitario": 29,
            "investigacion": 33, "edad": 47, "max_estudios": 50,
            "madre": 131, "padre": 132, "ingreso_superior": 133,
            "ingreso_suficiente": 134, "vivienda": 135,
            "incidencia": [137, 138, 139, 140, 141, 142],
        },
    },
    "percepcion": {
        "nombre": "Estudio de Percepción de Egresados 2022",
        "patron": "ESTUDIO DE PERCEPCION EGRESADOS*.xlsx",
        "hoja": "BASE DE DATOS CONSOLIDADA (2)",
        "encabezado": 0,
        "recoleccion": "2022 (consolidado multisede)",
        "descripcion": "Encuesta de seguimiento con preguntas retrospectivas: estrato al graduarse y actual, primer empleo y empleo actual.",
        "columnas": {
            "consentimiento": 1, "sede": 5, "fecha_grado": 34, "genero": 39,
            "estrato_grado": 41, "estrato_actual": 42, "padres": 49,
            "otros_titulos": 35, "recomienda": 119, "estudiaria_otro": 120,
            "formacion_continua": 121,
            "calidad_vida": [128, 129, 130, 131, 132, 133],
            "tiempo_primer_empleo": 137, "contrato_primer": 138,
            "relacion_primer": 139, "correspondencia_primer": 141,
            "continua_primer": 143, "contrato_actual": 149,
            "correspondencia_actual": 152, "correo": 155,
        },
    },
    "formulario": {
        "nombre": "Formulario de actualización de datos 2023–2026",
        "patron": "Formulario de actualizaci*.xlsx",
        "hoja": "Sheet1",
        "encabezado": 0,
        "recoleccion": "feb-2023 a feb-2026",
        "descripcion": "Formulario permanente de la Dirección de Graduados, concentrado en la Seccional Bucaramanga.",
        "columnas": {
            "fecha": 1, "documento": 6, "edad": 7, "sexo": 8, "estrato": 11,
            "tipo_programa": 21, "programa_bga": 22, "ocupacion": 24,
            "contrato": 28, "cargo": 30, "tiempo_busqueda": 33, "ingreso": 38,
            "interes_posgrado": 39, "tipo_posgrado": 40, "aplicabilidad": 42,
            "red": 43, "reconocimiento": 45, "consentimiento": 50,
        },
    },
}

# Base que se lee solo para verificar duplicación; no entra al análisis.
BASE_DUPLICADA = {
    "nombre": "Base Bucaramanga 2022 (Observatorio Laboral)",
    "patron": "BASE DE DATOS BUCARAMANGA*.xlsx",
    "hoja": "Hoja1",
    "encabezado": 1,
    "col_correo": 133,
}

# ---------------------------------------------------------------------------
# Datos personales: nunca se imprimen ni se exportan
# ---------------------------------------------------------------------------
PATRON_PII = (
    r"nombre|apellido|documento|identificaci|correo|celular|tel[eé]fono|"
    r"direcci[oó]n|e-?mail|c[eé]dula|organizaci[oó]n|empresa donde|"
    r"nombre de la empresa"
)

# ---------------------------------------------------------------------------
# Reglas de clasificación (se aplican en orden; gana la primera que coincide)
# ---------------------------------------------------------------------------
# Cada regla: (patrón sobre el texto normalizado de la pregunta,
#              dimensión, aspecto, momento, uso)
# Dimensiones del modelo (lámina 3): personal, profesional, social, académica.
# Se agregan "Relación con la Universidad" (lámina 3, "Relación con la
# Universidad") y "Contexto" para variables de caracterización.
REGLAS = [
    (r"consentimiento|politica de tratamiento|como institucion de educacion superior|manifiesta conocer|autorizo",
     "Control", "Consentimiento informado", "No aplica", "Control de calidad"),
    (r"^marca temporal|^hora de|^id$|^unnamed|^column$",
     "Control", "Metadatos del formulario", "No aplica", "Control de calidad"),
    (r"espacios academicos|asignaturas|areas, tecnicas o herramientas|actividades extracurriculares|observaciones o comentarios|indique la razon|logros o resultados que desea",
     "Académica", "Opinión abierta sobre la formación", "Retrospectivo", "Currículo (texto abierto)"),
    (r"momento de obtener el titulo",
     "Social", "Condición socioeconómica de origen", "Antes", "Indicador de transformación"),
    (r"estrato socioeconomico actual|^estrato socioeconomico$",
     "Social", "Condición socioeconómica actual", "Actual", "Indicador de transformación"),
    (r"padres|madre|padre|hermanos",
     "Social", "Origen familiar (educación del hogar)", "Antes", "Indicador de transformación"),
    (r"familia contaba|familia tenia",
     "Social", "Origen familiar (capital social)", "Antes", "Caracterización"),
    (r"superior al valor de los ingresos",
     "Social", "Cambio en ingresos", "Cambio percibido", "Indicador de transformación"),
    (r"bienes materiales|calidad de su vivienda|condiciones de salud|seguridad social|eventos culturales|tiempo de ocio",
     "Personal", "Bienestar y calidad de vida", "Cambio percibido", "Indicador de transformación"),
    (r"mejoramiento de su calidad de vida|satisfaccion general|incidencia de la formacion|condiciones de su vivienda|ingreso actual es",
     "Personal", "Bienestar y calidad de vida", "Cambio percibido", "Indicador de transformación"),
    (r"primer empleo|primer trabajo",
     "Profesional", "Trayectoria laboral: primer empleo", "Antes", "Indicador de transformación"),
    (r"empleo actual|empleo mas reciente|ultimo trabajo|^tipo de contrato:2|culminacion de su primer empleo",
     "Profesional", "Trayectoria laboral: empleo actual", "Actual", "Indicador de transformación"),
    (r"aplicabilidad|pertinente|competencias y habilidades adquiridas|la formacion recibida en la universidad ha si",
     "Profesional", "Relación formación–ocupación", "Contribución percibida", "Indicador de transformación"),
    (r"laborando|ocupacion actual|tipo de vinculacion|tipo de contrato|cargo|tiempo que lleva|numero de empleados|busqueda de empleo|sector economico|clasificacion de la empresa|trabajo independiente|pensionado|ingreso mensual",
     "Profesional", "Situación laboral actual", "Actual", "Indicador de transformación"),
    (r"nivel de logro en el que la formacion|favorecio en usted|exponer|pensamiento critico|metodos|leer y comprender|argumentativa|segunda lengua|ideas originales|conflictos interpersonales|liderazgo|tomar decisiones|resolver problemas|investigacion o proyecto|herramientas informaticas|multiculturales|insercion en el mercado|compartir informacion|trabajar en equipo|mantenerse actualizado|distintas areas|eticos y morales",
     "Personal", "Competencias desarrolladas", "Contribución percibida", "Indicador de transformación"),
    (r"distincion|premio|reconocimiento|gremio|asociacion|red academica|proyectos comunitarios|comunidad beneficiada|proyectos de investigacion|ano de vinculacion|ano de desarrollo|redes o asociaciones",
     "Social", "Participación social, académica y logros", "Actual", "Indicador de transformación"),
    (r"te interesaria|le gustaria estudiar|estudiaria otro|que temas|area del conocimiento|cual de este tipo|tematica u area|educacion continua",
     "Relación con la Universidad", "Demanda de formación (portafolio)", "Actual", "Portafolio de servicios"),
    (r"recomendado|expectativas de formacion|red de amigos|medios desea recibir|conoces algun tomasino|practica o pasantia|logro permanecer|medio que utiliza",
     "Relación con la Universidad", "Vínculo y valoración de la Universidad", "Retrospectivo", "Portafolio de servicios"),
    (r"maximo nivel de estudios|mayor nivel de estudios|otros titulos|titulo obtenido|nivel de formacion|tipo de programa eres|^preg |^maestr |^especial |^docto |^bogota$|^bucaramanga$|^villavicencio$|^tunja$|^vuad$|programa del (pregrado|posgrado)|programa de posgrado|^medellin$",
     "Académica", "Formación alcanzada y posterior", "Actual", "Caracterización"),
    (r"sede|seccional|programa academico|programa del cual|graduado de la seccional|te graduaste de algun posgrado|modalidad|universidad$|institucion en la que",
     "Contexto", "Programa y sede", "No aplica", "Segmentación"),
    (r"ano de graduacion|fecha de graduacion",
     "Contexto", "Cohorte de graduación", "No aplica", "Segmentación"),
    (r"edad|fecha de nacimiento|sexo|genero|estado civil|hijos|personas a cargo|menores de dos|entre \d+ y \d+ anos|mayores de 25|rol en el hogar|orden de nacimiento|responsabilidad economica",
     "Personal", "Condiciones sociodemográficas", "Actual", "Caracterización"),
    (r"pais|ciudad|departamento|residenciado|vives|reside|exterior|si la respuesta anterior es otro",
     "Contexto", "Territorio de residencia", "Actual", "Segmentación"),
]

# Etiquetas de sede homologadas entre bases.
SEDES = {
    "Sede Principal Bogotá y DUAD": "Bogotá",
    "Bogotá": "Bogotá",
    "Seccional Bucaramanga": "Bucaramanga",
    "Bucaramanga": "Bucaramanga",
    "Seccional Villavicencio": "Villavicencio",
    "Villavicencio": "Villavicencio",
    "Seccional Tunja": "Tunja",
    "Tunja": "Tunja",
    "Educación abierta y a distancia": "VUAD",
    "Medellín": "Medellín",
}
