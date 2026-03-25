import pandas as pd
import time

class cargadorDatos:

    def __init__(self, ruta):
        self.ruta = ruta
        self.df = None

    def cargarDatos(self):
        self.df = pd.read_csv(self.ruta, encoding="utf-8")
        print("======================================")
        print("         CARGA DE DATOS     ")
        print("======================================")
        print("El dataset posee:", self.df.shape[0], "filas\n")
        print("Nombre de las columnas", self.df.columns)
        print("======================================")

    def mostrarVistaPrevia(self):
        print("======================================")
        print("         VISTA PREVIA DEL DATASET     ")
        print("======================================")
        print(f"\n Filas     : {self.df.shape[0]}")
        print(f" Columnas  : {self.df.shape[1]}")
        print(f" Duplicados: {self.df.duplicated().sum()}")
        print(f" Nulos     : {self.df.isnull().sum().sum()}")

        print("\n--- HEAD ---")
        print(self.df.head())

        print("\n--- TAIL ---")
        print(self.df.tail())

        print("======================================\n")

    def resumenNulos(self):
        nulos = self.df.isnull().sum()
        porcentaje = (self.df.isnull().mean() * 100).round(2)

        resumen = pd.DataFrame({
            "valores nulos": nulos,
            "porcentaje %": porcentaje
        })

        return resumen

    def porcentajeNulos(self):
        print("======================================")
        print("         PORCENTAJE VALORES NULOS     ")
        print("======================================")
        print("Porcentaje de valores nulos por cada variable")
        return self.df.isnull().mean()*100
        print("======================================")


    def valoresNulos(self):
        print("======================================")
        print("         VALORES NULOS POR VARIABLE     ")
        print("======================================")
        print("Valores nulos por cada variable\n")
        return self.df.isnull().sum()

    def limpiarColumnas(self):
        print("======================================")
        print("         COLUMNAS A ELIMINAR      ")
        print("======================================")
        print(self.df.columns)

        columnas_eliminar = [
            "adult",
            "backdrop_path",
            "genre_ids",
            "id",
            "popularity",
            "poster_path",
            "video"
        ]

        self.df.drop(columns=columnas_eliminar, inplace=True)

        print("======================================")
        print("         COLUMNAS A UTILIZAR     ")
        print("======================================")
        print("Columnas actuales despues de la limpieza:")
        print(self.df.columns)

    def guardarDatos(self):
        print("======================================")
        print("         GUARDADO DEL NUEVO DATASET     ")
        print("======================================")
        ruta_salida = "../data/processed/tmdb_limpio.csv"

        self.df.to_csv(ruta_salida, index=False)

        print("\nDataset limpio guardado en:")
        print(ruta_salida)