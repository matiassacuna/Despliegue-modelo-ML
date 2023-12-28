from dvc import api    # Importa la interfaz de DVC (data version control)
import pandas as pd
from io import StringIO  # Permite leer y escribir cadenas como archivos
import sys      # Provee acceso a algunas variables utilizadas o mantenidas por el intérprete
import logging   # Configura y controla mensajes de registro


# Configurar el sistema de registro: Configura cómo se mostrarán los mensajes de registro
logger = logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(name)s:%(message)s',
    level=logging.INFO,
    datefmt='%H:%M:%S',
    stream=sys.stderr
)

# Configurar el registro para el nombre del módulo actual: Obtiene un objeto de registro para el módulo actual.
logging.getLogger(__name__)

# Registrar información sobre la obtención de datos: Imprime un mensaje informativo indicando que se están obteniendo datos.
logging.info('Fetching data..')


# Obtener rutas de archivos remotos: Utiliza DVC para leer datos desde ubicaciones remotas.
movie_data_path = api.read('dataset/movies.csv', remote='dataset-track',encoding="utf8")
finantial_data_path = api.read('dataset/finantials.csv', remote='dataset-track',encoding="utf8")
opening_data_path = api.read('dataset/opening_gross.csv', remote='dataset-track',encoding="utf8")


# Convertir datos de cadena a DataFrames: Convierte datos de cadena a DataFrames para que puedan ser manipulados.
fin_data = pd.read_csv(StringIO(finantial_data_path))
movie_data = pd.read_csv(StringIO(movie_data_path))
opening_data = pd.read_csv(StringIO(opening_data_path))

# Seleccionar columnas numéricas de un DataFrame: Selecciona las columnas numéricas del DataFrame movie_data y agrega la columna 'movie_title'.
numeric_column_mask = (movie_data.dtypes == float) | (movie_data.dtypes == int)
numeric_columns = [column for column in numeric_column_mask.index if numeric_column_mask[column]] 
movie_data = movie_data[numeric_columns+['movie_title']]

# Seleccionar columnas específicas de otro DataFrame: Selecciona las columnas específicas del DataFrame fin_data.
fin_data = fin_data[['movie_title', 'production_budget','worldwide_gross']]

# Realizar unión de DataFrames: Realiza uniones entre DataFrames usando la columna 'movie_title'.
fin_movie_data = pd.merge(fin_data, movie_data, on='movie_title', how='left')
full_movie_data = pd.merge(opening_data, fin_movie_data, on='movie_title', how='left')

# Eliminar columnas no deseadas:
full_movie_data = full_movie_data.drop(['gross','movie_title'], axis=1)

# Guardar el DataFrame resultante como un archivo CSV:
full_movie_data.to_csv('dataset/full_data.csv', index=False)

# Registrar información sobre la finalización de la preparación de datos: Imprime un mensaje informativo indicando que los datos se han obtenido y preparado.
logging.info('Data Fetched and prepared...')