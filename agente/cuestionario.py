"""Contenido del «Modelo de Cuestionario Común Multisede» (propuesta del equipo, Fase 2).

Fuente única para el documento Word/PDF (generar_cuestionario.py) y para la página
del Streamlit. Solo texto: no lee bases ni contiene datos de personas.

NUCLEO: secciones (letra, título, nota, [(código, pregunta, opciones, origen)]).
TRAZA: código -> (dimensión, indicador, PENSER, Percepción, Formulario);
       ✓ = existe igual o casi igual · ≈ = existe, recodificable · — = no existe.
"""

# ---------------------------------------------------------------------------
# Escalas estándar
# ---------------------------------------------------------------------------
NIVEL = "1 Muy bajo\n2 Bajo\n3 Medio\n4 Alto\n5 Muy alto\n99 No aplica"
ACUERDO = ("1 Totalmente en desacuerdo\n2 En desacuerdo\n3 Ni de acuerdo ni en desacuerdo\n"
           "4 De acuerdo\n5 Totalmente de acuerdo")
INCIDENCIA = "0 No incidió\n1 Muy baja\n2 Baja\n3 Media\n4 Alta\n5 Muy alta"
SINO = "1 Sí\n2 No"
ESTRATO = "1 · 2 · 3 · 4 · 5 · 6\n7 Sin estratificar / vivía fuera de Colombia\n98 Prefiero no responder"
SMMLV = ("0 Sin ingresos\n1 Menos de 1 SMMLV\n2 De 1 a menos de 2\n3 De 2 a menos de 3\n"
         "4 De 3 a menos de 4\n5 De 4 a menos de 5\n6 De 5 a menos de 7\n7 De 7 a menos de 10\n"
         "8 10 SMMLV o más\n98 Prefiero no responder")
CARGO = ("1 Directivo\n2 Coordinación / mando medio\n3 Profesional\n4 Técnico o tecnólogo\n"
         "5 Asistencial, auxiliar u operativo\n6 Propietario(a) / independiente")
RELACION = "1 Directa\n2 Indirecta\n3 Ninguna"
ESCOLARIDAD = ("1 Ninguno\n2 Primaria\n3 Secundaria básica (hasta 9.º)\n4 Media (bachiller)\n"
               "5 Técnico o tecnológico\n6 Universitario\n7 Especialización\n8 Maestría\n"
               "9 Doctorado\n97 No sabe")

