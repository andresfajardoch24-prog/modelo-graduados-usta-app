"""Documento técnico del Modelo de Seguimiento y Evaluación de la Transformación
de los Graduados (USTA), organizado por las fases del modelo (lámina 6).

Se ejecuta en local:  streamlit run app.py  (desde esta carpeta).
Solo lee salidas agregadas del agente de perfilado; nunca abre las bases con
datos personales, así que puede correr sin acceso a DATAS GRADUADOS.
"""
import html
import importlib
import json
import sys
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
from agente import config as _config, cuestionario as Q, fichas as F, textos as _textos  # noqa: E402

# Streamlit solo vigila la carpeta de app.py: sin esto, tras un push el servidor (local o
# Streamlit Cloud) seguiría usando la versión vieja de los módulos de agente/ que ya tenía en memoria.
for _m in (_config, _textos, Q, F):
    importlib.reload(_m)
from agente.textos import (ACTIVIDADES_FASE2, CRONOGRAMA_FASE2, DIMENSIONES,  # noqa: E402
                           FUENTES_EXTERNAS, INSTRUMENTO, METODOS, PALETA_VEREDICTO,
                           SIGNIFICADO_VEREDICTO)

RESULTADOS = F.config.CARPETA_ENTREGABLES
DOCX_FICHAS = RESULTADOS / "Fichas_Tecnicas_Indicadores.docx"
DOCX_IMPACTO = RESULTADOS / "Impacto_vs_Transformacion_del_Graduado.docx"
DOCX_CUESTIONARIO = RESULTADOS / "Modelo_Cuestionario_Comun_Graduados.docx"
PDF_CUESTIONARIO = RESULTADOS / "Modelo_Cuestionario_Comun_Graduados.pdf"

NAVY, NAVY2, GOLD, SERIES, GRIS = "#0A2557", "#123C7C", "#F2B705", "#1F5FBF", "#B8C2D3"
NOMBRE_CORTO = {"penser": "PENSER 2025", "percepcion": "Percepción 2022", "formulario": "Formulario 2023–26"}
ORDEN_COH = ["Hasta 2010", "2011–2015", "2016–2018", "2019–2021", "2022–2024", "2022"]

st.set_page_config(page_title="Modelo de Transformación del Graduado · USTA", page_icon="🎓",
                   layout="wide")


# ---------------------------------------------------------------------------
# Datos (solo agregados)
# ---------------------------------------------------------------------------
@st.cache_data
def cargar():
    datos, dic, explica = F.cargar()
    leer = lambda p: json.loads(p.read_text(encoding="utf-8"))  # noqa: E731
    conceptual = leer(F.config.CONTENIDO_CONCEPTUAL)
    marcos = leer(F.config.CONTENIDO_MARCOS)
    return (datos, F.diccionario_con_veredicto(dic), explica, conceptual, marcos,
            F.fichas(datos, dic, explica))


DATOS, DIC, EXPLICA, CONC, MARCOS, FICHAS = cargar()
IND = {i["id"]: i for i in DATOS["indicadores"]}
MODELO = CONC["modelo"]


# ---------------------------------------------------------------------------
# Estilo y componentes
# ---------------------------------------------------------------------------
st.markdown(f"""
<style>
h1, h2, h3 {{ color: {NAVY}; font-family: Cambria, Georgia, serif; }}
.kicker {{ color: #7A5A00; font-size: .78rem; letter-spacing: .14em; text-transform: uppercase;
          font-weight: 700; margin-bottom: -.4rem; }}
/* Cuadros simétricos: un cuadro solo en su columna ocupa todo el alto de la fila. */
[data-testid="stColumn"] > [data-testid="stVerticalBlock"] > [data-testid="stElementContainer"]:only-child,
[data-testid="stColumn"] > [data-testid="stVerticalBlock"] > [data-testid="stElementContainer"]:only-child [data-testid="stMarkdown"],
[data-testid="stColumn"] > [data-testid="stVerticalBlock"] > [data-testid="stElementContainer"]:only-child [data-testid="stMarkdownContainer"] {{
    height: 100%; }}
.card, .fase {{ height: 100%; box-sizing: border-box; display: flex; flex-direction: column; }}
.card .fuente:last-child, .fase .pie {{ margin-top: auto !important; padding-top: .5rem; }}
.fase.ruta .titulo {{ font-weight: 700; font-size: 1.35rem; line-height: 1.25; color: #fff;
                     min-height: 3.75em; margin: .35rem 0 .6rem 0; }}
.fase.ruta .producto {{ line-height: 1.5; min-height: 4.5em; }}
.card {{ background: #fff; border: 1px solid #E3E8F0; border-radius: 10px; padding: 1rem 1.1rem;
        box-shadow: 0 1px 2px rgba(10,37,87,.05); }}
.card h4 {{ margin: 0 0 .35rem 0; color: {NAVY}; font-size: 1.02rem; }}
.card p {{ margin: 0; font-size: .92rem; color: #33415C; }}
.navy {{ background: {NAVY}; color: #fff; border-radius: 10px; padding: 1rem 1.2rem; }}
.navy b {{ color: {GOLD}; }}
.simple {{ background: #FFF4D1; border-left: 4px solid {GOLD}; border-radius: 6px;
          padding: .7rem 1rem; margin: .4rem 0 1rem 0; color: #3D2E00; }}
.fuente {{ color: #6B7A93; font-size: .78rem; margin-top: .3rem; }}
.chip {{ display: inline-block; padding: .1rem .55rem; border-radius: 999px; font-size: .75rem;
        font-weight: 600; margin: 0 .25rem .25rem 0; background: #E8EEF8; color: {NAVY2}; }}
.chip.gold {{ background: #FFF4D1; color: #7A5A00; }}
.chip.ok {{ background: #E3F4EA; color: #1E6B3C; }}
.chip.no {{ background: #F6E3E3; color: #8A2323; }}
.fase {{ border-radius: 10px; padding: .9rem 1rem; color: #fff; height: 100%; }}
.fase small {{ opacity: .85; }}
table.ficha {{ width: 100%; border-collapse: collapse; font-size: .92rem; }}
table.ficha th {{ width: 24%; text-align: left; vertical-align: top; background: #EEF2F8; color: {NAVY};
                 padding: .45rem .7rem; border: 1px solid #D5DCE8; }}
table.ficha td {{ padding: .45rem .7rem; border: 1px solid #D5DCE8; background: #fff; }}
.big {{ font-size: 2.2rem; font-weight: 700; color: {SERIES}; line-height: 1.1; }}
</style>""", unsafe_allow_html=True)


def encabezado(kicker: str, titulo: str, intro: str | None = None):
    st.markdown(f'<div class="kicker">{kicker}</div>', unsafe_allow_html=True)
    st.title(titulo)
    if intro:
        st.markdown(intro)


def simple(texto: str):
    st.markdown(f'<div class="simple"><b>En pocas palabras:</b> {texto}</div>',
                unsafe_allow_html=True)


def nota(titulo: str, texto: str):
    """Recuadro amarillo con una explicación para quien no es especialista."""
    st.markdown(f'<div class="simple"><b>{titulo}</b> {texto}</div>', unsafe_allow_html=True)


def guia_graficos(linea_dorada: bool = False):
    with st.expander("¿Cómo leer estos gráficos?"):
        st.markdown(
            "- **La barra** es el porcentaje (o el puntaje) del grupo.\n"
            "- **La línea negra** en la punta es el *intervalo de confianza*: el rango donde "
            "probablemente está el valor real. Es más corta cuantas más personas respondieron.\n"
            "- **Si las líneas negras de dos grupos se cruzan**, la diferencia entre ellos puede ser "
            "casualidad: no se puede decir que uno esté mejor que el otro.\n"
            "- **Barras grises**: menos de 30 respuestas. Son muy pocas para sacar conclusiones.\n"
            + ("- **La línea dorada punteada** es el promedio general, para comparar cada grupo con él.\n"
               if linea_dorada else "")
            + "- Las cifras describen a **quienes respondieron** la encuesta, no a todos los graduados.")


def lectura_pct(r: dict) -> str:
    """Frase sencilla para un resultado con porcentaje e intervalo."""
    return (f"Resultado «{html.escape(str(r['etiqueta']))}»: <b>{fmt(r['pct'])} %</b> de los "
            f"{fmt(r['n'], 0)} graduados que respondieron, es decir, más o menos <b>{round(r['pct'])} de "
            f"cada 100</b>. Con 95 % de confianza, el valor real está entre {fmt(r['li'])} % y {fmt(r['ls'])} %.")


def comparar_grupos(filas: list, que: str, sufijo: str = " %") -> str | None:
    """Compara el grupo más alto y el más bajo y dice si la diferencia es clara."""
    ok = [r for r in filas if r.get("suficiente", True) and r.get("pct") is not None]
    if len(ok) < 2:
        return None
    alto, bajo = max(ok, key=lambda r: r["pct"]), min(ok, key=lambda r: r["pct"])
    clara = alto["li"] > bajo["ls"]
    return (f"Entre {que}s con suficientes respuestas, el valor más alto es <b>«{html.escape(str(alto['etiqueta']))}»</b> "
            f"({fmt(alto['pct'])}{sufijo}) y el más bajo <b>«{html.escape(str(bajo['etiqueta']))}»</b> "
            f"({fmt(bajo['pct'])}{sufijo}). "
            + ("Sus intervalos no se cruzan: la diferencia <b>probablemente es real</b>, aunque no dice por qué ocurre."
               if clara else
               "Sus intervalos se cruzan: la diferencia <b>podría ser casualidad</b>."))


def fuente(texto: str):
    st.markdown(f'<div class="fuente">Fuente: {texto}</div>', unsafe_allow_html=True)


def card(titulo: str, cuerpo: str, pie: str = ""):
    pie_html = f'<div class="fuente">{pie}</div>' if pie else ""
    st.markdown(f'<div class="card"><h4>{titulo}</h4><p>{cuerpo}</p>{pie_html}</div>',
                unsafe_allow_html=True)


def chips(items, clase=""):
    return "".join(f'<span class="chip {clase}">{i}</span>' for i in items)


def fmt(x, dec=1):
    return f"{x:,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def etiqueta_cohorte(et: str, base: str) -> str:
    # La encuesta de Percepción es de 2022: su última cohorte solo tiene graduados de 2022.
    return "2022" if base == "percepcion" and et == "2022–2024" else et


