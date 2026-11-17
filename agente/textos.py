"""Textos del documento técnico que no salen de los datos ni de contenido/*.json.

Los usan el Streamlit (streamlit_app/app.py) y la versión HTML
(generar_html.py), para que las dos digan lo mismo. Todo lo que hay aquí es
propuesta del equipo salvo que diga otra cosa.
"""

DIMENSIONES = {
    "Social": {"icono": "🤝", "que": "Cambios en la posición social y económica: estrato, ingresos, "
               "llegar más lejos que los padres y participar en la comunidad."},
    "Profesional": {"icono": "💼", "que": "Cómo entra y avanza en el trabajo: rapidez para emplearse, "
                    "estabilidad y relación del empleo con lo que estudió."},
    "Personal": {"icono": "🌱", "que": "Calidad de vida y bienestar después del título, y lo que el "
                 "graduado siente que la formación le aportó."},
    "Académica": {"icono": "🎓", "que": "Si sigue formándose después del grado: posgrados y otros títulos."},
    "Relación con la Universidad": {"icono": "🏛️", "que": "El vínculo con la USTA: recomendación e "
                                    "interés en volver a estudiar. No mide transformación; alimenta el portafolio."},
}

PALETA_VEREDICTO = {
    "Sirve: ya se usa": "#F2B705", "Sirve: disponible": "#1F5FBF", "Sirve con reservas": "#7FA6E0",
    "Sirve: para desagregar": "#0E7C86", "Sirve: para describir": "#8FC6CB",
    "Sirve: para el portafolio": "#2E7D32", "No se usa: control": "#C9CED8",
    "No se usa: dato personal": "#B23B3B", "Revisar": "#999999",
}

SIGNIFICADO_VEREDICTO = {
    "Sirve: ya se usa": "Alimenta uno de los 14 indicadores o el índice.",
    "Sirve: disponible": "Mide transformación (tiene un antes, un ahora o un cambio) pero aún no está en un indicador.",
    "Sirve con reservas": "Es percepción de lo que aportó la formación, o texto abierto que hay que codificar.",
    "Sirve: para desagregar": "Sede o año de grado: permite cortar los resultados por grupos.",
    "Sirve: para describir": "Caracteriza al graduado o su contexto (edad, territorio, programa).",
    "Sirve: para el portafolio": "Dice qué servicios o formación demanda el graduado.",
    "No se usa: control": "Consentimiento o metadatos del formulario.",
    "No se usa: dato personal": "Nombre, documento, correo, teléfono o empresa. Excluida (Ley 1581 de 2012).",
}

# (fuente, para qué, cómo acceder)
FUENTES_EXTERNAS = [
    ("Empleadores", "Valorar el desempeño del graduado (hoy nivel D: no hay base)", "Encuesta corta; reutilizar instrumentos del IMS 2019"),
    ("Observatorio Laboral para la Educación (MEN)", "Vinculación formal e ingreso de los graduados", "Solicitud institucional / convenio"),
    ("SNIES / registro de graduados USTA", "Totales para ponderar y verificar títulos de posgrado", "Solicitud a la Dirección de Graduados"),
    ("RUES y CvLAC", "Verificar emprendimientos, gremios e investigación", "Consulta pública, con consentimiento"),
    ("DANE, SECOP", "Contexto territorial y contratación pública", "Datos abiertos"),
]

# (método, para qué sirve, dónde se usa)
METODOS = [
    ("Proporción con intervalo de Wilson (95 %)", "Dar cada porcentaje con su margen de error, también en grupos pequeños", "Los 14 indicadores"),
    ("Matriz de transición", "Ver de dónde venían y a dónde llegaron", "Estrato, contrato, correspondencia empleo–formación"),
    ("Preguntas retrospectivas", "Obtener el «antes» en la misma encuesta", "Estrato al graduarse, primer empleo"),
    ("Pseudo-panel por cohortes", "Aproximar el efecto del tiempo comparando promociones", "Desgloses por cohorte"),
    ("Índice formativo (0–100)", "Resumir cuatro dimensiones en un número", "Prototipo de índice"),
    ("Análisis factorial (pendiente)", "Validar las escalas de competencias", "Fase 2"),
    ("Ponderación por raking (pendiente)", "Corregir que respondan más unos grupos que otros", "Fase 2, con totales del SNIES"),
]