# ---------------------------------------------------------------------------
# Núcleo común: (código, pregunta, opciones, origen)
# ---------------------------------------------------------------------------
NUCLEO = [
    ("A", "Datos del título de referencia",
     "Se precargan desde el registro académico; el graduado solo los confirma. Título de referencia: "
     "el más reciente obtenido en la USTA.", [
        ("A01", "Sede o seccional de la que se graduó.",
         "1 Bogotá (Sede Principal)\n2 Bucaramanga\n3 Tunja\n4 Villavicencio\n5 Medellín\n"
         "6 Universidad Abierta y a Distancia (VUAD)", "PENSER · Percepción · Formulario (una sola lista)"),
        ("A02", "Nivel del título de referencia.",
         "1 Tecnológico\n2 Profesional (pregrado)\n3 Especialización\n4 Maestría\n5 Doctorado",
         "Percepción · Formulario"),
        ("A03", "Programa académico.",
         "Lista institucional única con código SNIES, filtrada por A01 y A02", "PENSER · Percepción · Formulario"),
        ("A04", "Año y periodo de graduación.", "Año (aaaa) y periodo (I / II)", "PENSER · Percepción"),
        ("A05", "Modalidad en la que cursó el programa.",
         "1 Presencial\n2 A distancia\n3 Virtual\n4 Híbrida", "Percepción · Formulario"),
    ]),
    ("B", "Perfil y origen familiar", "Variables de contexto y de punto de partida (antes de la formación).", [
        ("B01", "Año de nacimiento.", "Número de 4 dígitos", "Ajustada (PENSER: edad; Percepción: fecha; Formulario: rango)"),
        ("B02", "Sexo / género con el que se identifica.",
         "1 Mujer\n2 Hombre\n3 No binario / otra identidad\n98 Prefiero no responder", "Percepción · Formulario"),
        ("B03", "Estado civil actual.",
         "1 Soltero(a)\n2 Casado(a)\n3 Unión libre\n4 Separado(a) o divorciado(a)\n5 Viudo(a)\n6 Vida religiosa",
         "Percepción · Formulario"),
        ("B04", "¿Cuántas personas dependen económicamente de usted?", "0 · 1 · 2 · 3 · 4 o más", "Percepción"),
        ("B05", "En cuanto a la responsabilidad económica de su hogar, usted es:",
         "1 Proveedor(a) principal\n2 Co-proveedor(a)\n3 Dependiente económico(a)", "PENSER"),
        ("B06", "País y municipio de residencia actual.", "Lista de países; si es Colombia, lista DIVIPOLA de municipios",
         "Ajustada (Percepción tenía 32 columnas de ciudad)"),
        ("B07", "Máximo nivel educativo alcanzado por su madre.", ESCOLARIDAD, "PENSER · Percepción"),
        ("B08", "Máximo nivel educativo alcanzado por su padre.", ESCOLARIDAD, "PENSER · Percepción"),
        ("B09", "Antes de usted, ¿alguien de su núcleo familiar (padres o hermanos) había obtenido un título universitario?",
         SINO, "Nueva (reemplaza los bloques de hermanos de PENSER)"),
    ]),
    ("C", "Condiciones de vida: antes y ahora",
     "Pares retrospectivos: la misma pregunta referida al momento del grado y al momento actual.", [
        ("C01", "Estrato socioeconómico de su vivienda cuando obtuvo el título.", ESTRATO, "Percepción"),
        ("C02", "Estrato socioeconómico de su vivienda actual.", ESTRATO, "Percepción · Formulario"),
        ("C03", "Ingreso mensual propio en el último año de estudios (en salarios mínimos de ese año).", SMMLV,
         "Ajustada (PENSER: Sí/No; Percepción: pesos de 2022)"),
        ("C04", "Ingreso mensual propio actual (en salarios mínimos del año en curso).", SMMLV, "Formulario (rangos ampliados)"),
        ("C05", "Considera que su ingreso actual es:",
         "1 Insuficiente: no cubre todas mis necesidades básicas\n2 Suficiente: cubre mis necesidades básicas, sin excedente\n"
         "3 Muy suficiente: cubre mis necesidades y deja excedente", "PENSER"),
        ("C06", "Desde que obtuvo su título… (Sí · No · No aplica para cada ítem)",
         "a. La calidad de su vivienda mejoró (compra o adecuaciones)\nb. Adquirió bienes (vivienda, vehículo, inversión)\n"
         "c. Accedió a mejor seguridad social (salud, pensión)\nd. Mejoraron sus condiciones de salud\n"
         "e. Aumentó su participación en actividades culturales, deportivas o artísticas\nf. Está satisfecho(a) con su tiempo libre",
         "Percepción · PENSER (vivienda)"),
        ("C07", "Su grado de satisfacción general con su vida actual es:", NIVEL.replace("\n99 No aplica", ""),
         "Percepción (escala ajustada)"),
    ]),
    ("D", "Trayectoria laboral: primer empleo y empleo actual",
     "D06–D11 solo si D01 = 1, 2 o 3. D12 solo si D01 = 4.", [
        ("D01", "¿Cuál es su situación laboral principal hoy?",
         "1 Empleado(a)\n2 Independiente / por cuenta propia\n3 Empresario(a) con empleados\n4 Desempleado(a), buscando trabajo\n"
         "5 Estudiando, sin trabajar\n6 Pensionado(a)\n7 Otra (hogar, no busca trabajo)", "Formulario (PENSER: Sí/No)"),
        ("D02", "¿Cuánto tardó en conseguir su primer empleo después de obtener el título?",
         "1 Ya trabajaba antes de graduarse\n2 Menos de 1 mes\n3 De 1 a 3 meses\n4 De 3 a 6 meses\n5 De 6 meses a 1 año\n"
         "6 Más de 1 año\n7 Aún no ha tenido empleo", "Percepción"),
        ("D03", "Relación entre su primer empleo y el título obtenido.", RELACION, "Percepción"),
        ("D04", "Nivel del cargo en su primer empleo.", CARGO, "Percepción (era texto libre)"),
        ("D05", "Grado de correspondencia entre las funciones de su primer empleo y las competencias del programa.",
         NIVEL, "Percepción (escala ajustada)"),
        ("D06", "Tipo de vinculación en su trabajo actual.",
         "1 Contrato a término indefinido\n2 Contrato a término fijo\n3 Prestación de servicios\n4 Obra o labor\n"
         "5 Honorarios / independiente\n6 Propietario(a) de empresa\n7 Otro", "PENSER · Percepción · Formulario"),
        ("D07", "Nivel del cargo en su trabajo actual.", CARGO, "PENSER · Percepción · Formulario"),
        ("D08", "Relación entre su trabajo actual y el título obtenido.", RELACION, "Percepción (escala corregida)"),
        ("D09", "Grado de correspondencia entre las funciones de su trabajo actual y las competencias del programa.",
         NIVEL, "Percepción · Formulario"),
        ("D10", "Sector económico de la organización donde trabaja.", "Lista de secciones CIIU Rev. 4 A.C. (21 opciones)",
         "Formulario (lista estandarizada)"),
        ("D11", "Origen del capital de la organización.", "1 Privado\n2 Público\n3 Mixto\n4 ONG / sin ánimo de lucro",
         "Formulario"),
        ("D12", "¿Hace cuánto tiempo busca empleo?",
         "1 Menos de 6 meses\n2 De 6 meses a 1 año\n3 De 1 a 2 años\n4 Más de 2 años", "Formulario"),
    ]),
    ("E", "Contribución percibida de la formación", "Lo que el graduado atribuye a su paso por la Universidad.", [
        ("E01", "«El programa del que me gradué es pertinente frente a las demandas del entorno social, laboral y académico.»",
         ACUERDO, "PENSER"),
        ("E02", "«Las competencias que adquirí en mi formación han sido suficientes para los retos de mi trabajo actual.»",
         ACUERDO, "PENSER (escala unificada)"),
        ("E03", "¿En qué nivel la Universidad favoreció en usted el desarrollo de…? (escala de nivel para cada ítem)",
         "a. Competencias profesionales propias del programa\nb. Comunicación escrita\nc. Comunicación oral\n"
         "d. Pensamiento crítico y analítico\ne. Identificación y solución de problemas\nf. Toma de decisiones y responsabilidad\n"
         "g. Creatividad e innovación\nh. Trabajo en equipo y relaciones interpersonales\ni. Liderazgo\n"
         "j. Formulación y gestión de proyectos o investigación\nk. Herramientas digitales e informáticas\nl. Segunda lengua\n"
         "m. Aprendizaje autónomo y actualización permanente\nn. Ética y responsabilidad social\n"
         "o. Comprensión y respeto de otras culturas\np. Manejo de emociones y del estrés",
         "PENSER (10 transversales + profesionales) · Percepción (23 genéricas)"),
        ("E04", "Indique cuánto incidió su formación en… (escala de incidencia para cada ítem)",
         "a. El mejoramiento de sus ingresos\nb. El acceso a oportunidades de empleo\nc. Las condiciones de su vivienda\n"
         "d. El acceso a servicios de salud\ne. El acceso a recreación y deporte\nf. El acceso a mayores niveles educativos",
         "PENSER (se agrega el nivel «Media»)"),
        ("E05", "«La formación recibida en la Universidad ha sido determinante en el mejoramiento de mi calidad de vida.»",
         ACUERDO, "PENSER · Percepción"),
    ]),
    ("F", "Dimensión académica", "Formación posterior al título de referencia (en cualquier institución).", [
        ("F01", "Máximo nivel educativo que ha alcanzado hoy.",
         "1 Técnico\n2 Tecnólogo\n3 Profesional\n4 Especialización\n5 Maestría\n6 Doctorado\n7 Posdoctorado",
         "PENSER · Percepción · Formulario"),
        ("F02", "¿Está estudiando actualmente?",
         "1 No\n2 Sí, en la Universidad Santo Tomás\n3 Sí, en otra institución", "Nueva"),
    ]),
    ("G", "Dimensión social y de reconocimiento", "Hechos ocurridos después de graduarse.", [
        ("G01", "Después de graduarse… (Sí · No para cada ítem)",
         "a. Ha recibido distinciones o premios (laborales, académicos o sociales)\n"
         "b. Pertenece a una red, gremio o asociación profesional o científica\n"
         "c. Ha liderado o acompañado proyectos comunitarios o sociales\n"
         "d. Ha participado en proyectos de investigación\ne. Ha creado una empresa o emprendimiento",
         "PENSER · Formulario (e: nueva)"),
    ]),
    ("H", "Relación con la Universidad", "Insumo para el portafolio de servicios a graduados.", [
        ("H01", "Grado de cumplimiento de sus expectativas de formación con lo que ofreció el programa.",
         NIVEL.replace("\n99 No aplica", ""), "Percepción (escala ajustada)"),
        ("H02", "¿Recomendaría el programa del que se graduó?", "1 Sí\n2 No\n3 No está seguro(a)", "Percepción (reformulada)"),
        ("H03", "¿Le interesaría volver a estudiar en la USTA? (puede marcar varias)",
         "1 Sí, un posgrado\n2 Sí, educación continua (cursos, diplomados)\n3 Sí, otro pregrado\n4 No",
         "Percepción · Formulario"),
        ("H04", "¿Por qué medios prefiere recibir información de la Universidad? (puede marcar varios)",
         "Correo electrónico · WhatsApp · Redes sociales · Llamada · Portal de graduados", "Formulario"),
    ]),
]

