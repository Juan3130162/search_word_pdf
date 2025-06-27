import os
import shutil
import PyPDF2
import re

def buscar_texto_en_pdf(ruta_pdf, palabras_a_buscar):
    """Busca las palabras dentro de un archivo PDF. Retorna una lista de palabras encontradas."""
    palabras_encontradas = []
    try:
        with open(ruta_pdf, 'rb') as archivo_pdf:
            lector_pdf = PyPDF2.PdfReader(archivo_pdf)
            # Iterar sobre cada página del PDF
            for num_pagina in range(len(lector_pdf.pages)):
                pagina = lector_pdf.pages[num_pagina]
                texto_pagina = pagina.extract_text()
                for palabra in palabras_a_buscar:
                    # Usamos expresiones regulares para buscar la palabra exacta (como palabra completa)
                    if re.search(rf'\b{re.escape(palabra)}\b', texto_pagina, re.IGNORECASE):
                        if palabra not in palabras_encontradas:
                            palabras_encontradas.append(palabra)
    except Exception as e:
        print(f"Error al procesar el archivo {ruta_pdf}: {e}")
    return palabras_encontradas

def copiar_archivos_pdf(origen, destino, palabras_a_buscar):
    """Recorre los PDFs en la carpeta origen y copia los que contienen alguna palabra a la carpeta destino."""
    if not os.path.exists(destino):
        os.makedirs(destino)
    
    archivos_copiados = set()  # Para evitar duplicados
    # Recorrer todos los archivos en la carpeta origen y subcarpetas
    for carpeta_raiz, subcarpetas, archivos in os.walk(origen):
        for archivo in archivos:
            if archivo.endswith(".pdf"):
                ruta_pdf = os.path.join(carpeta_raiz, archivo)
                print(f"Procesando archivo: {archivo}")  # Agregar esta línea
                palabras_encontradas = buscar_texto_en_pdf(ruta_pdf, palabras_a_buscar)
                if palabras_encontradas:
                    # Verificar si ya hemos copiado este archivo
                    if ruta_pdf not in archivos_copiados:
                        try:
                            destino_pdf = os.path.join(destino, archivo)
                            shutil.copy(ruta_pdf, destino_pdf)
                            archivos_copiados.add(ruta_pdf)
                            print(f"Archivo obtenido: {archivo}")
                            print(f"Facturas encontradas: {', '.join(palabras_encontradas)}")
                        except Exception as e:
                            print(f"Error al copiar el archivo {archivo}: {e}")

# Entradas fijas para las carpetas
ruta_origen = os.path.join("C:\\Users\\Usuario\\Documents", "RADICACION")
ruta_destino = os.path.join(os.getcwd(), "ENCONTRADOS")

# Palabras a buscar proporcionadas por el usuario
palabras_a_buscar = ["FE62545","FE62455","FE64057","FE64124","FM14851","FM15696","FM15725",
"FM15818","FE120440","FE120536","FE120548","FE120569","FE120561","FM12422","FE70383","FE100230",
"FE103319","FE129411","FY11486","FY11555","FY11580","FE143764"
                        ]

# Ejecutar la función de copia
copiar_archivos_pdf(ruta_origen, ruta_destino, [palabra.strip() for palabra in palabras_a_buscar])
