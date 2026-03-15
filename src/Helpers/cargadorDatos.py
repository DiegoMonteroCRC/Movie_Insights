import pandas as pd
import time

class cargadorDatos:

    def __init__(self, ruta):
        self.ruta = ruta
        self.df = None

    def cargarDatos(self):
        self.df = pd.read_csv(self.ruta, encoding="utf-8")
        print("**************************************\n")
        print("El dataset posee:", self.df.shape[0], "filas\n")
        print("Nombre de las columnas", self.df.columns)
        print("**************************************\n")

    def resumenNulos(self):
        nulos = self.df.isnull().sum()
        porcentaje = (self.df.isnull().mean() * 100).round(2)

        resumen = pd.DataFrame({
            "valores_nulos": nulos,
            "porcentaje_%": porcentaje
        })

        return resumen

    def porcentajeNulos(self):
        print("**************************************\n")
        print("Porcentaje de valores nulos por cada variable")
        return self.df.isnull().mean()*100

    def valoresNulos(self):
        print("**************************************\n")
        print("Valores nulos por cada variable\n")
        return self.df.isnull().sum()

    def limpiarColumnas(self):
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

        print("**************************************\n")
        print("Columnas actuales despues de la limpieza:")
        print(self.df.columns)

    def guardarDatos(self):
        ruta_salida = "../data/processed/tmdb_limpio.csv"

        self.df.to_csv(ruta_salida, index=False)

        print("\nDataset limpio guardado en:")
        print(ruta_salida)