def barras_ci(filas, etiqueta="etiqueta", valor="pct", alto=None, ref=None, orden=None,
              sufijo=" %", rango=(0, 100)):
    """Barras horizontales con intervalo de confianza; grupos con n < 30 en gris."""
    if not filas:
        st.caption("Sin datos para este corte.")
        return
    df = pd.DataFrame(filas)
    if orden:
        df["_o"] = df[etiqueta].map({k: i for i, k in enumerate(orden)}).fillna(99)
        df = df.sort_values("_o", ascending=False)
    else:
        df = df.iloc[::-1]
    ok = df.get("suficiente", pd.Series(True, index=df.index)).fillna(True)
    color = [SERIES if s else GRIS for s in ok]
    fig = go.Figure(go.Bar(
        x=df[valor], y=df[etiqueta], orientation="h", marker_color=color,
        error_x=dict(type="data", symmetric=False, array=df["ls"] - df[valor],
                     arrayminus=df[valor] - df["li"], color=NAVY, thickness=1.2, width=4),
        text=[f"{fmt(v)}{sufijo}" for v in df[valor]], textposition="outside",
        cliponaxis=False,
        customdata=df[["n", "li", "ls"]].values,
        hovertemplate="%{y}: %{x:.1f}" + sufijo + "<br>IC 95 %: %{customdata[1]:.1f}–%{customdata[2]:.1f}"
                      "<br>n = %{customdata[0]}<extra></extra>"))
    if ref is not None:
        fig.add_vline(x=ref, line_dash="dot", line_color=GOLD, line_width=2)
    fig.update_layout(height=alto or 70 + 42 * len(df), margin=dict(l=10, r=60, t=10, b=10),
                      xaxis=dict(range=list(rango), showgrid=True, gridcolor="#EEF1F6",
                                 ticksuffix=sufijo),
                      yaxis=dict(title=None), plot_bgcolor="#fff", showlegend=False)
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})


def tabla_html(df: pd.DataFrame):
    st.dataframe(df, hide_index=True, width="stretch")


# ---------------------------------------------------------------------------
# Inicio
# ---------------------------------------------------------------------------
def inicio():
    encabezado("Documento técnico del modelo · Consultoría Estadística USTA 2026-II",
               "Modelo de Seguimiento y Evaluación de la Transformación de los Graduados")
    st.markdown(f'<div class="navy"><b>Objetivo del modelo.</b> {MODELO["objetivo"]["texto"]}'
                f'<div style="opacity:.75;font-size:.8rem;margin-top:.4rem">{MODELO["objetivo"]["fuente"]}</div></div>',
                unsafe_allow_html=True)
    st.write("")
    simple("este documento reúne lo que se construyó en la Fase 1: qué es la transformación del "
           "graduado, en qué dimensiones se mira, qué variables de las bases sirven para medirla y "
           "por qué, los indicadores con sus fichas técnicas y un prototipo de índice. Termina con "
           "la propuesta para validar el modelo en la Fase 2.")

    tot = sum(b["registros_analizables"] for b in DATOS["bases"].values())
    c = st.columns(5)
    for col, (v, t) in zip(c, [(3, "bases de graduados"), (f"{tot:,}".replace(",", "."), "registros analizables"),
                               (len(DIC), "variables revisadas"), (len(IND), "indicadores con ficha"),
                               (fmt(DATOS["indice"]["general"]["media"]), "índice prototipo (0–100)")]):
        col.markdown(f'<div class="card"><div class="big">{v}</div><p>{t}</p></div>',
                     unsafe_allow_html=True)
    st.caption("El índice prototipo resume en un número de 0 a 100 cuánto cambió la vida de los graduados "
               "en cuatro dimensiones. No es una nota de aprobado o reprobado: sirve para comparar grupos "
               "y años entre sí.")

    st.subheader("Tres ideas para entender todo el documento")
    cols = st.columns(3)
    for col, (t, d) in zip(cols, [
        ("1 · Transformación no es impacto",
         "Medimos <b>qué cambió</b> en la vida del graduado (empleo, ingresos, estudios…). No afirmamos "
         "que la Universidad <b>causó</b> ese cambio: para eso haría falta comparar con personas parecidas "
         "que no estudiaron."),
        ("2 · Cada cifra trae su margen",
         "Los porcentajes salen de encuestas, no de todos los graduados. Por eso cada uno va con un "
         "<b>intervalo de confianza</b>: el rango donde probablemente está el valor real."),
        ("3 · Solo cifras agregadas",
         "Ninguna página muestra datos de una persona. Todo son porcentajes y promedios de grupos, "
         "como exige la ley de protección de datos (Ley 1581 de 2012)."),
    ]):
        with col:
            card(t, d)
    st.write("")
    nota("¿Primera vez aquí?", "Le sugerimos este recorrido: <b>Marco conceptual</b> (qué es la transformación) "
         "→ <b>Dimensiones, variables e indicadores</b> (qué se midió y qué resultó) → <b>Cuestionario común "
         "multisede</b> (qué se propone preguntar en adelante). Si encuentra una palabra técnica, búsquela en "
         "<b>Anexos · Glosario</b>.")

    st.subheader("Ruta del modelo y dónde estamos")
    colores = [NAVY, "#0E7C86", "#2E7D32", "#6B7A93"]
    estado = ["Cumplida (institucional)", "Entrega del equipo", "Propuesta del equipo", "Futuro"]
    cols = st.columns(4)
    for col, f, colr, est in zip(cols, MODELO["fases"], colores, estado):
        col.markdown(f'<div class="fase ruta" style="background:{colr}"><small>{f["periodo"]}</small>'
                     f'<div class="titulo">{f["fase"]}</div>'
                     f'<div class="producto">Producto: <b>{f["producto"]}</b></div>'
                     f'<div class="pie"><span class="chip gold">{est}</span></div></div>',
                     unsafe_allow_html=True)
    fuente(MODELO["fases_fuente"])

    st.subheader("Objetivos de esta consultoría")
    obj = EXPLICA["objetivos"]
    st.markdown(f"**Objetivo general.** {obj['general']}")
    cols = st.columns(3)
    for col, e in zip(cols, obj["especificos"]):
        with col:
            card(e["verbo"], e["texto"], f"Evidencia: {e['evidencia']}")
    fuente(obj["origen"])

    st.subheader("Cómo leer este documento")
    st.markdown("""
| Sección del menú | Responde a… |
|---|---|
| **Fase 0 · Formulación** | ¿Qué se propuso el proyecto y con qué referentes? |
| **Fase 1 · Marco conceptual** | ¿Qué entendemos por transformación? (pregunta 1 del modelo) |
| **Fase 1 · Dimensiones, variables e indicadores** ⭐ | ¿Qué se puede medir y con cuáles variables? (preguntas 2 y 4) |
| **Fase 1 · Fuentes de información** | ¿Con qué información contamos? (pregunta 3) |
| **Fase 1 · Instrumentos y métodos** | ¿Cómo se mide y qué hay que preguntar en adelante? (pregunta 4) |
| **Fase 1 · Diseño del modelo** | El índice, los usos de la evidencia y el plan (pregunta 5) |
| **Fase 2 · Validación (propuesta)** | ¿Qué debe hacerse en el piloto? |
| **Anexos** | Fichas técnicas de los 14 indicadores y glosario |
""")
    st.caption("Las afirmaciones tomadas de un documento llevan su fuente. Lo que no la lleva es "
               "propuesta del equipo consultor. Todas las cifras son agregadas: ninguna página "
               "muestra datos personales.")


# ---------------------------------------------------------------------------
# Fase 0
# ---------------------------------------------------------------------------
def fase0():
    encabezado("Fase 0 · ago-2025 – oct-2025", "Formulación del proyecto",
               "La fase 0 la cerró la Universidad con el proyecto aprobado. Aquí se resume lo que "
               "de ella toma esta consultoría: objetivos, referentes, método y alineación institucional.")
    simple("antes de empezar a medir, la Universidad definió <b>qué quería saber</b> de sus graduados, "
           "<b>en qué autores e informes</b> se apoya y <b>cómo</b> se iba a estudiar. Esta página resume "
           "esas decisiones: son las reglas de juego del resto del documento.")
    t1, t2, t3, t4 = st.tabs(["Objetivos y alcance", "Referentes teóricos", "Diseño metodológico",
                              "Alineación institucional"])
    with t1:
        st.markdown(f"**Propósito del modelo.** {MODELO['proposito']['texto']}")
        fuente(MODELO["proposito"]["fuente"])
        st.markdown("#### ¿El alcance es un modelo o un índice?")
        c1, c2 = st.columns(2)
        with c1:
            card("El alcance es el modelo",
                 "Un sistema completo: qué es la transformación, qué se mide, con qué fuentes, con qué "
                 "indicadores y para qué se usa la evidencia. La consultoría entrega su base técnica.")
        with c2:
            card("El índice es una pieza del modelo",
                 "Un número de 0 a 100 que resume cuatro dimensiones. Es un prototipo para discutir "
                 "en la Fase 2, no el fin del estudio.")
        st.markdown("#### Lo que no incluye esta etapa")
        st.markdown("- Afirmar que la Universidad **causó** los cambios (eso es impacto, no transformación).\n"
                    "- Recolectar datos nuevos: se trabajó con las tres bases existentes.\n"
                    "- Fijar pesos definitivos del índice: le corresponde a la validación.")
    with t2:
        nota("¿Qué son los referentes?", "Las teorías, estudios e informes en los que se apoya el modelo. "
             "Cada bloque dice qué plantean (con su fuente) y, al final, <b>qué le aporta al proyecto</b>; "
             "si tiene poco tiempo, lea solo esa línea.")
        for b in MARCOS["teorico"]:
            with st.expander(f"{b['n']}. {b['titulo']}", expanded=b["n"] in ("2", "3")):
                for p in b["puntos"]:
                    st.markdown(f"- {p['texto']}  \n  <span class='fuente'>{p['fuente']}</span>",
                                unsafe_allow_html=True)
                st.markdown(f"**Aporte al proyecto:** {b['aporte']}")
        st.info(f"**Vacío que atiende el proyecto.** {MARCOS['vacio']}")
    with t3:
        m = MARCOS["metodologico"]
        st.markdown(f"**Tipo de estudio.** {m['tipo']['texto']}")
        st.markdown(f"_{m['tipo']['mixto']}_")
        fuente("; ".join(m["tipo"]["fuentes"]))
        c1, c2 = st.columns(2)
        c1.markdown(f"**Unidad de análisis:** {m['unidad']}  \n**Muestreo:** {m['muestreo']['texto']}")
        c2.markdown("**Exclusiones:**\n" + "\n".join(f"- {e}" for e in m["exclusiones"]))
        with st.expander("¿Qué quieren decir estos términos?", expanded=True):
            st.markdown(
                "- **Cuantitativo y descriptivo:** se trabaja con números para *describir* cómo están los "
                "graduados, no para probar qué causó su situación.\n"
                "- **No experimental:** nadie fue asignado a un grupo; se observa lo que ya pasó.\n"
                "- **Preguntas retrospectivas:** se le pide a la persona recordar cómo estaba antes "
                "(por ejemplo, su estrato al graduarse).\n"
                "- **Comparación entre cohortes (pseudo-panel):** como no se sigue a las mismas personas, se "
                "compara a quienes se graduaron hace poco con quienes se graduaron hace más tiempo.\n"
                "- **Unidad de análisis:** a quién se estudia; aquí, cada graduado.\n"
                "- **Muestreo no probabilístico, por autoselección:** respondió quien quiso. Por eso los "
                "resultados describen a quienes respondieron y no se pueden generalizar sin cuidado a "
                "todos los graduados.")
        st.markdown("#### Etapas del trabajo")
        tabla_html(pd.DataFrame([{"Etapa": f["fase"], "Qué se hace": f["detalle"],
                                  "Pregunta del modelo": f["pregunta"]} for f in m["fases"]]))
        st.markdown("#### Técnicas")
        tabla_html(pd.DataFrame(m["tecnicas"]).rename(columns={"tecnica": "Técnica", "para": "Para qué"}))
    with t4:
        st.markdown("El modelo responde a dos usos institucionales definidos en la lámina 4 y a la "
                    "exigencia de acreditación del CESU.")
        nota("En palabras sencillas:", "la información sirve para dos cosas concretas: <b>mejorar los "
             "programas</b> (qué enseñar, qué cambiar) y <b>ofrecer servicios útiles a los graduados</b> "
             "(cursos, empleo, redes). Además, el CESU (Consejo Nacional de Educación Superior) pide a las "
             "universidades conocer qué pasa con sus graduados para acreditar su calidad.")
        c1, c2 = st.columns(2)
        u = CONC["usos"]
        with c1:
            card(u["curricular"]["titulo"], "<br>".join(f"• {x}" for x in u["curricular"]["que_permite"]),
                 u["fuente"])
        with c2:
            card(u["portafolio"]["titulo"], "<br>".join(f"• {x}" for x in u["portafolio"]["ambitos"]),
                 u["fuente"])
        st.write("")
        norm = next(b for b in MARCOS["teorico"] if b["n"] == "6")
        st.markdown(f"**Marco normativo.** {norm['puntos'][0]['texto']}")
        fuente(norm["puntos"][0]["fuente"])


