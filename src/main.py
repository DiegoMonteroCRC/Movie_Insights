from src.helpers.cargadorDatos import cargadorDatos

ruta = "../data/raw/tmdb_2020_to_2025.csv"

cargador = cargadorDatos(ruta)

cargador.cargarDatos()

print(cargador.valoresNulos())
print(cargador.porcentajeNulos())
