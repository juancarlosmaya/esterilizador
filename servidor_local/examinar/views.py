from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import fitz  # PyMuPDF, para leer PDFs
import re    # Expresiones regulares
import os
import datetime

# Create your views here.
def listado_view(request):
    #DIRECTORIO= "/Users/JUAN CARLOS/Desktop/Esterilizador/Datalogger/REGISTROS"
    DIRECTORIO= "/Esterilizador/servidor_local/static"
    registrosi=os.listdir(DIRECTORIO)
    print(registrosi)
    print("EL MEDIA ROOT ES:")
    print(str(settings.MEDIA_ROOT))

    registros_pdf = []
    fechas = []
    metadata_archivos = {} # Diccionario para almacenar metadatos
    for archivo in registrosi:
        if archivo.lower().endswith(".pdf"): # Verifica la extensión
            registros_pdf.append(archivo)
            ruta_completa = os.path.join(DIRECTORIO, archivo)
            try:
                doc = fitz.open(ruta_completa)
                metadata = doc.metadata
                metadata_archivos[archivo] = metadata # Guarda los metadatos
                print(f"Metadatos de {archivo}:")
                for clave, valor in metadata.items():
                    print(f"  {clave}: {valor}")
                fechas.append(datetime.datetime.strptime(metadata['creationDate'][2:-1], "%Y%m%d%H%M%S")) # Guarda la fecha de creación
                #xmp_data = doc.xmp_metadata
                #if xmp_data:
                #    print("\nMetadatos XMP:")
                #    print(xmp_data)
                #doc.close() # Cierra el documento después de usarlo
            except fitz.fitz.FileDataError: #Manejo de error si el archivo no es un PDF válido
                print(f"Error: {archivo} no es un PDF valido o está corrupto")
            except Exception as e:
                print(f"Error al leer metadatos de {archivo}: {e}")
            registros_fechas = zip(registros_pdf, [archivo[:-4] for archivo in registros_pdf], fechas)  # guarda el listado de archivos en pdf, el litado de archivos sin extension, y las fechas de los registros
    return render(request,"examinar/examinar.html",{'registros_fechas':registros_fechas})

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


def examinar_registro(request,archivo):
    # Ruta al archivo PDF exportado como texto
    ruta_archivo = "/Esterilizador/servidor_local/static/" + archivo +".pdf"
    # Extraer texto del PDF
    texto_extraido = extraer_texto_pdf(ruta_archivo)

    # Procesar los datos extraídos
    resultados = procesar_datos_texto(texto_extraido)

    # Mostrar los resultados
    print("Series extraídas:")
    print("Temperaturas (TEMP):", resultados["TEMP"])
    print("Presiones (P):", resultados["P"])
    metadata = {}
    try:
        doc = fitz.open(ruta_archivo )
        metadata = doc.metadata
        metadados_archivo = metadata
        print(f"Metadatos de {archivo}:")
        print(metadados_archivo)
       
        # Extraer datos relevantes
        author_parts = metadados_archivo['author'].split(', ')
        
        keywords_parts = {k.split(':')[0]: k.split(':')[1] for k in metadados_archivo['keywords'].split(',')}
        creation_date = metadados_archivo['creationDate'][2:]  # Eliminar el prefijo "D:"

        # Formatear fecha y hora
        fecha_hora = datetime.datetime.strptime(creation_date, "%Y%m%d%H%M%S")
        fecha = fecha_hora.strftime("%d de %B de %Y")
        hora = fecha_hora.strftime("%I:%M %p")
        nueva_variable = list(keywords_parts.items()) + [('fecha', fecha), ('hora', hora)]

                                                                                                                                                                                                                                                                                                                                                                                                                                                           
    except fitz.fitz.FileDataError: #Manejo de error si el archivo no es un PDF válido
            print(f"Error: {archivo} no es un PDF valido o está corrupto")
    except Exception as e:
            print(f"Error al leer metadatos de {archivo}: {e}")
    #registros_fechas = zip(registros_pdf, [archivo[:-4] for archivo in registros_pdf], fechas)  # guarda el listado de archivos en pdf, el litado de archivos sin extension, y las fechas de los registros
    return render(request,"examinar/examinar_registro.html",{'metadatos':nueva_variable,'temperaturas':resultados["TEMP"],'presiones':resultados["P"]})

   