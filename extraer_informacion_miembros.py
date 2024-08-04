import pandas as pd
from PIL import Image
import pytesseract
import os
import re

# Cargar el archivo CSV
csv = 'RESULTADOS_2024_CSV_V1.csv'
data = pd.read_csv(csv)

# Ruta del directorio de actas
directorio_actas = '/Users/jesusgarcia/Projects/resultadosvnzla/actas'

# Añadir nuevas columnas
new_columns = {"Presidente": None, "CI_Presidente": None, "Secretario": None, "CI_Secretario": None,
            "Miembro A": None, "CI_Miembro_A": None, "Testigo A": None, "CI_Testigo_A": None,
            "Testigo B": None, "CI_Testigo_B": None, "Operador": None, "CI_Operador": None}
for col in new_columns.keys():
    data[col] = None

# Configurar la ruta de Tesseract si es necesario
# pytesseract.pytesseract.tesseract_cmd = r'RUTA_A_TESSERACT'

# Función para extraer la información de la imagen
def extraer_info_miembros(imgPath):

    img = Image.open(imgPath)
    text = pytesseract.image_to_string(img, lang='spa')
    text = os.linesep.join([s for s in text.splitlines() if s])
    
    data = new_columns
    
    lines = list(enumerate(text.split('\n')))

    for idx, line in lines:
        if "Presidente" in line:
            info = extraer_informacion(idx, lines)
            data['Presidente'] = info['Nombre']
            data['CI_Presidente'] = info['CI']
            continue
        if "Secretario" in line:
            info = extraer_informacion(idx, lines)
            data['Secretario'] = info['Nombre']
            data['CI_Secretario'] = info['CI']
            continue
        if "Miembro A" in line:
            info = extraer_informacion(idx, lines)
            data['Miembro A'] = info['Nombre']
            data['CI_Miembro_A'] = info['CI']
            continue
        if "Testigo A" in line:
            info = extraer_informacion(idx, lines)
            data['Testigo A'] = info['Nombre']
            data['CI_Testigo_A'] = info['CI']
            continue
        if "Testigo B" in line:
            info = extraer_informacion(idx, lines)
            data['Testigo B'] = info['Nombre']
            data['CI_Testigo_B'] = info['CI']
            continue
        if "Operador" in line:
            info = extraer_informacion(idx, lines)
            data['Operador'] = info['Nombre']
            data['CI_Operador'] = info['CI']
            continue

    return data

def extraer_informacion(idx, lines):
    
    informacion = {
        'Nombre': None,
        'CI': None
    }

    nombre = lines[idx+1][1].split(":")
    informacion['Nombre'] = nombre[1].strip() if len(nombre) > 1 else None
    patron = re.compile(r'\d{6,10}', re.IGNORECASE)
    match = patron.search(lines[idx+2][1])
    if match:
        informacion['CI'] = match.group(0).strip()
    return informacion

#Inicializar contador
f = open('contador.txt', 'r')
empezar = int(f.read())
f.close()

contador = empezar

# Procesar cada registro y llenar el DataFrame
for idx, row in data.iterrows():

    try:

        if idx + 1 < empezar:
            continue

        contador += 1

        print(f'Procesando acta {contador} de {len(data)}')

        url = row['URL']
        file = os.path.join(directorio_actas, url[url.rfind('/')+1:])
        info = extraer_info_miembros(imgPath=file)
        for key, value in info.items():
            data.at[idx, key] = value
        
        #Actualizar csv cuando el contador llega a 100 resultados``
        if contador % 100 == 0:
            data.to_csv(csv, index=False)
            f = open('contador.txt', 'w')
            f.write(str(contador))
            f.close()
        
        if contador >= len(data):
            data.to_csv(csv, index=False)
            print('Proceso finalizado')
            quit()
    
    except Exception as e:
        print(f'Error procesado el acta {contador}: {e}')
        f = open('logs.txt', 'w')
        f.write(f'Error procesado el acta {contador}: {e}')
        f.close()
        continue
