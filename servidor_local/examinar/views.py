from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import fitz  # PyMuPDF, para leer PDFs
import re    # Expresiones regulares
import os
import datetime
import json

# Create your views here.
def index(request):
    return render(request, "pagina_inicio.html")

def listado_view(request):
    DIRECTORIO = os.path.join(settings.BASE_DIR, 'static')
    registrosi=os.listdir(DIRECTORIO)  ## Lista todos los archivos en la carpeta
    print(registrosi)
    print("EL MEDIA ROOT ES:")
    print(str(settings.MEDIA_ROOT))

    registros_validos = []             ## Lista para almacenar diccionarios {'pdf': nombre de archivo, 'nombre': nombre de archivo sin extension, 'fecha': fecha de creacion de archivo}
    
    for archivo in registrosi:
        if archivo.lower().endswith(".pdf"):
            ruta_completa = os.path.join(DIRECTORIO, archivo)
            try:
                doc = fitz.open(ruta_completa)
                metadata = doc.metadata
                # Use current time as fallback if creationDate is missing or malformed
                try:
                    fecha_raw = metadata.get('creationDate', '')
                    if fecha_raw and len(fecha_raw) >= 16:
                        fecha = datetime.datetime.strptime(fecha_raw[2:16], "%Y%m%d%H%M%S")
                    else:
                        fecha = datetime.datetime.fromtimestamp(os.path.getmtime(ruta_completa))
                except Exception:
                    fecha = datetime.datetime.fromtimestamp(os.path.getmtime(ruta_completa))
                
                registros_validos.append({
                    'pdf': archivo,
                    'nombre': archivo[:-4],
                    'fecha': fecha
                })
                doc.close()
            except Exception as e:
                print(f"Error procesando {archivo}: {e}")
    
    # Sort by date descending
    registros_validos.sort(key=lambda x: x['fecha'], reverse=True)
    
    # Re-structure for the template (it expects a zip of 3 elements)
    # Actually, it's easier to change the template to use the dict list, 
    # but to maintain compatibility without major template changes:
    registros_fechas = [ (r['pdf'], r['nombre'], r['fecha']) for r in registros_validos ]
    
    return render(request, "examinar/examinar.html", {'registros_fechas': registros_fechas})

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
        "NUMERO_CICLO" : 0,
        "TEMP": [],
        "P": []        
    }

    try:
        for linea in texto.splitlines():
            # Buscar coincidencias de TEMP y P usando expresiones regulares
            print(linea)
            temp_match = re.search(r"TEMP:\s*(\d+)", linea)
            p_match = re.search(r"P:\s*(\d+)\s*kpa", linea)
            ciclo_match = re.search(r"CICLO N:\s*�*\s*(\d+)", linea)

            if ciclo_match:
                datos['NUMERO_CICLO'] = ciclo_match.group(1)# Capture the numeric value

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
    ruta_archivo = os.path.join(settings.BASE_DIR, 'static', f"{archivo}.pdf")
    # Extraer texto del PDF
    texto_extraido = extraer_texto_pdf(ruta_archivo)

    # Procesar los datos extraídos
    resultados = procesar_datos_texto(texto_extraido)

    # Mostrar los resultados
    print("Series extraídas:")
    print(f"Número de ciclo: {resultados['NUMERO_CICLO']}")
    print("Temperaturas (TEMP):", resultados["TEMP"])
    print("Presiones (P):", resultados["P"])
    metadatos_formateados = []
    keywords_parts ={}
    fecha = ""
    hora = ""
    numero_ciclo = 0
    try:
        doc = fitz.open(ruta_archivo )
        metadata = doc.metadata
        metadados_archivo = metadata
        print(f"Metadatos de {archivo}:")
        print(metadados_archivo)

        numero_ciclo = resultados['NUMERO_CICLO']
       
        # Extraer datos relevantes
        author_parts = metadados_archivo['author'].split(', ')
        print("voy aqui")
        keywords_parts = ({k.split(':')[0]: k.split(':')[1] for k in metadados_archivo['keywords'].split(',')} if metadados_archivo.get('keywords') else {})
        print("voy aqui2")
        creation_date = metadados_archivo['creationDate'][2:]  # Eliminar el prefijo "D:"   
        print(creation_date)
        
        # Remove trailing "Z"
        if creation_date.endswith("Z"):
            creation_date = creation_date[:-1]
        # Formatear fecha y hora
        fecha_hora = datetime.datetime.strptime(creation_date, "%Y%m%d%H%M%S")
        print(fecha_hora)
        fecha = fecha_hora.strftime("%d de %B de %Y")
        hora = fecha_hora.strftime("%I:%M %p")

                                                                                                                                                                                                                                                                                                                                                                                                                                                           
    except fitz.fitz.FileDataError: #Manejo de error si el archivo no es un PDF válido
            print(f"Error: {archivo} no es un PDF valido o está corrupto")
    except Exception as e:
        print(f"Error al leer metadatos de {archivo}: {e}")
    
    # Formatear metadatos para visualización
    
    if keywords_parts:
        for k, v in keywords_parts.items():
            metadatos_formateados.append((k.replace('_', ' ').capitalize(), v))
    
    metadatos_formateados.extend([
        ('Fecha de registro', fecha),
        ('Hora de registro', hora),
        ('Número de ciclo', numero_ciclo)
    ])

    context = {
        'metadatos': metadatos_formateados,
        'temperaturas': json.dumps(resultados["TEMP"][1:]), # Skip first garbage value if exists or just pass all
        'presiones': json.dumps(resultados["P"])
    }

    return render(request, "examinar/examinar_registro.html", context)

   