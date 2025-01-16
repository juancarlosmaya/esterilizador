import re
import fitz  # PyMuPDF

def extraer_texto_pdf(ruta_pdf):
    """
    Extrae el texto de un archivo PDF usando PyMuPDF (fitz).
    :param ruta_pdf: Ruta del archivo PDF.
    :return: Texto extraído del PDF.
    """
    texto = ""
    try:
        with fitz.open(ruta_pdf) as pdf:
            for pagina in pdf:
                texto += pagina.get_text()
    except Exception as e:
        print(f"Ocurrió un error al leer el PDF: {e}")
    return texto

def procesar_datos_texto(texto):
    """
    Procesa el texto extraído y obtiene las series de temperaturas y presiones.
    :param texto: Texto extraído del archivo PDF.
    :return: Diccionario con las series de TEMP y P.
    """
    datos = {
        "TEMP": [],
        "P": []
    }

    try:
        for linea in texto.splitlines():
            # Buscar coincidencias de TEMP y P usando expresiones regulares
            print(linea)
            temp_match = re.search(r"TEMP:\s*(\d+)", linea)
            p_match = re.search(r"P:\s*(\d+)\s*kpa", linea)

            if temp_match:
                # Agregar la temperatura extraída a la lista TEMP
                datos["TEMP"].append(int(temp_match.group(1)))

            if p_match:
                # Agregar la presión extraída a la lista P
                datos["P"].append(int(p_match.group(1)))

    except Exception as e:
        print(f"Ocurrió un error al procesar el texto: {e}")

    return datos

# Ruta al archivo PDF exportado como texto
ruta_archivo = "/Esterilizador/servidor_local/static/FECHA081223HORAINICIO183431SN150P10FEB048RVCICLON47.pdf"
# Extraer texto del PDF
texto_extraido = extraer_texto_pdf(ruta_archivo)

# Procesar los datos extraídos
resultados = procesar_datos_texto(texto_extraido)

# Mostrar los resultados
print("Series extraídas:")
print("Temperaturas (TEMP):", resultados["TEMP"])
print("Presiones (P):", resultados["P"])