# ---------------------------------------------------------------------------
# Fase 1 · 1. Marco conceptual
# ---------------------------------------------------------------------------
def f1_marco():
    encabezado("Fase 1 · Conceptualización", "Marco conceptual de la transformación del graduado")
    tr = CONC["transformacion"]
    st.markdown(f'<div class="navy"><b>Transformación del graduado.</b> {tr["definicion_modelo"]["texto"]}'
                f'<div style="opacity:.75;font-size:.8rem;margin-top:.4rem">{tr["definicion_modelo"]["fuente"]}</div></div>',
                unsafe_allow_html=True)
    st.write("")
    simple("la transformación es <b>lo que cambió en la vida del graduado</b> desde que estudió. "
           "No es lo mismo que el impacto, que es <b>la parte de ese cambio que se debe a la Universidad</b>.")

    st.subheader("Observación frente a causa")
    ej = tr["ejemplo_modelo"]
    c1, c2 = st.columns(2)
    with c1:
        card("✔ Transformación (lo que mide el modelo)", f"«{ej['observacion']}»")
    with c2:
        card("✖ Impacto causal (exige más)", f"«{ej['causal']}»")
    st.caption(ej["lectura"] + " · " + ej["fuente"])
    nota("Un ejemplo cotidiano:", "si una persona hoy gana más que cuando se graduó, eso es "
         "<b>transformación</b>, y se puede observar con una encuesta. Decir que gana más <b>gracias a</b> "
         "la Universidad es <b>impacto</b>: también pudo influir la economía, su familia o su ciudad. Para "
         "afirmarlo habría que compararla con alguien muy parecido que no estudió, y esos datos no existen. "
         "Por eso el modelo habla de transformación.")

    st.subheader("Definición operativa para medir")
    do = tr["definicion_operativa"]
    st.caption("«Operativa» quiere decir: la definición convertida en reglas concretas para decidir qué "
               "cuenta como transformación al revisar los datos.")
    st.markdown(f"> {do['texto']}")
    for c in do["criterios"]:
        st.markdown(f"- {c}")
    fuente(do["origen"])

    st.subheader("Conceptos que no hay que confundir")
    tabla_html(pd.DataFrame(tr["diferencias"]).rename(
        columns={"concepto": "Concepto", "que_es": "Qué es", "pregunta": "Pregunta que responde"}))

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Seguimiento y evaluación")
        st.caption("En corto: el seguimiento **observa** (toma los datos cada cierto tiempo) y la "
                   "evaluación **interpreta** (dice si lo observado es bueno y qué hacer).")
        for s in tr["seguimiento_vs_evaluacion"]:
            card(s["concepto"], f"{s['funcion']}. <i>{s['pregunta']}</i>")
            st.write("")
        fuente(tr["seguimiento_fuente"])
    with c2:
        st.subheader("Factores externos")
        st.markdown("Influyen en los resultados del graduado además de la formación; por eso se lee "
                    "segmentado y no se afirma causalidad:")
        st.markdown(chips(tr["factores_externos"]["lista"]), unsafe_allow_html=True)
        fuente(tr["factores_externos"]["fuente"])
        st.caption("«Leer segmentado» es comparar grupos parecidos entre sí (misma sede, mismo programa, "
                   "mismo año de grado) en vez de mezclar a todos, para que esos factores pesen menos.")

    st.subheader("Las cinco preguntas del modelo y dónde se responden")
    donde = {1: "Esta página", 2: "Dimensiones, variables e indicadores", 3: "Fuentes de información",
             4: "Instrumentos y métodos · Diseño del modelo", 5: "Diseño del modelo"}
    tabla_html(pd.DataFrame([{"#": p["n"], "Pregunta": p["pregunta"], "Tareas": " · ".join(p["tareas"]),
                              "Dónde se responde": donde[p["n"]]} for p in MODELO["preguntas"]]))
    fuente(MODELO["preguntas_fuente"])


# ---------------------------------------------------------------------------
# Fase 1 · 2. Dimensiones, variables e indicadores (sección central)
# ---------------------------------------------------------------------------
def f1_dimensiones():
    encabezado("Fase 1 · Conceptualización · sección central",
               "Definición de dimensiones, variables e indicadores")
    simple("la transformación se mira en <b>cuatro dimensiones</b>. Dentro de cada una hay "
           "<b>aspectos</b> (por ejemplo, movilidad social). Cada aspecto se mide con <b>variables</b> "
           "(preguntas de las encuestas) y las variables se combinan en <b>indicadores</b>.")
    st.markdown(chips(["Dimensión", "→ Aspecto", "→ Variable", "→ Indicador", "→ Índice"], "gold"),
                unsafe_allow_html=True)
    soc = IND.get("SOC-01")
    if soc:
        r = soc["resultados"][0]
        st.markdown(
            "**Un ejemplo de la cadena completa:** dimensión **Social** → aspecto **movilidad social** → "
            "variables **«estrato al graduarse»** y **«estrato actual»** → indicador **SOC-01 Movilidad de "
            f"estrato**, que da {fmt(r['pct'])} % ({r['etiqueta'].lower()}). Esas mismas variables forman el "
            "componente social del **índice** de 0 a 100.")
    t1, t2, t3, t4 = st.tabs(["① Dimensiones", "② Variables: ¿cuáles sirven y por qué?",
                              "③ Indicadores", "④ Matriz de medibilidad"])
    with t1:
        _dimensiones()
    with t2:
        _variables()
    with t3:
        _indicadores()
    with t4:
        _matriz()


def _dimensiones():
    nota("Cómo leer cada recuadro:", "a la izquierda, qué mira la dimensión y cuántas variables e indicadores "
         "tiene. A la derecha, sus aspectos (la letra entre paréntesis dice qué tan sólida es la evidencia, "
         "de A a D) y el resultado principal de cada indicador. <b>n</b> es el número de personas que "
         "respondieron: cuanto más grande, más confiable el porcentaje.")
    aspectos = CONC["aspectos"]["lista"]
    conteo = DIC[DIC["veredicto"].str.startswith("Sirve")].groupby("dimension").size()
    for nombre, info in DIMENSIONES.items():
        asp = [a for a in aspectos if a["dimension"] == nombre]
        inds = [i for i in DATOS["indicadores"] if i["dimension"] == nombre]
        with st.container(border=True):
            c1, c2 = st.columns([2, 3])
            with c1:
                st.markdown(f"### {info['icono']} {nombre}")
                st.markdown(info["que"])
                st.markdown(f"**{conteo.get(nombre, 0)}** variables útiles · **{len(inds)}** indicadores")
            with c2:
                if asp:
                    st.markdown("**Aspectos:** " + chips([f"{a['aspecto']} ({a['evidencia']})" for a in asp]),
                                unsafe_allow_html=True)
                for i in inds:
                    r = i["resultados"][0]
                    st.markdown(f"`{i['id']}` **{i['nombre']}** — {fmt(r['pct'])} % "
                                f"<span class='fuente'>({r['etiqueta']}, n = {fmt(r['n'], 0)})</span>",
                                unsafe_allow_html=True)
    st.caption("Entre paréntesis, el nivel de evidencia del aspecto: A hecho verificable, B cambio "
               "declarado, C percepción, D no disponible. Dimensiones: Modelo 2026, lámina 3.")