# (dimensión, pregunta antes/ahora, escala, qué cambia frente a hoy, alimenta)
INSTRUMENTO = [
    ("Identificación", "Huella cifrada del documento, programa, sede, fecha de grado", "—",
     "Llave estable para seguir a la misma persona (hoy solo 89 coinciden entre bases)", "Todos"),
    ("Social", "Estrato al graduarse / estrato actual", "1 a 6", "Igual que Percepción", "SOC-01, índice"),
    ("Social", "Máximo nivel educativo de la madre y del padre", "Categorías de PENSER", "Unifica las dos versiones actuales", "SOC-02"),
    ("Social", "Ingreso mensual al graduarse / actual", "Rangos en SMMLV", "Hoy solo hay «¿es mayor?» (sí/no)", "SOC-03"),
    ("Profesional", "Situación laboral al graduarse / actual", "Empleado, independiente, buscando, inactivo", "Misma escala en las tres bases", "PRO-01, PRO-04"),
    ("Profesional", "Tiempo hasta el primer empleo", "Categorías de Percepción", "Sin cambios", "PRO-01, índice"),
    ("Profesional", "Tipo de contrato del primer empleo / actual", "6 categorías cerradas", "Hoy 22 variantes de texto", "PRO-03"),
    ("Profesional", "Correspondencia del empleo con la formación, primero / actual", "0 a 5", "Sin cambios", "PRO-02, índice"),
    ("Profesional", "Nivel del cargo, primero / actual", "Operativo, profesional, coordinación, dirección", "Hoy en texto libre: no medible", "Nuevo: desarrollo profesional"),
    ("Personal", "Seis mejoras de bienestar después del título", "Sí / No", "Sin cambios", "PER-01, índice"),
    ("Académica", "Máximo nivel de estudios y estudios en curso", "Niveles SNIES", "Unifica PENSER y Percepción", "ACA-01, índice"),
    ("Académica / Social", "Investigación, proyectos comunitarios, gremios, distinciones", "Sí / No + año", "El año permite saber si fue después del grado", "ACA-02"),
    ("Relación", "Recomendación del programa e interés en formación continua", "0 a 10 / Sí-No", "Sin cambios", "REL-01, REL-02"),
]

# Actividades de la Fase 2 (lámina 6) con la propuesta del equipo.
ACTIVIDADES_FASE2 = [
    ("Aplicación piloto en programas o seccionales",
     "Aplicar el instrumento mínimo común en 2 o 3 programas de Bogotá y una seccional, a "
     "graduados de 1, 3 y 5 años. Incluir a quienes se gradúan en el periodo (línea base)."),
    ("Recolección y análisis de información",
     "Calcular los 14 indicadores y el índice con el agente de perfilado; ponderar con totales "
     "del SNIES; comparar con los resultados de esta fase."),
    ("Contraste con actores clave",
     "Taller con directores de programa para leer los resultados; encuesta corta a empleadores; "
     "grupos focales con graduados para validar las dimensiones."),
    ("Ajustes al modelo y a los instrumentos",
     "Definir pesos del índice con expertos y comparar con pesos iguales; corregir la escala "
     "académica; recodificar el nivel del cargo."),
    ("Documentación de resultados y lecciones",
     "Actualizar las fichas técnicas con la nueva línea base y fijar metas; bitácora de decisiones."),
]

# (actividad, inicio, fin, periodo, realizada) en meses desde noviembre; diciembre y enero sin actividades.
CRONOGRAMA_FASE2 = [
    ("Ajustar instrumento y diseño muestral", 0, 1, "nov", True),
    ("Aplicación piloto", 3, 4.5, "feb – mediados de mar", False),
    ("Análisis y ponderación", 4, 5.5, "mar – mediados de abr", False),
    ("Contraste con actores clave", 4.5, 6, "mediados de mar – abr", False),
    ("Ajustes y documentación", 5, 6, "abr", False),
]