# Matriz de trazabilidad: código -> (dimensión, indicador, PENSER, Percepción, Formulario)
#   ✓ = existe igual o casi igual · ≈ = existe, recodificable · — = no existe
TRAZA = {
    "A01": ("Contexto", "Segmentación por sede", "≈", "✓", "≈"),
    "A02": ("Contexto", "Segmentación por nivel", "—", "✓", "≈"),
    "A03": ("Contexto", "Segmentación por programa", "✓", "≈", "≈"),
    "A04": ("Contexto", "Cohorte (años desde el grado)", "✓", "✓", "—"),
    "A05": ("Contexto", "Segmentación por modalidad", "—", "✓", "✓"),
    "B01": ("Personal", "Edad / grupos de edad", "≈", "✓", "≈"),
    "B02": ("Personal", "Segmentación por sexo", "—", "✓", "✓"),
    "B03": ("Personal", "Contexto del hogar", "—", "✓", "≈"),
    "B04": ("Personal", "Contexto del hogar", "—", "✓", "≈"),
    "B05": ("Personal", "Contexto del hogar", "✓", "—", "—"),
    "B06": ("Contexto", "Segmentación territorial", "≈", "≈", "✓"),
    "B07": ("Social", "SOC-02 Primera generación", "✓", "≈", "—"),
    "B08": ("Social", "SOC-02 Primera generación", "✓", "≈", "—"),
    "B09": ("Social", "SOC-02 Primera generación", "≈", "—", "—"),
    "C01": ("Social", "SOC-01 Movilidad de estrato", "—", "✓", "—"),
    "C02": ("Social", "SOC-01 Movilidad de estrato", "—", "✓", "✓"),
    "C03": ("Social", "SOC-03 Mejora de ingresos", "≈", "≈", "—"),
    "C04": ("Social", "SOC-03 Mejora de ingresos", "≈", "≈", "✓"),
    "C05": ("Personal", "Suficiencia del ingreso (nuevo)", "✓", "—", "—"),
    "C06": ("Personal", "PER-01 Mejoras de bienestar", "≈", "✓", "—"),
    "C07": ("Personal", "Satisfacción con la vida (nuevo)", "—", "≈", "—"),
    "D01": ("Profesional", "PRO-04 Empleabilidad actual", "≈", "≈", "✓"),
    "D02": ("Profesional", "PRO-01 Inserción en ≤ 3 meses", "—", "✓", "—"),
    "D03": ("Profesional", "PRO-05 Pertinencia del primer empleo", "—", "✓", "—"),
    "D04": ("Profesional", "Movilidad ocupacional (nuevo)", "—", "≈", "—"),
    "D05": ("Profesional", "PRO-02 Mejora de la correspondencia", "—", "≈", "—"),
    "D06": ("Profesional", "PRO-03 Contrato indefinido", "≈", "≈", "≈"),
    "D07": ("Profesional", "Movilidad ocupacional (nuevo)", "≈", "≈", "≈"),
    "D08": ("Profesional", "Pertinencia del empleo actual", "—", "≈", "—"),
    "D09": ("Profesional", "PRO-02 Mejora de la correspondencia", "—", "≈", "≈"),
    "D10": ("Profesional", "Segmentación por sector", "—", "—", "≈"),
    "D11": ("Profesional", "Segmentación por sector", "—", "—", "✓"),
    "D12": ("Profesional", "Duración del desempleo", "—", "—", "✓"),
    "E01": ("Académica", "Pertinencia del programa (nuevo)", "✓", "—", "—"),
    "E02": ("Profesional", "Suficiencia de competencias", "✓", "—", "≈"),
    "E03": ("Personal", "Índice de competencias favorecidas (nuevo)", "≈", "≈", "—"),
    "E04": ("Personal", "PER-02 Contribución percibida", "≈", "—", "—"),
    "E05": ("Personal", "PER-02 Contribución percibida", "≈", "≈", "—"),
    "F01": ("Académica", "ACA-01 Formación posterior", "✓", "✓", "≈"),
    "F02": ("Académica", "ACA-01 Formación posterior", "—", "—", "—"),
    "G01": ("Social", "ACA-02 Participación social y académica", "✓", "≈", "✓"),
    "H01": ("Relación USTA", "Cumplimiento de expectativas", "—", "≈", "—"),
    "H02": ("Relación USTA", "REL-02 Recomendación", "—", "≈", "—"),
    "H03": ("Relación USTA", "REL-01 Demanda de formación USTA", "—", "≈", "≈"),
    "H04": ("Relación USTA", "Canales de contacto", "—", "—", "✓"),
}

