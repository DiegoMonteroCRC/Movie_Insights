import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

#  CONFIGURACION

st.set_page_config(page_title="Movie Insights", layout="wide")

CREMA    = "#FAF3E0"
CREMA2   = "#F2E8CC"
BORDE    = "#D4B896"
ROJO     = "#C0392B"
ROJO_OSC = "#96281B"
DORADO   = "#C8960C"
NARANJA  = "#E07B39"
TEXTO    = "#2C1A0E"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Crimson+Text:wght@400;600&display=swap');

.stApp {{ background-color: {CREMA}; color: {TEXTO}; }}

[data-testid="stSidebar"] {{ background-color: {CREMA2}; border-right: 2px solid {BORDE}; }}
[data-testid="stSidebar"] * {{ color: {TEXTO} !important; }}

h1, h2, h3 {{ font-family: 'Playfair Display', serif !important; color: {ROJO_OSC} !important; }}

[data-testid="stMetric"] {{
    background-color: white;
    border: 1.5px solid {BORDE};
    border-top: 3px solid {ROJO};
    border-radius: 8px;
    padding: 12px !important;
}}
[data-testid="stMetricLabel"] {{ color: {ROJO_OSC} !important; font-size: 13px !important; }}
[data-testid="stMetricValue"] {{ color: {DORADO} !important; font-size: 26px !important; font-weight: 700 !important; }}

hr {{ border-color: {BORDE} !important; }}
</style>
""", unsafe_allow_html=True)

#  DATOS

@st.cache_data
def cargar_datos():
    df = pd.read_csv(r"C:\Movie_Insights\Data\processed\tmdb_limpio.csv")
    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
    df["anio"] = df["release_date"].dt.year
    df["mes"]  = df["release_date"].dt.month
    return df

df = cargar_datos()

#  HELPER

def fig_style():
    plt.rcParams.update({
        "figure.facecolor": CREMA,
        "axes.facecolor":   CREMA,
        "axes.edgecolor":   BORDE,
        "axes.labelcolor":  TEXTO,
        "xtick.color":      TEXTO,
        "ytick.color":      TEXTO,
        "text.color":       TEXTO,
        "grid.color":       BORDE,
        "grid.linestyle":   "--",
        "grid.alpha":       0.6,
    })

#  SIDEBAR

with st.sidebar:
    st.markdown(f"""
    <div style='text-align:center; padding: 16px 0;'>
        <div style='font-family: Playfair Display, serif; font-size: 22px;
                    font-weight:700; color:{ROJO_OSC};'>Movie Insights</div>
        <div style='font-size:11px; color:#8B7355; letter-spacing:2px; margin-top:4px;'>
            EDA · 2020-2025
        </div>
    </div>
    <hr>
    """, unsafe_allow_html=True)

    seccion = st.radio("Ir a seccion", [
        "Resumen General",
        "Calificaciones",
        "El Efecto Pandemia",
        "El Dominio del Ingles",
        "Temporada de Estrenos",
        "Peores Peliculas",
        "Joyas Escondidas",
        "Quien Vota Mas",
        "Populares por Año",
    ])

    st.markdown("<hr>", unsafe_allow_html=True)

    filtro_votos = st.slider("Minimo de votos", 0, 500, 10, step=10)
    df_f = df[df["vote_count"] >= filtro_votos].copy()

    st.markdown(f"""
    <div style='text-align:center; font-size:12px; color:#8B7355; margin-top:12px;'>
        Mostrando <b style='color:{ROJO};'>{len(df_f):,}</b> de {len(df):,} peliculas
    </div>
    """, unsafe_allow_html=True)

#  HEADER
st.markdown(f"""
<div style='text-align:center; padding: 24px 0 8px 0;'>
    <h1 style='font-size:2.8em; margin-bottom:4px;'>Movie Insights</h1>
    <p style='color:#8B7355; font-size:13px; letter-spacing:2px;'>
        ANALISIS EXPLORATORIO · 2020-2025
    </p>
