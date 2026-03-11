import pandas as pd

class cargadorDatos:

    def __init__(self, ruta):
        self.ruta = ruta
        self.df = None

    def cargarDatos(self):
        self.df = pd.read_csv(self.ruta)
        print("**************************************\n")
        print("El dataset posee:", self.df.shape[0], "filas\n")
        print("Nombre de las columnas", self.df.columns)
        print("**************************************\n")

    def porcentajeNulos(self):
        print("**************************************\n")
        print("Porcentaje de valores nulos por cada variable")
        return self.df.isnull().mean()*100

    def valoresNulos(self):
        print("**************************************\n")
        print("Valores nulos por cada variable\n")
        return self.df.isnull().sum()