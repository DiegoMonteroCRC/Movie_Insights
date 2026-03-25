![Banner](https://capsule-render.vercel.app/api?type=waving&color=C0392B&height=180&section=header&text=Movie%20Insights&fontSize=55&fontColor=ffffff&desc=Análisis%20exploratorio%20y%20visualización%20interactiva%20de%20películas&descSize=18&descAlignY=75)

![GitHub last commit](https://img.shields.io/github/last-commit/DiegoMonteroCRC/Movie_Insights?color=C0392B)
![GitHub repo size](https://img.shields.io/github/repo-size/DiegoMonteroCRC/Movie_Insights?color=C0392B)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/DiegoMonteroCRC/Movie_Insights?color=C0392B)

---

## Información del Proyecto

| Campo | Detalle |
|---|---|
| **Curso** | BD-143 Programación II |
| **Cuatrimestre** | I Cuatrimestre 2026 |
| **Institución** | Colegio Universitario de Cartago (CUC) |
| **Profesor** | Osvaldo González Chaves |

---

## Descripción

**Movie Insights** es un sistema desarrollado en Python que permite ingestar, limpiar, analizar y visualizar datos de películas provenientes de archivos CSV. El sistema está construido bajo el paradigma de **Programación Orientada a Objetos (POO)** y cuenta con tres componentes principales:

- Procesamiento de datos desde consola `src/`
- Análisis Exploratorio de Datos **EDA** en Jupyter Notebook `notebooks/`
- Dashboard interactivo con Streamlit `dashboard/`

El dataset utilizado proviene de **TMDB (The Movie Database)** y contiene información de películas del período **2020 al 2025**.

---

## Autores

| | Usuario |
|---|---|
| **Luis Diego Montero** | [@DiegoMonteroCRC](https://github.com/DiegoMonteroCRC) |
| **Nadin Rojas** | [@nadinrojas](https://github.com/nadinrojas) |

---

## Estructura del Proyecto

```plaintext
Movie_Insights/
│
├── dashboard/
│   ├── app.py               # Aplicación Streamlit (dashboard visual)
│   └── main.py              # Punto de entrada del dashboard
│
├── data/
│   ├── raw/
│   │   └── tmdb_2020_to_2025.csv    # Dataset original de TMDB
│   └── processed/
│       └── tmdb_limpio.csv          # Dataset limpio generado automáticamente
│
├── notebooks/
│   └── 01_EDA.ipynb/
│       ├── 01_EDA.ipynb     # Notebook con análisis exploratorio
│       └── 01_EDA.html      # Exportación HTML del notebook
│
├── src/
│   ├── clases/
│   │   └── cargadorDatos.py # Clase principal de carga y limpieza de datos
│   └── main.py              # Punto de entrada del procesamiento
│
├── README.md
└── LICENSE
```

---

## Tecnologías

| Tipo | Detalle |
|---|---|
| **IDE** | PyCharm |
| **Lenguaje** | Python |
| **Librerías** | Pandas, Streamlit, Matplotlib, Seaborn |
| **Herramientas** | Jupyter Notebook |
| **Control de versiones** | GitHub |

---

## ¿Cómo ejecutar?

### 1. Clonar el repositorio

```bash
git clone https://github.com/DiegoMonteroCRC/Movie_Insights.git
cd Movie_Insights
```

### 2. Instalar dependencias

```bash
pip install pandas streamlit matplotlib seaborn jupyter
```

### 3. Procesar datos

Ejecuta la carga y limpieza de datos:

```bash
python src/main.py
```

Esto carga el dataset original, aplica la limpieza y genera automáticamente el archivo en `data/processed/tmdb_limpio.csv`.

### 4. Iniciar el dashboard

Ejecutar el siguiente script desde Pycharm

```bash
streamlit run dashboard/app.py
```
Esto abrirá el navegador web para la interacción con el dashboard


## Funcionalidades

### `src/clases/cargadorDatos.py`
Clase principal encargada del manejo de datos:

| Método | Descripción |
|---|---|
| `cargarDatos()` | Carga el CSV y muestra información básica del dataset |
| `mostrarVistaPrevia()` | Muestra head, tail, dimensiones, duplicados y nulos |
| `resumenNulos()` | Retorna un DataFrame con conteo y porcentaje de nulos |
| `limpiarColumnas()` | Elimina columnas innecesarias para el análisis |
| `guardarDatos()` | Exporta el dataset limpio a `data/processed/` |

### `dashboard/app.py`
Dashboard interactivo que permite:
- Visualizar métricas generales del dataset
- Explorar distribuciones de calificaciones y votos
- Filtrar películas por año e idioma
- Analizar tendencias por período

### `notebooks/01_EDA.ipynb`
Análisis Exploratorio de Datos documentado que incluye:
- Resumen estadístico descriptivo
- Análisis de valores nulos y outliers
- Matriz de correlación
- Visualizaciones de distribución

---

## Dataset

| Campo | Detalle |
|---|---|
| **Fuente** | TMDB (The Movie Database) |
| **Período** | 2020 – 2025 |
| **Archivo** | `tmdb_2020_to_2025.csv` |
| **Variables clave** | `title`, `release_date`, `vote_average`, `vote_count`, `original_language`, `overview` |

---

![Footer](https://capsule-render.vercel.app/api?type=waving&color=C0392B&height=100&section=footer)
