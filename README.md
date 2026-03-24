
# Movie Insights

Sistema de análisis exploratorio y visualización interactiva de películas, desarrollado con Python y POO

# Información del proyecto

## Curso
BD-143 Programación II

## Cuatrimestre
I Cuatrimestre 2026

## Institución
Colegio Universitario de Cartago

## Profesor
Osvaldo Gonzalez Chavez


## Descripción

Movie Insights es un sistema desarrollado en Python que permite ingestar, limpiar, analizar y visualizar datos de películas provenientes de archivos CSV. El sistema está construido bajo el paradigma de Programación Orientada a Objetos (POO) y cuenta con tres componentes principales:

- Procesamiento de datos desde consola ``src/``

- Análisis Exploratorio de Datos ``EDA`` en Jupyter Notebook ``notebooks/`` 

- Dashboard interactivo con Streamlit `dashboard/`

El dataset utilizado proviene de TMDB (The Movie Database) y contiene información de películas del período 2020 al 2025.
## Authors

- [@DiegoMonteroCRC](https://github.com/DiegoMonteroCRC)
- [@nadinrojas](https://github.com/nadinrojas)
# Estructura del proyecto

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
│       └── tmdb_limpio.csv          # Dataset limpio generado y guardado automaticamente 
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
## Tecnologías

**IDE:** PyCharm

**Lenguaje:** Pyton

**Librerías:** Pandas, Streamlit, Mathplotlib, Seaborn

**Herramientas:** Jupyter Notebook

**Control de versiones:** Github 


# Como ejecutar?

## 1.Clonar el repositorio


```bash
git clone https://github.com/tu-usuario/Movie_Insights.git
cd Movie_Insights
```

## 2. Instalar dependencias
```bash
pip install pandas streamlit matplotlib seaborn jupyter
```

## 3. Procesar datos
Ejecuta la carga y limpieza de datos
```bash
python src/main.py
```
Esto carga el dataset original con los datos completos, aplicará la limpieza y va a generar un archivo en ``data/processed/tmdb_limpio.csv``

## 4. Iniciar el dashboard 
Ejecutar el siguiente script desde Pycharm
```bash
streamlit run dashboard/app.py
```
Esto abrirá el navegador web para la interacción con el dashboard
    
# Funcionalidades

``src/clases/cargadorDatos.py`` 

Clase principal encargada del manejo de datos:

``cargarDatos()`` — Carga el CSV y muestra información básica del dataset

``mostrarVistaPrevia()`` — Muestra head, tail, dimensiones, duplicados y nulos

``resumenNulos()`` — Retorna un DataFrame con conteo y porcentaje de nulos

``limpiarColumnas()`` — Elimina columnas innecesarias para el análisis

``guardarDatos()`` — Exporta el dataset limpio a data/processed/

``dashboard/app.py``

Dashboard interactivo que permite:

- Visualizar métricas generales del dataset
- Explorar distribuciones de calificaciones y votos
- Filtrar películas por año e idioma
- Analizar tendencias por período

``notebooks/01_EDA.ipynb``

Análisis Exploratorio de Datos documentado que incluye:

- Resumen estadístico descriptivo
- Análisis de valores nulos y outliers
- Matriz de correlación
- Visualizaciones de distribución
## Dataset

**Fuente** TMDB (The Movie Database)

**Período** 2020 – 2025

**Archivo** ``rawtmdb_2020_to_2025.csv``

**Variables clave** ``title``, ``release_date``, ``vote_average``, ``vote_count``, ``original_language``, ``overview``
