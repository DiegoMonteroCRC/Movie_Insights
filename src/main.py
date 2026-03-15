import time
from src.helpers.cargadorDatos import cargadorDatos

ruta = "../data/raw/tmdb_2020_to_2025.csv"

cargador = cargadorDatos(ruta)

print("\nCargando dataset...")
time.sleep(5)
cargador.cargarDatos()

print("\nCalculando valores nulos...")
time.sleep(6)
print(cargador.resumenNulos())

print("\nLimpiando columnas innecesarias...")
time.sleep(6)
cargador.limpiarColumnas()

print("\nGuardando dataset limpio...")
time.sleep(6)
cargador.guardarDatos()
