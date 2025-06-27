import os
import fitz 

def buscar_palabra_en_pdf(ruta_carpeta, palabra_buscar):
    """
    Busca una palabra específica en todos los archivos PDF dentro de una carpeta.

    Args:
        ruta_carpeta (str): La ruta a la carpeta que contiene los archivos PDF.
        palabra_buscar (str): La palabra que se va a buscar dentro de los PDFs.
    """
    print(f"Buscando la palabra '{palabra_buscar}' en los PDFs de la carpeta '{ruta_carpeta}'...\n")
    encontrado_en_algun_pdf = False  # Variable para rastrear si se encontró la palabra en algún PDF

    for nombre_archivo in os.listdir(ruta_carpeta):
        if nombre_archivo.lower().endswith(".pdf"): # Verifica que el archivo sea un PDF
            ruta_archivo_pdf = os.path.join(ruta_carpeta, nombre_archivo)
            try:
                with fitz.open(ruta_archivo_pdf) as pdf_documento:
                    for numero_pagina in range(pdf_documento.page_count):
                        pagina = pdf_documento.load_page(numero_pagina)
                        texto_pagina = pagina.get_text("text") # Extrae el texto de la página
                        if palabra_buscar.lower() in texto_pagina.lower(): # Busca la palabra (insensible a mayúsculas/minúsculas)
                            print(f"Palabra '{palabra_buscar}' encontrada en el archivo: {nombre_archivo}, Página: {numero_pagina + 1}")
                            encontrado_en_algun_pdf = True
            except Exception as e: # Manejo de errores por si un PDF no se puede abrir
                print(f"Error al procesar el archivo: {nombre_archivo}. Error: {e}")

    if not encontrado_en_algun_pdf:
        print(f"La palabra '{palabra_buscar}' no fue encontrada en ningún archivo PDF dentro de la carpeta '{ruta_carpeta}'.")
    else:
        print("\nBúsqueda completada.")

if __name__ == "__main__":
    carpeta_soportes = "SOPORTES" 
    palabra_a_buscar = "2302369"

    ruta_completa_carpeta = os.path.join(os.path.dirname(os.path.abspath(__file__)), carpeta_soportes) # Obtiene la ruta completa

    if not os.path.exists(ruta_completa_carpeta) or not os.path.isdir(ruta_completa_carpeta): # Verifica que la carpeta exista
        print(f"Error: La carpeta '{carpeta_soportes}' no existe o no es una carpeta en la ubicación del script.")
    else:
        buscar_palabra_en_pdf(ruta_completa_carpeta, palabra_a_buscar)