MODULOS = [
    ("M1", "Graduados en el exterior", "Formulario", "Sedes con graduados fuera del país",
     ["País de residencia y tiempo en ese país (menos de 1 año · 1–2 · 2–5 · 5–10 · más de 10 años)",
      "Motivo principal (trabajo · estudio · familia · otro)",
      "¿Su trabajo en el exterior está relacionado con su título? (directa · indirecta · ninguna)"]),
    ("M2", "Búsqueda de empleo y servicios de la Universidad", "Formulario", "Oficinas de graduados / bolsa de empleo",
     ["Medio principal de búsqueda de empleo (portal web · redes sociales · familiares o conocidos · Servicio Público de Empleo · "
      "bolsa de empleo USTA · cajas de compensación · otro)",
      "¿Ha usado los servicios de la Oficina de Graduados? (Sí · No) y satisfacción (escala de nivel)"]),
    ("M3", "Prácticas y actividades extracurriculares", "Percepción", "Comités curriculares",
     ["¿Realizó práctica o pasantía en una organización externa? (Sí · No · No recuerda)",
      "¿La práctica contribuyó a su formación? (escala de nivel) · ¿Fue contratado(a) por esa organización? (Sí · No)",
      "Actividades que más aportaron a su inserción laboral (práctica · trabajo de grado · judicatura · semilleros · "
      "movilidad · educación continua · voluntariado · ninguna; selección múltiple)"]),
    ("M4", "Retroalimentación curricular (abiertas)", "Percepción", "Innovación curricular por programa",
     ["¿Qué espacios académicos o actividades aportaron más a su formación?",
      "¿Qué espacios académicos aportaron menos?",
      "¿Qué áreas, técnicas o herramientas debería incluir el programa para el desempeño actual de sus graduados?"]),
    ("M5", "Empresa, emprendimiento e independientes", "Formulario", "Unidades de emprendimiento",
     ["Tiempo en su trabajo actual (menos de 6 meses · 6–12 meses · 1–3 años · 3–5 años · más de 5 años)",
      "Tamaño de la organización (1–9 · 10–49 · 50–199 · 200 o más empleados)",
      "Si creó empresa: año de creación, número de empleos que genera y sector (CIIU)"]),
    ("M6", "Hogar y capital familiar", "PENSER · Percepción · Formulario", "Estudios de movilidad social",
     ["¿Tiene hijos? (Sí · No) · Rol en el hogar (jefe(a) · cónyuge · hijo(a) · otro)",
      "Número de hermanos y orden de nacimiento",
      "Al obtener el título, ¿su familia tenía empresa propia? ¿tenía contactos en instituciones públicas o privadas? (Sí · No)"]),
    ("M7", "Detalle de reconocimientos y redes", "PENSER · Formulario", "Se activa si G01 a, b, c o d = Sí",
     ["Tipo de distinción (laboral · académica · social · otra), entidad que la otorga y año",
      "Nombre de la red o asociación y año de vinculación",
      "Población beneficiada por el proyecto comunitario y principales logros (abierta)"]),
]