def _variables():
    nota("¿Qué es una variable?", "Cada pregunta de una encuesta, guardada como una columna en la base de "
         "datos. Por ejemplo, «¿cuál es su estrato actual?» es una variable. No todas sirven para medir "
         "transformación: algunas solo describen a la persona y otras tienen muy pocas respuestas.")
    st.markdown(f"Se revisaron **las {len(DIC)} variables** de las tres bases. Para cada una se respondieron "
                "cinco preguntas:")
    cols = st.columns(5)
    criterios = [("1. ¿Es pertinente?", "¿Corresponde a un aspecto de alguna dimensión del modelo?"),
                 ("2. ¿Tiene un momento?", "¿Dice cómo estaba antes, cómo está ahora o qué cambió? Sin dos momentos es seguimiento, no transformación."),
                 ("3. ¿Tiene respuestas?", "¿Cuántas personas la contestaron? Las preguntas filtradas solo sirven para su subgrupo."),
                 ("4. ¿Qué tan sólida es?", "Nivel de evidencia: hecho verificable, cambio declarado o percepción."),
                 ("5. ¿Se puede usar?", "Si identifica a la persona (Ley 1581) o es un control del formulario, no se analiza.")]
    for col, (t, d) in zip(cols, criterios):
        with col:
            card(t, d)
    st.write("")

    # Embudo
    total = len(DIC)
    analizables = DIC[~DIC["veredicto"].str.startswith("No se usa")]
    transf = DIC[DIC["veredicto"].isin(["Sirve: ya se usa", "Sirve: disponible", "Sirve con reservas"])]
    usadas = DIC[DIC["veredicto"] == "Sirve: ya se usa"]
    c1, c2 = st.columns([3, 2])
    with c1:
        fig = go.Figure(go.Funnel(
            y=["Variables en las 3 bases", "Analizables (sin datos personales ni controles)",
               "Miden algún aspecto de la transformación", "Ya alimentan indicadores o el índice"],
            x=[total, len(analizables), len(transf), len(usadas)],
            marker_color=[GRIS, NAVY2, SERIES, GOLD], textinfo="value",
            textfont=dict(size=16)))
        fig.update_layout(height=300, margin=dict(l=10, r=10, t=10, b=10), plot_bgcolor="#fff")
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
    with c2:
        st.markdown("#### Cómo leer el embudo")
        st.markdown(f"- **{len(transf)}** variables sirven para medir transformación.\n"
                    f"- Solo **{len(usadas)}** se usan hoy: se eligieron las que tienen dos momentos, "
                    "más respuestas y escalas claras.\n"
                    f"- Las **{len(DIC[DIC['veredicto'] == 'Sirve: disponible'])}** «disponibles» son "
                    "candidatas para nuevos indicadores en la Fase 2.\n"
                    "- El resto describe al graduado, alimenta el portafolio o no se puede usar.")

    # Veredicto por base
    orden = F.ORDEN_VEREDICTO
    paleta = PALETA_VEREDICTO
    nb = NOMBRE_CORTO
    tab = DIC.groupby(["base", "veredicto"]).size().unstack(fill_value=0)
    fig = go.Figure()
    for v in orden:
        if v in tab:
            fig.add_bar(y=[nb[b] for b in tab.index], x=tab[v], name=v, orientation="h",
                        marker_color=paleta[v])
    fig.update_layout(barmode="stack", height=250, margin=dict(l=10, r=10, t=30, b=10),
                      legend=dict(orientation="h", y=-0.25), plot_bgcolor="#fff",
                      title=dict(text="Veredicto por base (número de variables)", font=dict(size=14)))
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
    st.caption("Cada barra es una encuesta y cada color un veredicto. Cuanto más largo el tramo de los colores "
               "«Sirve…», más útil es esa encuesta para medir transformación.")

    with st.expander("¿Qué significa cada veredicto?", expanded=False):
        expl = SIGNIFICADO_VEREDICTO
        tabla_html(pd.DataFrame([{"Veredicto": k, "Significado": v,
                                  "Variables": int((DIC["veredicto"] == k).sum())} for k, v in expl.items()]))

    st.markdown("#### Explorar las variables")
    c1, c2, c3, c4 = st.columns([1.2, 1.4, 1.6, 2])
    bases = c1.multiselect("Base", list(nb), default=list(nb), format_func=lambda b: nb[b])
    dims = c2.multiselect("Dimensión", sorted(DIC["dimension"].unique()))
    vers = c3.multiselect("Veredicto", [v for v in orden if v in set(DIC["veredicto"])],
                          default=["Sirve: ya se usa", "Sirve: disponible"])
    texto = c4.text_input("Buscar en la pregunta", placeholder="p. ej. estrato, empleo, posgrado")
    vista = DIC[DIC["base"].isin(bases)]
    if dims:
        vista = vista[vista["dimension"].isin(dims)]
    if vers:
        vista = vista[vista["veredicto"].isin(vers)]
    if texto:
        vista = vista[vista["pregunta"].str.contains(texto, case=False, na=False)]
    vista = vista.assign(base=vista["base"].map(nb), respondida=100 - vista["faltantes_pct"])
    st.caption(f"{len(vista)} variables")
    st.dataframe(
        vista[["base", "pregunta", "dimension", "aspecto", "momento", "respondida", "veredicto",
               "por_que", "usada_en"]],
        hide_index=True, width="stretch", height=520, row_height=64,
        column_config={
            "base": st.column_config.TextColumn("Base", width="small"),
            "pregunta": st.column_config.TextColumn("Pregunta (variable)", width="large"),
            "dimension": "Dimensión", "aspecto": "Aspecto", "momento": "Momento",
            "respondida": st.column_config.ProgressColumn("% con respuesta", format="%.0f %%",
                                                          min_value=0, max_value=100),
            "veredicto": "Veredicto",
            "por_que": st.column_config.TextColumn("¿Por qué?", width="large"),
            "usada_en": "Usada en",
        })
    st.caption("Diccionario generado por el agente de perfilado (reglas en agente/config.py). "
               "La columna «Momento» dice si la pregunta mira el antes, el presente o el cambio.")


def _base_desglose(ind):
    return ind["resultados"][0]["base"]


def _indicadores():
    nota("¿Qué es un indicador?", f"Una cifra que resume un aspecto de la transformación, casi siempre "
         f"como porcentaje. Los {len(IND)} indicadores convierten las variables útiles en porcentajes que se "
         "pueden comparar entre sedes y años. Cada uno tiene ficha técnica en <b>Anexos</b>. La columna "
         "«Tipo» dice si el indicador mide un <b>cambio</b> (antes → después), una <b>situación actual</b>, "
         "lo que el graduado <b>atribuye</b> a su formación o un insumo para el <b>portafolio</b> de servicios.")
    tipos = {"cambio": "Cambio (antes → después)", "nivel": "Nivel (situación actual)",
             "contribución": "Contribución percibida", "portafolio": "Portafolio de servicios"}
    resumen = pd.DataFrame([{"Código": i["id"], "Indicador": i["nombre"], "Dimensión": i["dimension"],
                             "Tipo": tipos.get(i["tipo"], i["tipo"]),
                             "Resultado": f"{fmt(i['resultados'][0]['pct'])} %",
                             "n": i["resultados"][0]["n"],
                             "Evidencia": F.META[i["id"]]["evidencia"]} for i in DATOS["indicadores"]])
    tabla_html(resumen)

    st.markdown("#### Ver un indicador")
    sel = st.selectbox("Indicador", list(IND), format_func=lambda k: f"{k} · {IND[k]['nombre']}")
    ind = IND[sel]
    lect = EXPLICA["lecturas"].get(sel, {})
    st.markdown(f"**Pregunta que responde:** {lect.get('pregunta', '')}")
    nota("Lectura en palabras sencillas:", lectura_pct(ind["resultados"][0]))
    c1, c2 = st.columns([3, 2])
    with c1:
        filas = [{**r, "etiqueta": f"{r['etiqueta']}"} for r in ind["resultados"]]
        barras_ci(filas)
        if ind["extra"] and "distribucion" in ind["extra"]:
            st.markdown("**Distribución completa**")
            barras_ci(ind["extra"]["distribucion"])
        if ind["extra"] and "items" in ind["extra"]:
            st.markdown("**Por ítem**")
            barras_ci(ind["extra"]["items"])
    with c2:
        st.markdown(f"**Definición.** {ind['definicion']}")
        st.markdown(f"**Fórmula.** `{ind['formula']}`")
        st.markdown(f"**Universo.** {ind['universo']}")
        st.markdown(f'<div class="simple"><b>Ojo:</b> {lect.get("ojo", "")}</div>', unsafe_allow_html=True)
        st.markdown(f"**Limitaciones.** {ind['limitaciones']}")
    base = _base_desglose(ind)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Por sede**")
        barras_ci(ind["por_sede"])
    with c2:
        st.markdown("**Por cohorte de grado**")
        coh = [{**r, "etiqueta": etiqueta_cohorte(r["etiqueta"], base)} for r in ind["por_cohorte"]]
        barras_ci(coh, orden=ORDEN_COH)
    frases = [f for f in (comparar_grupos(ind["por_sede"], "sede"),
                          comparar_grupos(coh, "cohorte")) if f]
    if frases:
        nota("¿Qué dicen estas comparaciones?", "<br><br>".join(frases))
    st.caption("Barras grises: menos de 30 respuestas, no se interpretan. Línea negra: intervalo de "
               "confianza de Wilson al 95 %. Los porcentajes describen a quienes respondieron, no a "
               "todos los graduados.")
    guia_graficos()
    if ind["extra"] and "matriz" in ind["extra"]:
        m = ind["extra"]["matriz"]
        st.markdown("**Matriz de transición: de dónde venían (filas) y a dónde llegaron (columnas), % por fila**")
        z = m["pct_fila"] if "pct_fila" in m else m["conteos"]
        fig = go.Figure(go.Heatmap(z=z, x=[str(e) for e in m["etiquetas"]], y=[str(e) for e in m["etiquetas"]],
                                   colorscale=[[0, "#F4F7FC"], [1, SERIES]], showscale=False,
                                   text=[[fmt(v) for v in fila] for fila in z], texttemplate="%{text}"))
        fig.update_layout(height=360, margin=dict(l=10, r=10, t=10, b=10),
                          xaxis_title="Después", yaxis_title="Antes", yaxis_autorange="reversed")
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
        st.caption("La diagonal son quienes se quedaron igual. Arriba de la diagonal, quienes subieron.")


def _matriz():
    a = CONC["aspectos"]
    st.markdown("Qué aspectos de la transformación (lámina 3) se pueden medir con las bases "
                "disponibles, con qué nivel de evidencia y con qué indicador.")
    nota("Para qué sirve esta tabla:", "muestra de un vistazo qué parte del modelo ya se puede medir y qué "
         "parte <b>todavía no</b>, porque las encuestas actuales no lo preguntan. Lo que no se puede medir "
         "hoy es justamente lo que debe cubrir el cuestionario común de la Fase 2.")
    df = pd.DataFrame([{"Aspecto": x["aspecto"], "Dimensión": x["dimension"], "¿Medible?": x["medible"],
                        "Evidencia": x["evidencia"], "Base": x["base"], "Cómo se mide": x["como"],
                        "Indicadores": ", ".join(x["indicadores"]) or "—"} for x in a["lista"]])
    tabla_html(df)
    fuente(a["fuente"])
    st.markdown("#### Niveles de evidencia")
    st.caption("De la más sólida (A, se puede comprobar con un registro) a la más débil (C, opinión de la "
               "persona). D significa que hoy no hay datos.")
    cols = st.columns(4)
    for col, n in zip(cols, CONC["niveles_evidencia"]):
        with col:
            card(f"{n['nivel']} · {n['nombre']}", n["descripcion"], f"Ej.: {n['ejemplo']}")


