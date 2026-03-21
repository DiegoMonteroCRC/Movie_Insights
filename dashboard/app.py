import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# ─────────────────────────────────────────
#  CONFIGURACIÓN GENERAL
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Movie Insights · EDA",
    layout="wide",
)

# ─────────────────────────────────────────
#  ESTILOS PERSONALIZADOS
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Lato:wght@300;400;700&display=swap');

/* Fondo y texto general */
.stApp { background-color: #2c0000; color: #f0e0d0; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #3d0000 0%, #5c0000 100%);
    border-right: 1px solid #8B0000;
}
[data-testid="stSidebar"] * { color: #f0e0d0 !important; }

/* Títulos principales */
h1, h2, h3 { font-family: 'Playfair Display', serif !important; }
h1 { color: #FFD700 !important; }
h2 { color: #E74C3C !important; }
h3 { color: #F39C12 !important; }

/* Métricas */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #1a0000, #2c0000);
    border: 1px solid #8B0000;
    border-radius: 10px;
    padding: 12px !important;
}
[data-testid="stMetricLabel"] { color: #F39C12 !important; font-size: 13px !important; }
[data-testid="stMetricValue"] { color: #FFD700 !important; font-size: 28px !important; }

/* Tablas */
thead tr th {
    background: linear-gradient(135deg, #8B0000, #C0392B) !important;
    color: #FFD700 !important;
}
tbody tr:nth-child(even) { background-color: rgba(139,0,0,0.15) !important; }
tbody tr td { color: #f0e0d0 !important; }

/* Divider */
hr { border-color: #8B0000 !important; }

/* Radio / selectbox */
.stRadio label, .stSelectbox label { color: #F39C12 !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
#  CARGA DE DATOS
# ─────────────────────────────────────────
@st.cache_data
def cargar_datos():
    df = pd.read_csv(r"C:\Movie_Insights\Data\processed\tmdb_limpio.csv")
    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
    df["anio"] = df["release_date"].dt.year
    return df

df = cargar_datos()
df_calidad = df[df["vote_count"] >= 10].copy()

# ─────────────────────────────────────────
#  PALETA DE COLORES
# ─────────────────────────────────────────
ROJO      = "#C0392B"
ROJO_OSC  = "#8B0000"
DORADO    = "#FFD700"
SALMON    = "#E74C3C"
NARANJA   = "#F39C12"
FONDO     = "#2c0000"
FONDO2    = "#3d0000"

def estilo_figura():
    plt.rcParams.update({
        "figure.facecolor": FONDO2,
        "axes.facecolor":   FONDO2,
        "axes.edgecolor":   ROJO_OSC,
        "axes.labelcolor":  "#f0e0d0",
        "xtick.color":      "#f0e0d0",
        "ytick.color":      "#f0e0d0",
        "text.color":       "#f0e0d0",
        "grid.color":       "#3a0000",
        "grid.linestyle":   "--",
        "grid.alpha":       0.5,
    })

# ─────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 10px 0 20px 0;'>
        <div style='font-size:40px;'>🎬</div>
        <div style='font-family: Playfair Display, serif; font-size:22px;
                    color:#FFD700; font-weight:700;'>Movie Insights</div>
        <div style='font-size:12px; color:#aaa; letter-spacing:2px;'>EDA · TMDB 2020-2025</div>
    </div>
    <hr style='border-color:#8B0000;'>
    """, unsafe_allow_html=True)

    seccion = st.radio(
        "Navegación",
        [" Resumen General",
         " Calificaciones",
         " Evolución Anual",
         " Idiomas",
         " Populares por Año"]
    )

    st.markdown("<hr>", unsafe_allow_html=True)
    filtro_votos = st.slider(
        "Mínimo de votos",
        min_value=0, max_value=500, value=10, step=10
    )
    df_filtrado = df[df["vote_count"] >= filtro_votos].copy()

    st.markdown(f"""
    <div style='text-align:center; margin-top:20px; font-size:12px; color:#888;'>
        Mostrando <b style='color:#FFD700;'>{len(df_filtrado):,}</b> películas<br>
        de un total de <b style='color:#aaa;'>{len(df):,}</b>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────
#  HEADER PRINCIPAL
# ─────────────────────────────────────────
st.markdown("""
<div style='text-align:center; padding: 30px 0 10px 0;'>
    <h1 style='font-family: Playfair Display, serif; font-size: 3em;
               background: linear-gradient(135deg, #8B0000, #E74C3C, #F39C12);
               -webkit-background-clip: text; -webkit-text-fill-color: transparent;
               margin-bottom: 4px;'>
         Movie Insights
    </h1>
    <p style='color:#aaa; font-size:14px; letter-spacing:2px;'>
        ANÁLISIS EXPLORATORIO · TMDB 2020–2025
    </p>
</div>
<hr style='border-color:#8B0000; margin-bottom:30px;'>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════
#  SECCIÓN 1: RESUMEN GENERAL
# ══════════════════════════════════════════
if seccion == " Resumen General":
    st.markdown("##  Resumen General")

    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de películas", f"{len(df):,}")
    col2.metric("Calificación promedio", f"{df_filtrado['vote_average'].mean():.2f} ")
    col3.metric("Votos promedio", f"{int(df_filtrado['vote_count'].mean()):,}")
    col4.metric("Idiomas distintos", df["original_language"].nunique())

    st.markdown("<br>", unsafe_allow_html=True)

    # Tabla resumen descriptivo
    st.markdown("###  Estadísticas Descriptivas")
    numericas = df_filtrado[["vote_average", "vote_count"]]
    resumen = numericas.agg([
        "count", "mean", "std", "min",
        lambda x: x.quantile(0.25),
        "median",
        lambda x: x.quantile(0.75),
        "max"
    ]).round(2)
    resumen.index = ["count", "mean", "std", "min", "Q1", "median", "Q3", "max"]
    st.dataframe(resumen, use_container_width=True)

    st.markdown("""
    >  **Interpretación:** Con el filtro aplicado, la calificación promedio sube considerablemente
    respecto al dataset completo, donde los ceros de películas sin votos distorsionaban la media.
    """)

# ══════════════════════════════════════════
#  SECCIÓN 2: CALIFICACIONES
# ══════════════════════════════════════════
elif seccion == " Calificaciones":
    st.markdown("##  Distribución de Calificaciones")

    col1, col2 = st.columns(2)

    # Histograma de calificaciones
    with col1:
        st.markdown("### Histograma de vote_average")
        estilo_figura()
        fig, ax = plt.subplots(figsize=(7, 4))
        n, bins, patches = ax.hist(
            df_filtrado["vote_average"].dropna(),
            bins=30, edgecolor="#0d0000", linewidth=0.5
        )
        # Degradado de color en las barras
        for i, patch in enumerate(patches):
            t = i / len(patches)
            r = int(139 + (243 - 139) * t)
            g = int(0 + (156 - 0) * t)
            b = int(0 + (18 - 0) * t)
            patch.set_facecolor(f"#{r:02x}{g:02x}{b:02x}")
        ax.axvline(df_filtrado["vote_average"].mean(), color=DORADO,
                   linestyle="--", linewidth=1.5, label=f"Media: {df_filtrado['vote_average'].mean():.2f}")
        ax.axvline(df_filtrado["vote_average"].median(), color=NARANJA,
                   linestyle=":", linewidth=1.5, label=f"Mediana: {df_filtrado['vote_average'].median():.2f}")
        ax.legend(facecolor=FONDO2, edgecolor=ROJO_OSC)
        ax.set_xlabel("Calificación")
        ax.set_ylabel("Frecuencia")
        ax.grid(True)
        st.pyplot(fig)
        plt.close()
        st.markdown("> La distribución se aproxima a una campana centrada en 6-7, con pocas películas en los extremos.")

    # Boxplot
    with col2:
        st.markdown("### Boxplot · vote_average vs vote_count")
        estilo_figura()
        fig, axes = plt.subplots(1, 2, figsize=(7, 4))

        for ax_i, (col_name, color, label) in zip(
            axes,
            [("vote_average", "#e74c3c", "Calificación"),
             ("vote_count",   "#f1948a", "Votos")]
        ):
            bp = ax_i.boxplot(
                df_filtrado[col_name].dropna(),
                patch_artist=True,
                boxprops=dict(facecolor=color, alpha=0.7),
                medianprops=dict(color=DORADO, linewidth=2),
                whiskerprops=dict(color=ROJO),
                capprops=dict(color=ROJO),
                flierprops=dict(markerfacecolor=color, marker="o", alpha=0.4)
            )
            ax_i.set_title(col_name, color="#f0e0d0")
            ax_i.set_ylabel(label)
            ax_i.grid(True)

        st.pyplot(fig)
        plt.close()
        st.markdown("> `vote_count` muestra outliers extremos: unos pocos blockbusters concentran miles de votos.")

    # Top 10 mejor calificadas
    st.markdown("###  Top 10 Películas Mejor Calificadas")
    top10 = (df_filtrado[df_filtrado["vote_count"] >= 100]
             .sort_values("vote_average", ascending=False)
             .head(10)[["title", "vote_average", "vote_count", "anio"]]
             .reset_index(drop=True))
    top10.index += 1
    st.dataframe(top10, use_container_width=True)

# ══════════════════════════════════════════
#  SECCIÓN 3: EVOLUCIÓN ANUAL
# ══════════════════════════════════════════
elif seccion == " Evolución Anual":
    st.markdown("##  Evolución Anual de Películas")

    por_anio = df_filtrado.groupby("anio").agg(
        total=("title", "count"),
        calificacion=("vote_average", "mean"),
        votos=("vote_count", "mean")
    ).round(2).reset_index()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Producción por año")
        estilo_figura()
        fig, ax = plt.subplots(figsize=(7, 4))
        bars = ax.bar(por_anio["anio"].astype(str), por_anio["total"],
                      color=[ROJO_OSC, ROJO, SALMON, NARANJA, ROJO, ROJO_OSC],
                      edgecolor=FONDO, linewidth=0.8)
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 10,
                    str(int(bar.get_height())),
                    ha="center", va="bottom", color=DORADO, fontsize=9)
        ax.set_xlabel("Año")
        ax.set_ylabel("Cantidad de películas")
        ax.grid(axis="y")
        st.pyplot(fig)
        plt.close()

    with col2:
        st.markdown("### Calificación promedio por año")
        estilo_figura()
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.plot(por_anio["anio"].astype(str), por_anio["calificacion"],
                marker="o", color=SALMON, linewidth=2.5, markersize=8,
                markerfacecolor=DORADO, markeredgecolor=ROJO_OSC)
        ax.fill_between(range(len(por_anio)), por_anio["calificacion"],
                        alpha=0.15, color=ROJO)
        for i, (x, y) in enumerate(zip(por_anio["anio"].astype(str), por_anio["calificacion"])):
            ax.text(i, y + 0.03, f"{y:.2f}", ha="center", color=DORADO, fontsize=9)
        ax.set_xlabel("Año")
        ax.set_ylabel("Calificación promedio")
        ax.grid(True)
        st.pyplot(fig)
        plt.close()

    st.markdown("""
    >  **Hipótesis:** El pico de votos en 2020-2022 coincide con la pandemia: más tiempo en casa
    impulsó el consumo de películas y la interacción en plataformas de valoración.
    """)

    # Heatmap anual
    st.markdown("###  Heatmap: Películas por mes y año")
    df_temp = df_filtrado.copy()
    df_temp["mes"] = df_temp["release_date"].dt.month
    pivot = df_temp.groupby(["anio", "mes"])["title"].count().unstack(fill_value=0)
    meses = ["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]
    pivot.columns = [meses[m-1] for m in pivot.columns]

    estilo_figura()
    fig, ax = plt.subplots(figsize=(12, 3.5))
    sns.heatmap(pivot, ax=ax, cmap="YlOrRd", linewidths=0.5,
                linecolor="#0d0000", annot=True, fmt="d",
                cbar_kws={"shrink": 0.7},
                annot_kws={"size": 8, "color": "#0d0000"})
    ax.set_title("Cantidad de estrenos por mes y año", color=DORADO, pad=12)
    ax.set_xlabel("")
    ax.set_ylabel("Año")
    st.pyplot(fig)
    plt.close()
    st.markdown("> Se identifican patrones de estreno: ciertos meses concentran más lanzamientos (temporadas altas).")

# ══════════════════════════════════════════
#  SECCIÓN 4: IDIOMAS
# ══════════════════════════════════════════
elif seccion == " Idiomas":
    st.markdown("##  Distribución por Idioma")

    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown("### Top 10 idiomas por cantidad de películas")
        top_idiomas = (df_filtrado["original_language"]
                       .value_counts()
                       .head(10)
                       .reset_index())
        top_idiomas.columns = ["Idioma", "Películas"]

        estilo_figura()
        fig, ax = plt.subplots(figsize=(7, 5))
        colors = [ROJO_OSC, ROJO, SALMON, NARANJA,
                  "#c0392b", "#922b21", "#f1948a", "#f5b7b1", "#f39c12", "#d4ac0d"]
        bars = ax.barh(top_idiomas["Idioma"][::-1], top_idiomas["Películas"][::-1],
                       color=colors[::-1], edgecolor=FONDO)
        for bar in bars:
            ax.text(bar.get_width() + 5, bar.get_y() + bar.get_height() / 2,
                    str(int(bar.get_width())),
                    va="center", color=DORADO, fontsize=9)
        ax.set_xlabel("Cantidad de películas")
        ax.grid(axis="x")
        st.pyplot(fig)
        plt.close()

    with col2:
        st.markdown("### Participación de idiomas")
        top5 = df_filtrado["original_language"].value_counts().head(5)
        otros = df_filtrado["original_language"].value_counts().iloc[5:].sum()
        datos_pie = pd.concat([top5, pd.Series({"Otros": otros})])

        estilo_figura()
        fig, ax = plt.subplots(figsize=(6, 5))
        colores_pie = [ROJO_OSC, ROJO, SALMON, NARANJA, "#f1948a", "#555"]
        wedges, texts, autotexts = ax.pie(
            datos_pie.values,
            labels=datos_pie.index,
            autopct="%1.1f%%",
            colors=colores_pie,
            startangle=140,
            wedgeprops=dict(edgecolor=FONDO, linewidth=1.5)
        )
        for text in texts:
            text.set_color("#f0e0d0")
        for autotext in autotexts:
            autotext.set_color(DORADO)
            autotext.set_fontweight("bold")
        st.pyplot(fig)
        plt.close()

    st.markdown("""
    >  **El inglés domina** con amplia mayoría. Esto refleja la hegemonía de Hollywood y
    la naturaleza global de la base de datos TMDB, donde el contenido angloparlante tiene
    mayor representación y comunidad de votantes.
    """)

    # Calificación promedio por idioma
    st.markdown("###  Calificación promedio por idioma (top 8 con más películas)")
    top8_idiomas = df_filtrado["original_language"].value_counts().head(8).index.tolist()
    df_top8 = df_filtrado[df_filtrado["original_language"].isin(top8_idiomas)]
    calif_por_idioma = (df_top8.groupby("original_language")["vote_average"]
                        .mean().sort_values(ascending=False).round(2))

    estilo_figura()
    fig, ax = plt.subplots(figsize=(10, 3.5))
    bars = ax.bar(calif_por_idioma.index, calif_por_idioma.values,
                  color=SALMON, edgecolor=FONDO, width=0.6)
    ax.axhline(df_filtrado["vote_average"].mean(), color=DORADO,
               linestyle="--", linewidth=1.5, label="Promedio global")
    for bar, val in zip(bars, calif_por_idioma.values):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.03,
                f"{val:.2f}", ha="center", color=DORADO, fontsize=9)
    ax.set_xlabel("Idioma")
    ax.set_ylabel("Calificación promedio")
    ax.legend(facecolor=FONDO2, edgecolor=ROJO_OSC)
    ax.set_ylim(0, 10)
    ax.grid(axis="y")
    st.pyplot(fig)
    plt.close()

# ══════════════════════════════════════════
#  SECCIÓN 5: Populares por Año
# ══════════════════════════════════════════
elif seccion == " Populares por Año":
    st.markdown("##  Películas más populares por año")

    anios = sorted(df_filtrado["anio"].dropna().unique().astype(int))
    anio_sel = st.select_slider("Selecciona un año", options=anios, value=anios[-2])

    df_anio = (df_filtrado[df_filtrado["anio"] == anio_sel]
               .sort_values("vote_count", ascending=False)
               .head(10)
               .reset_index(drop=True))
    df_anio.index += 1

    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.markdown(f"###  Top 10 más votadas en {int(anio_sel)}")
        estilo_figura()
        fig, ax = plt.subplots(figsize=(8, 5))
        colores = [ROJO_OSC, ROJO, SALMON, NARANJA, ROJO,
                   ROJO_OSC, ROJO, SALMON, NARANJA, ROJO]
        bars = ax.barh(
            df_anio["title"].str[:30][::-1],
            df_anio["vote_count"][::-1],
            color=colores, edgecolor=FONDO
        )
        for bar in bars:
            ax.text(bar.get_width() + 20,
                    bar.get_y() + bar.get_height() / 2,
                    f"{int(bar.get_width()):,}",
                    va="center", color=DORADO, fontsize=8)
        ax.set_xlabel("Número de votos")
        ax.grid(axis="x")
        st.pyplot(fig)
        plt.close()

    with col2:
        st.markdown(f"###  Calificación de las top 10")
        estilo_figura()
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.barh(
            df_anio["title"].str[:25][::-1],
            df_anio["vote_average"][::-1],
            color=SALMON, edgecolor=FONDO
        )
        ax.axvline(df_filtrado["vote_average"].mean(),
                   color=DORADO, linestyle="--", linewidth=1.5,
                   label=f"Promedio global: {df_filtrado['vote_average'].mean():.2f}")
        ax.set_xlabel("Calificación")
        ax.set_xlim(0, 10)
        ax.legend(facecolor=FONDO2, edgecolor=ROJO_OSC, fontsize=8)
        ax.grid(axis="x")
        st.pyplot(fig)
        plt.close()

    st.markdown("###  Detalle completo")
    st.dataframe(
        df_anio[["title", "original_language", "vote_average", "vote_count"]],
        use_container_width=True
    )

    st.markdown(f"""
    >  **{int(anio_sel)}:** Las películas más populares no siempre son las mejor calificadas.
    Puedes mover el slider para comparar cómo cambia el ranking entre años.
    """)