REEMPLAZOS = [
    ("78 columnas de escolaridad de los hermanos (PENSER III.15), entre 68 % y 99,7 % vacías",
     "B09: una pregunta directa de primera generación universitaria"),
    ("Fecha de nacimiento exacta (Percepción) / edad en rangos (Formulario)",
     "B01: año de nacimiento; da la edad exacta y es un dato menos sensible"),
    ("28 columnas de programa separadas por sede y nivel (Percepción)", "A03: una lista única con código SNIES, precargada"),
    ("32 columnas de ciudad, una por departamento (Percepción)", "B06: una lista DIVIPOLA"),
    ("Rangos de salario en pesos de 2022, distintos según el nivel de formación (Percepción)",
     "C03 y C04: los mismos rangos en SMMLV para todos; comparables entre años"),
    ("«¿Su ingreso actual es superior al de su último año de estudio? Sí/No» (PENSER III.18)",
     "Se deriva de C03 frente a C04 y además da la magnitud del cambio"),
    ("Nivel educativo de los padres en un solo campo con 40 combinaciones (Percepción)", "B07 y B08 por separado"),
    ("Escalas mezcladas en una misma pregunta (PENSER III.19.1 e IV.20; relación del empleo actual en Percepción)",
     "Una escala estándar por tipo de pregunta (sección 6)"),
    ("«¿Se encuentra laborando actualmente? Sí/No» (PENSER I.1)", "D01: situación laboral con 7 categorías"),
    ("Nombre de la organización y cargo en texto libre (PENSER I.2.1 e I.2.3)",
     "D07 y D10 cerrados; el texto libre identifica a la persona y es difícil de codificar"),
    ("Número de documento dentro de la encuesta", "Identificador seudonimizado generado por el sistema (sección 9)"),
    ("«¿Conoces algún Tomasino viviendo en el exterior?» (Formulario)",
     "Se retira del instrumento de medición: es una acción de difusión, no una variable"),
]