# ---------------------------------------------------------------------------
# Fase 1 · 3. Fuentes
# ---------------------------------------------------------------------------
def f1_fuentes():
    encabezado("Fase 1 · Conceptualización", "Identificación y preparación de fuentes de información")
    simple("se usaron tres encuestas a graduados. Se limpiaron (sin consentimiento, duplicados y "
           "filas de control fuera) y se revisó si se podían unir: casi no comparten personas, así que "
           "la transformación se mide con preguntas de «antes y ahora» y comparando promociones.")
    cols = st.columns(3)
    for col, (k, b) in zip(cols, DATOS["bases"].items()):
        with col:
            card(b["nombre"], f"{b['descripcion']}<br><br><b>{fmt(b['registros_originales'], 0)}</b> registros → "
                 f"<b>{fmt(b['registros_analizables'], 0)}</b> analizables · {b['variables']} variables",
                 f"Recolección: {b['recoleccion']}")
    st.subheader("Depuración documentada")
    nota("¿Qué es depurar?", "Limpiar la base antes de analizarla: quitar a quien no dio permiso para usar "
         "sus datos, las respuestas repetidas y las filas de prueba. La tabla dice cuántas filas salieron "
         "en cada paso y por qué, para que cualquiera pueda repetir el proceso.")
    sel = st.radio("Base", list(DATOS["bases"]), horizontal=True,
                   format_func=lambda k: DATOS["bases"][k]["nombre"])
    b = DATOS["bases"][sel]
    tabla_html(pd.DataFrame(b["limpieza"]).rename(columns={"paso": "Paso", "filas": "Filas", "motivo": "Motivo"}))
    c1, c2 = st.columns(2)
    for col, campo, titulo in [(c1, "sede", "Composición por sede"), (c2, "cohorte", "Composición por cohorte")]:
        filas = b["composicion"].get(campo) or []
        with col:
            st.markdown(f"**{titulo}**")
            if filas:
                df = pd.DataFrame(filas)
                if campo == "cohorte":
                    df["categoria"] = [etiqueta_cohorte(c, sel) for c in df["categoria"]]
                    df["_o"] = df["categoria"].map({k: i for i, k in enumerate(ORDEN_COH)}).fillna(99)
                    df = df.sort_values("_o")
                fig = go.Figure(go.Bar(x=df["pct"], y=df["categoria"], orientation="h", marker_color=SERIES,
                                       text=[f"{fmt(p)} % ({n})" for p, n in zip(df["pct"], df["n"])],
                                       textposition="outside", cliponaxis=False))
                fig.update_layout(height=60 + 34 * len(df), margin=dict(l=10, r=70, t=5, b=5),
                                  yaxis_autorange="reversed", plot_bgcolor="#fff", xaxis_ticksuffix=" %")
                st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
            else:
                st.caption("No disponible.")
    st.caption("La composición muestra de qué sedes y años de grado son quienes respondieron. Si una sede o "
               "un periodo pesa mucho, los resultados generales se parecen más a ese grupo.")
    st.subheader("¿Se pueden unir las bases?")
    nota("¿Por qué importa?", "Si la misma persona aparece en dos encuestas de años distintos, se puede ver "
         "<b>su</b> cambio real, sin depender de lo que recuerda. La tabla muestra que muy pocas personas "
         "coinciden entre bases; por eso la transformación se mide con preguntas de «antes y ahora» y "
         "comparando promociones.")
    tabla_html(pd.DataFrame(DATOS["cruces"]).rename(columns={
        "par": "Cruce", "criterio": "Llave", "a": "Registros A", "b": "Registros B",
        "comunes": "En común", "lectura": "Lectura"}))
    st.caption("Los cruces se hicieron con huellas cifradas (SHA-256): ningún documento ni correo sale del equipo. "
               "Una huella cifrada es un código que siempre sale igual para el mismo documento, pero del "
               "que no se puede volver a obtener el documento.")
    st.subheader("Fuentes que el modelo pide y aún no están")
    st.markdown("La lámina 2 pide triangular con empleadores y fuentes externas. Propuesta para la Fase 2:")
    st.caption("«Triangular» es contrastar lo que dice el graduado con otra fuente (un registro oficial, el "
               "empleador) para confirmar que el dato es cierto.")
    tabla_html(pd.DataFrame(FUENTES_EXTERNAS, columns=["Fuente", "Para qué", "Cómo"]))
    fuente("Modelo 2026, lámina 2 (fuentes); propuesta del equipo (uso y forma de acceso).")


# ---------------------------------------------------------------------------
# Fase 1 · 4. Instrumentos y métodos
# ---------------------------------------------------------------------------


def f1_instrumentos():
    encabezado("Fase 1 · Conceptualización", "Diseño de instrumentos y métodos de análisis")
    simple("para medir transformación hay que preguntar <b>lo mismo, de la misma forma, en dos "
           "momentos</b>. Hoy cada encuesta pregunta distinto. Proponemos un módulo mínimo común "
           "para todas las encuestas futuras y los métodos para analizarlo.")
    st.subheader("Métodos de análisis")
    nota("No hace falta conocer cada técnica:", "la columna «Para qué sirve» explica en una frase qué "
         "pregunta responde cada método. Los nombres técnicos están para que un estadístico pueda "
         "revisar y repetir el trabajo.")
    tabla_html(pd.DataFrame(METODOS, columns=["Método", "Para qué sirve", "Dónde se usa"]))
    st.subheader("Instrumento mínimo común (propuesta)")
    st.markdown("Preguntas que toda encuesta de graduados de la USTA debería incluir, con la misma "
                "redacción y escala, para que los indicadores se puedan calcular igual cada año.")
    tabla_html(pd.DataFrame(INSTRUMENTO, columns=["Dimensión", "Pregunta (antes / ahora)", "Escala",
                                                  "Qué cambia frente a hoy", "Alimenta"]))
    st.subheader("¿Cuándo preguntar?")
    st.caption("Preguntar en varios momentos es como tomar fotos de la misma persona a lo largo del tiempo: "
               "al compararlas se ve el cambio, sin depender de lo que la persona recuerda.")
    cols = st.columns(4)
    for col, (t, d) in zip(cols, [("Al grado", "Línea base: la situación «antes». Elimina el sesgo de recuerdo."),
                                  ("1 año", "Inserción laboral y primer empleo."),
                                  ("3 años", "Trayectoria: cambios de empleo, posgrado."),
                                  ("5 años o más", "Movilidad social y consolidación.")]):
        with col:
            card(t, d)
    st.caption("Propuesta del equipo. Con la misma persona medida en varios momentos (panel) se "
               "pasa de comparar promociones a seguir trayectorias reales.")
    st.page_link(PAGINA_CUESTIONARIO, label="Ver el cuestionario común completo (Fase 2)",
                 icon=":material/arrow_forward:")


# ---------------------------------------------------------------------------
# Fase 1 · 5. Diseño del modelo y plan
# ---------------------------------------------------------------------------
def f1_diseno():
    encabezado("Fase 1 · Conceptualización", "Diseño del modelo y plan de implementación")
    st.subheader("El modelo en una línea")
    pasos = [("Fuentes", "3 encuestas + fuentes externas"), ("Variables", f"{len(DIC)} revisadas"),
             ("Indicadores", f"{len(IND)} con ficha"), ("Índice", "prototipo 0–100"),
             ("Usos", "currículo y portafolio")]
    cols = st.columns(len(pasos))
    for i, (col, (t, d)) in enumerate(zip(cols, pasos)):
        bg = GOLD if t == "Índice" else NAVY
        fg = NAVY if t == "Índice" else "#fff"
        col.markdown(f'<div class="fase" style="background:{bg};color:{fg};text-align:center">'
                     f'<h4 style="color:{fg};margin:0">{t}</h4><small>{d}</small></div>', unsafe_allow_html=True)
    st.caption("Seguimiento (observar) → evaluación (interpretar) → decisiones. Modelo 2026, láminas 3 y 4.")
    simple("se parte de las encuestas, se escogen las preguntas útiles, se convierten en porcentajes "
           "(indicadores), se resumen en un solo número (índice) y todo eso se usa para dos decisiones: "
           "mejorar los programas y diseñar servicios para los graduados.")

    st.subheader("Prototipo de Índice de Transformación del Graduado")
    ix = DATOS["indice"]
    simple(f"cada graduado recibe de 0 a 100 en cada dimensión y el índice es el promedio de las cuatro. "
           f"En promedio los graduados obtienen <b>{fmt(ix['general']['media'])}</b> de 100 "
           f"(IC 95 %: {fmt(ix['general']['li'])}–{fmt(ix['general']['ls'])}; n = {fmt(ix['n'], 0)}).")
    cols = st.columns(5)
    for col, (k, v) in zip(cols, ix["componentes"].items()):
        col.markdown(f'<div class="card"><p>{k}</p><div class="big">{fmt(v["media"])}</div><p>de 100</p></div>',
                     unsafe_allow_html=True)
    cols[4].markdown(f'<div class="card" style="background:{NAVY}"><p style="color:#fff">Índice</p>'
                     f'<div class="big" style="color:{GOLD}">{fmt(ix["general"]["media"])}</div>'
                     f'<p style="color:#fff">de 100</p></div>', unsafe_allow_html=True)
    st.write("")
    comp = ix["componentes"]
    alto = max(comp, key=lambda k: comp[k]["media"])
    bajo = min(comp, key=lambda k: comp[k]["media"])
    nota("Cómo leer estas cifras:", f"el índice no es una nota de aprobado o reprobado; es un punto en una "
         f"escala que sirve para comparar grupos y, en el futuro, años. Hoy la dimensión más alta es "
         f"<b>{alto}</b> ({fmt(comp[alto]['media'])}) y la más baja <b>{bajo}</b> ({fmt(comp[bajo]['media'])}). "
         "Una cifra baja no significa necesariamente un mal resultado: depende de cómo se puntúa cada "
         "dimensión (ver «Cómo se calcula cada componente»).")
    with st.expander("Cómo se calcula cada componente"):
        for c in CONC["indice"]["componentes"]:
            st.markdown(f"- **{c['dimension']}:** {c['regla']}")
        st.markdown(f"**Agregación:** {CONC['indice']['agregacion']}")
        st.markdown(f"**Por qué una sola base:** {CONC['indice']['por_que_una_base']}")
        st.markdown(f"**Alfa de Cronbach = {fmt(ix['alfa_cronbach'], 2)}.** {CONC['indice']['lectura_alfa']}")
    c1, c2 = st.columns(2)
    filas = lambda L, b: [{**r, "etiqueta": etiqueta_cohorte(r["grupo"], b), "pct": r["media"],  # noqa: E731
                           "suficiente": r["suficiente"]} for r in L]
    with c1:
        st.markdown("**Por cohorte de grado**")
        barras_ci(filas(ix["por_cohorte"], "percepcion"), orden=ORDEN_COH, sufijo="",
                  ref=ix["general"]["media"])
    with c2:
        st.markdown("**Por sede**")
        barras_ci(filas(ix["por_sede"], "percepcion"), sufijo="", ref=ix["general"]["media"])
    st.caption("Línea dorada: promedio general. Las sedes no se ordenan como ranking: las muestras no "
               "son representativas y falta ponderar.")
    frases = [f for f in (comparar_grupos(filas(ix["por_cohorte"], "percepcion"), "cohorte", ""),
                          comparar_grupos(filas(ix["por_sede"], "percepcion"), "sede", "")) if f]
    if frases:
        nota("¿Qué dicen estas comparaciones?", "<br><br>".join(frases))
    guia_graficos(linea_dorada=True)
    st.markdown("**Lo que falta para validar el índice**")
    for p in CONC["indice"]["pendiente"] + ["Revisar la escala académica: hoy quien tiene solo pregrado recibe 0"]:
        st.markdown(f"- {p}")

    st.subheader("Usos de la evidencia")
    u = CONC["usos"]
    c1, c2 = st.columns(2)
    for col, k in [(c1, "curricular"), (c2, "portafolio")]:
        with col:
            st.markdown(f"**{u[k]['titulo']}**")
            for e in u[k]["evidencia_disponible"]:
                st.markdown(f"- {e['insumo']} " + (chips(e["indicadores"]) if e["indicadores"] else ""),
                            unsafe_allow_html=True)
    fuente(u["fuente"])

    st.subheader("Plan de implementación")
    tabla_html(pd.DataFrame([{"Fase": f["fase"], "Periodo": f["periodo"], "Producto": f["producto"]}
                             for f in MODELO["fases"]]))
    fuente(MODELO["fases_fuente"])
    st.markdown("**Próximos pasos técnicos**")
    tabla_html(pd.DataFrame(CONC["proximos_pasos"]).rename(columns={"paso": "Paso", "para": "Para qué"}))


