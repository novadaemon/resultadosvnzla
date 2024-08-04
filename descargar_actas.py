import pandas as pd
import requests
from PIL import Image
from io import BytesIO
import os

# Cargar el archivo CSV
csv_path = 'RESULTADOS_2024_CSV_V1.csv'
data = pd.read_csv(csv_path)

# Crear un directorio para guardar las imágenes descargadas
output_dir = 'actas'
os.makedirs(output_dir, exist_ok=True)

# Función para descargar una imagen desde una URL y guardarla localmente
def descargar_imagen(url, output_path):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            img.save(output_path)
            print(f"Imagen descargada y guardada en {output_path}")
        else:
            print(f"Error al descargar la imagen de {url}: Status code {response.status_code}")
    except Exception as e:
        print(f"Error al descargar la imagen de {url}: {e}")

# Recorrer cada fila del CSV y descargar la imagen
for idx, row in data.iterrows():
    url = row['URL']
    output_path = os.path.join(output_dir, url[url.rfind('/')+1:])
    descargar_imagen(url, output_path)