# ---------------------------------------------------------------------------
# Lectura sencilla (solo para la página Streamlit; el Word no los usa)
# ---------------------------------------------------------------------------
# Sección -> (para qué sirve, qué permitirá decir)
PARA_QUE = {
    "A": ("Saber de qué sede, programa y año es cada graduado.",
          "Separar los resultados: «graduados de Bucaramanga de 2021 frente a los de Tunja de 2021»."),
    "B": ("Conocer el punto de partida de la persona y de su familia.",
          "«¿Qué parte de nuestros graduados es la primera generación universitaria de su familia?»"),
    "C": ("Comparar cómo vivía la persona al graduarse y cómo vive hoy.",
          "«¿Qué parte de los graduados subió de estrato o de ingreso desde que se graduó?»"),
    "D": ("Seguir el camino laboral: el primer empleo frente al empleo actual.",
          "«¿Cuánto tardan en conseguir trabajo y ese trabajo tiene que ver con lo que estudiaron?»"),
    "E": ("Recoger lo que el graduado atribuye a su formación en la USTA.",
          "«¿Qué competencias sienten los graduados que la Universidad les ayudó a desarrollar?»"),
    "F": ("Saber si la persona siguió estudiando después del título.",
          "«¿Qué parte de los graduados hizo un posgrado, y dónde?»"),
    "G": ("Registrar logros y participación social después del grado.",
          "«¿Cuántos han creado empresa, recibido premios o liderado proyectos comunitarios?»"),
    "H": ("Conocer la relación actual del graduado con la Universidad.",
          "Diseñar el portafolio de servicios: qué cursos ofrecer y por qué medio avisar."),
}