# ---------------------------------------------------------------------------
# Fase 2 · Validación (propuesta)
# ---------------------------------------------------------------------------
def fase2():
    encabezado("Fase 2 · nov-2026 – abr-2027 · propuesta del equipo", "Validación en contexto")
    simple("la Fase 2 prueba el modelo en pequeño (un piloto) antes de aplicarlo a toda la "
           "Universidad. Aquí está lo que proponemos para cada actividad de la lámina 6.")
    rol = MODELO["rol_equipo_tecnico"]
    st.markdown(f"**Equipo técnico:** {rol['actor']}. Roles: " + chips(rol["roles"]), unsafe_allow_html=True)
    fuente(rol["fuente"])
    st.caption("Un piloto es un ensayo general: se aplica el modelo a un grupo pequeño para corregir errores "
               "antes de extenderlo a todas las sedes.")
    acts = ACTIVIDADES_FASE2
    for i, (t, d) in enumerate(acts, 1):
        with st.container(border=True):
            st.markdown(f"**{i}. {t}**  \n{d}")

    st.subheader("Cronograma propuesto")
    meses = ["nov", "dic", "ene", "feb", "mar", "abr"]
    gantt = CRONOGRAMA_FASE2
    fig = go.Figure()
    for nombre, ini, fin, periodo, hecha in gantt:
        estado = "Realizada" if hecha else "Pendiente"
        fig.add_bar(y=[nombre], x=[fin - ini], base=[ini], orientation="h",
                    marker_color="#2E7D32" if hecha else SERIES,
                    text=["✓ Realizada"] if hecha else None, textposition="inside",
                    insidetextanchor="middle", textfont=dict(color="#fff"),
                    hovertemplate=f"{nombre}: {periodo} · {estado}<extra></extra>")
    fig.update_layout(height=260, showlegend=False, margin=dict(l=10, r=10, t=10, b=10),
                      xaxis=dict(tickvals=[i + .5 for i in range(6)], ticktext=meses, range=[0, 6],
                                 gridcolor="#EEF1F6"),
                      yaxis=dict(autorange="reversed"), plot_bgcolor="#fff")
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
    st.markdown(chips(["■ Realizada"], "ok") + chips(["■ Pendiente"]), unsafe_allow_html=True)
    st.caption("Cada barra es una actividad y su largo, los meses que dura. Las barras que se superponen "
               "ocurren al mismo tiempo.")

    st.subheader("¿Cuántas respuestas necesita el piloto?")
    c1, c2 = st.columns([1, 2])
    margen = c1.slider("Margen de error deseado (± puntos porcentuales)", 3, 12, 7)
    n = round(1.96 ** 2 * 0.25 / (margen / 100) ** 2)
    c2.markdown(f'<div class="card"><p>Respuestas necesarias por grupo (programa × cohorte) para '
                f'estimar un porcentaje con ±{margen} puntos al 95 %:</p><div class="big">{fmt(n, 0)}</div>'
                f'<p>Fórmula: n = 1,96² × 0,25 / margen². Supone el caso más exigente (50 %).</p></div>',
                unsafe_allow_html=True)
    nota("Cómo interpretarlo:", f"si el piloto encuentra, por ejemplo, que 60 % de un grupo tiene empleo "
         f"relacionado con su carrera, con {fmt(n, 0)} respuestas se podría decir que el valor real está entre "
         f"{60 - margen} % y {60 + margen} %. Un margen más pequeño da más precisión, pero exige muchas más "
         "respuestas: reducir el margen a la mitad multiplica por cuatro las encuestas necesarias. "
         "<b>Mueva el control</b> para verlo.")


# ---------------------------------------------------------------------------
# Fase 2 · Cuestionario común multisede (propuesta)
# ---------------------------------------------------------------------------
PARES_ANTES_AHORA = [("Estrato", "C01", "C02"), ("Ingreso en SMMLV", "C03", "C04"),
                     ("Nivel del cargo", "D04", "D07"), ("Correspondencia empleo–formación", "D05", "D09"),
                     ("Nivel educativo", "A02", "F01")]
COLOR_COMPARA = {"✓": "#2E7D32", "≈": GOLD, "—": GRIS}
NOMBRE_COMPARA = {"✓": "✓ Igual o casi igual", "≈": "≈ Recodificable", "—": "— No existe"}


def _lista(txt: str) -> str:
    return "<br>".join(html.escape(x) for x in txt.split("\n"))


def _q_resumen():
    """Lectura de un minuto: problema, ejemplo concreto y propuesta."""
    st.subheader("La idea en un minuto")
    pasos = [("1 · Hoy", "Hay <b>tres encuestas</b> a graduados (PENSER 2025, Percepción 2022 y el formulario "
                         "de actualización), hechas en momentos y sedes distintas."),
             ("2 · El problema", "Preguntan lo mismo <b>con palabras y opciones distintas</b>. Es como medir "
                                 "con una regla en centímetros y otra en pulgadas: los números no se pueden sumar."),
             ("3 · La propuesta", "Un <b>núcleo de preguntas idéntico</b> en todas las sedes, más módulos que cada "
                                  "sede puede agregar al final si los necesita."),
             ("4 · Lo que se gana", "Comparar sedes, programas y cohortes <b>con la misma regla</b>, y ver cómo "
                                    "cambia la vida del graduado con el tiempo.")]
    cols = st.columns(4)
    for col, (t, d) in zip(cols, pasos):
        with col:
            card(t, d)
    st.write("")
    with st.expander("Ver un ejemplo real del problema: cómo se pregunta hoy el ingreso", expanded=True):
        cols = st.columns(len(Q.EJEMPLO_INGRESO) + 1)
        for col, (base, como, prob) in zip(cols, Q.EJEMPLO_INGRESO):
            with col:
                card(base, html.escape(como), f"✗ {html.escape(prob)}")
        with cols[-1]:
            st.markdown('<div class="card" style="border:2px solid #2E7D32"><h4>Propuesta (C03 y C04)</h4>'
                        "<p>Dos preguntas con <b>los mismos rangos en salarios mínimos</b>: el ingreso en el "
                        "último año de estudios y el ingreso actual.</p>"
                        '<div class="fuente" style="color:#1E6B3C">✓ Se ve si mejoró y cuánto, y se compara '
                        "entre años y sedes.</div></div>", unsafe_allow_html=True)


def f2_cuestionario():
    n_total, n_pre = Q.total_preguntas(), Q.N_PRECARGADAS
    encabezado("Fase 2 · Validación · propuesta del equipo", "Cuestionario común multisede")
    simple("las tres encuestas actuales preguntan lo mismo de formas distintas, y por eso no se pueden "
           "sumar ni comparar entre sedes. Proponemos un <b>núcleo de preguntas idéntico en todas las "
           "sedes</b> (mismo texto, orden, opciones y códigos), más módulos opcionales que cada sede "
           "añade al final.")
    _q_resumen()
    st.subheader("El cuestionario en cifras")
    cols = st.columns(4)
    for col, (num, txt) in zip(cols, [(n_total, f"preguntas en el núcleo ({n_pre} precargadas del registro)"),
                                      (n_total - n_pre, "las responde el graduado: 15 a 18 minutos"),
                                      (len(Q.NUCLEO), "secciones: personal, profesional, social, académica y relación USTA"),
                                      (len(Q.MODULOS), "módulos opcionales por sede")]):
        with col:
            st.markdown(f'<div class="card"><div class="big">{num}</div><p>{txt}</p></div>',
                        unsafe_allow_html=True)
    d1, d2, _ = st.columns([1, 1, 2])
    if DOCX_CUESTIONARIO.exists():
        d1.download_button("Descargar el cuestionario (Word)", DOCX_CUESTIONARIO.read_bytes(),
                           file_name=DOCX_CUESTIONARIO.name, icon=":material/download:")
    if PDF_CUESTIONARIO.exists():
        d2.download_button("Descargar en PDF", PDF_CUESTIONARIO.read_bytes(),
                           file_name=PDF_CUESTIONARIO.name, icon=":material/picture_as_pdf:")

    st.subheader("Explore la propuesta")
    st.caption("Recorra las pestañas en orden. Cada una empieza con una explicación corta; si encuentra una "
               "palabra técnica, búsquela en la pestaña ⑦ Glosario.")
    t1, t2, t3, t4, t5, t6, t7 = st.tabs(["① Núcleo común", "② Módulos opcionales", "③ Escalas estándar",
                                          "④ Trazabilidad", "⑤ Qué cambia", "⑥ Protocolo y piloto",
                                          "⑦ Glosario"])
    with t1:
        _q_nucleo()
    with t2:
        _q_modulos()
    with t3:
        _q_escalas()
    with t4:
        _q_traza()
    with t5:
        nota("¿Qué es esta lista?", "Preguntas de los estudios actuales que no pasan al núcleo tal como están. "
              "Se cambian por una de tres razones: <b>no se pueden comparar</b> (escalas o rangos distintos), "
              "<b>dan demasiado trabajo</b> (decenas de columnas casi vacías) o <b>exponen datos personales</b> "
              "sin necesidad (documento, nombre de la empresa en texto libre).")
        tabla_html(pd.DataFrame(Q.REEMPLAZOS, columns=["Pregunta actual", "Propuesta"]))
    with t6:
        _q_protocolo()
    with t7:
        busca = st.text_input("Buscar término", key="glosario_cuestionario")
        g = [x for x in Q.GLOSARIO if not busca or busca.lower() in (x[0] + x[1]).lower()]
        for termino, definicion in g:
            st.markdown(f"**{termino}.** {definicion}")
        if not g:
            st.caption("No hay términos con esa búsqueda.")