</div>
<hr>
""", unsafe_allow_html=True)

#  1. RESUMEN GENERAL

if seccion == "Resumen General":
    st.markdown("## Resumen General")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total peliculas",       f"{len(df):,}")
    c2.metric("Calificacion promedio", f"{df_f['vote_average'].mean():.2f}")
    c3.metric("Votos promedio",        f"{int(df_f['vote_count'].mean()):,}")
    c4.metric("Idiomas distintos",     df["original_language"].nunique())

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Estadisticas descriptivas")
    resumen = df_f[["vote_average", "vote_count"]].describe().round(2)
    st.dataframe(resumen, use_container_width=True)

    st.info("Con el filtro de votos aplicado, la calificacion promedio sube porque se eliminan las peliculas sin votos que arrastraban la media hacia cero.")


#  2. CALIFICACIONES

elif seccion == "Calificaciones":
    st.markdown("## Distribucion de Calificaciones")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("### Histograma")
        fig_style()
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.hist(df_f["vote_average"].dropna(), bins=30, color=ROJO, edgecolor=CREMA, alpha=0.85)
        ax.axvline(df_f["vote_average"].mean(),   color=DORADO,  linestyle="--", linewidth=1.8,
                   label=f"Media: {df_f['vote_average'].mean():.2f}")
        ax.axvline(df_f["vote_average"].median(), color=NARANJA, linestyle=":",  linewidth=1.8,
                   label=f"Mediana: {df_f['vote_average'].median():.2f}")
        ax.set_xlabel("Calificacion")
        ax.set_ylabel("Frecuencia")
        ax.legend(facecolor=CREMA, edgecolor=BORDE)
        ax.grid(True)
        st.pyplot(fig)
        plt.close()

    with c2:
        st.markdown("### Top 10 mejor calificadas (min. 100 votos)")
        top10 = (df_f[df_f["vote_count"] >= 100]
                 .nlargest(10, "vote_average")
                 [["title", "vote_average", "vote_count", "anio"]]
                 .reset_index(drop=True))
        top10.index += 1
        st.dataframe(top10, use_container_width=True)

    st.info("La distribucion se centra entre 6 y 7. Son pocas las peliculas que llegan a los extremos.")



# 3. EL EFECTO PANDEMIA

elif seccion == "El Efecto Pandemia":
    st.markdown("## El Efecto Pandemia: Menos Estrenos, Mas Votos")
    st.markdown("""
    > Durante 2020 y 2021 los cines cerraron y las producciones se frenaron.
    > Pero la gente encerrada en casa tenia mas tiempo para ver peliculas y calificarlas.
    > La hipotesis: **menos peliculas estrenadas, pero mas participacion de la audiencia por titulo**.
    """)

    # Votos promedio por año
    pandemia = (df.groupby("anio")
                .agg(total_peliculas=("title","count"),
                     votos_prom=("vote_count","mean"),
                     votos_total=("vote_count","sum"))
                .round(1).reset_index())

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("### Estrenos por año vs. votos promedio por pelicula")
        fig_style()
        fig, ax1 = plt.subplots(figsize=(7, 4))

        # cantidad de peliculas
        colores_pan = [ROJO if a in [2020, 2021] else NARANJA for a in pandemia["anio"]]
        ax1.bar(pandemia["anio"].astype(str), pandemia["total_peliculas"],
                color=colores_pan, edgecolor=CREMA, width=0.5, alpha=0.85, label="Peliculas estrenadas")
        ax1.set_xlabel("Año")
        ax1.set_ylabel("Cantidad de peliculas", color=ROJO_OSC)
        ax1.tick_params(axis="y", labelcolor=ROJO_OSC)

        # votos promedio
        ax2 = ax1.twinx()
        ax2.plot(pandemia["anio"].astype(str), pandemia["votos_prom"],
                 marker="o", color=DORADO, linewidth=2.5,
                 markersize=8, markerfacecolor=DORADO, markeredgecolor=ROJO_OSC, label="Votos prom/pelicula")
        ax2.set_ylabel("Votos promedio por pelicula", color=DORADO)
        ax2.tick_params(axis="y", labelcolor=DORADO)

        # Leyenda combinada
        leg1 = mpatches.Patch(color=ROJO,   label="Años pandemia (2020-2021)")
        leg2 = mpatches.Patch(color=NARANJA, label="Años post-pandemia")
        leg3 = plt.Line2D([0],[0], color=DORADO, marker="o", linewidth=2, label="Votos prom/pelicula")
        ax1.legend(handles=[leg1, leg2, leg3], facecolor=CREMA, edgecolor=BORDE, fontsize=8)
        ax1.grid(axis="y")
        st.pyplot(fig)
        plt.close()

    with c2:
        st.markdown("### Votos totales acumulados por año")
        fig_style()
        fig, ax = plt.subplots(figsize=(7, 4))
        colores_tot = [ROJO if a in [2020, 2021] else NARANJA for a in pandemia["anio"]]
        bars = ax.bar(pandemia["anio"].astype(str), pandemia["votos_total"],
                      color=colores_tot, edgecolor=CREMA, width=0.6)
        for bar, val in zip(bars, pandemia["votos_total"]):
            ax.text(bar.get_x() + bar.get_width() / 2,
                    val + 5000, f"{int(val):,}",
                    ha="center", color=ROJO_OSC, fontsize=8, fontweight="bold")
        ax.set_xlabel("Año")
        ax.set_ylabel("Total de votos acumulados")
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x):,}"))
        ax.grid(axis="y")
        leyenda = [mpatches.Patch(color=ROJO,    label="Pandemia (2020-2021)"),
                   mpatches.Patch(color=NARANJA, label="Post-pandemia")]
        ax.legend(handles=leyenda, facecolor=CREMA, edgecolor=BORDE)
        st.pyplot(fig)
        plt.close()

    # Tabla resumen
    st.markdown("### Resumen por año")
    tabla = pandemia.copy()
    tabla.columns = ["Año", "Peliculas Estrenadas", "Votos Prom/Pelicula", "Votos Totales"]
    tabla["Votos Totales"] = tabla["Votos Totales"].apply(lambda x: f"{int(x):,}")
    st.dataframe(tabla.reset_index(drop=True), use_container_width=True)

    st.warning("2020 y 2021 tuvieron menos estrenos que los años siguientes, pero el votos promedio por pelicula fue mas alto — consistente con la hipotesis de que el publico encerrado en casa interactuaba mas con el cine.")


# 4. DOMINIO DEL INGLES

elif seccion == "El Dominio del Ingles":
    st.markdown("## El Dominio del Ingles... pero no en Calidad")
    st.markdown("""
    > El ingles domina en **cantidad** (56% de las peliculas), pero en **calidad es de los peores** con 4.47 de promedio.
    > El coreano lidera en calidad con **5.94** — el cine coreano es claramente mas apreciado por su audiencia.
    """)

    lang = (df_f.groupby("original_language")
            .agg(peliculas=("title","count"), rating_prom=("vote_average","mean"))
            .reset_index())
    lang = lang[lang["peliculas"] >= 30]

    top_cant = lang.nlargest(10, "peliculas")
    top_cal  = lang.nlargest(10, "rating_prom")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("### Cantidad de peliculas por idioma (top 10)")
        fig_style()
        fig, ax = plt.subplots(figsize=(7, 5))
        colores = [ROJO if x == "en" else NARANJA for x in top_cant["original_language"]]
        ax.barh(top_cant["original_language"][::-1], top_cant["peliculas"][::-1],
                color=colores[::-1], edgecolor=CREMA, height=0.6)
        ax.set_xlabel("Cantidad de peliculas")
        ax.grid(axis="x")
        leyenda = [mpatches.Patch(color=ROJO, label="Ingles"),
                   mpatches.Patch(color=NARANJA, label="Otros")]
        ax.legend(handles=leyenda, facecolor=CREMA, edgecolor=BORDE)
        st.pyplot(fig)
        plt.close()

    with c2:
        st.markdown("### Rating promedio por idioma (top 10 en calidad)")
        fig_style()
        fig, ax = plt.subplots(figsize=(7, 5))
        colores2 = [ROJO if x == "en" else DORADO for x in top_cal["original_language"]]
        ax.barh(top_cal["original_language"][::-1], top_cal["rating_prom"][::-1],
                color=colores2[::-1], edgecolor=CREMA, height=0.6)
        ax.axvline(df_f["vote_average"].mean(), color=ROJO_OSC, linestyle="--",
                   linewidth=1.5, label=f"Promedio global: {df_f['vote_average'].mean():.2f}")
        ax.set_xlabel("Calificacion promedio")
        ax.set_xlim(0, 8)
        ax.legend(facecolor=CREMA, edgecolor=BORDE)
        ax.grid(axis="x")
        st.pyplot(fig)
        plt.close()

    st.success("El coreano (ko) lidera en calidad con 5.94, siendo solo el 2.2% del dataset. Cantidad no es sinonimo de calidad.")


#5. TEMPORADA DE ESTRENOS

elif seccion == "Temporada de Estrenos":
    st.markdown("## Temporada de Oscar")
    st.markdown("""
    > Los estrenos se **disparan en septiembre, octubre y noviembre** — la temporada de premios.
    > El fin de año concentra las peliculas con mayor visibilidad y votos.
    """)

    MESES = {1:"Ene",2:"Feb",3:"Mar",4:"Abr",5:"May",6:"Jun",
             7:"Jul",8:"Ago",9:"Sep",10:"Oct",11:"Nov",12:"Dic"}

    por_mes = df_f.groupby("mes")["title"].count().reset_index()
    por_mes["mes_nombre"] = por_mes["mes"].map(MESES)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("### Estrenos por mes (2020-2025)")
        fig_style()
        fig, ax = plt.subplots(figsize=(7, 4))
        colores_mes = [ROJO if m in [9, 10, 11] else NARANJA for m in por_mes["mes"]]
        ax.bar(por_mes["mes_nombre"], por_mes["title"],
               color=colores_mes, edgecolor=CREMA, width=0.7)
        ax.set_xlabel("Mes")
        ax.set_ylabel("Cantidad de estrenos")
        ax.grid(axis="y")
        leyenda = [mpatches.Patch(color=ROJO,    label="Temporada premios (Sep-Nov)"),
                   mpatches.Patch(color=NARANJA, label="Resto del año")]
        ax.legend(handles=leyenda, facecolor=CREMA, edgecolor=BORDE)
        st.pyplot(fig)
        plt.close()

    with c2:
        st.markdown("### Heatmap de estrenos por mes y año")
        pivot = df_f.groupby(["anio","mes"])["title"].count().unstack(fill_value=0)
        pivot.columns = [MESES[m] for m in pivot.columns]
        fig_style()
        fig, ax = plt.subplots(figsize=(7, 4))
        sns.heatmap(pivot, ax=ax, cmap="YlOrRd", linewidths=0.5,
                    linecolor=CREMA, annot=True, fmt="d",
                    annot_kws={"size": 8}, cbar_kws={"shrink": 0.7})
        ax.set_xlabel("")
        ax.set_ylabel("Año")
        st.pyplot(fig)
        plt.close()

    st.info("Oct y Nov concentran consistentemente los picos de estrenos.")


# 6. PEORES PELICULAS

elif seccion == "Peores Peliculas":
    st.markdown("## Peores Peliculas")
    st.markdown("""
    > Peliculas con **muchos votos** pero **calificacion baja** — los grandes fracasos con audiencia masiva.
    > *Snow White* (2025) acumula mas de 1,400 votos con apenas 4.3.
    """)

    verguenza = (df[df["vote_count"] >= 100]
                 .nsmallest(15, "vote_average")
                 [["title", "vote_average", "vote_count", "anio", "original_language"]]
                 .reset_index(drop=True))
    verguenza.index += 1

    c1, c2 = st.columns([1.3, 1])

    with c1:
        st.markdown("### Las peores con mas de 100 votos")
        top_v = verguenza.head(10)
        fig_style()
        fig, ax = plt.subplots(figsize=(8, 6))
        colores_v = [ROJO_OSC if v < 4.0 else ROJO for v in top_v["vote_average"]]
        ax.barh(top_v["title"].str[:35][::-1], top_v["vote_average"][::-1],
                color=colores_v[::-1], edgecolor=CREMA, height=0.6)
        ax.axvline(5.0, color=DORADO, linestyle="--", linewidth=1.5, label="Umbral 5.0")
        ax.set_xlabel("Calificacion promedio")
        ax.set_xlim(0, 7)
        ax.legend(facecolor=CREMA, edgecolor=BORDE)
        ax.grid(axis="x")
        st.pyplot(fig)
        plt.close()

    with c2:
        st.markdown("### Tabla completa")
        st.dataframe(verguenza, use_container_width=True, height=420)

    st.error("Snow White (2025) es la mas votada de la lista: 1,444 votos y solo 4.30 de calificacion. Fracaso masivo.")


# 7. JOYAS ESCONDIDAS

elif seccion == "Joyas Escondidas":
    st.markdown("## Las Joyas Escondidas")
    st.markdown("""
    > Peliculas con **minimo 100 votos** y **alta calificacion** fuera de Hollywood.
    > *La Leyenda de los Chaneques* (mexicana, 8.38) e *Impossible Things* (espanola, 8.44)
    > superan a grandes producciones en rating.
    """)

    joyas = (df[df["vote_count"] >= 100]
             .nlargest(20, "vote_average")
             [["title", "original_language", "vote_average", "vote_count", "anio"]])
    joyas = joyas[joyas["original_language"] != "en"].head(10).reset_index(drop=True)
    joyas.index += 1

    c1, c2 = st.columns([1.2, 1])

    with c1:
        st.markdown("### Top joyas (sin ingles)")
        fig_style()
        fig, ax = plt.subplots(figsize=(8, 5))
        colores_j = [DORADO if x == "es" else NARANJA for x in joyas["original_language"]]
        ax.barh(joyas["title"].str[:35][::-1], joyas["vote_average"][::-1],
                color=colores_j[::-1], edgecolor=CREMA, height=0.6)
        ax.axvline(df_f["vote_average"].mean(), color=ROJO, linestyle="--",
                   linewidth=1.5, label=f"Promedio global: {df_f['vote_average'].mean():.2f}")
        ax.set_xlabel("Calificacion promedio")
        ax.set_xlim(5, 10)
        ax.grid(axis="x")
        leyenda = [mpatches.Patch(color=DORADO, label="Espanol"),
                   mpatches.Patch(color=NARANJA, label="Otros idiomas"),
                   mpatches.Patch(color=ROJO,   label="Promedio global")]
        ax.legend(handles=leyenda, facecolor=CREMA, edgecolor=BORDE)
        st.pyplot(fig)
        plt.close()

    with c2:
        st.markdown("### Tabla")
        st.dataframe(joyas, use_container_width=True, height=380)

    st.success("El cine en espanol tiene fuerte presencia entre las joyas — tanto latinoamericano como espanol.")


# 8. QUIEN VOTA MAS

elif seccion == "Quien Vota Mas":
    st.markdown("## Que comunidad vota más?")
    st.markdown("""
    > Total de votos acumulados por idioma — revela que comunidades son las mas activas
    > y comprometidas a la hora de calificar peliculas.
    """)

    nombres = {"en":"Ingles","fr":"Frances","ja":"Japones","es":"Espanol","ko":"Coreano",
               "it":"Italiano","de":"Aleman","zh":"Chino","hi":"Hindi","tl":"Filipino",
               "pt":"Portugues","pl":"Polaco","da":"Danes","no":"Noruego","ru":"Ruso",
               "sv":"Sueco","nl":"Holandes","id":"Indonesio","th":"Tailandes","fi":"Finlandes"}

    lang_stats = (df.groupby("original_language")
                  .agg(peliculas=("title","count"),
                       votos_total=("vote_count","sum"),
                       rating_prom=("vote_average","mean"))
                  .reset_index())
    lang_stats = lang_stats[lang_stats["peliculas"] >= 30].copy()
    lang_stats["idioma"] = lang_stats["original_language"].map(nombres).fillna(lang_stats["original_language"])
    lang_stats = lang_stats.sort_values("votos_total", ascending=False).head(12)

    st.markdown("### Total de votos acumulados por comunidad (top 12)")
    fig_style()
    fig, ax = plt.subplots(figsize=(10, 6))

    colores_b = [ROJO if x == "en" else DORADO if x in ["ko","ja","es"] else NARANJA
                 for x in lang_stats["original_language"]]

    bars = ax.barh(lang_stats["idioma"][::-1], lang_stats["votos_total"][::-1],
                   color=colores_b[::-1], edgecolor=CREMA, height=0.65)

    for bar in bars:
        valor = bar.get_width()
        ax.text(valor + 5000, bar.get_y() + bar.get_height() / 2,
                f"{int(valor):,}", va="center", color=TEXTO, fontsize=9, fontweight="bold")

    ax.set_xlabel("Total de votos acumulados")
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.grid(axis="x")
    leyenda = [mpatches.Patch(color=ROJO,    label="Ingles (domina en volumen)"),
               mpatches.Patch(color=DORADO,  label="Coreano / Japones / Espanol"),
               mpatches.Patch(color=NARANJA, label="Resto")]
    ax.legend(handles=leyenda, facecolor=CREMA, edgecolor=BORDE)
    st.pyplot(fig)
    plt.close()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Detalle top 4")
    cols = st.columns(4)
    for col, (_, row) in zip(cols, lang_stats.head(4).iterrows()):
        col.metric(
            label=row["idioma"],
            value=f"{int(row['votos_total']):,}",
            delta=f"{int(row['peliculas'])} peliculas"
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.dataframe(
        lang_stats[["idioma","peliculas","votos_total","rating_prom"]]
        .rename(columns={"idioma":"Idioma","peliculas":"Peliculas",
                         "votos_total":"Total Votos","rating_prom":"Rating Prom."})
        .reset_index(drop=True),
        use_container_width=True
    )

    st.info("El ingles acumula la mayor cantidad de votos por amplio margen, pero tambien tiene el mayor numero de peliculas. El coreano, con muchas menos peliculas, logra un volumen de votos sorprendentemente alto.")


# 9. POPULARES POR AÑO
# ══════════════════════════════════════════
elif seccion == "Populares por Año":
    st.markdown("## Peliculas mas Populares por Año")

    anios = sorted(df_f["anio"].dropna().unique().astype(int))
    anio_sel = st.select_slider("Selecciona un año", options=anios, value=anios[-2])

    df_anio = (df_f[df_f["anio"] == anio_sel]
               .sort_values("vote_count", ascending=False)
               .head(10).reset_index(drop=True))
    df_anio.index += 1

    c1, c2 = st.columns([1.4, 1])

    with c1:
        st.markdown(f"### Top 10 mas votadas en {int(anio_sel)}")
        fig_style()
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.barh(df_anio["title"].str[:35][::-1], df_anio["vote_count"][::-1],
                color=ROJO, edgecolor=CREMA, height=0.6)
        for i, (_, row) in enumerate(df_anio[::-1].iterrows()):
            ax.text(row["vote_count"] + 20, i, f"{int(row['vote_count']):,}",
                    va="center", color=ROJO_OSC, fontsize=8)
        ax.set_xlabel("Numero de votos")
        ax.grid(axis="x")
        st.pyplot(fig)
        plt.close()

    with c2:
        st.markdown("### Calificacion de esas 10")
        fig_style()
        fig, ax = plt.subplots(figsize=(5, 5))
        prom = df_f["vote_average"].mean()
        colores_a = [DORADO if v >= prom else ROJO for v in df_anio["vote_average"]]
        ax.barh(df_anio["title"].str[:25][::-1], df_anio["vote_average"][::-1],
                color=colores_a[::-1], edgecolor=CREMA, height=0.6)
        ax.axvline(prom, color=ROJO_OSC, linestyle="--",
                   linewidth=1.5, label=f"Promedio: {prom:.2f}")
        ax.set_xlabel("Calificacion")
        ax.set_xlim(0, 10)
        ax.legend(facecolor=CREMA, edgecolor=BORDE, fontsize=8)
        ax.grid(axis="x")
        st.pyplot(fig)
        plt.close()

    st.markdown("### Detalle")
    st.dataframe(df_anio[["title", "original_language", "vote_average", "vote_count"]],
                 use_container_width=True)
    st.info(f"En {int(anio_sel)}, popularidad no es igual a calidad. Las mas votadas no siempre son las mejor calificadas.")