# Un mismo tema (el ingreso) preguntado de tres formas: (base, cómo pregunta, problema)
EJEMPLO_INGRESO = [
    ("PENSER 2025", "«¿Su ingreso actual es superior al de su último año de estudio?» Sí / No",
     "Dice si mejoró, pero no cuánto."),
    ("Percepción 2022", "Rangos de salario en pesos de 2022, distintos según el nivel de formación",
     "Los pesos de 2022 pierden valor con la inflación y los rangos no coinciden entre niveles."),
    ("Formulario 2023–26", "Solo el ingreso actual, en rangos",
     "No pregunta por el ingreso al graduarse: no se puede ver el cambio."),
]

# Graduado ficticio para explicar los pares antes/ahora: (tema, al grado, hoy, ¿mejoró?)
EJEMPLO_GRADUADO = [
    ("Estrato (C01 → C02)", "2", "3", True),
    ("Ingreso (C03 → C04)", "De 1 a 2 SMMLV", "De 3 a 4 SMMLV", True),
    ("Nivel del cargo (D04 → D07)", "Asistencial", "Profesional", True),
    ("Correspondencia con lo estudiado (D05 → D09)", "3 Medio", "4 Alto", True),
    ("Nivel educativo (A02 → F01)", "Profesional", "Profesional", False),
]

GLOSARIO = [
    ("Núcleo común", "Las preguntas que todas las sedes hacen exactamente igual. Es lo que permite comparar."),
    ("Módulo opcional", "Bloque extra que una sede agrega si le interesa un tema. Va siempre después del núcleo."),
    ("Pregunta precargada", "Dato que la Universidad ya tiene (sede, programa, año de grado). El graduado solo lo confirma."),
    ("Par «antes / ahora»", "La misma pregunta hecha dos veces: cómo estaba al graduarse y cómo está hoy."),
    ("Pregunta retrospectiva", "Pide recordar una situación pasada. Es útil, pero la memoria puede fallar (sesgo de recuerdo)."),
    ("SMMLV", "Salario mínimo mensual legal vigente. Medir el ingreso en salarios mínimos evita que la inflación "
              "distorsione la comparación entre años."),
    ("Cohorte", "Grupo de personas que se graduaron en el mismo año o periodo."),
    ("Escala de respuesta", "Las opciones de una pregunta, por ejemplo de 1 «Muy bajo» a 5 «Muy alto»."),
    ("Indicador", "Cifra que resume un aspecto de la transformación; por ejemplo, el % de graduados que subió de estrato (SOC-01)."),
    ("Trazabilidad", "Poder decir de dónde viene cada pregunta y para qué indicador sirve."),
    ("Identificador seudonimizado", "Código que reemplaza el documento de identidad: une las respuestas de una misma "
                                    "persona en distintos años sin revelar quién es."),
    ("Panel", "Seguimiento a las mismas personas en el tiempo, preguntándoles varias veces."),
    ("Prueba cognitiva", "Algunos graduados responden en voz alta para detectar preguntas que se entienden mal."),
    ("Alfa de Cronbach", "Mide si un grupo de preguntas sobre un mismo tema se responde de forma coherente. "
                         "Va de 0 a 1; desde 0,7 suele considerarse aceptable."),
    ("Análisis factorial confirmatorio", "Prueba estadística de que las preguntas se agrupan como se espera "
                                         "(por ejemplo, las 16 competencias de E03)."),
    ("SNIES · DIVIPOLA · CIIU", "Listas oficiales de Colombia: de programas académicos, de municipios y de sectores "
                                "económicos. Usarlas evita respuestas escritas a mano que luego no coinciden."),
    ("Ley 1581 de 2012", "Ley colombiana de protección de datos personales: exige consentimiento y cuidado con la información."),
]


def preguntas():
    """Lista plana del núcleo: dicts con sección y campos de cada pregunta."""
    return [{"seccion": letra, "titulo_seccion": titulo, "codigo": cod, "pregunta": p,
             "opciones": o, "origen": orig}
            for letra, titulo, _, preg in NUCLEO for cod, p, o, orig in preg]


def total_preguntas() -> int:
    return sum(len(p) for *_, p in NUCLEO)


N_PRECARGADAS = len(NUCLEO[0][3])