def _q_nucleo():
    nota("¿Qué es el núcleo?", "Las preguntas obligatorias, iguales en todas las sedes. Están ordenadas en "
          "ocho secciones (A a H), del dato más simple (de qué programa se graduó) al más personal (qué le "
          "aportó la Universidad).")
    st.markdown("**La clave: pares «antes / ahora».** Se hace la misma pregunta dos veces, una sobre el momento "
                "del grado y otra sobre el presente. Así se observa la transformación aunque la persona "
                "responda una sola vez.")
    cols = st.columns(len(PARES_ANTES_AHORA))
    for col, (t, a, b) in zip(cols, PARES_ANTES_AHORA):
        with col:
            card(t, f"<b>{a}</b> al grado → <b>{b}</b> hoy")
    st.write("")
    with st.expander("Ejemplo: así se leerían las respuestas de un graduado (caso ficticio)"):
        mejoro, igual = chips(["↑ Mejoró"], "ok"), chips(["= Igual"])
        filas = "".join(
            f"<tr><td>{html.escape(t)}</td><td>{html.escape(a)}</td><td>{html.escape(b)}</td>"
            f"<td>{mejoro if m else igual}</td></tr>"
            for t, a, b, m in Q.EJEMPLO_GRADUADO)
        st.markdown('<table class="ficha"><tr><th>Tema</th><th>Al graduarse</th><th>Hoy</th><th>Lectura</th></tr>'
                    f"{filas}</table>", unsafe_allow_html=True)
        st.markdown("Una sola persona no dice mucho. Pero al **sumar cientos de respuestas** con las mismas "
                    "preguntas se obtienen los indicadores del modelo; por ejemplo, *«qué porcentaje de los "
                    "graduados de 2022 subió al menos un estrato»* (SOC-01), y se puede comparar ese "
                    "porcentaje entre sedes y programas.")
        st.caption("Datos inventados solo para explicar; no corresponden a ninguna persona.")
    with st.expander("¿Cómo leer cada tarjeta de pregunta?"):
        st.markdown(f"- {chips(['C01'], 'gold')} **Código**: el nombre fijo de la pregunta. Es igual en todas "
                    "las sedes y es el nombre de la columna en la base de datos.\n"
                    f"- {chips(['Social'])} **Dimensión** del modelo a la que aporta (personal, profesional, "
                    "social, académica o relación con la USTA).\n"
                    "- **Texto en negrita**: la pregunta tal como la lee el graduado.\n"
                    "- **A la derecha**: las opciones de respuesta, con su número.\n"
                    "- **Origen**: de qué encuesta actual viene. **Alimenta**: el indicador que calcula.",
                    unsafe_allow_html=True)
    st.write("")
    busca = st.text_input("Buscar en todas las preguntas", placeholder="p. ej. ingreso, estrato, competencias")
    if busca:
        b = busca.lower()
        lista = [p for p in Q.preguntas() if b in (p["pregunta"] + p["opciones"] + p["codigo"]).lower()]
        st.caption(f"{len(lista)} pregunta(s) encontradas.")
    else:
        secciones = {f"{s[0]} · {s[1]}": s for s in Q.NUCLEO}
        sel = st.radio("Sección", list(secciones), horizontal=True, label_visibility="collapsed")
        letra, _, nota_sec, _ = secciones[sel]
        para, ejemplo = Q.PARA_QUE[letra]
        nota("¿Para qué sirve esta sección?", f"{html.escape(para)}<br><b>Ejemplo de uso:</b> "
              f"<i>{html.escape(ejemplo)}</i>")
        st.caption(nota_sec)
        lista = [p for p in Q.preguntas() if p["seccion"] == letra]
    for p in lista:
        dim, ind, *_ = Q.TRAZA[p["codigo"]]
        with st.container(border=True):
            c1, c2 = st.columns([3, 2])
            c1.markdown(f'{chips([p["codigo"]], "gold")}{chips([dim])}<br><b>{html.escape(p["pregunta"])}</b>'
                        f'<div class="fuente">Origen: {html.escape(p["origen"])} · Alimenta: {html.escape(ind)}</div>',
                        unsafe_allow_html=True)
            c2.markdown(f'<div style="font-size:.9rem;color:#33415C">{_lista(p["opciones"])}</div>',
                        unsafe_allow_html=True)


def _q_modulos():
    nota("¿Qué es un módulo?", "Un bloque de preguntas extra sobre un tema que no le interesa a todas las "
          "sedes por igual; por ejemplo, una sede con muchos graduados fuera del país usaría M1. Es como un "
          "menú: cada sede elige los que necesita y los pone <b>después</b> del núcleo, sin cambiar su texto. "
          "Así también se pueden comparar las sedes que usen el mismo módulo.")
    for i in range(0, len(Q.MODULOS), 2):
        cols = st.columns(2)
        for col, (cod, titulo, origen, uso, items) in zip(cols, Q.MODULOS[i:i + 2]):
            with col:
                card(f"{cod} · {titulo}", "<br>".join(f"• {html.escape(x)}" for x in items),
                     f"Origen: {origen} · Útil para: {uso}")
        st.write("")


def _q_escalas():
    nota("¿Qué es una escala y por qué unificarla?", "La escala es el conjunto de opciones de respuesta. Hoy "
          "una encuesta pregunta de 1 a 4, otra de 1 a 5 y otra solo Sí/No sobre el mismo tema, y así un "
          "«4» no significa lo mismo en todas. La propuesta usa <b>pocas escalas fijas</b>: cada tipo de "
          "pregunta tiene siempre las mismas opciones.")
    filas = [("Nivel (contribución, correspondencia, satisfacción)", Q.NIVEL), ("Acuerdo (afirmaciones)", Q.ACUERDO),
             ("Incidencia (E04)", Q.INCIDENCIA), ("Ingreso (C03, C04)", Q.SMMLV),
             ("Códigos especiales (todas)", "97 No sabe\n98 Prefiero no responder\n99 No aplica\nVacío = salto")]
    cols = st.columns(len(filas))
    for col, (t, esc) in zip(cols, filas):
        with col:
            card(t, _lista(esc))
    st.write("")
    st.markdown('<div class="simple"><b>¿Por qué en SMMLV?</b> Los rangos en pesos pierden vigencia con la '
                "inflación (Percepción usa pesos de 2022). En salarios mínimos, las cohortes y los años se "
                "comparan entre sí. C03 es retrospectiva y tiene sesgo de recuerdo.</div>", unsafe_allow_html=True)
    nota("¿Por qué los códigos 97, 98 y 99?", "No es lo mismo «no sé» que «no quiero responder» o «no me "
          "aplica» (por ejemplo, preguntar por el cargo a quien no trabaja). Si se mezclan con las respuestas "
          "reales, los promedios y porcentajes se distorsionan; con códigos aparte se pueden excluir del "
          "cálculo y, a la vez, contar cuántas personas no respondieron.")


def _q_traza():
    nota("¿Qué muestra esta pestaña?", "Para cada pregunta del núcleo: a qué dimensión del modelo aporta, qué "
          "indicador alimenta y si ya existe en alguna de las tres encuestas actuales. Sirve para saber qué "
          "datos históricos se pueden aprovechar y cuáles empiezan desde cero.")
    st.markdown(f"{chips(['✓'], 'ok')} la base ya tiene esa pregunta, igual o casi igual · "
                f"{chips(['≈'], 'gold')} tiene algo parecido que se puede convertir (recodificar) · "
                f"{chips(['—'])} no la tiene.", unsafe_allow_html=True)
    bases = ["PENSER 2025", "Percepción 2022", "Formulario 2023–26"]
    n = len(Q.TRAZA)
    usable = [sum(1 for v in Q.TRAZA.values() if v[2 + i] != "—") for i in range(3)]
    en_las_tres = sum(1 for v in Q.TRAZA.values() if all(m != "—" for m in v[2:]))
    nuevas = sum(1 for v in Q.TRAZA.values() if all(m == "—" for m in v[2:]))
    mejor = max(range(3), key=lambda i: usable[i])
    nota("Cómo leer el gráfico:", f"la base más cercana al núcleo es <b>{bases[mejor]}</b>, que tiene de "
          f"alguna forma {usable[mejor]} de las {n} preguntas. Solo <b>{en_las_tres}</b> aparecen en las tres "
          f"bases a la vez, y {nuevas} {'no está' if nuevas == 1 else 'no están'} en ninguna. Por eso hoy "
          "solo una parte pequeña de la información se puede comparar entre las tres encuestas.")
    fig = go.Figure()
    for marca in ["✓", "≈", "—"]:
        cuenta = [sum(1 for v in Q.TRAZA.values() if v[2 + i] == marca) for i in range(3)]
        fig.add_bar(y=bases, x=cuenta, orientation="h", name=NOMBRE_COMPARA[marca],
                    marker_color=COLOR_COMPARA[marca], text=cuenta, textposition="inside",
                    hovertemplate="%{y}: %{x} preguntas<extra>" + NOMBRE_COMPARA[marca] + "</extra>")
    fig.update_layout(barmode="stack", height=230, margin=dict(l=10, r=10, t=30, b=10),
                      plot_bgcolor="#fff",
                      legend=dict(orientation="h", y=1.02, yanchor="bottom", x=0, traceorder="normal"),
                      xaxis=dict(title=f"Preguntas del núcleo (de {len(Q.TRAZA)})", gridcolor="#EEF1F6"),
                      yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
    texto = {p["codigo"]: p["pregunta"] for p in Q.preguntas()}
    df = pd.DataFrame([[k, texto[k], *v] for k, v in Q.TRAZA.items()],
                      columns=["Código", "Pregunta", "Dimensión", "Indicador que alimenta", *bases])
    dims = st.multiselect("Filtrar por dimensión", sorted(df["Dimensión"].unique()), placeholder="Todas")
    tabla_html(df[df["Dimensión"].isin(dims)] if dims else df)
    st.caption("Ninguna base histórica cubre el núcleo completo: por eso hoy no se pueden comparar sedes "
               "ni cohortes con las mismas preguntas.")


def _q_protocolo():
    cols = st.columns(4)
    for col, (t, d) in zip(cols, [
        ("Cuándo", "Una vez al año, en la misma ventana en todas las sedes, a los graduados de hace "
                   "<b>1, 3 y 5 años</b>. El primer año, todas las cohortes de los últimos cinco años como línea base."),
        ("Unión de respuestas", "Identificador <b>seudonimizado</b> derivado del documento con una clave "
                                "institucional: une las respuestas de un graduado entre años sin guardar su documento."),
        ("Estandarización", "Una sola versión (v1.0) con control de cambios central. Columnas exportadas con "
                            "los códigos (A01…H04). Ninguna sede edita el núcleo."),
        ("Datos personales", "Consentimiento según la Ley 1581 de 2012. Solo resultados agregados, sin celdas "
                             "de menos de 5 personas.")]):
        with col:
            card(t, d)
    st.subheader("¿A quién se le pregunta cada año?")
    nota("La idea:", "cada graduado responde <b>tres veces</b>: al año, a los tres y a los cinco años de "
          "graduarse. Así se ve cómo evoluciona la misma persona, y cada año se encuesta a tres grupos a la vez.")
    fig = go.Figure()
    colores = [SERIES, GOLD, "#2E7D32"]
    fig.add_vrect(x0=2030.6, x1=2031.4, fillcolor="#FFF4D1", line_width=0, layer="below")
    for (cohorte, color) in zip([2026, 2028, 2030], colores):
        anios = [cohorte + k for k in (1, 3, 5)]
        fig.add_scatter(x=anios, y=[f"Graduados {cohorte}"] * 3, mode="lines+markers+text",
                        line=dict(color=color, width=2, dash="dot"), marker=dict(size=16, color=color),
                        text=["1 año", "3 años", "5 años"], textposition="top center",
                        hovertemplate=f"Graduados {cohorte} · encuesta de %{{x}}<extra></extra>",
                        showlegend=False)
    fig.update_layout(height=270, margin=dict(l=10, r=10, t=10, b=10), plot_bgcolor="#fff",
                      xaxis=dict(dtick=1, title="Año en que responden la encuesta", gridcolor="#EEF1F6"),
                      yaxis=dict(range=[2.4, -0.7]))
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
    st.caption("Calendario ilustrativo con tres cohortes. En 2031 (franja amarilla) responden a la vez los "
               "graduados de 2030 (1 año), 2028 (3 años) y 2026 (5 años).")
    st.subheader("Ruta de validación del cuestionario")
    nota("¿Por qué validar?", "Antes de usarlo en todas las sedes hay que comprobar que las preguntas se "
          "entienden, que no toma demasiado tiempo y que mide lo que dice medir. Son cinco pasos, del más "
          "sencillo al más técnico.")
    tabla_html(pd.DataFrame([
        ("1. Revisión de expertos", "Experto temático y directores de graduados de cada sede revisan redacción y pertinencia.",
         "Personas que conocen el tema leen las preguntas y proponen mejoras.", "Versión 0.9"),
        ("2. Prueba cognitiva", "10 a 15 graduados por sede responden en voz alta para detectar preguntas confusas.",
         "Se escucha cómo entiende la gente cada pregunta.", "Ajustes de redacción"),
        ("3. Piloto en dos o más sedes", "Aplicación real a una cohorte: tiempo, abandono y vacíos por pregunta.",
         "Un ensayo general antes del estreno.", "Base piloto"),
        ("4. Validación estadística", "Alfa de Cronbach y análisis factorial confirmatorio de E03; consistencia de los pares antes/ahora.",
         "Se comprueba con números que las respuestas son coherentes.", "Informe técnico"),
        ("5. Cierre", "Se congela el núcleo y se publica el diccionario de datos.",
         "Se fija la versión oficial y ya no se cambia sin control.", "Instrumento v1.0 (Fase 3)"),
    ], columns=["Paso", "Qué se hace", "En palabras sencillas", "Producto"]))
    st.caption("El tamaño de muestra por grupo se calcula en la página «Propuesta de piloto». "
               "Las cohortes de 1, 3 y 5 años son propuesta del equipo; el Manual para estudios de seguimiento "
               "a graduados (sección 5.1.6) respalda el panel para observar el cambio individual.")


# ---------------------------------------------------------------------------
# Anexos
# ---------------------------------------------------------------------------
def anexo_fichas():
    encabezado("Anexos", "Fichas técnicas de los indicadores")
    st.markdown("Cada ficha documenta qué mide el indicador, cómo se calcula, de dónde salen los "
                "datos, qué tan sólida es la evidencia y cuál es su línea base.")
    nota("¿Qué es una ficha técnica?", "Es como la <b>hoja de vida de un indicador</b>: deja por escrito todo "
         "lo necesario para que otra persona, en otra sede o en otro año, lo calcule exactamente igual. Si "
         "tiene poco tiempo, lea tres filas: <b>Pregunta que responde</b>, <b>Línea base</b> (el valor de hoy, "
         "contra el que se comparará en el futuro) e <b>Interpretación</b>.")
    if DOCX_FICHAS.exists():
        st.download_button("Descargar las 14 fichas (Word)", DOCX_FICHAS.read_bytes(),
                           file_name=DOCX_FICHAS.name, icon=":material/download:")
    sel = st.selectbox("Indicador", [f["id"] for f in FICHAS],
                       format_func=lambda k: f"{k} · {IND[k]['nombre']}")
    f = next(x for x in FICHAS if x["id"] == sel)
    st.markdown(f"### {f['id']} · {f['nombre']}")
    st.markdown(chips([f["dimension"], f["aspecto"], f"Tipo: {f['tipo']}",
                       f"Evidencia {f['evidencia']}: {f['evidencia_nombre']}"]), unsafe_allow_html=True)
    nota("En pocas palabras:", lectura_pct(IND[sel]["resultados"][0]))
    filas = [("Pregunta que responde", f["pregunta"]), ("Definición", f["definicion"]),
             ("Fórmula", f["formula"]), ("Unidad de medida", f["unidad"]), ("Universo", f["universo"]),
             ("Fuentes", ", ".join(f["fuentes"])),
             ("Variables", "\n".join(f"{v['base']} · col. {v['posicion']}: {v['pregunta']}" for v in f["variables"])),
             ("Método de estimación", f["metodo"]), ("Desagregación", f["desagregacion"]),
             ("Línea base", "; ".join(f"{r['etiqueta']}: {fmt(r['pct'])} % (IC 95 % {fmt(r['li'])}–{fmt(r['ls'])}; n = {r['n']})"
                                      for r in f["linea_base"])),
             ("Interpretación", f["interpretacion"]), ("Limitaciones", f["limitaciones"]),
             ("Uso en el modelo", f["uso"]), ("Verificación externa", f["verificacion"]),
             ("Periodicidad", f["periodicidad"]), ("Responsable", f["responsable"]), ("Meta", f["meta"])]
    cuerpo = "".join(f"<tr><th>{html.escape(k)}</th><td>{html.escape(v).replace(chr(10), '<br>')}</td></tr>"
                     for k, v in filas)
    st.markdown(f'<table class="ficha">{cuerpo}</table>', unsafe_allow_html=True)
    st.caption(f"Nivel de evidencia, uso, verificación, periodicidad, responsable y meta: {F.ORIGEN_PROPUESTA}.")


def anexo_glosario():
    encabezado("Anexos", "Glosario, límites y documentos de apoyo")
    if DOCX_IMPACTO.exists():
        st.download_button("Descargar: Impacto vs. transformación del graduado (Word)",
                           DOCX_IMPACTO.read_bytes(), file_name=DOCX_IMPACTO.name,
                           icon=":material/download:")
    st.subheader("Límites de esta fase")
    st.caption("Todo estudio tiene límites. Decirlos con claridad evita que las cifras se usen para "
               "afirmar más de lo que permiten.")
    for l in CONC["limitaciones"]:
        st.markdown(f"- **{l['titulo']}.** {l['texto']}")
    st.subheader("Glosario")
    st.caption("Si solo quiere la idea general, lea la columna «En palabras sencillas». Los términos del "
               "cuestionario común (SMMLV, cohorte, seudonimizado…) están en la pestaña ⑦ de esa página.")
    q = st.text_input("Buscar término")
    g = [x for x in CONC["glosario"] if not q or q.lower() in (x["termino"] + x["definicion"]).lower()]
    tabla_html(pd.DataFrame(g).rename(columns={"termino": "Término", "definicion": "Definición",
                                               "simple": "En palabras sencillas"}))


# ---------------------------------------------------------------------------
# Navegación por fases
# ---------------------------------------------------------------------------
PAGINA_CUESTIONARIO = st.Page(f2_cuestionario, title="Cuestionario común multisede", icon=":material/quiz:")
pg = st.navigation({
    "Inicio": [st.Page(inicio, title="Portada", icon=":material/home:", default=True)],
    "Fase 0 · Formulación": [st.Page(fase0, title="Objetivos, referentes y método", icon=":material/flag:")],
    "Fase 1 · Conceptualización y diseño": [
        st.Page(f1_marco, title="1. Marco conceptual", icon=":material/menu_book:"),
        st.Page(f1_dimensiones, title="2. Dimensiones, variables e indicadores", icon=":material/star:"),
        st.Page(f1_fuentes, title="3. Fuentes de información", icon=":material/database:"),
        st.Page(f1_instrumentos, title="4. Instrumentos y métodos", icon=":material/assignment:"),
        st.Page(f1_diseno, title="5. Diseño del modelo y plan", icon=":material/account_tree:"),
    ],
    "Fase 2 · Validación": [st.Page(fase2, title="Propuesta de piloto", icon=":material/groups:"),
                            PAGINA_CUESTIONARIO],
    "Anexos": [st.Page(anexo_fichas, title="Fichas técnicas", icon=":material/description:"),
               st.Page(anexo_glosario, title="Glosario y documentos", icon=":material/dictionary:")],
})
with st.sidebar:
    st.markdown(f"<div style='color:{NAVY};font-weight:700'>Universidad Santo Tomás</div>"
                "<div class='fuente'>Consultoría Estadística 2026-II<br>Dylan Fajardo · Valentina Huertas · "
                "Manuel Molina</div>", unsafe_allow_html=True)
pg.run()
